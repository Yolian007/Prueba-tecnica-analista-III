"""Rutas y controladores de la API REST para el conciliador de facturas."""

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas.conciliacion import RespuestaConciliacion, ErrorResponse
from app.services.lector_csv import (
    leer_csv_facturas,
    leer_csv_contabilidad,
    ErrorValidacionCSV,
)
from app.services.conciliacion import procesar_conciliacion

enrutador = APIRouter()
router = enrutador


@enrutador.get(
    "/health",
    summary="Verificación del estado del servicio",
    description="Retorna el estado de disponibilidad y operatividad del servicio.",
    tags=["Salud"],
)
def verificar_salud() -> dict:
    """Verifica que el servicio esté activo y listo para procesar solicitudes."""
    return {"estado": "activo", "servicio": "Conciliador de Facturas"}


@enrutador.post(
    "/api/conciliacion",
    response_model=RespuestaConciliacion,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Error en archivos de entrada"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Error interno del servidor"},
    },
    summary="Conciliar facturas vs registros contables",
    description="Recibe dos archivos CSV (facturas y contabilidad) y retorna el detalle de inconsistencias y resumen.",
    tags=["Conciliación"],
)
async def conciliar_archivos(
    facturas: UploadFile = File(..., description="Archivo CSV con facturas emitidas"),
    contabilidad: UploadFile = File(..., description="Archivo CSV con registros contables"),
) -> RespuestaConciliacion:
    """Procesa y concilia los archivos de facturas y contabilidad cargados."""
    if not facturas or not facturas.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar el archivo CSV de facturas.",
        )

    if not contabilidad or not contabilidad.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar el archivo CSV de contabilidad.",
        )

    # Lectura del contenido de los archivos cargados
    try:
        contenido_facturas = await facturas.read()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No fue posible leer el archivo de facturas: {str(exc)}",
        ) from exc

    try:
        contenido_contabilidad = await contabilidad.read()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No fue posible leer el archivo de contabilidad: {str(exc)}",
        ) from exc

    # Procesamiento y lectura de CSV a DataFrames
    try:
        df_facturas = leer_csv_facturas(
            contenido_facturas, nombre_archivo=facturas.filename or "facturas.csv"
        )
    except ErrorValidacionCSV as err_csv:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err_csv),
        ) from err_csv
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar el archivo de facturas: {str(exc)}",
        ) from exc

    try:
        df_contabilidad = leer_csv_contabilidad(
            contenido_contabilidad, nombre_archivo=contabilidad.filename or "contabilidad.csv"
        )
    except ErrorValidacionCSV as err_csv:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err_csv),
        ) from err_csv
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar el archivo de contabilidad: {str(exc)}",
        ) from exc

    # Ejecución de la lógica de negocio de conciliación
    try:
        resultado = procesar_conciliacion(df_facturas, df_contabilidad)
        return RespuestaConciliacion.model_validate(resultado)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno durante el procesamiento de la conciliación: {str(exc)}",
        ) from exc
