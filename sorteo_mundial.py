import streamlit as st
import random

st.set_page_config(page_title="Sorteo Mundial Interactivo", layout="wide")
st.title("🌍 Simulador Interactivo de Sorteo Mundial con Bombos y Posiciones")

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

# --- Inicializamos 12 grupos con 4 posiciones vacías ---
if "grupos" not in st.session_state:
    st.session_state.grupos = {chr(65+i): [None]*4 for i in range(12)}  # A-L

# --- Función para mostrar bombos ---
def mostrar_bombo_objetos(bombo, color):
    for item in bombo:
        st.markdown(f"<div style='background-color:{color}; padding:8px; border-radius:8px; margin-bottom:4px'>{item['pais']}</div>", unsafe_allow_html=True)

# --- Función para repartir Bombo 1 con restricciones ---
def repartir_bombo1_con_restricciones():
    if not bombo1:
        st.warning("Bombo 1 vacío")
        return
    
    # Asignaciones fijas
    fijas = {"México": "A", "Canadá": "B", "USA": "D"}
    for pais, grupo in fijas.items():
        obj = next((x for x in bombo1 if x["pais"] == pais), None)
        if obj:
            st.session_state.grupos[grupo][0] = obj["pais"]
            bombo1.remove(obj)
    
    # Países restantes
    paises_restantes = bombo1.copy()
    grupos_restantes = [letra for letra in st.session_state.grupos if letra not in fijas.values()]
    random.shuffle(paises_restantes)
    
    for i, letra in enumerate(grupos_restantes):
        if i < len(paises_restantes):
            st.session_state.grupos[letra][0] = paises_restantes[i]["pais"]
    bombo1.clear()
    st.success("Bombo 1 repartido con restricciones")

# --- Función para repartir Bombo 2 con restricción UEFA ---
def repartir_bombo2_con_restriccion_uefa():
    if not bombo2:
        st.warning("Bombo 2 vacío")
        return
    
    paises_restantes = bombo2.copy()
    random.shuffle(paises_restantes)
    
    for letra in st.session_state.grupos:
        pos = 1  # Bombo 2 corresponde a la posición 1
        if st.session_state.grupos[letra][pos] is None:
            # Buscar un país que cumpla la restricción UEFA
            for i, pais_obj in enumerate(paises_restantes):
                # Contar cuántos UEFA ya tiene el grupo
                uefa_count = sum(1 for p in st.session_state.grupos[letra] if p in [x["pais"] for x in bombo1+bombo2+bombo3+bombo4 if x["confederacion"]=="UEFA"])
                if pais_obj["confederacion"] == "UEFA" and uefa_count >= 2:
                    continue  # No puede asignar más UEFA
                # Asignar el país al grupo
                st.session_state.grupos[letra][pos] = pais_obj["pais"]
                paises_restantes.pop(i)
                break
    # Limpiar bombo2
    bombo2.clear()
    st.success("Bombo 2 repartido con restricción UEFA (máx 2 por grupo)")

# --- Botón limpiar ---
def limpiar_grupos():
    for letra in st.session_state.grupos:
        st.session_state.grupos[letra] = [None]*4
    st.success("✅ Grupos limpiados")

# --- Mostrar bombos ---
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

# --- Botones para sorteo por bombo ---
st.markdown("---")
st.subheader("🎲 Repartir bombo completo a grupos")

col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)

with col_b1:
    if st.button("Repartir Bombo 1"):
        repartir_bombo1_con_restricciones()
with col_b2:
    if st.button("Repartir Bombo 2"):
        repartir_bombo2_con_restriccion_uefa()
with col_b3:
    if st.button("Repartir Bombo 3"):
        repartir_bombo(bombo3, 2)
with col_b4:
    if st.button("Repartir Bombo 4"):
        repartir_bombo(bombo4, 3)
with col_b5:
    if st.button("Limpiar Grupos"):
        limpiar_grupos()

# --- Mostrar tablas de grupos ---
st.markdown("---")
st.subheader("📋 Grupos actuales")
cols = st.columns(6)
for i, letra in enumerate(st.session_state.grupos):
    with cols[i % 6]:
        st.table({f"Grupo {letra}": st.session_state.grupos[letra]})
