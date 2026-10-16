"""Pruebas unitarias para el servicio de lectura y validación de archivos CSV."""

import io
import pytest
from app.services.lector_csv import (
    leer_csv,
    leer_csv_facturas,
    leer_csv_contabilidad,
    ErrorValidacionCSV,
    COLUMNAS_FACTURAS,
    COLUMNAS_CONTABILIDAD,
)


CSV_FACTURAS_VALIDO = """id_factura,nit_proveedor,fecha_factura,concepto,base_gravable,tarifa_iva,valor_iva,tarifa_retencion,valor_retencion,total_factura
FAC-0001,900123456-1,2024-01-15,Servicios de consultoría,1000000,0.19,190000,0.04,40000,1150000
FAC-0002,900654321-2,2024-01-16,Suministros de papelería,500000,0.19,95000,0.025,12500,582500
"""

CSV_CONTABILIDAD_VALIDO = """id_factura,fecha_contabilizacion,cuenta_contable,centro_costo,valor_debito,valor_credito,estado
FAC-0001,2024-01-16,513505,CC-100,1150000,0,Contabilizada
FAC-0002,2024-01-17,513510,CC-200,582500,0,Contabilizada
"""


def test_leer_facturas_validas():
    """Valida que un CSV de facturas con estructura correcta sea leído con éxito."""
    df = leer_csv_facturas(CSV_FACTURAS_VALIDO.encode("utf-8"))
    assert len(df) == 2
    for columna in COLUMNAS_FACTURAS:
        assert columna in df.columns
    assert df.iloc[0]["id_factura"] == "FAC-0001"
    assert df.iloc[0]["nit_proveedor"] == "900123456-1"


def test_leer_contabilidad_valida():
    """Valida que un CSV de registros contables sea leído correctamente."""
    df = leer_csv_contabilidad(io.BytesIO(CSV_CONTABILIDAD_VALIDO.encode("utf-8")))
    assert len(df) == 2
    for columna in COLUMNAS_CONTABILIDAD:
        assert columna in df.columns
    assert df.iloc[1]["id_factura"] == "FAC-0002"
    assert df.iloc[1]["estado"] == "Contabilizada"


def test_archivo_vacio():
    """Verifica que un archivo vacío genere una excepción descriptiva."""
    with pytest.raises(ErrorValidacionCSV, match="está vacío o no contiene registros"):
        leer_csv_facturas(b"")

    with pytest.raises(ErrorValidacionCSV, match="está vacío o no contiene registros"):
        leer_csv_contabilidad("   \n   \n")


def test_columnas_faltantes():
    """Verifica que falte una o más columnas obligatorias dispare un error."""
    csv_incompleto = """id_factura,nit_proveedor,fecha_factura
FAC-0001,900123456-1,2024-01-15
"""
    with pytest.raises(ErrorValidacionCSV, match="no contiene las columnas requeridas"):
        leer_csv_facturas(csv_incompleto.encode("utf-8"))


def test_csv_con_columnas_extra():
    """Verifica que columnas adicionales en el CSV sean toleradas y preservadas."""
    csv_extra = """id_factura,nit_proveedor,fecha_factura,concepto,base_gravable,tarifa_iva,valor_iva,tarifa_retencion,valor_retencion,total_factura,observaciones,sucursal
FAC-0001,900123456-1,2024-01-15,Servicios de auditoría,1000000,0.19,190000,0.04,40000,1150000,Factura aprobada,Bogotá
"""
    df = leer_csv_facturas(csv_extra.encode("utf-8"))
    assert len(df) == 1
    assert "observaciones" in df.columns
    assert "sucursal" in df.columns
    assert df.iloc[0]["sucursal"] == "Bogotá"


def test_codificacion_latin1():
    """Comprueba la correcta lectura de archivos con acentos y codificación Latin-1."""
    csv_latin1 = "id_factura,nit_proveedor,fecha_factura,concepto,base_gravable,tarifa_iva,valor_iva,tarifa_retencion,valor_retencion,total_factura\nFAC-0099,900111-1,2024-02-01,Reparación y dotación eléctrica,200000,0.19,38000,0,0,238000\n"
    bytes_latin1 = csv_latin1.encode("latin-1")
    df = leer_csv_facturas(bytes_latin1)
    assert len(df) == 1
    assert "Reparación" in df.iloc[0]["concepto"]
