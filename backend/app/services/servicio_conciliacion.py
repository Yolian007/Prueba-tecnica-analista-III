"""Servicio de aplicación para orquestar la conciliación de archivos cargados."""

from fastapi import HTTPException, UploadFile, status
import pandas as pd

from app.schemas.conciliacion import RespuestaConciliacion
from app.services.conciliacion import procesar_conciliacion
from app.services.lector_csv import (
    ErrorValidacionCSV,
    leer_csv_contabilidad,
    leer_csv_facturas,
)
from app.services.reglas import MotorReglasConciliacion


class ServicioConciliacion:
    """Orquestador de caso de uso para procesar y conciliar archivos CSV."""

    def __init__(self, motor: MotorReglasConciliacion | None = None) -> None:
        self.motor = motor or MotorReglasConciliacion()

    async def _leer_bytes_archivo(self, archivo: UploadFile, nombre_parametro: str) -> bytes:
        """Extrae el contenido en bytes de un archivo subido validando su presencia."""
        if not archivo or not archivo.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Debe proporcionar el archivo CSV de {nombre_parametro}.",
            )
        try:
            return await archivo.read()
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No fue posible leer el archivo de {nombre_parametro}: {str(exc)}",
            ) from exc

    def _convertir_csv_a_dataframe(
        self,
        contenido: bytes,
        nombre_archivo: str,
        es_factura: bool,
    ) -> pd.DataFrame:
        """Parsea los bytes a DataFrame aplicando las validaciones de columnas."""
        tipo_archivo = "facturas" if es_factura else "contabilidad"
        funcion_lectura = leer_csv_facturas if es_factura else leer_csv_contabilidad

        try:
            return funcion_lectura(contenido, nombre_archivo=nombre_archivo)
        except ErrorValidacionCSV as err_csv:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(err_csv),
            ) from err_csv
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al procesar el archivo de {tipo_archivo}: {str(exc)}",
            ) from exc

    async def procesar_archivos_subidos(
        self,
        archivo_facturas: UploadFile,
        archivo_contabilidad: UploadFile,
    ) -> RespuestaConciliacion:
        """Coordina el flujo completo: lectura, parseo tabular y ejecución de reglas."""
        # 1. Lectura asíncrona de los flujos de bytes
        bytes_facturas = await self._leer_bytes_archivo(archivo_facturas, "facturas")
        bytes_contabilidad = await self._leer_bytes_archivo(archivo_contabilidad, "contabilidad")

        # 2. Parseo y validación estructural a DataFrames
        df_facturas = self._convertir_csv_a_dataframe(
            bytes_facturas,
            nombre_archivo=archivo_facturas.filename or "facturas.csv",
            es_factura=True,
        )
        df_contabilidad = self._convertir_csv_a_dataframe(
            bytes_contabilidad,
            nombre_archivo=archivo_contabilidad.filename or "contabilidad.csv",
            es_factura=False,
        )

        # 3. Ejecución de la lógica de negocio a través del motor de reglas
        try:
            return procesar_conciliacion(df_facturas, df_contabilidad, motor=self.motor)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno durante el procesamiento de la conciliación: {str(exc)}",
            ) from exc


def obtener_servicio_conciliacion() -> ServicioConciliacion:
    """Proveedor de dependencias para inyectar el servicio de conciliación en controladores."""
    return ServicioConciliacion()
