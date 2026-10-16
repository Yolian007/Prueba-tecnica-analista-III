"""Pruebas unitarias para el motor de conciliación de facturas."""

import pandas as pd
from app.services.conciliacion import procesar_conciliacion


def _crear_df_facturas(filas: list[dict]) -> pd.DataFrame:
    """Helper para crear DataFrame de facturas a partir de una lista de diccionarios."""
    columnas_base = {
        "id_factura": "FAC-0001",
        "nit_proveedor": "900123456-1",
        "fecha_factura": "2024-01-15",
        "concepto": "Servicios de soporte",
        "base_gravable": "1000000",
        "tarifa_iva": "0.19",
        "valor_iva": "190000",
        "tarifa_retencion": "0.04",
        "valor_retencion": "40000",
        "total_factura": "1150000",
    }
    datos = []
    for fila in filas:
        registro = columnas_base.copy()
        registro.update(fila)
        datos.append(registro)
    return pd.DataFrame(datos)


def _crear_df_contabilidad(ids: list[str]) -> pd.DataFrame:
    """Helper para crear DataFrame de contabilidad."""
    datos = [
        {
            "id_factura": ident,
            "fecha_contabilizacion": "2024-01-16",
            "cuenta_contable": "513505",
            "centro_costo": "CC-100",
            "valor_debito": "1150000",
            "valor_credito": "0",
            "estado": "Contabilizada",
        }
        for ident in ids
    ]
    return pd.DataFrame(datos)


def test_factura_correcta():
    """Valida una factura que cumple todas las reglas de negocio y está en contabilidad."""
    df_f = _crear_df_facturas([{"id_factura": "FAC-0001"}])
    df_c = _crear_df_contabilidad(["FAC-0001"])

    resultado = procesar_conciliacion(df_f, df_c)

    assert resultado["resumen"]["total_facturas"] == 1
    assert resultado["resumen"]["correctas"] == 1
    assert resultado["resumen"]["con_inconsistencia"] == 0

    factura = resultado["resultados"][0]
    assert factura["estado"] == "Correcta"
    assert factura["inconsistencias"] == []
    assert factura["iva_esperado"] == "190000.00"
    assert factura["total_esperado"] == "1150000.00"


def test_diferencia_iva():
    """Valida la detección de discrepancia entre IVA reportado y el IVA esperado calculado."""
    # base = 3800000, tarifa = 0.05 -> esperado = 190000, reportado = 215000
    # retención = 152000. total esperado = 3800000 + 190000 - 152000 = 3838000
    df_f = _crear_df_facturas([{
        "id_factura": "FAC-0006",
        "base_gravable": "3800000",
        "tarifa_iva": "0.05",
        "valor_iva": "215000",
        "tarifa_retencion": "0.04",
        "valor_retencion": "152000",
        "total_factura": "3838000",
    }])
    df_c = _crear_df_contabilidad(["FAC-0006"])

    resultado = procesar_conciliacion(df_f, df_c)
    factura = resultado["resultados"][0]

    assert factura["estado"] == "Con inconsistencia"
    assert "Diferencia en IVA" in factura["inconsistencias"]
    assert "Diferencia en total" not in factura["inconsistencias"]
    assert factura["iva_reportado"] == "215000.00"
    assert factura["iva_esperado"] == "190000.00"


def test_diferencia_total():
    """Valida la detección de discrepancia en el total cuando el total reportado no coincide con el cálculo."""
    # base = 1000000, iva = 190000, ret = 40000 -> esperado = 1150000, reportado = 1200000
    df_f = _crear_df_facturas([{
        "id_factura": "FAC-0009",
        "total_factura": "1200000",
    }])
    df_c = _crear_df_contabilidad(["FAC-0009"])

    resultado = procesar_conciliacion(df_f, df_c)
    factura = resultado["resultados"][0]

    assert factura["estado"] == "Con inconsistencia"
    assert "Diferencia en total" in factura["inconsistencias"]
    assert "Diferencia en IVA" not in factura["inconsistencias"]


def test_factura_duplicada():
    """Valida que facturas con el mismo identificador repetido se marquen como duplicadas."""
    df_f = _crear_df_facturas([
        {"id_factura": "FAC-0004"},
        {"id_factura": "FAC-0004"},
    ])
    df_c = _crear_df_contabilidad(["FAC-0004"])

    resultado = procesar_conciliacion(df_f, df_c)

    assert resultado["resumen"]["total_facturas"] == 2
    assert resultado["resumen"]["con_inconsistencia"] == 2
    assert "Factura duplicada" in resultado["resultados"][0]["inconsistencias"]
    assert "Factura duplicada" in resultado["resultados"][1]["inconsistencias"]


def test_factura_sin_contabilidad():
    """Valida la detección de facturas que no cuentan con ningún asiento contable registrado."""
    df_f = _crear_df_facturas([{"id_factura": "FAC-0021"}])
    df_c = _crear_df_contabilidad(["FAC-0001", "FAC-0002"])

    resultado = procesar_conciliacion(df_f, df_c)
    factura = resultado["resultados"][0]

    assert factura["estado"] == "Con inconsistencia"
    assert "Factura sin registro contable" in factura["inconsistencias"]


def test_multiples_inconsistencias():
    """Valida que una factura con múltiples errores registre todas las inconsistencias detectadas."""
    df_f = _crear_df_facturas([
        {
            "id_factura": "FAC-0099",
            "nit_proveedor": "",
            "concepto": "",
            "valor_iva": "999999",
            "total_factura": "888888",
        },
        {
            "id_factura": "FAC-0099",
        },
    ])
    df_c = _crear_df_contabilidad(["FAC-OTRA"])

    resultado = procesar_conciliacion(df_f, df_c)
    factura = resultado["resultados"][0]

    assert factura["estado"] == "Con inconsistencia"
    assert "Diferencia en IVA" in factura["inconsistencias"]
    assert "Diferencia en total" in factura["inconsistencias"]
    assert "Factura duplicada" in factura["inconsistencias"]
    assert "Factura sin registro contable" in factura["inconsistencias"]
    assert "Campo obligatorio vacío: nit_proveedor" in factura["inconsistencias"]
    assert "Campo obligatorio vacío: concepto" in factura["inconsistencias"]


def test_campo_vacio_nit():
    """Valida que la ausencia de NIT del proveedor sea detectada como inconsistencia obligatoria."""
    df_f = _crear_df_facturas([{
        "id_factura": "FAC-0013",
        "nit_proveedor": "",
    }])
    df_c = _crear_df_contabilidad(["FAC-0013"])

    resultado = procesar_conciliacion(df_f, df_c)
    factura = resultado["resultados"][0]

    assert factura["estado"] == "Con inconsistencia"
    assert "Campo obligatorio vacío: nit_proveedor" in factura["inconsistencias"]


def test_resumen_correcto():
    """Valida que los contadores globales del resumen coincidan con la suma de estados."""
    df_f = _crear_df_facturas([
        {"id_factura": "FAC-0001"},  # Correcta
        {"id_factura": "FAC-0002"},  # Correcta
        {"id_factura": "FAC-0003", "total_factura": "9999999"},  # Con inconsistencia
    ])
    df_c = _crear_df_contabilidad(["FAC-0001", "FAC-0002", "FAC-0003"])

    resultado = procesar_conciliacion(df_f, df_c)

    resumen = resultado["resumen"]
    assert resumen["total_facturas"] == 3
    assert resumen["correctas"] == 2
    assert resumen["con_inconsistencia"] == 1
    assert resumen["correctas"] + resumen["con_inconsistencia"] == resumen["total_facturas"]
