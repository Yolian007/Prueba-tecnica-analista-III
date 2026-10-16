"""Configuración central del servicio FastAPI."""

import os
from typing import List
from dotenv import load_dotenv

# Carga de variables de entorno desde archivo .env local si existe
load_dotenv()


class Configuracion:
    """Clase de configuración que carga parámetros desde variables de entorno con valores por defecto."""

    TITULO_PROYECTO: str = os.getenv("TITULO_PROYECTO", "Conciliador de Facturas y Retenciones")
    VERSION: str = os.getenv("VERSION_PROYECTO", "1.0.0")
    DESCRIPCION: str = os.getenv(
        "DESCRIPCION_PROYECTO",
        "Servicio backend para conciliación automática de facturas y registros contables.",
    )
    HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("BACKEND_PORT", "8000"))

    @property
    def ORIGENES_PERMITIDOS(self) -> List[str]:
        """Retorna la lista de orígenes permitidos para solicitudes de CORS."""
        origenes_crudos = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200")
        if not origenes_crudos:
            return ["http://localhost:4200"]
        return [origen.strip() for origen in origenes_crudos.split(",") if origen.strip()]


# Instancia singleton para uso en toda la aplicación
configuracion = Configuracion()
settings = configuracion
