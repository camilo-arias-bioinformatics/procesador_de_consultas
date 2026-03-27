import streamlit as st
import pandas as pd
from logica import calcular_promedios
import google.generativeai as genai

# 👉 API KEY directa
genai.configure(api_key"AIzaSyChuJKYxO5TNCl2E9lvK_meiCUJJI-y1rM")

# Modelo (este sí existe en v1beta)
model = genai.GenerativeModel("models/text-bison-001")

# Título
st.title("Chatbot de promedios")

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
Responde SOLO con base en estos promedios:

{contexto}

Pregunta: {pregunta}
"""

    try:
        response = model.generate_content(prompt)
        respuesta = response.text
    except Exception as e:
        respuesta = f"Error: {str(e)}"

    st.session_state.historial.append(("usuario", pregunta))
    st.session_state.historial.append(("assistant", respuesta))

# Mostrar chat
for rol, mensaje in st.session_state.historial:
    with st.chat_message(rol):
        st.write(mensaje)
