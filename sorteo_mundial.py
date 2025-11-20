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

# --- Bombos como listas de objetos (estado inicial) ---
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

# --- Construir mapa inmutable país -> confederación (para referencia aunque los bombos se vacíen) ---
country_conf = {}
for b in (bombo1 + bombo2 + bombo3 + bombo4):
    country_conf[b["pais"]] = b["confederacion"]

# --- Mapa ISO alpha-2 para banderas (usado con FlagCDN). Ajusta si quieres otro código. ---
iso_map = {
    "México":"mx","Canadá":"ca","USA":"us","España":"es","Argentina":"ar",
    "Francia":"fr","Inglaterra":"gb","Portugal":"pt","Holanda":"nl","Brasil":"br",
    "Bélgica":"be","Alemania":"de","Croacia":"hr","Marruecos":"ma","Colombia":"co",
    "Uruguay":"uy","Suiza":"ch","Senegal":"sn","Japón":"jp","Irán":"ir",
    "Corea":"kr","Austria":"at","Ecuador":"ec","Australia":"au","Noruega":"no",
    "Panamá":"pa","Egipto":"eg","Argelia":"dz","Escocia":"gb","Paraguay":"py",
    "Costa de Marfil":"ci","Túnez":"tn","Sudáfrica":"za","Qatar":"qa","Uzbekistán":"uz",
    "Arabia Saudí":"sa","Jordania":"jo","Curazao":"cw","Nueva Zelanda":"nz","Haití":"ht",
    "Ghana":"gh","Cabo Verde":"cv"
    # ICP1, ICP2, UEFA1.. left out -> will show placeholder
}

# --- Función para obtener URL de la bandera (FlagCDN, 40px width) ---
def flag_url_for(country):
    code = iso_map.get(country)
    if not code:
        return ""  # placeholder (no url)
    # FlagCDN provides PNGs at https://flagcdn.com/w40/{code}.png
    return f"https://flagcdn.com/w40/{code}.png"

# --- Inicializamos sesión ---
if "grupos" not in st.session_state:
    st.session_state.grupos = {chr(65+i): [None]*4 for i in range(12)}  # A-L

if "botones" not in st.session_state:
    st.session_state.botones = {"b1": True, "b2": False, "b3": False, "b4": False}

# --- Función mostrar bombos ---
def mostrar_bombo_objetos(bombo):
    for item in bombo:
        color = conf_colors.get(item["confederacion"], "#FFFFFF")
        bandera_url = flag_url_for(item["pais"])
        if bandera_url:
            img_html = f"<img src='{bandera_url}' width='24' style='margin-left:8px; vertical-align:middle'/>"
        else:
            img_html = "&#10067;"  # question emoji (HTML entity)
        st.markdown(
            f"<div style='padding:8px; border-radius:8px; margin-bottom:4px; display:flex; align-items:center; justify-content:space-between'>"
            f"<div style='display:flex; align-items:center'><span style='display:inline-block; width:8px; height:24px; background-color:{color}; margin-right:8px; vertical-align:middle'></span>"
            f"{item['pais']}</div>"
            f"<div>{img_html}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

# --- Función mostrar grupos ---
def mostrar_grupos_coloreados():
    cols = st.columns(6)
    for i, letra in enumerate(st.session_state.grupos):
        with cols[i % 6]:
            html_table = "<table style='border-collapse:collapse; width:100%'>"
            for idx, pais in enumerate(st.session_state.grupos[letra]):
                if pais:
                    # la confederación la consultamos desde country_conf (inmutable)
                    conf = country_conf.get(pais)
                    color = conf_colors.get(conf, "#000000")
                    bandera_url = flag_url_for(pais)
                    if bandera_url:
                        bandera_html = f"<img src='{bandera_url}' width='24' style='margin-left:8px; vertical-align:middle'/>"
                    else:
                        bandera_html = "&#10067;"
                    # fila con rayita izquierda + bandera al final
                    html_table += (
                        f"<tr>"
                        f"<td style='padding:6px; border-left:8px solid {color}; display:flex; justify-content:space-between; align-items:center'>"
                        f"<div style='flex:1'>{pais}</div>"
                        f"<div style='margin-left:8px'>{bandera_html}</div>"
                        f"</td>"
                        f"</tr>"
                    )
                else:
                    html_table += "<tr><td style='padding:6px'>---</td></tr>"
            html_table += "</table>"
            st.markdown(f"<b>Grupo {letra}</b><br>{html_table}", unsafe_allow_html=True)

# --- Funciones repartir bombos ---
def repartir_bombo1_con_restricciones():
    global bombo1
    if not bombo1:
        return
    fijas = {"México": "A", "Canadá": "B", "USA": "D"}
    for pais, grupo in fijas.items():
        obj = next((x for x in bombo1 if x["pais"] == pais), None)
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
    if not bombo:
        return
    paises = bombo.copy()
    random.shuffle(paises)
    for pais_obj in paises:
        asignado = False
        intentos = list(st.session_state.grupos.keys())
        random.shuffle(intentos)
        for letra in intentos:
            grupo = st.session_state.grupos[letra]
            confs = []
            # consultamos confs desde country_conf (no dependemos de bombos que se vacían)
            for p in grupo:
                if p:
                    confs.append(country_conf.get(p))
            uefa_count = confs.count("UEFA")
            if pais_obj["confederacion"] == "UEFA" and uefa_count < 2 and grupo[posicion] is None:
                st.session_state.grupos[letra][posicion] = pais_obj["pais"]
                asignado = True
                break
            elif pais_obj["confederacion"] != "UEFA" and pais_obj["confederacion"] not in confs and grupo[posicion] is None:
                st.session_state.grupos[letra][posicion] = pais_obj["pais"]
                asignado = True
                break
        if not asignado:
            for letra in st.session_state.grupos:
                if st.session_state.grupos[letra][posicion] is None:
                    st.session_state.grupos[letra][posicion] = pais_obj["pais"]
                    break
    bombo.clear()
    st.session_state.botones[key] = False
    if habilitar_siguiente:
        st.session_state.botones[habilitar_siguiente] = True

# --- Limpiar ---
def limpiar_grupos():
    for letra in st.session_state.grupos:
        st.session_state.grupos[letra] = [None] * 4
    st.session_state.botones = {"b1": True, "b2": False, "b3": False, "b4": False}
    # Re-populate bombos? No — si quieres que limpiar también restaure bombos originales,
    # deberíamos mantener copias iniciales y reasignarlas aquí. Actualmente "Limpiar" solo limpia grupos y botones.

# --- Botones con on_click ---
def repartir_bombo1_click():
    repartir_bombo1_con_restricciones()

def repartir_bombo2_click():
    repartir_bombo_con_restricciones(bombo2, 1, "b2", "b3")

def repartir_bombo3_click():
    repartir_bombo_con_restricciones(bombo3, 2, "b3", "b4")

def repartir_bombo4_click():
    repartir_bombo_con_restricciones(bombo4, 3, "b4")

def limpiar_grupos_click():
    limpiar_grupos()

# --- Mostrar guía de colores ---
st.subheader("🎨 Guía de confederaciones")
cols_conf = st.columns(len(conf_colors))
for i, conf in enumerate(conf_colors):
    with cols_conf[i]:
        st.markdown(
            f"<div style='display:flex; align-items:center'>"
            f"<div style='width:20px; height:20px; background-color:{conf_colors[conf]}; margin-right:8px'></div>"
            f"{conf}</div>",
            unsafe_allow_html=True
        )

# --- Mostrar Bombos ---
st.subheader("🎟 Bombos")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**Bombo 1**")
    mostrar_bombo_objetos(bombo1)
with col2:
    st.markdown("**Bombo 2**")
    mostrar_bombo_objetos(bombo2)
with col3:
    st.markdown("**Bombo 3**")
    mostrar_bombo_objetos(bombo3)
with col4:
    st.markdown("**Bombo 4**")
    mostrar_bombo_objetos(bombo4)

# --- Botones ---
st.markdown("---")
col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
with col_b1:
    st.button("Repartir Bombo 1", disabled=not st.session_state.botones["b1"], on_click=repartir_bombo1_click)
with col_b2:
    st.button("Repartir Bombo 2", disabled=not st.session_state.botones["b2"], on_click=repartir_bombo2_click)
with col_b3:
    st.button("Repartir Bombo 3", disabled=not st.session_state.botones["b3"], on_click=repartir_bombo3_click)
with col_b4:
    st.button("Repartir Bombo 4", disabled=not st.session_state.botones["b4"], on_click=repartir_bombo4_click)
with col_b5:
    st.button("Limpiar Grupos", on_click=limpiar_grupos_click)

# --- Mostrar Grupos ---
st.markdown("---")
st.subheader("📋 Grupos actuales")
mostrar_grupos_coloreados()
