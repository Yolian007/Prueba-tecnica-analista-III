"""Módulo de utilidades y funciones de validación de datos contables y fiscales."""

from decimal import Decimal, InvalidOperation
from typing import Any
import pandas as pd


def normalize_id(identificador: Any) -> str:
    """Normaliza un identificador eliminando espacios en blanco al inicio y al final.

    Args:
        identificador: Valor a normalizar (cadena, número o nulo).

    Returns:
        Cadena de texto limpia o vacía si el valor original es nulo.
    """
    if identificador is None or pd.isna(identificador):
        return ""
    texto = str(identificador).strip()
    if texto.lower() in ("nan", "none", "null", "<na>"):
        return ""
    return texto


def validate_required_field(valor: Any) -> bool:
    """Comprueba si un campo requerido contiene información no nula y no vacía.

    Args:
        valor: Valor a verificar.

    Returns:
        True si el campo tiene contenido válido, False en caso contrario.
    """
    if valor is None or pd.isna(valor):
        return False
    texto = str(valor).strip()
    if not texto or texto.lower() in ("nan", "none", "null", "<na>"):
        return False
    return True


def validate_numeric_field(valor: Any, nombre_campo: str = "campo") -> Decimal:
    """Convierte un valor a tipo Decimal para cálculos monetarios exactos.

    Args:
        valor: Dato numérico o cadena de texto que representa una cifra.
        nombre_campo: Nombre descriptivo del campo para mensajes de error.

    Returns:
        Valor convertido a Decimal.

    Raises:
        ValueError: Si el campo está vacío, es nulo o no representa un número válido.
    """
    if valor is None or pd.isna(valor):
        raise ValueError(f"El campo '{nombre_campo}' está vacío o no contiene un valor numérico.")

    if isinstance(valor, Decimal):
        return valor

    texto_limpio = str(valor).strip().replace("$", "").replace(" ", "")
    if not texto_limpio or texto_limpio.lower() in ("nan", "none", "null", "<na>"):
        raise ValueError(f"El campo '{nombre_campo}' está vacío o no contiene un valor numérico.")

    try:
        return Decimal(texto_limpio)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(
            f"El campo '{nombre_campo}' contiene un valor numérico inválido: '{valor}'."
        ) from exc


def validate_tarifa(tarifa: Any) -> bool:
    """Valida que una tarifa porcentual se encuentre en el rango permitido [0, 1].

    Args:
        tarifa: Valor porcentual expresado en formato decimal (ej: 0.19, 0.05, 0.0).

    Returns:
        True si la tarifa es válida y está entre 0 y 1, False en caso contrario.
    """
    try:
        valor_decimal = validate_numeric_field(tarifa, "tarifa")
        return Decimal("0.0") <= valor_decimal <= Decimal("1.0")
    except (ValueError, InvalidOperation):
        return False


# Alias en español para mantener coherencia semántica en todo el código
normalizar_id = normalize_id
validar_campo_requerido = validate_required_field
validar_campo_numerico = validate_numeric_field
validar_tarifa = validate_tarifa
