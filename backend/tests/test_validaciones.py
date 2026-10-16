"""Pruebas unitarias para las funciones de validación y conversión."""

from decimal import Decimal
import pytest
from app.services.validaciones import (
    normalizar_id,
    validar_campo_numerico,
    validar_campo_requerido,
    validar_tarifa,
    normalize_id,
    validate_numeric_field,
    validate_required_field,
    validate_tarifa,
)


def test_convertir_numero_valido():
    """Valida la conversión exitosa de diversas representaciones numéricas a Decimal."""
    assert validar_campo_numerico("1000.50", "campo") == Decimal("1000.50")
    assert validar_campo_numerico(500, "campo") == Decimal("500")
    assert validar_campo_numerico(Decimal("123.45"), "campo") == Decimal("123.45")
    assert validar_campo_numerico("  $ 450000.00 ", "campo") == Decimal("450000.00")
    assert validar_campo_numerico("0.19", "tarifa") == Decimal("0.19")
    # Compatibilidad con alias
    assert validate_numeric_field("1000.50", "campo") == Decimal("1000.50")


def test_convertir_numero_invalido():
    """Verifica que valores no numéricos o vacíos generen ValueError descriptivo."""
    with pytest.raises(ValueError, match="contiene un valor numérico inválido"):
        validar_campo_numerico("invalido", "tarifa")

    with pytest.raises(ValueError, match="está vacío o no contiene un valor numérico"):
        validar_campo_numerico("", "base")

    with pytest.raises(ValueError, match="está vacío o no contiene un valor numérico"):
        validar_campo_numerico(None, "base")

    with pytest.raises(ValueError, match="contiene un valor numérico inválido"):
        validar_campo_numerico("12.34.56", "total")


def test_normalizar_id():
    """Verifica la eliminación de espacios en blanco y tratamiento de nulos en identificadores."""
    assert normalizar_id("  FAC-0001   ") == "FAC-0001"
    assert normalizar_id("FAC-0002\n") == "FAC-0002"
    assert normalizar_id(None) == ""
    assert normalizar_id("nan") == ""
    assert normalizar_id("   ") == ""
    # Compatibilidad con alias
    assert normalize_id("  FAC-0001   ") == "FAC-0001"


def test_campo_vacio():
    """Valida la detección correcta de campos con o sin contenido."""
    assert validar_campo_requerido("") is False
    assert validar_campo_requerido("   ") is False
    assert validar_campo_requerido(None) is False
    assert validar_campo_requerido("nan") is False
    assert validar_campo_requerido("null") is False
    assert validar_campo_requerido("Contenido válido") is True
    assert validar_campo_requerido("900123456-1") is True
    # Compatibilidad con alias
    assert validate_required_field("Contenido válido") is True


def test_validar_tarifa():
    """Verifica que las tarifas porcentuales en decimal estén dentro del rango permitido [0, 1]."""
    assert validar_tarifa("0.19") is True
    assert validar_tarifa(Decimal("0.05")) is True
    assert validar_tarifa("0.0") is True
    assert validar_tarifa("1.0") is True
    assert validar_tarifa("-0.05") is False
    assert validar_tarifa("1.5") is False
    assert validar_tarifa("no-aplica") is False
    assert validar_tarifa(0.19) is True
    # Compatibilidad con alias
    assert validate_tarifa("0.19") is True
