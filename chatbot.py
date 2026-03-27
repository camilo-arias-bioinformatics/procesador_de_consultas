import pandas as pd
from logica import *  # Importa todas las funciones de logica.py

# Cargar datasets
df_1 = pd.read_csv("datos/procesados/Data_Recordings_Cleaned_Normalized.zip")
df_2 = pd.read_csv("datos/procesados/Metrics_Subgroups_Cleaned_Normalized.zip")

# Diccionario de datasets
datasets = {
    "data_recordings": df_1,
    "metrics_subgroups": df_2
}

# Equivalencias entre variables técnicas y lenguaje natural
equivalencias = {
    # Recordings
    "fecha": ["fecha", "día", "día de visita", "día que visitó"],
    "hora": ["hora", "hora exacta", "entrada a la página"],
    "duracion_sesion": ["duración de la sesión", "cuánto duró la visita"],
    "duracion_sesion_segundos": ["duración en segundos", "tiempo en segundos"],
    "direccion_url_entrada": ["entrada url", "página de entrada", "por dónde entró"],
    "direccion_url_salida": ["última página", "página de salida", "por dónde salió"],
    "referente": ["referente", "de dónde venía", "fuente"],
    "id_usuario_clarity": ["id usuario", "identificador", "id técnico"],
    "explorador": ["navegador", "explorador", "Chrome, Safari"],
    "dispositivo": ["dispositivo", "tipo de equipo", "celular, computador, tablet"],
    "sistema_operativo": ["sistema operativo", "OS", "Android, iOS, Windows"],
    "pais": ["país", "ubicación", "desde dónde se conectó"],
    "recuento_paginas": ["páginas visitadas", "cuántas páginas", "recuento páginas"],
    "clics_sesion": ["clics totales", "clics durante la sesión"],
    "clicks_por_pagina": ["clics por página", "promedio de clics por página"],
    "tiempo_por_pagina": ["tiempo por página", "tiempo promedio por página"],
    "interaccion_total": ["interacción total", "actividad general", "nivel de interacción"],
    "abandono_rapido": ["abandono rápido", "se fue inmediatamente"],
    "posible_frustracion": ["frustración", "dificultad", "molestia"],
    "standarized_engagement_score": ["engagement", "nivel de interés", "compromiso usuario"],
    "entrada_es_home": ["empezó en home", "entrada es home", "inicio en página principal"],
    "trafico_externo": ["tráfico externo", "vino desde fuera", "Google o redes"],

    # Metrics
    "sessionsCount": ["visitas totales", "número de sesiones", "cuántas visitas hubo"],
    "sessionsWithMetricPercentage": ["porcentaje de visitas con métrica", "visitas con métrica"],
    "sessionsWithoutMetricPercentage": ["porcentaje de visitas sin métrica", "visitas sin métrica"],
    "pagesViews": ["vistas de página", "cuántas veces se vieron las páginas"],
    "subTotal": ["total parcial", "subtotal"],
    "Url": ["url", "página web", "dirección web"],
    "Device": ["dispositivo", "tipo de aparato", "celular, computador, tablet"],
    "OS": ["sistema operativo", "SO", "Android, iPhone, Windows"],
    "metricName": ["nombre de métrica", "indicador", "métrica"],
    "averageScrollDepth": ["profundidad scroll", "qué tanto bajó en la página"],
    "totalSessionCount": ["total de visitas", "total general de sesiones"],
    "totalBotSessionCount": ["visitas de bots", "sesiones de bots"],
    "distinctUserCount": ["usuarios distintos", "personas diferentes", "usuarios únicos"],
    "pagesPerSessionPercentage": ["páginas por sesión", "promedio de páginas por visita"],
    "totalTime": ["tiempo total", "duración total"],
    "activeTime": ["tiempo activo", "actividad efectiva"]
}

def encontrar_columna(pregunta, dataset_columns):
    """
    Busca si alguna palabra clave de la pregunta coincide con las equivalencias.
    Devuelve la columna técnica correspondiente o None si no encuentra.
    """
    pregunta = pregunta.lower()
    for col, claves in equivalencias.items():
        for clave in claves:
            if clave in pregunta:
                if col in dataset_columns:  # Verifica que exista en el dataset
                    return col
    return None

def responder(pregunta):
    """
    Función principal del chatbot que interpreta la pregunta y aplica funciones de logica.py.
    """
    pregunta = pregunta.lower()

    # Detecta qué dataset usar según palabras clave en la pregunta
    dataset = df_1  # default
    if "metrics" in pregunta:
        dataset = df_2
    elif "recordings" in pregunta:
        dataset = df_1

    # Busca si hay alguna columna mencionada en lenguaje natural
    columna = encontrar_columna(pregunta, dataset.columns)
    if columna:
        return f"Parece que te refieres a la columna '{columna}'. Podemos aplicar funciones sobre ella."

    # Lista de funciones disponibles en logica.py
    funciones_disponibles = {f: globals()[f] for f in dir() if callable(globals()[f])}

    # Detecta si alguna función de logica.py se menciona en la pregunta
    for nombre_func in funciones_disponibles:
        if nombre_func.lower() in pregunta:
            try:
                resultado = funciones_disponibles[nombre_func](dataset)
                return f"Resultado de {nombre_func}: {resultado}"
            except Exception as e:
                return f"Error al ejecutar {nombre_func}: {str(e)}"

    # Responde preguntas sobre máximos y mínimos
    if "mayor" in pregunta or "más alto" in pregunta:
        try:
            promedios = calcular_promedios(dataset)
            var = max(promedios, key=promedios.get)
            return f"La variable con mayor promedio es {var} con {promedios[var]:.2f}"
        except:
            return "No se pudo calcular el mayor promedio."

    if "menor" in pregunta or "más bajo" in pregunta:
        try:
            promedios = calcular_promedios(dataset)
            var = min(promedios, key=promedios.get)
            return f"La variable con menor promedio es {var} con {promedios[var]:.2f}"
        except:
            return "No se pudo calcular el menor promedio."

    return "No entendí la pregunta. Puedes intentar mencionar el nombre de la función o variable que quieres usar."
