# archivo: sorteo_mundial_interactivo.py

import streamlit as st
import random

st.set_page_config(page_title="Sorteo Mundial Interactivo", layout="wide")
st.title("🌍 Simulador Interactivo de Sorteo Mundial")

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

# --- Inicializamos 12 grupos ---
if "grupos" not in st.session_state:
    st.session_state.grupos = {chr(65+i): [] for i in range(12)}  # A-L

# --- Función para sacar país de un bombo ---
def sacar_pais(bombo):
    if bombo:
        pais = random.choice(bombo)
        bombo.remove(pais)
        return pais
    return None

# --- Función para asignar al siguiente grupo disponible ---
def asignar_al_grupo(pais):
    # Grupos llenos si ya tienen 4 países
    for letra in st.session_state.grupos:
        if len(st.session_state.grupos[letra]) < 4:
            st.session_state.grupos[letra].append(pais["pais"])
            return letra
    return None

# --- Botones para cada bombo ---
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

# --- Mostrar las 12 tablas de grupos ---
st.markdown("---")
st.subheader("📋 Grupos actuales")

cols = st.columns(6)  # 2 filas de 6 columnas
for i, letra in enumerate(st.session_state.grupos):
    with cols[i % 6]:
        st.table({f"Grupo {letra}": st.session_state.grupos[letra]})
