import pandas as pd
from logica import *  # Importa todas las funciones de logica.py

# Cargar datasets
df_1 = pd.read_csv("datos/procesados/Data_Recordings_Cleaned_Normalized.zip")
df_2 = pd.read_csv("datos/procesados/Metrics_Subgroups_Cleaned_Normalized.zip")

# Crear un diccionario de datasets por nombre para poder elegir dinámicamente
datasets = {
    "data_recordings": df_1,
    "metrics_subgroups": df_2
}

def responder(pregunta):
    """
    Esta función interpreta la pregunta y llama a la función adecuada de logica.py.
    Se asume que las funciones en logica.py aceptan un DataFrame como primer argumento.
    """

    pregunta = pregunta.lower()

    # Lista de funciones importadas dinámicamente
    funciones_disponibles = {f: globals()[f] for f in dir() if callable(globals()[f])}

    # Búsqueda de palabras clave
    if "promedio" in pregunta or "mean" in pregunta:
        if "data_recordings" in pregunta:
            return f"El promedio de las columnas es:\n{calcular_promedios(datasets['data_recordings'])}"
        elif "metrics_subgroups" in pregunta:
            return f"El promedio de las columnas es:\n{calcular_promedios(datasets['metrics_subgroups'])}"
    
    # Ejemplo: identificar funciones en logica.py por coincidencia de nombre en la pregunta
    for nombre_func in funciones_disponibles:
        if nombre_func.lower() in pregunta:
            try:
                # Intenta aplicar la función al primer dataset por defecto
                resultado = funciones_disponibles[nombre_func](df_1)
                return f"Resultado de {nombre_func}: {resultado}"
            except Exception as e:
                return f"Error al ejecutar {nombre_func}: {str(e)}"

    # Preguntas sobre máximos o mínimos
    if "mayor" in pregunta or "más alto" in pregunta:
        promedios = calcular_promedios(df_1)
        var = max(promedios, key=promedios.get)
        return f"La variable con mayor promedio es {var} con {promedios[var]:.2f}"

    if "menor" in pregunta or "más bajo" in pregunta:
        promedios = calcular_promedios(df_1)
        var = min(promedios, key=promedios.get)
        return f"La variable con menor promedio es {var} con {promedios[var]:.2f}"

    return "No entendí la pregunta. Puedes intentar mencionando el nombre de la función que quieres usar."
