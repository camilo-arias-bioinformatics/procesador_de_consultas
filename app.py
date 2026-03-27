import streamlit as st
import pandas as pd
from logica import calcular_promedios
from google import genai

# 👉 API KEY directa
client = genai.Client(api_key="AIzaSyChuJKYxO5TNCl2E9lvK_meiCUJJI-y1rM")

# Título
st.title("Chatbot de promedios (con Gemini)")

# Cargar datos
df = pd.read_csv("data.csv")

# Calcular promedios
promedios = calcular_promedios(df)

# Convertir promedios a texto
contexto = "\n".join([f"{k}: {v:.2f}" for k, v in promedios.items()])

# Mostrar datos
st.subheader("Datos")
st.write(df)

# Inicializar historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Input tipo chat
pregunta = st.chat_input("Haz una pregunta")

# Procesar pregunta
if pregunta:

    prompt = f"""
Eres un asistente que responde preguntas SOLO con base en estos promedios:

{contexto}

Reglas:
- No inventes datos
- Usa solo la información proporcionada
- Responde de forma clara

Pregunta: {pregunta}
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",  # modelo actual compatible
            contents=prompt
        )

        # Manejo robusto de respuesta
        if hasattr(response, "text") and response.text:
            respuesta = response.text
        else:
            respuesta = "No se pudo generar respuesta."

    except Exception as e:
        respuesta = f"Error: {str(e)}"

    st.session_state.historial.append(("usuario", pregunta))
    st.session_state.historial.append(("assistant", respuesta))

# Mostrar chat
for rol, mensaje in st.session_state.historial:
    with st.chat_message(rol):
        st.write(mensaje)
