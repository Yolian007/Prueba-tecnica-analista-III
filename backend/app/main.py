"""Punto de entrada principal de la aplicación FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import configuracion

app = FastAPI(
    title=configuracion.TITULO_PROYECTO,
    version=configuracion.VERSION,
    description=configuracion.DESCRIPCION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuración del middleware de CORS para comunicación con el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=configuracion.ORIGENES_PERMITIDOS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de enrutador principal de la API
app.include_router(router)


@app.get("/", include_in_schema=False)
def ruta_raiz():
    """Redirección informativa en la raíz de la API."""
    return {
        "mensaje": "Bienvenido al API del Conciliador de Facturas y Retenciones",
        "documentacion": "/docs",
        "salud": "/health",
    }
