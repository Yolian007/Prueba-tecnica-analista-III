"""Pruebas unitarias para el servicio de aplicación ServicioConciliacion."""

import io
import pytest
from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers

from app.services.servicio_conciliacion import (
    ServicioConciliacion,
    obtener_servicio_conciliacion,
)

CSV_FACTURAS = """id_factura,nit_proveedor,fecha_factura,concepto,base_gravable,tarifa_iva,valor_iva,tarifa_retencion,valor_retencion,total_factura
FAC-0001,900123456-1,2024-01-15,Servicios de consultoría,1000000,0.19,190000,0.04,40000,1150000
"""

CSV_CONTABILIDAD = """id_factura,fecha_contabilizacion,cuenta_contable,centro_costo,valor_debito,valor_credito,estado
FAC-0001,2024-01-16,513505,CC-100,1150000,0,Contabilizada
"""


def _crear_upload_file(nombre: str, contenido: str) -> UploadFile:
    """Helper para crear un objeto UploadFile en memoria para pruebas."""
    stream = io.BytesIO(contenido.encode("utf-8"))
    return UploadFile(
        file=stream,
        filename=nombre,
        headers=Headers({"content-type": "text/csv"}),
    )


@pytest.mark.anyio
async def test_servicio_conciliacion_exitoso():
    """Valida la orquestación exitosa de archivos a través del servicio."""
    servicio = ServicioConciliacion()
    archivo_f = _crear_upload_file("facturas.csv", CSV_FACTURAS)
    archivo_c = _crear_upload_file("contabilidad.csv", CSV_CONTABILIDAD)

    resultado = await servicio.procesar_archivos_subidos(archivo_f, archivo_c)

    assert resultado.resumen.total_facturas == 1
    assert resultado.resumen.correctas == 1
    assert resultado.resumen.con_inconsistencia == 0
    assert len(resultado.resultados) == 1
    assert resultado.resultados[0].id_factura == "FAC-0001"
    assert resultado.resultados[0].estado == "Correcta"


@pytest.mark.anyio
async def test_servicio_archivo_faltante():
    """Verifica que se lance HTTPException si el archivo o su nombre están ausentes."""
    servicio = ServicioConciliacion()
    archivo_f = UploadFile(file=io.BytesIO(b""), filename="")
    archivo_c = _crear_upload_file("contabilidad.csv", CSV_CONTABILIDAD)

    with pytest.raises(HTTPException) as exc_info:
        await servicio.procesar_archivos_subidos(archivo_f, archivo_c)

    assert exc_info.value.status_code == 400
    assert "Debe proporcionar el archivo CSV de facturas" in exc_info.value.detail


@pytest.mark.anyio
async def test_servicio_csv_invalido():
    """Verifica que un CSV sin encabezados requeridos dispare HTTPException 400."""
    servicio = ServicioConciliacion()
    archivo_f = _crear_upload_file("facturas.csv", "columna_invalida\n123\n")
    archivo_c = _crear_upload_file("contabilidad.csv", CSV_CONTABILIDAD)

    with pytest.raises(HTTPException) as exc_info:
        await servicio.procesar_archivos_subidos(archivo_f, archivo_c)

    assert exc_info.value.status_code == 400
    assert "columnas requeridas" in exc_info.value.detail


def test_obtener_servicio_conciliacion_factory():
    """Verifica la función factoría utilizada para la inyección de dependencias."""
    instancia = obtener_servicio_conciliacion()
    assert isinstance(instancia, ServicioConciliacion)
