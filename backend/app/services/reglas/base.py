"""Contratos e interfaces base para el motor de reglas de conciliación."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Set


@dataclass
class ContextoFactura:
    """Contexto enriquecido de una factura para evaluación de reglas contables."""

    id_factura: str
    nit_proveedor: str
    fecha_factura: str
    concepto: str
    base_gravable: Decimal
    tarifa_iva: Decimal
    valor_iva: Decimal
    tarifa_retencion: Decimal
    valor_retencion: Decimal
    total_factura: Decimal
    iva_esperado: Decimal
    total_esperado: Decimal
    tiene_base_vacia: bool
    fila_cruda: Dict[str, Any]
    ids_duplicados: Set[str] = field(default_factory=set)
    ids_contabilidad: Set[str] = field(default_factory=set)
    retencion_esperada: Decimal = Decimal("0.00")
    estados_contabilidad_factura: Set[str] = field(default_factory=set)
    valores_contabilidad_factura: List[Decimal] = field(default_factory=list)


class ReglaConciliacion(ABC):
    """Interfaz base para toda regla de negocio en el proceso de conciliación."""

    @abstractmethod
    def evaluar(self, contexto: ContextoFactura) -> List[str]:
        """Evalúa el contexto de la factura y retorna una lista de inconsistencias detectadas.

        Args:
            contexto: Datos numéricos, textuales y de referencia de la factura.

        Returns:
            Lista con descripciones de inconsistencias encontradas (vacía si es correcta).
        """
        pass
