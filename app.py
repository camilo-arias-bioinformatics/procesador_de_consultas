import streamlit as st
import pandas as pd
from logica import calcular_promedios
import google.generativeai as genai

# 🔐 Configurar API KEY (pon tu clave aquí o usa st.secrets)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Cargar modelo (rápido y gratis)
model = genai.GenerativeModel("gemini-1.5-flash")

# Título
st.title("Chatbot de promedios con Gemini")

# Cargar datos
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

# 🔁 Función que usa Gemini
def responder_con_llm(pregunta, promedios):
    contexto = f"""
    Estos son los promedios de las variables:

    variable_1: {promedios['variable_1']}
    variable_2: {promedios['variable_2']}

    Responde SOLO con base en estos datos.
    Si te preguntan cuál es mayor, compáralos correctamente.
    """

    prompt = contexto + "\nPregunta: " + pregunta

    response = model.generate_content(prompt)
    
    return response.text

# Procesar pregunta
if pregunta:
    respuesta = responder_con_llm(pregunta, promedios)
    
    st.session_state.historial.append(("usuario", pregunta))
    st.session_state.historial.append(("assistant", respuesta))

# Mostrar chat
for rol, mensaje in st.session_state.historial:
    with st.chat_message(rol):
        st.write(mensaje)
