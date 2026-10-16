"""Servicio principal de conciliación entre facturas y registros contables."""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Any, List, Optional, Set
import pandas as pd

from app.schemas.conciliacion import (
    ResultadoFactura,
    ResumenConciliacion,
    RespuestaConciliacion,
)
from app.services.validaciones import (
    normalize_id,
    validate_required_field,
    validate_numeric_field,
)
from app.services.reglas import (
    ContextoFactura,
    MotorReglasConciliacion,
)

DOS_DECIMALES = Decimal("0.01")


def _formatear_decimal(valor: Decimal) -> str:
    """Formatea un valor Decimal a cadena con exactamente dos decimales."""
    return f"{valor.quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP):.2f}"


class ContenedorResultado(dict):
    """Diccionario para compatibilidad con código legado que requiere acceso por atributo."""

    def __getattr__(self, clave: str) -> Any:
        try:
            valor = self[clave]
            if isinstance(valor, dict) and not isinstance(valor, ContenedorResultado):
                return ContenedorResultado(valor)
            return valor
        except KeyError as exc:
            raise AttributeError(f"No existe la clave o atributo '{clave}'.") from exc


def _extraer_contexto_fila(
    fila: pd.Series,
    ids_duplicados: Set[str],
    ids_contabilidad: Set[str],
) -> ContextoFactura:
    """Parsea y prepara el contexto numérico y de metadatos de una fila para evaluación."""
    id_factura = str(fila.get("id_factura", "")).strip()

    # Conversión de base gravable
    tiene_base_vacia = not validate_required_field(fila.get("base_gravable"))
    if tiene_base_vacia:
        base_gravable = Decimal("0.00")
    else:
        try:
            base_gravable = validate_numeric_field(fila.get("base_gravable"), "base_gravable").quantize(
                DOS_DECIMALES, rounding=ROUND_HALF_UP
            )
        except (ValueError, InvalidOperation):
            tiene_base_vacia = True
            base_gravable = Decimal("0.00")

    # Conversión de tarifa IVA
    try:
        tarifa_iva = validate_numeric_field(fila.get("tarifa_iva", "0"), "tarifa_iva")
    except (ValueError, InvalidOperation):
        tarifa_iva = Decimal("0.0")

    # Conversión de valor IVA reportado
    try:
        valor_iva = validate_numeric_field(fila.get("valor_iva", "0"), "valor_iva").quantize(
            DOS_DECIMALES, rounding=ROUND_HALF_UP
        )
    except (ValueError, InvalidOperation):
        valor_iva = Decimal("0.00")

    # Conversión de tarifa retención
    try:
        tarifa_retencion = validate_numeric_field(fila.get("tarifa_retencion", "0"), "tarifa_retencion")
    except (ValueError, InvalidOperation):
        tarifa_retencion = Decimal("0.0")

    # Conversión de valor retención reportado
    try:
        valor_retencion = validate_numeric_field(fila.get("valor_retencion", "0"), "valor_retencion").quantize(
            DOS_DECIMALES, rounding=ROUND_HALF_UP
        )
    except (ValueError, InvalidOperation):
        valor_retencion = Decimal("0.00")

    # Conversión de total factura reportado
    try:
        total_factura = validate_numeric_field(fila.get("total_factura", "0"), "total_factura").quantize(
            DOS_DECIMALES, rounding=ROUND_HALF_UP
        )
    except (ValueError, InvalidOperation):
        total_factura = Decimal("0.00")

    # Cálculos esperados con redondeo financiero
    iva_esperado = (base_gravable * tarifa_iva).quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP)
    total_esperado = (base_gravable + iva_esperado - valor_retencion).quantize(
        DOS_DECIMALES, rounding=ROUND_HALF_UP
    )

    return ContextoFactura(
        id_factura=id_factura,
        nit_proveedor=str(fila.get("nit_proveedor", "")).strip(),
        fecha_factura=str(fila.get("fecha_factura", "")).strip(),
        concepto=str(fila.get("concepto", "")).strip(),
        base_gravable=base_gravable,
        tarifa_iva=tarifa_iva,
        valor_iva=valor_iva,
        tarifa_retencion=tarifa_retencion,
        valor_retencion=valor_retencion,
        total_factura=total_factura,
        iva_esperado=iva_esperado,
        total_esperado=total_esperado,
        tiene_base_vacia=tiene_base_vacia,
        fila_cruda=fila.to_dict(),
        ids_duplicados=ids_duplicados,
        ids_contabilidad=ids_contabilidad,
    )


def procesar_conciliacion(
    df_facturas: pd.DataFrame,
    df_contabilidad: pd.DataFrame,
    motor: Optional[MotorReglasConciliacion] = None,
) -> RespuestaConciliacion:
    """Ejecuta las reglas de negocio para conciliar facturas frente a registros contables.

    Args:
        df_facturas: DataFrame con los datos de las facturas.
        df_contabilidad: DataFrame con los registros contables.
        motor: Instancia opcional del motor de reglas (usa el predeterminado si es None).

    Returns:
        Instancia de RespuestaConciliacion tipada con resumen y resultados detallados.
    """
    motor_activo = motor or MotorReglasConciliacion()

    df_f = df_facturas.copy()
    df_c = df_contabilidad.copy()

    # Normalización de identificadores
    if "id_factura" in df_f.columns:
        df_f["id_factura"] = df_f["id_factura"].apply(normalize_id)
    else:
        df_f["id_factura"] = ""

    if "id_factura" in df_c.columns:
        df_c["id_factura"] = df_c["id_factura"].apply(normalize_id)
    else:
        df_c["id_factura"] = ""

    # Identificadores presentes en contabilidad
    ids_contabilidad: Set[str] = {
        str(ident).strip()
        for ident in df_c["id_factura"].dropna()
        if str(ident).strip() != ""
    }

    # Detección de identificadores duplicados en facturación
    facturas_con_id = df_f[df_f["id_factura"] != ""]["id_factura"]
    conteo_ids = facturas_con_id.value_counts()
    ids_duplicados: Set[str] = set(conteo_ids[conteo_ids > 1].index)

    resultados_facturas: List[ResultadoFactura] = []

    for _, fila in df_f.iterrows():
        contexto = _extraer_contexto_fila(fila, ids_duplicados, ids_contabilidad)
        inconsistencias = motor_activo.evaluar_factura(contexto)
        estado = "Correcta" if len(inconsistencias) == 0 else "Con inconsistencia"

        item = ResultadoFactura(
            id_factura=contexto.id_factura,
            nit_proveedor=contexto.nit_proveedor,
            fecha_factura=contexto.fecha_factura,
            concepto=contexto.concepto,
            base_gravable=_formatear_decimal(contexto.base_gravable),
            iva_reportado=_formatear_decimal(contexto.valor_iva),
            iva_esperado=_formatear_decimal(contexto.iva_esperado),
            total_reportado=_formatear_decimal(contexto.total_factura),
            total_esperado=_formatear_decimal(contexto.total_esperado),
            retencion_reportada=_formatear_decimal(contexto.valor_retencion),
            estado=estado,
            inconsistencias=inconsistencias,
        )
        resultados_facturas.append(item)

    total_facturas = len(resultados_facturas)
    correctas = sum(1 for item in resultados_facturas if item.estado == "Correcta")
    con_inconsistencia = sum(1 for item in resultados_facturas if item.estado == "Con inconsistencia")

    resumen = ResumenConciliacion(
        total_facturas=total_facturas,
        correctas=correctas,
        con_inconsistencia=con_inconsistencia,
    )

    return RespuestaConciliacion(
        resumen=resumen,
        resultados=resultados_facturas,
    )
