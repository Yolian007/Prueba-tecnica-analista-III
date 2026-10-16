"""Punto de entrada principal de la aplicación FastAPI."""

import time
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import configuracion
from app.core.logger import obtener_logger

logger = obtener_logger(__name__)

app = FastAPI(
    title=configuracion.TITULO_PROYECTO,
    version=configuracion.VERSION,
    description=configuracion.DESCRIPCION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuración del middleware de CORS para comunicación con el frontend
permitir_credenciales = "*" not in configuracion.ORIGENES_PERMITIDOS
app.add_middleware(
    CORSMiddleware,
    allow_origins=configuracion.ORIGENES_PERMITIDOS,
    allow_credentials=permitir_credenciales,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def registrar_tiempo_respuesta(request: Request, call_next):
    """Middleware que calcula el tiempo de procesamiento y lo inyecta en las cabeceras HTTP."""
    inicio = time.perf_counter()
    respuesta = await call_next(request)
    duracion = time.perf_counter() - inicio
    respuesta.headers["X-Process-Time"] = f"{duracion:.4f}s"
    return respuesta


@app.exception_handler(HTTPException)
async def manejador_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """Manejador centralizado para excepciones controladas de tipo HTTP."""
    logger.warning(f"Error HTTP {exc.status_code} en {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def manejador_excepcion_no_controlada(request: Request, exc: Exception) -> JSONResponse:
    """Manejador de respaldo para fallos imprevistos no controlados."""
    logger.exception(f"Excepción imprevista no capturada en {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocurrió un error inesperado durante el procesamiento."},
    )


# Inclusión de enrutador principal de la API
app.include_router(router)


@app.get("/", include_in_schema=False)
def ruta_raiz():
    """Redirección informativa en la raíz de la API."""
    return {
        "mensaje": "Bienvenido al API del Conciliador de Facturas y Retenciones",
        "documentacion": "/docs",
        "salud": "/salud",
    }
