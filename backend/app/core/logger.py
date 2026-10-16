"""Configuración centralizada de bitácora y registro de eventos (logging)."""

import logging
import sys


def configurar_logging(nivel: int = logging.INFO) -> None:
    """Configura el formato y nivel global para los registradores de eventos de la aplicación."""
    formato = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    formato_fecha = "%Y-%m-%d %H:%M:%S"

    # Evita duplicar manejadores si ya están configurados
    raiz = logging.getLogger()
    if not raiz.handlers:
        manejador = logging.StreamHandler(sys.stdout)
        manejador.setFormatter(logging.Formatter(formato, datefmt=formato_fecha))
        raiz.addHandler(manejador)
        raiz.setLevel(nivel)


def obtener_logger(nombre: str = "conciliador") -> logging.Logger:
    """Retorna una instancia configurada de logger para un módulo específico.

    Args:
        nombre: Nombre del módulo o componente que emite los registros.

    Returns:
        Instancia de logging.Logger.
    """
    configurar_logging()
    return logging.getLogger(nombre)
