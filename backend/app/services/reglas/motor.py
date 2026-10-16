"""Motor de ejecución y orquestación de reglas de conciliación."""

from typing import List, Sequence

from app.services.reglas.base import ContextoFactura, ReglaConciliacion
from app.services.reglas.reglas_contables import (
    ReglaIdentificadorObligatorio,
    ReglaBaseGravableObligatoria,
    ReglaDiferenciaIVA,
    ReglaDiferenciaTotal,
    ReglaFacturaDuplicada,
    ReglaFacturaSinContabilidad,
    ReglaCamposObligatoriosAdicionales,
)


class MotorReglasConciliacion:
    """Motor encargado de ejecutar secuencialmente las reglas de conciliación sobre una factura."""

    def __init__(self, reglas: Sequence[ReglaConciliacion] | None = None) -> None:
        if reglas is None:
            self.reglas: List[ReglaConciliacion] = self.obtener_reglas_predeterminadas()
        else:
            self.reglas = list(reglas)

    @staticmethod
    def obtener_reglas_predeterminadas() -> List[ReglaConciliacion]:
        """Retorna el conjunto estándar de reglas de negocio para la conciliación."""
        return [
            ReglaIdentificadorObligatorio(),
            ReglaBaseGravableObligatoria(),
            ReglaDiferenciaIVA(),
            ReglaDiferenciaTotal(),
            ReglaFacturaDuplicada(),
            ReglaFacturaSinContabilidad(),
            ReglaCamposObligatoriosAdicionales(),
        ]

    def agregar_regla(self, regla: ReglaConciliacion) -> None:
        """Permite registrar una regla adicional en el motor."""
        self.reglas.append(regla)

    def evaluar_factura(self, contexto: ContextoFactura) -> List[str]:
        """Aplica todas las reglas configuradas al contexto de una factura dada.

        Args:
            contexto: Contexto analizado de la factura actual.

        Returns:
            Lista consolidada con todas las inconsistencias encontradas.
        """
        inconsistencias: List[str] = []
        for regla in self.reglas:
            hallazgos = regla.evaluar(contexto)
            if hallazgos:
                inconsistencias.extend(hallazgos)
        return inconsistencias
