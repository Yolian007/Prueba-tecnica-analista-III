"""Configuración y fixtures globales para la suite de pruebas."""

import sys
from pathlib import Path

# Asegurar que el directorio raíz del backend esté en sys.path
DIRECTORIO_RAIZ = Path(__file__).resolve().parent.parent
if str(DIRECTORIO_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIRECTORIO_RAIZ))
