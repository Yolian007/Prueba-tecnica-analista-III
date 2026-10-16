"""Modelos de datos Pydantic para el proceso de conciliación de facturas."""

from typing import List
from pydantic import BaseModel, Field


class ModeloBase(BaseModel):
    """Modelo base que permite acceso por atributo y por clave para retrocompatibilidad."""

    def __getitem__(self, clave: str):
        return getattr(self, clave)


class ResultadoFactura(ModeloBase):
    """Modelo detallado del resultado de validación y conciliación de una factura individual."""

    id_factura: str = Field(..., description="Identificador único de la factura")
    nit_proveedor: str = Field(..., description="NIT o número de identificación tributaria del proveedor")
    fecha_factura: str = Field(..., description="Fecha de emisión de la factura en formato YYYY-MM-DD")
    concepto: str = Field(..., description="Descripción o concepto del bien o servicio facturado")
    base_gravable: str = Field(..., description="Valor base gravable de la factura en formato monetario")
    iva_reportado: str = Field(..., description="Valor de IVA reportado en la factura")
    iva_esperado: str = Field(..., description="Valor de IVA calculado según la base gravable y la tarifa")
    total_reportado: str = Field(..., description="Valor total reportado en la factura")
    total_esperado: str = Field(..., description="Valor total esperado según la fórmula base + IVA esperado - retención")
    retencion_reportada: str = Field(..., description="Valor de retención reportado en la factura")
    estado: str = Field(..., description="Estado de la factura: 'Correcta' o 'Con inconsistencia'")
    inconsistencias: List[str] = Field(default_factory=list, description="Lista de descripciones de inconsistencias halladas")


class ResumenConciliacion(ModeloBase):
    """Resumen cuantitativo global del proceso de conciliación."""

    total_facturas: int = Field(..., description="Cantidad total de facturas analizadas")
    correctas: int = Field(..., description="Cantidad de facturas sin inconsistencias")
    con_inconsistencia: int = Field(..., description="Cantidad de facturas que presentan alguna inconsistencia")


class RespuestaConciliacion(ModeloBase):
    """Estructura de respuesta final del servicio de conciliación."""

    resumen: ResumenConciliacion = Field(..., description="Resumen estadístico de la conciliación")
    resultados: List[ResultadoFactura] = Field(..., description="Lista con el detalle de cada factura procesada")


class ErrorResponse(ModeloBase):
    """Esquema estándar para mensajes de error del sistema."""

    detail: str = Field(..., description="Mensaje explicativo del error ocurrido")
