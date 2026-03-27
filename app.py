import streamlit as st
import pandas as pd
from logica import calcular_promedios
from chatbot import responder

# Título
st.title("Chatbot de promedios")

# Cargar datos directamente desde CSV
df = pd.read_csv("data.csv")

# Calcular promedios
promedios = calcular_promedios(df)

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
    respuesta = responder(pregunta, promedios)
    
    st.session_state.historial.append(("usuario", pregunta))
    st.session_state.historial.append(("assistant", respuesta))

# Mostrar chat
for rol, mensaje in st.session_state.historial:
    with st.chat_message(rol):
        st.write(mensaje)
