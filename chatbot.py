import pandas as pd
from logica import *  # Importa todas las funciones de logica.py

# Cargar datasets
df_1 = pd.read_csv("datos/procesados/Data_Recordings_Cleaned_Normalized.zip")
df_2 = pd.read_csv("datos/procesados/Metrics_Subgroups_Cleaned_Normalized.zip")

datasets = {
    "recordings": df_1,
    "metrics": df_2
}

# Equivalencias de variables técnicas ↔ lenguaje natural
equivalencias = {
    # Recordings
    "fecha": "día de la visita",
    "hora": "hora de entrada",
    "duracion_sesion": "duración de la sesión",
    "duracion_sesion_segundos": "duración de la sesión en segundos",
    "direccion_url_entrada": "página de entrada",
    "direccion_url_salida": "última página vista",
    "referente": "de dónde venía el usuario",
    "id_usuario_clarity": "identificador del usuario",
    "explorador": "navegador usado",
    "dispositivo": "tipo de equipo",
    "sistema_operativo": "sistema operativo",
    "pais": "país de conexión",
    "recuento_paginas": "cantidad de páginas visitadas",
    "clics_sesion": "clics totales",
    "clicks_por_pagina": "clics por página",
    "tiempo_por_pagina": "tiempo por página",
    "interaccion_total": "interacción total",
    "abandono_rapido": "abandono rápido",
    "posible_frustracion": "posible frustración",
    "standarized_engagement_score": "nivel de compromiso",
    "entrada_es_home": "entrada desde home",
    "trafico_externo": "tráfico externo",
    # Metrics
    "sessionsCount": "total de visitas",
    "sessionsWithMetricPercentage": "porcentaje de visitas con evento",
    "sessionsWithoutMetricPercentage": "porcentaje de visitas sin evento",
    "pagesViews": "vistas de página",
    "subTotal": "total parcial",
    "Url": "página web analizada",
    "Device": "tipo de dispositivo",
    "OS": "sistema operativo del dispositivo",
    "metricName": "nombre de la métrica",
    "averageScrollDepth": "profundidad promedio de scroll",
    "totalSessionCount": "total de sesiones",
    "totalBotSessionCount": "visitas de bots",
    "distinctUserCount": "usuarios distintos",
    "pagesPerSessionPercentage": "páginas por sesión",
    "totalTime": "tiempo total",
    "activeTime": "tiempo activo"
}

# Mensaje inicial que explica al usuario qué métricas puede solicitar
def mensaje_inicial():
    variables_naturales = [v for v in equivalencias.values()]
    return (
        "¡Hola! Puedes pedirme métricas sobre las siguientes variables de los datasets:\n"
        + ", ".join(variables_naturales)
        + "\nPor ejemplo, puedes preguntar: '¿Cuál es el promedio de duración de la sesión?' o "
          "'Muéstrame el total de visitas'."
    )

# Función principal de respuesta
def responder(pregunta):
    pregunta = pregunta.lower()

    # Revisar si se menciona alguna variable por su nombre natural
    for var_tecnica, var_natural in equivalencias.items():
        if var_natural in pregunta:
            # Decidir dataset por nombre de variable
            dataset = df_1 if var_tecnica in df_1.columns else df_2
            # Si existe función de logica.py con nombre 'calcular_<variable>' intentar usarla
            funcion_nombre = f"calcular_{var_tecnica}"
            if funcion_nombre in globals() and callable(globals()[funcion_nombre]):
                try:
                    resultado = globals()[funcion_nombre](dataset)
                    return f"Resultado de {var_natural}: {resultado}"
                except Exception as e:
                    return f"No se pudo calcular {var_natural}: {str(e)}"
            else:
                # Si no hay función específica, intentar promedio si es numérica
                if var_tecnica in dataset.columns and pd.api.types.is_numeric_dtype(dataset[var_tecnica]):
                    promedio = dataset[var_tecnica].mean()
                    return f"Promedio de {var_natural}: {promedio:.2f}"
                else:
                    return f"No tengo forma de calcular {var_natural} directamente."

    # Máximos y mínimos
    if "mayor" in pregunta or "más alto" in pregunta:
        promedios = df_1.mean(numeric_only=True)
        var = promedios.idxmax()
        return f"La variable con mayor promedio es {equivalencias.get(var, var)} con {promedios[var]:.2f}"
    
    if "menor" in pregunta or "más bajo" in pregunta:
        promedios = df_1.mean(numeric_only=True)
        var = promedios.idxmin()
        return f"La variable con menor promedio es {equivalencias.get(var, var)} con {promedios[var]:.2f}"

    return "No entendí la pregunta. Intenta mencionando el nombre de la variable o métrica que quieres consultar."
