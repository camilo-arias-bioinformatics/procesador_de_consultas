import streamlit as st
import pandas as pd
import logica  # all functions with metrics
from google import genai
import os

# 👉 API KEY directa
client = genai.Client(api_key="")

# Título
st.title("Chatbot de métricas (Gemini)")

# Función para cargar datasets dinámicamente
def cargar_datasets(path="datos/procesados"):
    dfs = {}
    for archivo in os.listdir(path):
        if archivo.endswith(".csv") or archivo.endswith(".zip"):
            nombre = archivo.split(".")[0]
            dfs[nombre] = pd.read_csv(os.path.join(path, archivo))
    return dfs

# Función para aplicar todas las funciones de logica.py a un df
def calcular_todas_metricas(df):
    resultados = {}
    for nombre_funcion in dir(logica):
        if nombre_funcion.startswith("_"):
            continue  # Ignorar funciones internas
        funcion = getattr(logica, nombre_funcion)
        try:
            # Intentamos aplicar la función si recibe un DataFrame
            res = funcion(df)
            resultados[nombre_funcion] = res
        except Exception:
            pass  # Ignorar funciones que no aplican a este df
    return resultados

# Cargar todos los datasets
datasets = cargar_datasets()

# Diccionario para guardar resultados de todas las métricas
metricas_por_dataset = {}

for nombre, df in datasets.items():
    metricas_por_dataset[nombre] = calcular_todas_metricas(df)

# Convertir a contexto legible para el chatbot
contexto = ""
for nombre, metricas in metricas_por_dataset.items():
    contexto += f"\n### Dataset: {nombre}\n"
    for k, v in metricas.items():
        if isinstance(v, (int, float)):
            contexto += f"{k}: {v:.2f}\n"
        else:
            contexto += f"{k}: {v}\n"

# Mostrar datasets y métricas en Streamlit
st.subheader("Datasets cargados")
for nombre, df in datasets.items():
    st.write(f"**{nombre}**")
    st.dataframe(df.head())

st.subheader("Métricas calculadas")
st.text(contexto)

# Historial de chat
if "historial" not in st.session_state:
    st.session_state.historial = []

# Input del usuario
pregunta = st.chat_input("Haz una pregunta sobre los datasets")

if pregunta:

    prompt = f"""
Eres un asistente que responde SOLO con base en estos datos:

{contexto}

Reglas:
- No inventes datos
- Sé claro y conciso

Pregunta: {pregunta}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        respuesta = response.text if response.text else "Sin respuesta."
    except Exception as e:
        respuesta = f"Error: {str(e)}"

    st.session_state.historial.append(("usuario", pregunta))
    st.session_state.historial.append(("assistant", respuesta))

# Mostrar historial del chat
for rol, mensaje in st.session_state.historial:
    with st.chat_message(rol):
        st.write(mensaje)
