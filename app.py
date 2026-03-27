import streamlit as st
import pandas as pd
from logica import calcular_promedios
import google.generativeai as genai

# 👉 PON TU API KEY AQUÍ DIRECTAMENTE
genai.configure(api_key="AIzaSyBJ2Qi7MmJQWRllziaVb4x9tQ-QQaj3fS4")

# Inicializar modelo
model = genai.GenerativeModel("gemini-1.0-pro")

# Título
st.title("Chatbot de promedios (con Gemini)")

# Cargar datos directamente desde CSV
df = pd.read_csv("data.csv")

# Calcular promedios
promedios = calcular_promedios(df)

# Convertir promedios a texto
contexto = "\n".join([f"{k}: {v:.2f}" for k, v in promedios.items()])

# Mostrar datos (opcional)
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

    response = model.generate_content(prompt)

    respuesta = response.text if hasattr(response, "text") else "No se pudo generar respuesta."

    st.session_state.historial.append(("usuario", pregunta))
    st.session_state.historial.append(("assistant", respuesta))

# Mostrar chat
for rol, mensaje in st.session_state.historial:
    with st.chat_message(rol):
        st.write(mensaje)
