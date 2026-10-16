"""Pruebas de integración para los endpoints de la API REST."""

import io
from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)

CSV_FACTURAS = """id_factura,nit_proveedor,fecha_factura,concepto,base_gravable,tarifa_iva,valor_iva,tarifa_retencion,valor_retencion,total_factura
FAC-0001,900123456-1,2024-01-15,Servicios de consultoría,1000000,0.19,190000,0.04,40000,1150000
FAC-0002,900654321-2,2024-01-16,Suministros de papelería,500000,0.19,95000,0.025,12500,582500
"""

CSV_CONTABILIDAD = """id_factura,fecha_contabilizacion,cuenta_contable,centro_costo,valor_debito,valor_credito,estado
FAC-0001,2024-01-16,513505,CC-100,1150000,0,Contabilizada
FAC-0002,2024-01-17,513510,CC-200,582500,0,Contabilizada
"""


def test_health_check():
    """Verifica que el endpoint /health responda correctamente con estado activo."""
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["estado"] == "activo"
    assert datos["servicio"] == "Conciliador de Facturas"


def test_conciliacion_exitosa():
    """Valida la conciliación completa de dos archivos CSV válidos a través de la API."""
    archivos = {
        "facturas": ("facturas.csv", io.BytesIO(CSV_FACTURAS.encode("utf-8")), "text/csv"),
        "contabilidad": ("contabilidad.csv", io.BytesIO(CSV_CONTABILIDAD.encode("utf-8")), "text/csv"),
    }
    respuesta = cliente.post("/api/conciliacion", files=archivos)
    assert respuesta.status_code == 200

    datos = respuesta.json()
    assert "resumen" in datos
    assert "resultados" in datos

    resumen = datos["resumen"]
    assert resumen["total_facturas"] == 2
    assert resumen["correctas"] == 2
    assert resumen["con_inconsistencia"] == 0

    assert len(datos["resultados"]) == 2
    assert datos["resultados"][0]["id_factura"] == "FAC-0001"
    assert datos["resultados"][0]["estado"] == "Correcta"


def test_falta_archivo():
    """Verifica que la petición falle si no se envía alguno de los archivos obligatorios."""
    # Envío únicamente de facturas sin contabilidad
    archivos = {
        "facturas": ("facturas.csv", io.BytesIO(CSV_FACTURAS.encode("utf-8")), "text/csv"),
    }
    respuesta = cliente.post("/api/conciliacion", files=archivos)
    assert respuesta.status_code in (400, 422)


def test_archivo_invalido():
    """Verifica que un archivo vacío o corrupto retorne error 400 con mensaje claro en español."""
    archivos = {
        "facturas": ("facturas.csv", io.BytesIO(b""), "text/csv"),
        "contabilidad": ("contabilidad.csv", io.BytesIO(CSV_CONTABILIDAD.encode("utf-8")), "text/csv"),
    }
    respuesta = cliente.post("/api/conciliacion", files=archivos)
    assert respuesta.status_code == 400
    datos = respuesta.json()
    assert "está vacío" in datos["detail"]


def test_columnas_faltantes():
    """Verifica que un archivo sin las columnas requeridas retorne error 400."""
    csv_incompleto = "id_factura,total_factura\nFAC-0001,1000\n"
    archivos = {
        "facturas": ("facturas.csv", io.BytesIO(csv_incompleto.encode("utf-8")), "text/csv"),
        "contabilidad": ("contabilidad.csv", io.BytesIO(CSV_CONTABILIDAD.encode("utf-8")), "text/csv"),
    }
    respuesta = cliente.post("/api/conciliacion", files=archivos)
    assert respuesta.status_code == 400
    datos = respuesta.json()
    assert "columnas requeridas" in datos["detail"]
