import streamlit as st
import pandas as pd
from logica import calcular_promedios
from google import genai

# 👉 API KEY directa
client = genai.Client(api_key="AIzaSyAbIHAtNbGlRiZniYb8ttmrq9PfuyUkTQQ")

# Título
st.title("Chatbot de promedios (Gemini)")

# Cargar datos
df = pd.read_csv("data.csv")

# Calcular promedios
promedios = calcular_promedios(df)

# Contexto
contexto = "\n".join([f"{k}: {v:.2f}" for k, v in promedios.items()])

# Mostrar datos
st.subheader("Datos")
st.write(df)

# Historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Input
pregunta = st.chat_input("Haz una pregunta")

if pregunta:

    prompt = f"""
Eres un asistente que responde SOLO con base en estos datos:

{contexto}

Reglas:
- No inventes datos
- Sé claro

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

# Mostrar chat
for rol, mensaje in st.session_state.historial:
    with st.chat_message(rol):
        st.write(mensaje)
