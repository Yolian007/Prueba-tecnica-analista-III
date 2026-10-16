"""Servicio de aplicación para orquestar la conciliación de archivos cargados."""

import time
from fastapi import HTTPException, UploadFile, status
import pandas as pd

from app.core.logger import obtener_logger
from app.schemas.conciliacion import RespuestaConciliacion
from app.services.conciliacion import procesar_conciliacion
from app.services.lector_csv import (
    ErrorValidacionCSV,
    leer_csv_contabilidad,
    leer_csv_facturas,
)
from app.services.reglas import MotorReglasConciliacion

logger = obtener_logger(__name__)


class ServicioConciliacion:
    """Orquestador de caso de uso para procesar y conciliar archivos CSV."""

    def __init__(self, motor: MotorReglasConciliacion | None = None) -> None:
        self.motor = motor or MotorReglasConciliacion()

    async def _leer_bytes_archivo(self, archivo: UploadFile, nombre_parametro: str) -> bytes:
        """Extrae el contenido en bytes de un archivo subido validando su presencia."""
        if not archivo or not archivo.filename:
            logger.warning(f"Intento de conciliación sin archivo requerido: {nombre_parametro}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Debe proporcionar el archivo CSV de {nombre_parametro}.",
            )
        try:
            return await archivo.read()
        except Exception as exc:
            logger.error(f"Error al leer bytes de {nombre_parametro}: {str(exc)}")
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
            logger.warning(f"Validación fallida en '{nombre_archivo}': {str(err_csv)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(err_csv),
            ) from err_csv
        except Exception as exc:
            logger.error(f"Error imprevisto procesando '{nombre_archivo}': {str(exc)}")
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
        nombre_f = archivo_facturas.filename or "facturas.csv"
        nombre_c = archivo_contabilidad.filename or "contabilidad.csv"
        logger.info(f"Iniciando conciliación para '{nombre_f}' y '{nombre_c}'")
        inicio = time.perf_counter()

        # 1. Lectura asíncrona de los flujos de bytes
        bytes_facturas = await self._leer_bytes_archivo(archivo_facturas, "facturas")
        bytes_contabilidad = await self._leer_bytes_archivo(archivo_contabilidad, "contabilidad")

        # 2. Parseo y validación estructural a DataFrames
        df_facturas = self._convertir_csv_a_dataframe(
            bytes_facturas,
            nombre_archivo=nombre_f,
            es_factura=True,
        )
        df_contabilidad = self._convertir_csv_a_dataframe(
            bytes_contabilidad,
            nombre_archivo=nombre_c,
            es_factura=False,
        )

        logger.info(
            f"Archivos parseados con éxito: {len(df_facturas)} facturas, "
            f"{len(df_contabilidad)} registros contables."
        )

        # 3. Ejecución de la lógica de negocio a través del motor de reglas
        try:
            resultado = procesar_conciliacion(df_facturas, df_contabilidad, motor=self.motor)
            duracion = time.perf_counter() - inicio
            logger.info(
                f"Conciliación completada en {duracion:.3f}s: "
                f"total={resultado.resumen.total_facturas}, "
                f"correctas={resultado.resumen.correctas}, "
                f"con_inconsistencia={resultado.resumen.con_inconsistencia}"
            )
            return resultado
        except Exception as exc:
            logger.exception("Fallo inesperado durante la ejecución de las reglas de conciliación")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno durante el procesamiento de la conciliación: {str(exc)}",
            ) from exc


def obtener_servicio_conciliacion() -> ServicioConciliacion:
    """Proveedor de dependencias para inyectar el servicio de conciliación en controladores."""
    return ServicioConciliacion()
