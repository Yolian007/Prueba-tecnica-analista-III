"""Servicio principal de conciliación entre facturas y registros contables."""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Any, Dict, List, Set
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

DOS_DECIMALES = Decimal("0.01")


class ContenedorResultado(dict):
    """Diccionario especializado que permite acceso tanto por clave como por atributo."""

    def __getattr__(self, clave: str) -> Any:
        try:
            valor = self[clave]
            if isinstance(valor, dict) and not isinstance(valor, ContenedorResultado):
                return ContenedorResultado(valor)
            return valor
        except KeyError as exc:
            raise AttributeError(f"No existe la clave o atributo '{clave}'.") from exc


def _formatear_decimal(valor: Decimal) -> str:
    """Formatea un valor Decimal a cadena con exactamente dos decimales."""
    return f"{valor.quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP):.2f}"


def procesar_conciliacion(df_facturas: pd.DataFrame, df_contabilidad: pd.DataFrame) -> dict:
    """Ejecuta las reglas de negocio para conciliar facturas frente a registros contables.

    Reglas aplicadas:
    1. Normalización de identificadores (id_factura).
    2. Identificación de facturas duplicadas en el archivo de facturas.
    3. Validación de campos obligatorios (id_factura, base_gravable, nit_proveedor, fecha_factura, concepto).
    4. Cálculo y verificación del IVA esperado: base_gravable * tarifa_iva.
    5. Cálculo y verificación del total esperado: base_gravable + iva_esperado - valor_retencion.
    6. Verificación de existencia de registro en contabilidad.
    7. Generación de resumen y clasificación en 'Correcta' o 'Con inconsistencia'.

    Args:
        df_facturas: DataFrame con los datos de las facturas.
        df_contabilidad: DataFrame con los registros contables.

    Returns:
        Diccionario compatible con RespuestaConciliacion con resumen y lista de resultados.
    """
    df_f = df_facturas.copy()
    df_c = df_contabilidad.copy()

    # Paso 1: Normalizar identificadores eliminando espacios
    if "id_factura" in df_f.columns:
        df_f["id_factura"] = df_f["id_factura"].apply(normalize_id)
    else:
        df_f["id_factura"] = ""

    if "id_factura" in df_c.columns:
        df_c["id_factura"] = df_c["id_factura"].apply(normalize_id)
    else:
        df_c["id_factura"] = ""

    # Paso 2: Obtener conjunto de IDs presentes en contabilidad (no vacíos)
    ids_contabilidad: Set[str] = {
        str(ident).strip()
        for ident in df_c["id_factura"].dropna()
        if str(ident).strip() != ""
    }

    # Paso 3: Detectar facturas duplicadas en el archivo de facturas (conteo > 1)
    facturas_con_id = df_f[df_f["id_factura"] != ""]["id_factura"]
    conteo_ids = facturas_con_id.value_counts()
    ids_duplicados: Set[str] = set(conteo_ids[conteo_ids > 1].index)

    resultados_facturas: List[Dict[str, Any]] = []

    # Paso 4: Evaluar cada factura fila por fila
    for _, fila in df_f.iterrows():
        inconsistencias: List[str] = []
        id_factura = str(fila.get("id_factura", "")).strip()

        # Validación 4b: Campo obligatorio id_factura
        if not id_factura:
            inconsistencias.append("Campo obligatorio vacío: id_factura")

        # Conversión de base gravable
        tiene_base_vacia = not validate_required_field(fila.get("base_gravable"))
        if tiene_base_vacia:
            inconsistencias.append("Campo obligatorio vacío: base_gravable")
            base_gravable = Decimal("0.00")
        else:
            try:
                base_gravable = validate_numeric_field(fila.get("base_gravable"), "base_gravable").quantize(
                    DOS_DECIMALES, rounding=ROUND_HALF_UP
                )
            except (ValueError, InvalidOperation):
                inconsistencias.append("Campo obligatorio vacío: base_gravable")
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

        # Paso 4d: Cálculo de IVA esperado
        iva_esperado = (base_gravable * tarifa_iva).quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP)

        # Paso 4e: Validación de diferencia en IVA
        if valor_iva != iva_esperado:
            inconsistencias.append("Diferencia en IVA")

        # Paso 4f: Cálculo de total esperado usando iva_esperado (regla de no propagación)
        total_esperado = (base_gravable + iva_esperado - valor_retencion).quantize(
            DOS_DECIMALES, rounding=ROUND_HALF_UP
        )

        # Paso 4g: Validación de diferencia en total
        if total_factura != total_esperado:
            inconsistencias.append("Diferencia en total")

        # Paso 4h: Validación de factura duplicada
        if id_factura and id_factura in ids_duplicados:
            inconsistencias.append("Factura duplicada")

        # Paso 4i: Validación de registro contable existente
        if id_factura and id_factura not in ids_contabilidad:
            inconsistencias.append("Factura sin registro contable")

        # Paso 4j: Validación de campos obligatorios adicionales
        for campo in ("nit_proveedor", "fecha_factura", "concepto"):
            if not validate_required_field(fila.get(campo)):
                inconsistencias.append(f"Campo obligatorio vacío: {campo}")

        # Paso 4k: Determinación de estado
        estado = "Correcta" if len(inconsistencias) == 0 else "Con inconsistencia"

        item_resultado = {
            "id_factura": id_factura,
            "nit_proveedor": str(fila.get("nit_proveedor", "")).strip(),
            "fecha_factura": str(fila.get("fecha_factura", "")).strip(),
            "concepto": str(fila.get("concepto", "")).strip(),
            "base_gravable": _formatear_decimal(base_gravable),
            "iva_reportado": _formatear_decimal(valor_iva),
            "iva_esperado": _formatear_decimal(iva_esperado),
            "total_reportado": _formatear_decimal(total_factura),
            "total_esperado": _formatear_decimal(total_esperado),
            "retencion_reportada": _formatear_decimal(valor_retencion),
            "estado": estado,
            "inconsistencias": inconsistencias,
        }
        resultados_facturas.append(item_resultado)

    # Paso 5: Construcción de resumen cuantitativo
    total_facturas = len(resultados_facturas)
    correctas = sum(1 for item in resultados_facturas if item["estado"] == "Correcta")
    con_inconsistencia = sum(1 for item in resultados_facturas if item["estado"] == "Con inconsistencia")

    resumen = {
        "total_facturas": total_facturas,
        "correctas": correctas,
        "con_inconsistencia": con_inconsistencia,
    }

    # Retorno en estructura de datos enriquecida compatible con dict y objeto
    resultado_final = ContenedorResultado({
        "resumen": ContenedorResultado(resumen),
        "resultados": [ContenedorResultado(r) for r in resultados_facturas],
    })

    return resultado_final
