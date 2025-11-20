import streamlit as st
import random
import copy
import io
import requests 
from PIL import Image, ImageDraw, ImageFont

# --- Configuración de la página ---
st.set_page_config(page_title="WC2026 Draw Simulator", layout="wide")
st.title("🌍 WC2026 Draw Simulator")

# --- COLORES ---
conf_colors = {
    "CONCACAF": "#FFD700",
    "CONMEBOL": "#ADFF2F",
    "UEFA": "#1E90FF",
    "CAF": "#FF6347",
    "AFC": "#FF69B4",
    "OFC": "#9370DB",
    "Variable1": "#D3D3D3", 
    "Variable2": "#A9A9A9" 
}

# --- DATOS MAESTROS (CONSTANTES) - EN INGLÉS ---
DATA_BOMBO_1 = [
    {"pais": "Mexico", "confederacion": "CONCACAF"},
    {"pais": "Canada", "confederacion": "CONCACAF"},
    {"pais": "USA", "confederacion": "CONCACAF"},
    {"pais": "Spain", "confederacion": "UEFA"},
    {"pais": "Argentina", "confederacion": "CONMEBOL"},
    {"pais": "France", "confederacion": "UEFA"},
    {"pais": "England", "confederacion": "UEFA"},
    {"pais": "Portugal", "confederacion": "UEFA"},
    {"pais": "Netherlands", "confederacion": "UEFA"},
    {"pais": "Brazil", "confederacion": "CONMEBOL"},
    {"pais": "Belgium", "confederacion": "UEFA"},
    {"pais": "Germany", "confederacion": "UEFA"}
]

DATA_BOMBO_2 = [
    {"pais": "Croatia", "confederacion": "UEFA"},
    {"pais": "Morocco", "confederacion": "CAF"},
    {"pais": "Colombia", "confederacion": "CONMEBOL"},
    {"pais": "Uruguay", "confederacion": "CONMEBOL"},
    {"pais": "Switzerland", "confederacion": "UEFA"},
    {"pais": "Senegal", "confederacion": "CAF"},
    {"pais": "Japan", "confederacion": "AFC"},
    {"pais": "Iran", "confederacion": "AFC"},
    {"pais": "South Korea", "confederacion": "AFC"},
    {"pais": "Austria", "confederacion": "UEFA"},
    {"pais": "Ecuador", "confederacion": "CONMEBOL"},
    {"pais": "Australia", "confederacion": "AFC"}
]

DATA_BOMBO_3 = [
    {"pais": "Norway", "confederacion": "UEFA"},
    {"pais": "Panama", "confederacion": "CONCACAF"},
    {"pais": "Egypt", "confederacion": "CAF"},
    {"pais": "Algeria", "confederacion": "CAF"},
    {"pais": "Scotland", "confederacion": "UEFA"},
    {"pais": "Paraguay", "confederacion": "CONMEBOL"},
    {"pais": "Ivory Coast", "confederacion": "CAF"},
    {"pais": "Tunisia", "confederacion": "CAF"},
    {"pais": "South Africa", "confederacion": "CAF"},
    {"pais": "Qatar", "confederacion": "AFC"},
    {"pais": "Uzbekistan", "confederacion": "AFC"},
    {"pais": "Saudi Arabia", "confederacion": "AFC"}
]

DATA_BOMBO_4 = [
    {"pais": "Jordan", "confederacion": "AFC"},
    {"pais": "Curacao", "confederacion": "CONCACAF"},
    {"pais": "New Zealand", "confederacion": "OFC"},
    {"pais": "Haiti", "confederacion": "CONCACAF"},
    {"pais": "Ghana", "confederacion": "CAF"},
    {"pais": "Cape Verde", "confederacion": "CAF"},
    {"pais": "ICP1", "confederacion": "Variable1"},
    {"pais": "ICP2", "confederacion": "Variable2"},
    {"pais": "UEFA1", "confederacion": "UEFA"},
    {"pais": "UEFA2", "confederacion": "UEFA"},
    {"pais": "UEFA3", "confederacion": "UEFA"},
    {"pais": "UEFA4", "confederacion": "UEFA"}
]

# --- MAPAS DE REFERENCIA ---
country_conf = {}
for b in (DATA_BOMBO_1 + DATA_BOMBO_2 + DATA_BOMBO_3 + DATA_BOMBO_4):
    country_conf[b["pais"]] = b["confederacion"]

# Mapa ISO alpha-2 (Actualizado a nombres en inglés)
iso_map = {
    "Mexico":"mx","Canada":"ca","USA":"us","Spain":"es","Argentina":"ar",
    "France":"fr","England":"gb","Portugal":"pt","Netherlands":"nl","Brazil":"br",
    "Belgium":"be","Germany":"de","Croatia":"hr","Morocco":"ma","Colombia":"co",
    "Uruguay":"uy","Switzerland":"ch","Senegal":"sn","Japan":"jp","Iran":"ir",
    "South Korea":"kr","Austria":"at","Ecuador":"ec","Australia":"au","Norway":"no",
    "Panama":"pa","Egypt":"eg","Algeria":"dz","Scotland":"gb","Paraguay":"py",
    "Ivory Coast":"ci","Tunisia":"tn","South Africa":"za","Qatar":"qa","Uzbekistan":"uz",
    "Saudi Arabia":"sa","Jordan":"jo","Curacao":"cw","New Zealand":"nz","Haiti":"ht",
    "Ghana":"gh","Cape Verde":"cv"
}

# --- FUNCIONES AUXILIARES ---

# 1. Banderas para HTML
def flag_url_for(country):
    code = iso_map.get(country)
    if not code: return ""
    return f"https://flagcdn.com/w40/{code}.png"

# 2. Banderas para Pillow (Cache)
flag_cache = {}
def get_flag_image(country_code, size=(20, 15)):
    if country_code not in flag_cache:
        url = f"https://flagcdn.com/w40/{country_code}.png"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img_data = response.content
            flag_img = Image.open(io.BytesIO(img_data)).convert("RGBA")
            flag_img = flag_img.resize(size, Image.LANCZOS)
            flag_cache[country_code] = flag_img
        except Exception as e:
            flag_cache[country_code] = None
    return flag_cache[country_code]

# --- INICIALIZAR SESIÓN ---
if "grupos" not in st.session_state:
    st.session_state.grupos = {chr(65+i): [None]*4 for i in range(12)}

if "botones" not in st.session_state:
    st.session_state.botones = {"b1": True, "b2": False, "b3": False, "b4": False}

if "bombo1" not in st.session_state:
    st.session_state.bombo1 = copy.deepcopy(DATA_BOMBO_1)
if "bombo2" not in st.session_state:
    st.session_state.bombo2 = copy.deepcopy(DATA_BOMBO_2)
if "bombo3" not in st.session_state:
    st.session_state.bombo3 = copy.deepcopy(DATA_BOMBO_3)
if "bombo4" not in st.session_state:
    st.session_state.bombo4 = copy.deepcopy(DATA_BOMBO_4)

# --- FUNCIONES DE UI ---
def mostrar_bombo_objetos(bombo):
    for item in bombo:
        color = conf_colors.get(item["confederacion"], "#FFFFFF")
        bandera_url = flag_url_for(item["pais"])
        img_html = f"<img src='{bandera_url}' width='24' style='margin-left:8px; vertical-align:middle'/>" if bandera_url else "&#10067;"
        
        st.markdown(
            f"<div style='padding:8px; border-radius:8px; margin-bottom:4px; display:flex; align-items:center; justify-content:space-between'>"
            f"<div style='display:flex; align-items:center'><span style='display:inline-block; width:8px; height:24px; background-color:{color}; margin-right:8px; vertical-align:middle'></span>"
            f"{item['pais']}</div>"
            f"<div>{img_html}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

def mostrar_grupos_coloreados():
    cols = st.columns(6)
    for i, letra in enumerate(st.session_state.grupos):
        with cols[i % 6]:
            html_table = "<table style='border-collapse:collapse; width:100%'>"
            for idx, pais in enumerate(st.session_state.grupos[letra]):
                if pais:
                    conf = country_conf.get(pais)
                    color = conf_colors.get(conf, "#000000")
                    bandera_url = flag_url_for(pais)
                    bandera_html = f"<img src='{bandera_url}' width='24' style='margin-left:8px; vertical-align:middle'/>" if bandera_url else "&#10067;"
                    
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
            st.markdown(f"<b>Group {letra}</b><br>{html_table}", unsafe_allow_html=True)

# --- GENERACIÓN DE IMAGEN (PILLOW) ---
def generar_imagen_resumen():
    W, H = 1200, 800
    bg_color = (240, 242, 246) 
    img = Image.new('RGB', (W, H), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Usamos fuente por defecto. Como todo está en inglés (ASCII), no habrá problemas.
    font_title = ImageFont.load_default()
    font_group = ImageFont.load_default()
    font_country = ImageFont.load_default()

    # Título centrado
    text = "WORLD CUP 2026 DRAW RESULTS"
    if hasattr(d, 'textbbox'):
        bbox = d.textbbox((0, 0), text, font=font_title)
        text_w = bbox[2] - bbox[0]
    else:
        text_w, _ = d.textsize(text, font=font_title)
        
    d.text(((W - text_w) / 2, 20), text, fill=(0,0,0), font=font_title)

    # Grilla
    margen_x = 20
    margen_y = 60
    ancho_grupo = (W - (margen_x * 2)) / 6
    alto_grupo = (H - (margen_y * 2)) / 2.2
    
    grupos_keys = list(st.session_state.grupos.keys())
    
    for i, letra in enumerate(grupos_keys):
        fila = 0 if i < 6 else 1
        columna = i % 6
        x = margen_x + (columna * ancho_grupo) + 5
        y = margen_y + (fila * alto_grupo) + 20
        
        # Caja Grupo
        d.rectangle([x, y, x + ancho_grupo - 10, y + alto_grupo - 10], fill="white", outline="#ccc", width=1)
        d.text((x + 10, y + 10), f"GROUP {letra}", fill="black", font=font_group)
        d.line([x+10, y+35, x + ancho_grupo - 20, y+35], fill="#ddd", width=1)
        
        # Países
        paises = st.session_state.grupos[letra]
        for idx, pais in enumerate(paises):
            y_pais = y + 50 + (idx * 35)
            if pais:
                conf = country_conf.get(pais, "Variable")
                hex_color = conf_colors.get(conf, "#000000")
                
                d.rectangle([x + 10, y_pais, x + 15, y_pais + 20], fill=hex_color)
                
                country_code = iso_map.get(pais)
                if country_code:
                    flag_img = get_flag_image(country_code)
                    if flag_img:
                        img.paste(flag_img, (int(x + 25), int(y_pais + 2)), flag_img)
                        d.text((x + 25 + flag_img.width + 5, y_pais + 2), pais, fill="black", font=font_country)
                    else:
                        d.text((x + 25, y_pais + 2), pais, fill="black", font=font_country)
                else:
                    d.text((x + 25, y_pais + 2), pais, fill="black", font=font_country)
            else:
                d.text((x + 25, y_pais + 2), "---", fill="gray", font=font_country)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- LÓGICA DE SORTEO ---

def repartir_bombo1_con_restricciones():
    bombo = st.session_state.bombo1
    if not bombo: return
    
    # Restricciones de anfitriones en Inglés
    fijas = {"Mexico": "A", "Canada": "B", "USA": "D"}
    
    for pais, grupo in fijas.items():
        obj = next((x for x in bombo if x["pais"] == pais), None)
        if obj:
            st.session_state.grupos[grupo][0] = obj["pais"]
            bombo.remove(obj)
            
    paises_restantes = bombo.copy()
    grupos_restantes = [l for l in st.session_state.grupos if l not in fijas.values()]
    random.shuffle(paises_restantes)
    
    for i, letra in enumerate(grupos_restantes):
        if i < len(paises_restantes):
            st.session_state.grupos[letra][0] = paises_restantes[i]["pais"]
            
    st.session_state.bombo1.clear()
    st.session_state.botones["b1"] = False
    st.session_state.botones["b2"] = True

def repartir_bombo_generico(bombo_list, posicion, key_actual, key_siguiente):
    if not bombo_list: return
    estado_inicial = copy.deepcopy(st.session_state.grupos)
    paises_a_repartir = bombo_list.copy()
    
    while True:
        st.session_state.grupos = copy.deepcopy(estado_inicial)
        random.shuffle(paises_a_repartir)
        exito_bombo = True
        for pais_obj in paises_a_repartir:
            asignado = False
            letras = list(st.session_state.grupos.keys())
            random.shuffle(letras)
            for letra in letras:
                grupo = st.session_state.grupos[letra]
                if grupo[posicion] is not None: continue
                
                confs_grupo = [country_conf.get(p) for p in grupo if p]
                uefa_count = confs_grupo.count("UEFA")
                mi_conf = pais_obj["confederacion"]
                
                es_valido = False
                if mi_conf == "UEFA":
                    if uefa_count < 2: es_valido = True
                else:
                    if mi_conf not in confs_grupo: es_valido = True
                
                if es_valido:
                    st.session_state.grupos[letra][posicion] = pais_obj["pais"]
                    asignado = True
                    break
            if not asignado:
                exito_bombo = False
                break
        if exito_bombo: break

    bombo_list.clear()
    st.session_state.botones[key_actual] = False
    if key_siguiente: st.session_state.botones[key_siguiente] = True

def repartir_bombo4_especial():
    bombo_list = st.session_state.bombo4
    if not bombo_list: return
    
    restricciones_icp1 = ["CAF", "CONCACAF", "OFC"]
    restricciones_icp2 = ["AFC", "CONCACAF", "CONMEBOL"]
    
    estado_inicial = copy.deepcopy(st.session_state.grupos)
    paises_a_repartir = bombo_list.copy()
    posicion = 3 
    
    while True:
        st.session_state.grupos = copy.deepcopy(estado_inicial)
        random.shuffle(paises_a_repartir)
        exito_bombo = True
        for pais_obj in paises_a_repartir:
            asignado = False
            letras = list(st.session_state.grupos.keys())
            random.shuffle(letras)
            for letra in letras:
                grupo = st.session_state.grupos[letra]
                if grupo[posicion] is not None: continue
                
                confs_grupo = [country_conf.get(p) for p in grupo if p]
                uefa_count = confs_grupo.count("UEFA")
                mi_conf = pais_obj["confederacion"]
                
                es_valido = False
                if mi_conf == "Variable1":
                    if not any(c in confs_grupo for c in restricciones_icp1): es_valido = True
                elif mi_conf == "Variable2":
                    if not any(c in confs_grupo for c in restricciones_icp2): es_valido = True
                elif mi_conf == "UEFA":
                    if uefa_count < 2: es_valido = True
                else:
                    if mi_conf not in confs_grupo: es_valido = True
                
                if es_valido:
                    st.session_state.grupos[letra][posicion] = pais_obj["pais"]
                    asignado = True
                    break
            if not asignado:
                exito_bombo = False
                break
        if exito_bombo: break

    bombo_list.clear()
    st.session_state.botones["b4"] = False

# --- CALLBACKS ---
def repartir_bombo1_click(): repartir_bombo1_con_restricciones()
def repartir_bombo2_click(): repartir_bombo_generico(st.session_state.bombo2, 1, "b2", "b3")
def repartir_bombo3_click(): repartir_bombo_generico(st.session_state.bombo3, 2, "b3", "b4")
def repartir_bombo4_click(): repartir_bombo4_especial()
def limpiar_grupos_click():
    for letra in st.session_state.grupos: st.session_state.grupos[letra] = [None] * 4
    st.session_state.bombo1 = copy.deepcopy(DATA_BOMBO_1)
    st.session_state.bombo2 = copy.deepcopy(DATA_BOMBO_2)
    st.session_state.bombo3 = copy.deepcopy(DATA_BOMBO_3)
    st.session_state.bombo4 = copy.deepcopy(DATA_BOMBO_4)
    st.session_state.botones = {"b1": True, "b2": False, "b3": False, "b4": False}

# --- INTERFAZ ---
st.subheader("🎨 Confederation Guide")
cols_conf = st.columns(len(conf_colors))
for i, conf in enumerate(conf_colors):
    with cols_conf[i]:
        st.markdown(f"<div style='display:flex; align-items:center'><div style='width:20px; height:20px; background-color:{conf_colors[conf]}; margin-right:8px'></div>{conf}</div>", unsafe_allow_html=True)

st.subheader("🎟 Pots")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**Pot 1**")
    mostrar_bombo_objetos(st.session_state.bombo1)
with col2:
    st.markdown("**Pot 2**")
    mostrar_bombo_objetos(st.session_state.bombo2)
with col3:
    st.markdown("**Pot 3**")
    mostrar_bombo_objetos(st.session_state.bombo3)
with col4:
    st.markdown("**Pot 4**")
    mostrar_bombo_objetos(st.session_state.bombo4)

st.markdown("---")
col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
with col_b1: st.button("Draw Pot 1", disabled=not st.session_state.botones["b1"], on_click=repartir_bombo1_click)
with col_b2: st.button("Draw Pot 2", disabled=not st.session_state.botones["b2"], on_click=repartir_bombo2_click)
with col_b3: st.button("Draw Pot 3", disabled=not st.session_state.botones["b3"], on_click=repartir_bombo3_click)
with col_b4: st.button("Draw Pot 4", disabled=not st.session_state.botones["b4"], on_click=repartir_bombo4_click)
with col_b5: st.button("🔄 Reset Draw", on_click=limpiar_grupos_click)

st.markdown("---")
st.subheader("📋 Groups")
mostrar_grupos_coloreados()

if not st.session_state.bombo4 and not st.session_state.botones["b4"]:
    st.markdown("---")
    st.markdown("## 📤 Share Results")
    col_img, col_share = st.columns([1, 2])
    with col_img:
        img_bytes = generar_imagen_resumen()
        st.download_button(label="📸 Download Image", data=img_bytes, file_name="wc2026_draw_results.png", mime="image/png", use_container_width=True)
    with col_share:
        share_text = "Don't miss this 2026 World Cup draw simulator!"
        share_url = "https://wc2026.streamlit.app"
        wa_url = f"https://api.whatsapp.com/send?text={share_text} {share_url}"
        tw_url = f"https://twitter.com/intent/tweet?text={share_text}&url={share_url}"
        fb_url = f"https://www.facebook.com/sharer/sharer.php?u={share_url}"
        c1, c2 , c3= st.columns(3)
        with c1: st.markdown(f"""<a href="{wa_url}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">Share on WhatsApp</button></a>""", unsafe_allow_html=True)
        with c2: st.markdown(f"""<a href="{tw_url}" target="_blank"><button style="background-color:#1DA1F2; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">Share on X</button></a>""", unsafe_allow_html=True)
        with c3: st.markdown(f"""<a href="{fb_url}" target="_blank"><button style="background-color:#1877F2; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer; font-weight:bold;">Facebook</button></a>""", unsafe_allow_html=True)