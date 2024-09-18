"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import pandas as pd


def clean_data():
    """
    Función para limpiar un dataframe cargado desde un archivo CSV, eliminando duplicados,
    manejando valores faltantes y estandarizando algunos formatos de columnas.
    """
    # Cargar el archivo CSV y establecer la primera columna como índice
    datos = pd.read_csv("solicitudes_credito.csv", sep=";", index_col=0)

    # Reemplazar guiones y guiones bajos por espacios, y convertir todo a minúsculas
    datos = datos.replace("-", " ", regex=True).replace("_", " ", regex=True)
    datos = datos.applymap(lambda valor: valor.lower() if isinstance(valor, str) else valor)

    # Limpiar y convertir la columna 'monto_del_credito' a formato numérico
    datos["monto_del_credito"] = (
        datos["monto_del_credito"]
        .str.strip()  # Eliminar espacios adicionales
        .str.replace("[,$]|(\.00$)", "", regex=True)  # Quitar símbolos no deseados
        .astype(float)  # Convertir a float
    )

    # Convertir la columna 'fecha_de_beneficio' a formato de fecha (probando distintos formatos)
    datos["fecha_de_beneficio"] = pd.to_datetime(
        datos["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    ).fillna(
        pd.to_datetime(datos["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    )

    # Convertir la columna 'comuna_ciudadano' a enteros
    datos["comuna_ciudadano"] = datos["comuna_ciudadano"].astype(int)

    # Eliminar filas duplicadas y aquellas con valores faltantes
    datos = datos.drop_duplicates().dropna()

    return datos

clean_data()