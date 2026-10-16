"""Rutas y controladores de la API REST para el conciliador de facturas."""

from typing import Dict
from fastapi import APIRouter, Depends, File, UploadFile, status

from app.schemas.conciliacion import RespuestaConciliacion, RespuestaError
from app.services.servicio_conciliacion import (
    ServicioConciliacion,
    obtener_servicio_conciliacion,
)

enrutador = APIRouter()
router = enrutador


@enrutador.get(
    "/salud",
    summary="Verificación del estado del servicio",
    description="Retorna el estado de disponibilidad y operatividad del servicio.",
    tags=["Salud"],
)
def verificar_salud() -> Dict[str, str]:
    """Verifica que el servicio esté activo y listo para procesar solicitudes."""
    return {"estado": "activo", "servicio": "Conciliador de Facturas"}


@enrutador.get("/health", include_in_schema=False)
def verificar_salud_alias() -> Dict[str, str]:
    """Ruta alias en inglés para compatibilidad con sistemas de monitoreo estándar."""
    return verificar_salud()


@enrutador.post(
    "/api/conciliacion",
    response_model=RespuestaConciliacion,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": RespuestaError,
            "description": "Error en archivos de entrada o estructura CSV inválida",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": RespuestaError,
            "description": "Error interno durante la ejecución del proceso",
        },
    },
    summary="Conciliar facturas vs registros contables",
    description="Recibe dos archivos CSV (facturas y contabilidad) y retorna el detalle de inconsistencias y resumen cuantitativo.",
    tags=["Conciliación"],
)
async def conciliar_archivos(
    facturas: UploadFile = File(..., description="Archivo CSV con facturas emitidas"),
    contabilidad: UploadFile = File(..., description="Archivo CSV con registros contables"),
    servicio: ServicioConciliacion = Depends(obtener_servicio_conciliacion),
) -> RespuestaConciliacion:
    """Controlador que delega la conciliación de facturas al servicio de aplicación."""
    return await servicio.procesar_archivos_subidos(
        archivo_facturas=facturas,
        archivo_contabilidad=contabilidad,
    )
