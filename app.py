import streamlit as st
import pandas as pd
from logica import calcular_promedios
from openai import OpenAI

# Inicializar cliente OpenAI usando secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Título
st.title("Chatbot de promedios (con LLM)")

# Cargar datos directamente desde CSV
df = pd.read_csv("data.csv")

# Calcular promedios
promedios = calcular_promedios(df)

# Convertir promedios a texto (esto es CLAVE)
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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    respuesta = response.choices[0].message.content

    st.session_state.historial.append(("usuario", pregunta))
    st.session_state.historial.append(("assistant", respuesta))

# Mostrar chat
for rol, mensaje in st.session_state.historial:
    with st.chat_message(rol):
        st.write(mensaje)
