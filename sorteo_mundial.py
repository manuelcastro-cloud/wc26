import streamlit as st
import random

st.set_page_config(page_title="Sorteo Mundial Interactivo", layout="wide")
st.title("🌍 Simulador Interactivo de Sorteo Mundial con Bombos y Restricciones")

# --- Colores por confederación ---
conf_colors = {
    "CONCACAF": "#FFD700",   # amarillo
    "CONMEBOL": "#ADFF2F",   # verde
    "UEFA": "#1E90FF",       # azul
    "CAF": "#FF6347",        # rojo
    "AFC": "#FF69B4",        # rosa
    "OFC": "#9370DB",        # morado
    "Variable": "#D3D3D3"    # gris
}

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

# --- Inicializamos sesión ---
if "grupos" not in st.session_state:
    st.session_state.grupos = {chr(65+i): [None]*4 for i in range(12)}  # A-L

if "botones" not in st.session_state:
    st.session_state.botones = {"b1": True, "b2": False, "b3": False, "b4": False}

# --- Función mostrar bombos ---
def mostrar_bombo_objetos(bombo):
    for item in bombo:
        color = conf_colors.get(item["confederacion"], "#FFFFFF")
        st.markdown(
            f"<div style='padding:8px; border-radius:8px; margin-bottom:4px'>"
            f"<span style='display:inline-block; width:8px; height:24px; background-color:{color}; margin-right:8px; vertical-align:middle'></span>"
            f"{item['pais']}</div>",
            unsafe_allow_html=True
        )

# --- Función mostrar grupos con rayita de confederación al inicio ---
def mostrar_grupos_coloreados():
    cols = st.columns(6)
    for i, letra in enumerate(st.session_state.grupos):
        with cols[i % 6]:
            html_table = "<table style='border-collapse:collapse; width:100%'>"
            for idx, pais in enumerate(st.session_state.grupos[letra]):
                if pais:
                    # Buscar confederación
                    conf = None
                    for b in [bombo1,bombo2,bombo3,bombo4]:
                        match = next((x for x in b if x["pais"]==pais), None)
                        if match:
                            conf = match["confederacion"]
                            break
                    color = conf_colors.get(conf,"#000000")
                    # Celda con rayita vertical al inicio
                    html_table += f"<tr><td style='padding:4px; border-left:8px solid {color}'>{pais}</td></tr>"
                else:
                    html_table += "<tr><td style='padding:4px'>---</td></tr>"
            html_table += "</table>"
            st.markdown(f"<b>Grupo {letra}</b><br>{html_table}", unsafe_allow_html=True)

# --- Funciones repartir bombos ---
def repartir_bombo1_con_restricciones():
    global bombo1
    if not bombo1: return
    fijas = {"México": "A", "Canadá": "B", "USA": "D"}
    for pais, grupo in fijas.items():
        obj = next((x for x in bombo1 if x["pais"]==pais), None)
        if obj:
            st.session_state.grupos[grupo][0] = obj["pais"]
            bombo1.remove(obj)
    paises_restantes = bombo1.copy()
    grupos_restantes = [l for l in st.session_state.grupos if l not in fijas.values()]
    random.shuffle(paises_restantes)
    for i, letra in enumerate(grupos_restantes):
        if i < len(paises_restantes):
            st.session_state.grupos[letra][0] = paises_restantes[i]["pais"]
    bombo1.clear()
    st.session_state.botones["b1"] = False
    st.session_state.botones["b2"] = True

def repartir_bombo_con_restricciones(bombo, posicion, key, habilitar_siguiente=None):
    if not bombo: return
    paises = bombo.copy()
    random.shuffle(paises)
    for pais_obj in paises:
        asignado = False
        intentos = list(st.session_state.grupos.keys())
        random.shuffle(intentos)
        for letra in intentos:
            grupo = st.session_state.grupos[letra]
            confs = []
            for idx,p in enumerate(grupo):
                if p:
                    for b in [bombo1,bombo2,bombo3,bombo4]:
                        match = next((x for x in b if x["pais"]==p), None)
                        if match: confs.append(match["confederacion"])
            uefa_count = confs.count("UEFA")
            if pais_obj["confederacion"]=="UEFA" and uefa_count<2 and grupo[posicion] is None:
                st.session_state.grupos[letra][posicion]=pais_obj["pais"]
                asignado=True
                break
            elif pais_obj["confederacion"]!="UEFA" and pais_obj["confederacion"] not in confs and grupo[posicion] is None:
                st.session_state.grupos[letra][posicion]=pais_obj["pais"]
                asignado=True
                break
        if not asignado:
            for letra in st.session_state.grupos:
                if st.session_state.grupos[letra][posicion] is None:
                    st.session_state.grupos[letra][posicion]=pais_obj["pais"]
                    break
    bombo.clear()
    st.session_state.botones[key] = False
    if habilitar_siguiente:
        st.session_state.botones[habilitar_siguiente] = True

# --- Limpiar ---
def limpiar_grupos():
    for letra in st.session_state.grupos:
        st.session_state.grupos[letra] = [None]*4
    st.session_state.botones = {"b1": True, "b2": False, "b3": False, "b4": False}

# --- Mostrar guía de colores ---
st.subheader("🎨 Guía de confederaciones")
cols_conf = st.columns(len(conf_colors))
for i, conf in enumerate(conf_colors):
    with cols_conf[i]:
        st.markdown(f"<div style='display:flex; align-items:center'><div style='width:20px; height:20px; background-color:{conf_colors[conf]}; margin-right:4px'></div>{conf}</div>", unsafe_allow_html=True)

# --- Mostrar Bombos ---
st.subheader("🎟 Bombos")
col1, col2, col3, col4 = st.columns(4)
with col1: mostrar_bombo_objetos(bombo1)
with col2: mostrar_bombo_objetos(bombo2)
with col3: mostrar_bombo_objetos(bombo3)
with col4: mostrar_bombo_objetos(bombo4)

# --- Botones ---
st.markdown("---")
col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
with col_b1:
    if st.session_state.botones["b1"]:
        if st.button("Repartir Bombo 1"): repartir_bombo1_con_restricciones()
with col_b2:
    if st.session_state.botones["b2"]:
        if st.button("Repartir Bombo 2"): repartir_bombo_con_restricciones(bombo2,1,"b2","b3")
with col_b3:
    if st.session_state.botones["b3"]:
        if st.button("Repartir Bombo 3"): repartir_bombo_con_restricciones(bombo3,2,"b3","b4")
with col_b4:
    if st.session_state.botones["b4"]:
        if st.button("Repartir Bombo 4"): repartir_bombo_con_restricciones(bombo4,3,"b4")
with col_b5:
    if st.button("Limpiar Grupos"): limpiar_grupos()

# --- Mostrar Grupos con rayitas ---
st.markdown("---")
st.subheader("📋 Grupos actuales")
mostrar_grupos_coloreados()
