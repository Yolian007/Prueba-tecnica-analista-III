"""Pruebas unitarias para el motor de reglas y reglas individuales de conciliación."""

from decimal import Decimal
from app.services.reglas import (
    ContextoFactura,
    MotorReglasConciliacion,
    ReglaIdentificadorObligatorio,
    ReglaBaseGravableObligatoria,
    ReglaDiferenciaIVA,
    ReglaDiferenciaRetencion,
    ReglaDiferenciaTotal,
    ReglaFacturaDuplicada,
    ReglaFacturaSinContabilidad,
    ReglaEstadoContabilizacion,
    ReglaCruceValorContable,
    ReglaCamposObligatoriosAdicionales,
)


def _crear_contexto_base(**kwargs) -> ContextoFactura:
    """Helper para instanciar un contexto de factura válido por defecto."""
    defaults = {
        "id_factura": "FAC-100",
        "nit_proveedor": "900123456-1",
        "fecha_factura": "2024-03-01",
        "concepto": "Servicio de consultoría",
        "base_gravable": Decimal("1000000.00"),
        "tarifa_iva": Decimal("0.19"),
        "valor_iva": Decimal("190000.00"),
        "tarifa_retencion": Decimal("0.04"),
        "valor_retencion": Decimal("40000.00"),
        "total_factura": Decimal("1150000.00"),
        "iva_esperado": Decimal("190000.00"),
        "total_esperado": Decimal("1150000.00"),
        "tiene_base_vacia": False,
        "fila_cruda": {
            "id_factura": "FAC-100",
            "nit_proveedor": "900123456-1",
            "fecha_factura": "2024-03-01",
            "concepto": "Servicio de consultoría",
        },
        "ids_duplicados": set(),
        "ids_contabilidad": {"FAC-100"},
    }
    defaults.update(kwargs)
    return ContextoFactura(**defaults)


def test_regla_identificador_obligatorio():
    """Valida la detección de identificador ausente o vacío."""
    regla = ReglaIdentificadorObligatorio()

    ctx_valido = _crear_contexto_base(id_factura="FAC-101")
    assert regla.evaluar(ctx_valido) == []

    ctx_vacio = _crear_contexto_base(id_factura="")
    assert regla.evaluar(ctx_vacio) == ["Campo obligatorio vacío: id_factura"]


def test_regla_base_gravable_obligatoria():
    """Valida la detección de base gravable ausente o no numérica."""
    regla = ReglaBaseGravableObligatoria()

    ctx_valido = _crear_contexto_base(tiene_base_vacia=False)
    assert regla.evaluar(ctx_valido) == []

    ctx_vacio = _crear_contexto_base(tiene_base_vacia=True)
    assert regla.evaluar(ctx_vacio) == ["Campo obligatorio vacío: base_gravable"]


def test_regla_diferencia_iva():
    """Valida la detección de discrepancias en el cálculo de IVA."""
    regla = ReglaDiferenciaIVA()

    ctx_correcto = _crear_contexto_base(
        valor_iva=Decimal("190000.00"),
        iva_esperado=Decimal("190000.00"),
    )
    assert regla.evaluar(ctx_correcto) == []

    ctx_discrepancia = _crear_contexto_base(
        valor_iva=Decimal("200000.00"),
        iva_esperado=Decimal("190000.00"),
    )
    assert regla.evaluar(ctx_discrepancia) == ["Diferencia en IVA"]


def test_regla_diferencia_total():
    """Valida la detección de discrepancias en el total de la factura."""
    regla = ReglaDiferenciaTotal()

    ctx_correcto = _crear_contexto_base(
        total_factura=Decimal("1150000.00"),
        total_esperado=Decimal("1150000.00"),
    )
    assert regla.evaluar(ctx_correcto) == []

    ctx_discrepancia = _crear_contexto_base(
        total_factura=Decimal("1200000.00"),
        total_esperado=Decimal("1150000.00"),
    )
    assert regla.evaluar(ctx_discrepancia) == ["Diferencia en total"]


def test_regla_factura_duplicada():
    """Valida la detección de identificadores repetidos en el archivo."""
    regla = ReglaFacturaDuplicada()

    ctx_no_duplicado = _crear_contexto_base(id_factura="FAC-100", ids_duplicados={"FAC-999"})
    assert regla.evaluar(ctx_no_duplicado) == []

    ctx_duplicado = _crear_contexto_base(id_factura="FAC-100", ids_duplicados={"FAC-100"})
    assert regla.evaluar(ctx_duplicado) == ["Factura duplicada"]


def test_regla_factura_sin_contabilidad():
    """Valida la detección de facturas que no existen en los registros contables."""
    regla = ReglaFacturaSinContabilidad()

    ctx_en_contabilidad = _crear_contexto_base(id_factura="FAC-100", ids_contabilidad={"FAC-100"})
    assert regla.evaluar(ctx_en_contabilidad) == []

    ctx_sin_contabilidad = _crear_contexto_base(id_factura="FAC-100", ids_contabilidad={"FAC-200"})
    assert regla.evaluar(ctx_sin_contabilidad) == ["Factura sin registro contable"]


def test_regla_campos_obligatorios_adicionales():
    """Valida la obligatoriedad de nit_proveedor, fecha_factura y concepto."""
    regla = ReglaCamposObligatoriosAdicionales()

    ctx_completo = _crear_contexto_base()
    assert regla.evaluar(ctx_completo) == []

    ctx_faltante = _crear_contexto_base(
        fila_cruda={
            "id_factura": "FAC-100",
            "nit_proveedor": "",
            "fecha_factura": "   ",
            "concepto": "Servicio",
        }
    )
    inconsistencias = regla.evaluar(ctx_faltante)
    assert "Campo obligatorio vacío: nit_proveedor" in inconsistencias
    assert "Campo obligatorio vacío: fecha_factura" in inconsistencias
    assert "Campo obligatorio vacío: concepto" not in inconsistencias


def test_motor_orquestacion_completa():
    """Verifica que el motor ejecute todas las reglas y consolide las inconsistencias."""
    motor = MotorReglasConciliacion()
    ctx_con_multiples_fallas = _crear_contexto_base(
        id_factura="FAC-DUP",
        valor_iva=Decimal("200000.00"),
        iva_esperado=Decimal("190000.00"),
        total_factura=Decimal("999999.00"),
        total_esperado=Decimal("1150000.00"),
        ids_duplicados={"FAC-DUP"},
        ids_contabilidad=set(),
    )
    resultado = motor.evaluar_factura(ctx_con_multiples_fallas)

    assert "Diferencia en IVA" in resultado
    assert "Diferencia en total" in resultado
    assert "Factura duplicada" in resultado
    assert "Factura sin registro contable" in resultado


def test_regla_diferencia_retencion():
    """Valida la detección de discrepancias en el cálculo de la retención."""
    regla = ReglaDiferenciaRetencion()

    ctx_correcto = _crear_contexto_base(
        valor_retencion=Decimal("40000.00"),
        retencion_esperada=Decimal("40000.00"),
    )
    assert regla.evaluar(ctx_correcto) == []

    ctx_discrepancia = _crear_contexto_base(
        valor_retencion=Decimal("50000.00"),
        retencion_esperada=Decimal("40000.00"),
    )
    assert regla.evaluar(ctx_discrepancia) == ["Diferencia en retención"]


def test_regla_estado_contabilizacion():
    """Valida que registros contables con estado Pendiente sean detectados."""
    regla = ReglaEstadoContabilizacion()

    ctx_contabilizado = _crear_contexto_base(
        id_factura="FAC-100",
        ids_contabilidad={"FAC-100"},
        estados_contabilidad_factura={"Contabilizada"},
    )
    assert regla.evaluar(ctx_contabilizado) == []

    ctx_pendiente = _crear_contexto_base(
        id_factura="FAC-100",
        ids_contabilidad={"FAC-100"},
        estados_contabilidad_factura={"Pendiente"},
    )
    assert regla.evaluar(ctx_pendiente) == ["Registro contable en estado Pendiente"]


def test_regla_cruce_valor_contable():
    """Valida el cruce entre el total de la factura y los importes registrados en contabilidad."""
    regla = ReglaCruceValorContable()

    ctx_coincidente = _crear_contexto_base(
        id_factura="FAC-100",
        total_factura=Decimal("1150000.00"),
        ids_contabilidad={"FAC-100"},
        valores_contabilidad_factura=[Decimal("1150000.00")],
    )
    assert regla.evaluar(ctx_coincidente) == []

    ctx_divergente = _crear_contexto_base(
        id_factura="FAC-100",
        total_factura=Decimal("1150000.00"),
        ids_contabilidad={"FAC-100"},
        valores_contabilidad_factura=[Decimal("2000000.00")],
    )
    assert regla.evaluar(ctx_divergente) == ["Diferencia con valor en contabilidad"]

