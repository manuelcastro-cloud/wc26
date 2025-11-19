# archivo: sorteo_mundial.py

import streamlit as st
import random

st.set_page_config(page_title="Simulador de Sorteo Mundial", layout="wide")
st.title("Simulador de Sorteo Mundial")

# --- Definimos los 4 bombos ---
bombo1 = ["México", "Canadá", "USA", "España", "Argentina", "Francia", "Inglaterra", "Portugal", "Holanda", "Brasil", "Bélgica", "Alemania"]
bombo2 = ["Croacia", "Marruecos", "Colombia", "Uruguay", "Suiza", "Senegal", "Japón", "Irán", "Korea", "Austria", "Ecuador", "Australia"]
bombo3 = ["Noruega", "Panama", "Egipto", "Argelia", "Escocia", "Paraguay", "Costa de Marfil", "Tunez", "Sudáfrica", "Qatar", "Uzbekistan", "Arabia Saudí"]
bombo4 = ["Jordania", "Curazao", "Nueva Zelanda", "Haití", "Ghana", "Cabo Verde", "ICP1", "ICP2", "UEFA1", "UEFA2", "UEFA3", "UEFA4"]

# --- Mostramos los bombos en columnas ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Bombo 1")
    st.write(bombo1)

with col2:
    st.subheader("Bombo 2")
    st.write(bombo2)

with col3:
    st.subheader("Bombo 3")
    st.write(bombo3)

with col4:
    st.subheader("Bombo 4")
    st.write(bombo4)

# --- Opcional: sacar país al azar de un bombo ---
st.markdown("---")
st.subheader("Sorteo al azar de un país")

bombo_seleccionado = st.selectbox("Selecciona un bombo", ["Bombo 1", "Bombo 2", "Bombo 3", "Bombo 4"])
if st.button("Sacar país al azar"):
    if bombo_seleccionado == "Bombo 1":
        pais = random.choice(bombo1)
    elif bombo_seleccionado == "Bombo 2":
        pais = random.choice(bombo2)
    elif bombo_seleccionado == "Bombo 3":
        pais = random.choice(bombo3)
    else:
        pais = random.choice(bombo4)
    
    st.success(f"🌍 País sacado: {pais}")
