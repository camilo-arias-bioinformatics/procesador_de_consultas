# Procesador de Consultas

Descripción
Este proyecto consiste en un sistema que analiza datos de comportamiento de usuarios en un sitio web a partir de bases de datos (recordings y metrics), con el fin de generar insights relevantes y permitir su consulta mediante un chatbot.

El sistema procesa la información, identifica patrones de navegación, interacción y abandono, y convierte esos datos en respuestas claras a través de una interfaz conversacional.
Objetivo
Transformar datos de navegación web en información útil para la toma de decisiones, permitiendo a los usuarios consultar el comportamiento del sitio de manera sencilla mediante preguntas.
Datos utilizados
- Recordings: información detallada de cada sesión de usuario.
- Metrics: datos agregados como totales, promedios y porcentajes.
Tecnologías utilizadas
- Python
- Google Colab
- Streamlit
- Pandas
- OpenAI / ChatGPT API
-import numpy as np
-import pandas as pd
-import matplotlib.pyplot as plt
-from sklearn.preprocessing import MinMaxScaler
-from sklearn.metrics import mean_
-Gemeni 
Funcionalidad del chatbot
El chatbot permite realizar preguntas como:
- ¿Cuáles son las páginas más visitadas?
- ¿Dónde abandonan los usuarios?
- ¿Qué nivel de interacción tienen los usuarios?
- ¿Cómo navegan dentro del sitio?
- ¿Qué patrones de comportamiento se identifican?

Las respuestas se generan a partir del análisis de las variables de las bases de datos.
Análisis e Insights
- Páginas o productos más visitados
- Puntos críticos de abandono
- Flujos de navegación
- Nivel de interacción promedio
- Patrones de comportamiento
Ejecución del proyecto
El proyecto se desarrolla en dos etapas:

1. Google Colab:
- Carga y limpieza de datos
- Procesamiento y análisis

2. Streamlit:
- Interfaz del chatbot
- Consulta de información

Para ejecutar:
streamlit run app.py
Consideraciones
- Depende de la calidad de los datos
- Requiere conexión a internet
- Algunas respuestas requieren interpretación
Conclusión
Este proyecto demuestra cómo transformar datos en conocimiento útil mediante análisis de datos e inteligencia artificial, facilitando la toma de decisiones.
