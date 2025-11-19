# archivo: sorteo_mundial_interactivo_bombos.py

import streamlit as st
import random

st.set_page_config(page_title="Sorteo Mundial Interactivo", layout="wide")
st.title("🌍 Simulador Interactivo de Sorteo Mundial con Bombos Visuales")

# --- Bombos como listas de objetos ---
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

# --- Inicializamos 12 grupos si no existen ---
if "grupos" not in st.session_state:
    st.session_state.grupos = {chr(65+i): [] for i in range(12)}  # A-L

# --- Funciones ---
def mostrar_bombo_objetos(bombo, color):
    for item in bombo:
        st.markdown(f"<div style='background-color:{color}; padding:8px; border-radius:8px; margin-bottom:4px'>{item['pais']}</div>", unsafe_allow_html=True)

def sacar_pais(bombo):
    if bombo:
        pais = random.choice(bombo)
        bombo.remove(pais)
        return pais
    return None

def asignar_al_grupo(pais):
    for letra in st.session_state.grupos:
        if len(st.session_state.grupos[letra]) < 4:
            st.session_state.grupos[letra].append(pais["pais"])
            return letra
    return None

# --- Mostrar bombos visualmente ---
st.subheader("🎟 Bombos")
col1, col2, col3, col4 = st.columns(4)
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

# --- Botones para sorteo ---
st.markdown("---")
st.subheader("🎲 Sacar país de cada bombo")

col_b1, col_b2, col_b3, col_b4 = st.columns(4)

with col_b1:
    if st.button("Sacar de Bombo 1"):
        pais = sacar_pais(bombo1)
        if pais:
            grupo = asignar_al_grupo(pais)
            st.success(f"{pais['pais']} asignado al Grupo {grupo}")
        else:
            st.warning("Bombo 1 vacío")

with col_b2:
    if st.button("Sacar de Bombo 2"):
        pais = sacar_pais(bombo2)
        if pais:
            grupo = asignar_al_grupo(pais)
            st.success(f"{pais['pais']} asignado al Grupo {grupo}")
        else:
            st.warning("Bombo 2 vacío")

with col_b3:
    if st.button("Sacar de Bombo 3"):
        pais = sacar_pais(bombo3)
        if pais:
            grupo = asignar_al_grupo(pais)
            st.success(f"{pais['pais']} asignado al Grupo {grupo}")
        else:
            st.warning("Bombo 3 vacío")

with col_b4:
    if st.button("Sacar de Bombo 4"):
        pais = sacar_pais(bombo4)
        if pais:
            grupo = asignar_al_grupo(pais)
            st.success(f"{pais['pais']} asignado al Grupo {grupo}")
        else:
            st.warning("Bombo 4 vacío")

# --- Mostrar tablas de grupos ---
st.markdown("---")
st.subheader("📋 Grupos actuales")
cols = st.columns(6)
for i, letra in enumerate(st.session_state.grupos):
    with cols[i % 6]:
        st.table({f"Grupo {letra}": st.session_state.grupos[letra]})
