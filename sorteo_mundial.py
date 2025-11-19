# archivo: sorteo_mundial_objetos.py

import streamlit as st
import random

st.set_page_config(page_title="Simulador de Sorteo Mundial", layout="wide")
st.title("🌍 Simulador de Sorteo Mundial - Bombos con Objetos")

# --- Definimos bombos como listas de objetos ---
bombo1 = [
    {"pais": "México", "confederacion": "CONCACAF"},
    {"pais": "Canadá", "confederacion": "CONCACAF"},
    {"pais": "USA", "confederacion": "CONCACAF"},
    {"pais": "España", "confederacion": "UEFA"},
    {"pais": "Argentina", "confederacion": "CONMEBOL"},
    {"pais": "Francia", "confederacion": "UEFA"},
    {"pais": "Inglaterra", "confederacion": "UEFA"},
    {"pais": "Portugal", "confederacion": "UEFA"},
    {"pais": "Holanda", "confederacion": "UEFA"},
    {"pais": "Brasil", "confederacion": "CONMEBOL"},
    {"pais": "Bélgica", "confederacion": "UEFA"},
    {"pais": "Alemania", "confederacion": "UEFA"}
]

bombo2 = [
    {"pais": "Croacia", "confederacion": "UEFA"},
    {"pais": "Marruecos", "confederacion": "CAF"},
    {"pais": "Colombia", "confederacion": "CONMEBOL"},
    {"pais": "Uruguay", "confederacion": "CONMEBOL"},
    {"pais": "Suiza", "confederacion": "UEFA"},
    {"pais": "Senegal", "confederacion": "CAF"},
    {"pais": "Japón", "confederacion": "AFC"},
    {"pais": "Irán", "confederacion": "AFC"},
    {"pais": "Corea", "confederacion": "AFC"},
    {"pais": "Austria", "confederacion": "UEFA"},
    {"pais": "Ecuador", "confederacion": "CONMEBOL"},
    {"pais": "Australia", "confederacion": "AFC"}
]

bombo3 = [
    {"pais": "Noruega", "confederacion": "UEFA"},
    {"pais": "Panamá", "confederacion": "CONCACAF"},
    {"pais": "Egipto", "confederacion": "CAF"},
    {"pais": "Argelia", "confederacion": "CAF"},
    {"pais": "Escocia", "confederacion": "UEFA"},
    {"pais": "Paraguay", "confederacion": "CONMEBOL"},
    {"pais": "Costa de Marfil", "confederacion": "CAF"},
    {"pais": "Túnez", "confederacion": "CAF"},
    {"pais": "Sudáfrica", "confederacion": "CAF"},
    {"pais": "Qatar", "confederacion": "AFC"},
    {"pais": "Uzbekistán", "confederacion": "AFC"},
    {"pais": "Arabia Saudí", "confederacion": "AFC"}
]

bombo4 = [
    {"pais": "Jordania", "confederacion": "AFC"},
    {"pais": "Curazao", "confederacion": "CONCACAF"},
    {"pais": "Nueva Zelanda", "confederacion": "OFC"},
    {"pais": "Haití", "confederacion": "CONCACAF"},
    {"pais": "Ghana", "confederacion": "CAF"},
    {"pais": "Cabo Verde", "confederacion": "CAF"},
    {"pais": "ICP1", "confederacion": "Variable"},
    {"pais": "ICP2", "confederacion": "Variable"},
    {"pais": "UEFA1", "confederacion": "UEFA"},
    {"pais": "UEFA2", "confederacion": "UEFA"},
    {"pais": "UEFA3", "confederacion": "UEFA"},
    {"pais": "UEFA4", "confederacion": "UEFA"}
]

# --- Mostrar bombos visualmente solo con el nombre del país ---
col1, col2, col3, col4 = st.columns(4)

def mostrar_bombo_objetos(bombo, color):
    for item in bombo:
        st.markdown(f"<div style='background-color:{color}; padding:8px; border-radius:8px; margin-bottom:4px'>{item['pais']}</div>", unsafe_allow_html=True)

with col1:
    st.subheader("Bombo 1")
    mostrar_bombo_objetos(bombo1, "#FFD700")

with col2:
    st.subheader("Bombo 2")
    mostrar_bombo_objetos(bombo2, "#ADFF2F")

with col3:
    st.subheader("Bombo 3")
    mostrar_bombo_objetos(bombo3, "#1E90FF")

with col4:
    st.subheader("Bombo 4")
    mostrar_bombo_objetos(bombo4, "#FF69B4")

# --- Sorteo al azar respetando objetos ---
st.markdown("---")
st.subheader("🎲 Sacar país al azar de un bombo")

bombo_seleccionado = st.selectbox("Selecciona un bombo", ["Bombo 1", "Bombo 2", "Bombo 3", "Bombo 4"])
if st.button("Sacar país al azar"):
    if bombo_seleccionado == "Bombo 1":
        item = random.choice(bombo1)
    elif bombo_seleccionado == "Bombo 2":
        item = random.choice(bombo2)
    elif bombo_seleccionado == "Bombo 3":
        item = random.choice(bombo3)
    else:
        item = random.choice(bombo4)
    
    st.success(f"🌍 País sacado: {item['pais']} (Confederación: {item['confederacion']})")
