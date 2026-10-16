"""Servicio para lectura, decodificación y validación de archivos CSV."""

import io
from typing import Any, List, Union
import pandas as pd


# Definición de columnas obligatorias para facturas y contabilidad
COLUMNAS_FACTURAS: List[str] = [
    "id_factura",
    "nit_proveedor",
    "fecha_factura",
    "concepto",
    "base_gravable",
    "tarifa_iva",
    "valor_iva",
    "tarifa_retencion",
    "valor_retencion",
    "total_factura",
]

COLUMNAS_CONTABILIDAD: List[str] = [
    "id_factura",
    "fecha_contabilizacion",
    "cuenta_contable",
    "centro_costo",
    "valor_debito",
    "valor_credito",
    "estado",
]


class ErrorValidacionCSV(ValueError):
    """Excepción personalizada para fallos en la lectura o validación de estructura de archivos CSV."""
    pass


def decodificar_contenido(contenido_bytes: bytes, nombre_archivo: str = "archivo") -> str:
    """Intenta decodificar el contenido en bytes probando diferentes codificaciones comunes.

    Prueba sucesivamente utf-8-sig, utf-8, latin-1 y cp1252.
    """
    codificaciones = ["utf-8-sig", "utf-8", "latin-1", "cp1252"]
    for codificacion in codificaciones:
        try:
            return contenido_bytes.decode(codificacion)
        except (UnicodeDecodeError, LookupError):
            continue

    raise ErrorValidacionCSV(
        f"No fue posible leer el archivo '{nombre_archivo}'. Formato o codificación inválida (se esperaba UTF-8 o Latin-1)."
    )


def leer_csv(
    origen_datos: Union[bytes, str, io.BytesIO, io.StringIO, Any],
    columnas_requeridas: List[str],
    nombre_archivo: str = "archivo",
) -> pd.DataFrame:
    """Lee y valida un archivo CSV asegurando su integridad y la presencia de columnas obligatorias.

    Args:
        origen_datos: Contenido en bytes, cadena, buffer en memoria u objeto de archivo.
        columnas_requeridas: Lista de nombres de columnas que deben estar presentes.
        nombre_archivo: Nombre descriptivo del archivo para mensajes de error.

    Returns:
        DataFrame de pandas con los datos leídos en formato texto.

    Raises:
        ErrorValidacionCSV: Si el archivo está vacío, corrupto o carece de columnas obligatorias.
    """
    texto_csv: str = ""

    # Extracción del contenido según el tipo recibido
    if isinstance(origen_datos, bytes):
        if not origen_datos.strip():
            raise ErrorValidacionCSV(f"El archivo '{nombre_archivo}' está vacío o no contiene registros.")
        texto_csv = decodificar_contenido(origen_datos, nombre_archivo)
    elif isinstance(origen_datos, str):
        if not origen_datos.strip():
            raise ErrorValidacionCSV(f"El archivo '{nombre_archivo}' está vacío o no contiene registros.")
        texto_csv = origen_datos
    elif hasattr(origen_datos, "read"):
        contenido_leido = origen_datos.read()
        if isinstance(contenido_leido, bytes):
            if not contenido_leido.strip():
                raise ErrorValidacionCSV(f"El archivo '{nombre_archivo}' está vacío o no contiene registros.")
            texto_csv = decodificar_contenido(contenido_leido, nombre_archivo)
        elif isinstance(contenido_leido, str):
            if not contenido_leido.strip():
                raise ErrorValidacionCSV(f"El archivo '{nombre_archivo}' está vacío o no contiene registros.")
            texto_csv = contenido_leido
        else:
            raise ErrorValidacionCSV(f"El formato del objeto de archivo '{nombre_archivo}' no es compatible.")
    else:
        raise ErrorValidacionCSV(f"Tipo de datos no soportado para la lectura del archivo '{nombre_archivo}'.")

    # Validación adicional de contenido en blanco
    if not texto_csv.strip():
        raise ErrorValidacionCSV(f"El archivo '{nombre_archivo}' está vacío o no contiene registros.")

    # Parseo a DataFrame utilizando Pandas
    try:
        df = pd.read_csv(
            io.StringIO(texto_csv),
            sep=",",
            dtype=str,
            keep_default_na=False,
            skipinitialspace=True,
        )
    except Exception as exc:
        raise ErrorValidacionCSV(
            f"No fue posible leer el archivo '{nombre_archivo}'. Formato o estructura CSV inválida."
        ) from exc

    # Validación de existencia de filas de datos
    if df.empty:
        raise ErrorValidacionCSV(f"El archivo '{nombre_archivo}' está vacío o no contiene filas de datos válidas.")

    # Limpieza de espacios en los nombres de las columnas
    df.columns = [str(col).strip() for col in df.columns]

    # Verificación de columnas obligatorias requeridas
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    if columnas_faltantes:
        faltantes_str = ", ".join(columnas_faltantes)
        raise ErrorValidacionCSV(
            f"El archivo '{nombre_archivo}' no contiene las columnas requeridas: {faltantes_str}."
        )

    # Reemplazo de posibles valores nulos por cadenas vacías y limpieza general
    df = df.fillna("")
    return df


def leer_csv_facturas(origen_datos: Any, nombre_archivo: str = "facturas.csv") -> pd.DataFrame:
    """Lee y valida el archivo CSV correspondiente a facturas emitidas."""
    return leer_csv(origen_datos, COLUMNAS_FACTURAS, nombre_archivo)


def leer_csv_contabilidad(origen_datos: Any, nombre_archivo: str = "contabilidad.csv") -> pd.DataFrame:
    """Lee y valida el archivo CSV correspondiente a registros contables."""
    return leer_csv(origen_datos, COLUMNAS_CONTABILIDAD, nombre_archivo)
