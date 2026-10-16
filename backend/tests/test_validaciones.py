"""Pruebas unitarias para las funciones de validación y conversión."""

from decimal import Decimal
import pytest
from app.services.validaciones import (
    validate_numeric_field,
    validate_required_field,
    normalize_id,
    validate_tarifa,
    validar_campo_numerico,
    validar_campo_requerido,
    normalizar_id,
    validar_tarifa,
)


def test_convertir_numero_valido():
    """Valida la conversión exitosa de diversas representaciones numéricas a Decimal."""
    assert validate_numeric_field("1000.50", "campo") == Decimal("1000.50")
    assert validate_numeric_field(500, "campo") == Decimal("500")
    assert validate_numeric_field(Decimal("123.45"), "campo") == Decimal("123.45")
    assert validate_numeric_field("  $ 450000.00 ", "campo") == Decimal("450000.00")
    assert validar_campo_numerico("0.19", "tarifa") == Decimal("0.19")


def test_convertir_numero_invalido():
    """Verifica que valores no numéricos o vacíos generen ValueError descriptivo."""
    with pytest.raises(ValueError, match="contiene un valor numérico inválido"):
        validate_numeric_field("invalido", "tarifa")

    with pytest.raises(ValueError, match="está vacío o no contiene un valor numérico"):
        validate_numeric_field("", "base")

    with pytest.raises(ValueError, match="está vacío o no contiene un valor numérico"):
        validate_numeric_field(None, "base")

    with pytest.raises(ValueError, match="contiene un valor numérico inválido"):
        validar_campo_numerico("12.34.56", "total")


def test_normalizar_id():
    """Verifica la eliminación de espacios en blanco y tratamiento de nulos en identificadores."""
    assert normalize_id("  FAC-0001   ") == "FAC-0001"
    assert normalize_id("FAC-0002\n") == "FAC-0002"
    assert normalize_id(None) == ""
    assert normalize_id("nan") == ""
    assert normalizar_id("   ") == ""


def test_campo_vacio():
    """Valida la detección correcta de campos con o sin contenido."""
    assert validate_required_field("") is False
    assert validate_required_field("   ") is False
    assert validate_required_field(None) is False
    assert validate_required_field("nan") is False
    assert validate_required_field("null") is False
    assert validate_required_field("Contenido válido") is True
    assert validar_campo_requerido("900123456-1") is True


def test_validar_tarifa():
    """Verifica que las tarifas porcentuales en decimal estén dentro del rango permitido [0, 1]."""
    assert validate_tarifa("0.19") is True
    assert validate_tarifa(Decimal("0.05")) is True
    assert validate_tarifa("0.0") is True
    assert validate_tarifa("1.0") is True
    assert validate_tarifa("-0.05") is False
    assert validate_tarifa("1.5") is False
    assert validate_tarifa("no-aplica") is False
    assert validar_tarifa(0.19) is True
