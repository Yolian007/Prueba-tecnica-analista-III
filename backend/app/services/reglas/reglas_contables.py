"""Implementación de las reglas de negocio individuales de conciliación."""

from typing import List

from app.services.reglas.base import ContextoFactura, ReglaConciliacion
from app.services.validaciones import validate_required_field


class ReglaIdentificadorObligatorio(ReglaConciliacion):
    """Verifica que el identificador de la factura no esté vacío."""

    def evaluar(self, contexto: ContextoFactura) -> List[str]:
        if not contexto.id_factura:
            return ["Campo obligatorio vacío: id_factura"]
        return []


class ReglaBaseGravableObligatoria(ReglaConciliacion):
    """Verifica que la base gravable esté presente y sea un número válido."""

    def evaluar(self, contexto: ContextoFactura) -> List[str]:
        if contexto.tiene_base_vacia:
            return ["Campo obligatorio vacío: base_gravable"]
        return []


class ReglaDiferenciaIVA(ReglaConciliacion):
    """Verifica que el IVA reportado coincida exactamente con base_gravable * tarifa_iva."""

    def evaluar(self, contexto: ContextoFactura) -> List[str]:
        if contexto.valor_iva != contexto.iva_esperado:
            return ["Diferencia en IVA"]
        return []


class ReglaDiferenciaTotal(ReglaConciliacion):
    """Verifica que el total reportado coincida con base + iva_esperado - retencion."""

    def evaluar(self, contexto: ContextoFactura) -> List[str]:
        if contexto.total_factura != contexto.total_esperado:
            return ["Diferencia en total"]
        return []


class ReglaFacturaDuplicada(ReglaConciliacion):
    """Detecta si la factura aparece repetida más de una vez en el archivo de facturación."""

    def evaluar(self, contexto: ContextoFactura) -> List[str]:
        if contexto.id_factura and contexto.id_factura in contexto.ids_duplicados:
            return ["Factura duplicada"]
        return []


class ReglaFacturaSinContabilidad(ReglaConciliacion):
    """Detecta si la factura no cuenta con registro en el sistema contable."""

    def evaluar(self, contexto: ContextoFactura) -> List[str]:
        if contexto.id_factura and contexto.id_factura not in contexto.ids_contabilidad:
            return ["Factura sin registro contable"]
        return []


class ReglaCamposObligatoriosAdicionales(ReglaConciliacion):
    """Verifica la obligatoriedad de nit_proveedor, fecha_factura y concepto."""

    CAMPOS = ("nit_proveedor", "fecha_factura", "concepto")

    def evaluar(self, contexto: ContextoFactura) -> List[str]:
        inconsistencias: List[str] = []
        for campo in self.CAMPOS:
            if not validate_required_field(contexto.fila_cruda.get(campo)):
                inconsistencias.append(f"Campo obligatorio vacío: {campo}")
        return inconsistencias
