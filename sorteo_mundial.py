import streamlit as st
import random
import copy
import io
import requests 
from PIL import Image, ImageDraw, ImageFont
from supabase import create_client

# --- SUPABASE ---
SUPABASE_URL = "https://gohsdckibmscvvfcxszw.supabase.co"
SUPABASE_KEY = "sb_publishable_q_7GWwouWZKDrNWsE9MSXQ_qQxlRdNX"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def guardar_simulacion_en_bd(grupos):
    try:
        payload = { "datos": grupos }
        supabase.table("simulaciones").insert(payload).execute()
        st.toast("Simulation saved! ✔️") # Usamos toast para que sea menos intrusivo
    except Exception as e:
        pass

# --- Configuración de la página ---
st.set_page_config(page_title="WC2026 Draw Simulator", layout="wide")

# --- INYECCIÓN DE CSS (ESTILOS RESPONSIVE) ---
st.markdown("""
<style>
    /* Contenedor flexible para las confederaciones */
    .conf-guide {
        display: flex;
        flex-wrap: wrap; /* Permite que bajen a la siguiente linea si no caben */
        gap: 10px;
        justify-content: center; /* Centrado */
        margin-bottom: 20px;
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    
    /* Items individuales de la guía */
    .conf-item {
        display: flex;
        align-items: center;
        font-size: 14px;
        font-weight: bold;
        background-color: white;
        padding: 5px 10px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Cuadrito de color */
    .conf-color-box {
        width: 15px;
        height: 15px;
        margin-right: 8px;
        border-radius: 3px;
    }

    /* Ajustes para móviles en títulos */
    @media (max-width: 768px) {
        h1 { font-size: 1.8rem !important; text-align: center; }
        .stButton button { width: 100%; } /* Botones full width en móvil */
    }
</style>
""", unsafe_allow_html=True)

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
    {"pais": "Croacia", "confederacion": "UEFA"},
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

iso_map = {
    "Mexico":"mx","Canada":"ca","USA":"us","Spain":"es","Argentina":"ar",
    "France":"fr","England":"gb","Portugal":"pt","Netherlands":"nl","Brazil":"br",
    "Belgium":"be","Germany":"de","Croacia":"hr","Morocco":"ma","Colombia":"co",
    "Uruguay":"uy","Switzerland":"ch","Senegal":"sn","Japan":"jp","Iran":"ir",
    "South Korea":"kr","Austria":"at","Ecuador":"ec","Australia":"au","Norway":"no",
    "Panama":"pa","Egypt":"eg","Algeria":"dz","Scotland":"gb","Paraguay":"py",
    "Ivory Coast":"ci","Tunisia":"tn","South Africa":"za","Qatar":"qa","Uzbekistan":"uz",
    "Saudi Arabia":"sa","Jordan":"jo","Curacao":"cw","New Zealand":"nz","Haiti":"ht",
    "Ghana":"gh","Cape Verde":"cv"
}

# --- FUNCIONES AUXILIARES ---
def flag_url_for(country):
    code = iso_map.get(country)
    if not code: return ""
    return f"https://flagcdn.com/w40/{code}.png"

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
    # Versión compacta para la parte inferior
    if not bombo:
        st.caption("Empty Pot / Sorteado")
        return
        
    # Mostramos en 3 columnas para ahorrar espacio
    cols = st.columns(3)
    for i, item in enumerate(bombo):
        col = cols[i % 3]
        color = conf_colors.get(item["confederacion"], "#FFFFFF")
        bandera_url = flag_url_for(item["pais"])
        img_html = f"<img src='{bandera_url}' width='16' style='margin-left:4px; vertical-align:middle'/>" if bandera_url else ""
        
        with col:
            st.markdown(
                f"<div style='font-size:12px; margin-bottom:2px; display:flex; align-items:center;'>"
                f"<span style='display:inline-block; width:6px; height:12px; background-color:{color}; margin-right:4px;'></span>"
                f"{item['pais']} {img_html}</div>",
                unsafe_allow_html=True
            )

def mostrar_grupos_coloreados():
    cols = st.columns(6)
    for i, letra in enumerate(st.session_state.grupos):
        with cols[i % 6]:
            html_table = "<table style='border-collapse:collapse; width:100%; margin-bottom:10px;'>"
            for idx, pais in enumerate(st.session_state.grupos[letra]):
                if pais:
                    conf = country_conf.get(pais)
                    color = conf_colors.get(conf, "#000000")
                    bandera_url = flag_url_for(pais)
                    bandera_html = f"<img src='{bandera_url}' width='20' style='margin-left:5px; vertical-align:middle'/>" if bandera_url else ""
                    
                    html_table += (
                        f"<tr>"
                        f"<td style='padding:4px; border-left:6px solid {color}; font-size:13px; display:flex; justify-content:space-between; align-items:center'>"
                        f"<div style='white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{pais}</div>"
                        f"<div>{bandera_html}</div>"
                        f"</td>"
                        f"</tr>"
                    )
                else:
                    html_table += "<tr><td style='padding:4px; color:#ccc; font-size:13px;'>---</td></tr>"
            html_table += "</table>"
            st.markdown(f"<div style='text-align:center; font-weight:bold; margin-bottom:2px;'>Group {letra}</div>{html_table}", unsafe_allow_html=True)

# --- GENERACIÓN DE IMAGEN (PILLOW) ---
def generar_imagen_resumen():
    W, H = 1200, 800
    bg_color = (240, 242, 246) 
    img = Image.new('RGB', (W, H), color=bg_color)
    d = ImageDraw.Draw(img)
    
    font_title = ImageFont.load_default()
    font_group = ImageFont.load_default()
    font_country = ImageFont.load_default()

    text = "WORLD CUP 2026 DRAW RESULTS"
    if hasattr(d, 'textbbox'):
        bbox = d.textbbox((0, 0), text, font=font_title)
        text_w = bbox[2] - bbox[0]
    else:
        text_w, _ = d.textsize(text, font=font_title)
        
    d.text(((W - text_w) / 2, 20), text, fill=(0,0,0), font=font_title)

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
        
        d.rectangle([x, y, x + ancho_grupo - 10, y + alto_grupo - 10], fill="white", outline="#ccc", width=1)
        d.text((x + 10, y + 10), f"GROUP {letra}", fill="black", font=font_group)
        d.line([x+10, y+35, x + ancho_grupo - 20, y+35], fill="#ddd", width=1)
        
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

# --- LÓGICA DE SORTEO (Igual a la anterior, solo callbacks) ---
def repartir_bombo1_con_restricciones():
    bombo = st.session_state.bombo1
    if not bombo: return
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

def repartir_bombo2():
    bombo_list = st.session_state.bombo2
    if not bombo_list: return
    estado_inicial = copy.deepcopy(st.session_state.grupos)
    paises_a_repartir = bombo_list.copy()
    posicion = 1
    max_intentos = 5000
    intentos = 0
    while intentos < max_intentos:
        intentos += 1
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
    if intentos < max_intentos:
        st.session_state.bombo2.clear()
        st.session_state.botones["b2"] = False
        st.session_state.botones["b3"] = True
    else:
        st.error("Retry Pot 2")

def repartir_bombo3():
    bombo_list = st.session_state.bombo3
    if not bombo_list: return
    estado_inicial = copy.deepcopy(st.session_state.grupos)
    paises_a_repartir = bombo_list.copy()
    posicion = 2
    max_intentos = 10000
    intentos = 0
    exclusion_c1 = ["AFC", "CONCACAF", "CONMEBOL"]
    exclusion_c2 = ["CAF", "CONCACAF"]
    while intentos < max_intentos:
        intentos += 1
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
        if exito_bombo:
            condicion1_ok = False
            condicion2_ok = False
            for letra in st.session_state.grupos:
                grupo = st.session_state.grupos[letra]
                confs_actuales = [country_conf.get(p) for p in grupo if p]
                if not any(c in exclusion_c1 for c in confs_actuales): condicion1_ok = True
                if not any(c in exclusion_c2 for c in confs_actuales): condicion2_ok = True
            if condicion1_ok and condicion2_ok: break
            else: exito_bombo = False
    if intentos < max_intentos:
        st.session_state.bombo3.clear()
        st.session_state.botones["b3"] = False
        st.session_state.botones["b4"] = True
    else:
        st.error("Retry Pot 3")

def repartir_bombo4_especial():
    bombo_list = st.session_state.bombo4
    if not bombo_list: return
    restricciones_icp1 = ["CAF", "CONCACAF", "OFC"]
    restricciones_icp2 = ["AFC", "CONCACAF", "CONMEBOL"]
    estado_inicial = copy.deepcopy(st.session_state.grupos)
    paises_a_repartir = bombo_list.copy()
    posicion = 3 
    max_intentos = 5000 
    intentos = 0
    with st.spinner('Calculating...'):
        while intentos < max_intentos:
            intentos += 1
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
    if intentos >= max_intentos:
        st.error("Constraint conflict. Try Pot 4 again.")
        st.session_state.grupos = copy.deepcopy(estado_inicial)
    else:
        st.session_state.bombo4.clear()
        st.session_state.botones["b4"] = False
        st.success("Draw Complete!")

# --- CALLBACKS ---
def repartir_bombo1_click(): repartir_bombo1_con_restricciones()
def repartir_bombo2_click(): repartir_bombo2()
def repartir_bombo3_click(): repartir_bombo3()
def repartir_bombo4_click(): repartir_bombo4_especial()
def limpiar_grupos_click():
    for letra in st.session_state.grupos: st.session_state.grupos[letra] = [None] * 4
    st.session_state.bombo1 = copy.deepcopy(DATA_BOMBO_1)
    st.session_state.bombo2 = copy.deepcopy(DATA_BOMBO_2)
    st.session_state.bombo3 = copy.deepcopy(DATA_BOMBO_3)
    st.session_state.bombo4 = copy.deepcopy(DATA_BOMBO_4)
    st.session_state.botones = {"b1": True, "b2": False, "b3": False, "b4": False}

# --- UI LAYOUT ORGANIZADO ---

# 1. Guía de Confederaciones (HTML Flexbox horizontal responsive)
html_conf = '<div class="conf-guide">'
for conf, color in conf_colors.items():
    html_conf += f'<div class="conf-item"><div class="conf-color-box" style="background-color:{color};"></div>{conf}</div>'
html_conf += '</div>'
st.markdown(html_conf, unsafe_allow_html=True)

# 2. Botones de Control (Arriba para fácil acceso en móvil)
st.markdown("### Controls")
col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
with col_b1: st.button("Draw Pot 1", disabled=not st.session_state.botones["b1"], on_click=repartir_bombo1_click, use_container_width=True)
with col_b2: st.button("Draw Pot 2", disabled=not st.session_state.botones["b2"], on_click=repartir_bombo2_click, use_container_width=True)
with col_b3: st.button("Draw Pot 3", disabled=not st.session_state.botones["b3"], on_click=repartir_bombo3_click, use_container_width=True)
with col_b4: st.button("Draw Pot 4", disabled=not st.session_state.botones["b4"], on_click=repartir_bombo4_click, use_container_width=True)
with col_b5: st.button("🔄 Reset", on_click=limpiar_grupos_click, use_container_width=True)

# 3. Grupos (Resultados - Centro de atención)
st.markdown("---")
st.subheader("📋 Groups")
mostrar_grupos_coloreados()

# 4. Compartir (Solo al final)
if not st.session_state.bombo4 and not st.session_state.botones["b4"]:
    guardar_simulacion_en_bd(st.session_state.grupos)
    st.markdown("---")
    st.markdown("## 📤 Share Results")
    col_img, col_share = st.columns([1, 2])
    with col_img:
        img_bytes = generar_imagen_resumen()
        st.image(img_bytes, use_container_width=True) # Preview en pantalla
        st.download_button(label="📸 Download Image", data=img_bytes, file_name="wc2026_draw_results.png", mime="image/png", use_container_width=True)
    with col_share:
        share_text = "Don't miss this 2026 World Cup draw simulator!"
        share_url = "https://wc26final.onrender.com"
        wa_url = f"https://api.whatsapp.com/send?text={share_text} {share_url}"
        tw_url = f"https://twitter.com/intent/tweet?text={share_text}&url={share_url}"
        fb_url = f"https://www.facebook.com/sharer/sharer.php?u={share_url}"
        c1, c2 , c3= st.columns(3)
        with c1: st.markdown(f"""<a href="{wa_url}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">WhatsApp</button></a>""", unsafe_allow_html=True)
        with c2: st.markdown(f"""<a href="{tw_url}" target="_blank"><button style="background-color:#000000; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">X (Twitter)</button></a>""", unsafe_allow_html=True)
        with c3: st.markdown(f"""<a href="{fb_url}" target="_blank"><button style="background-color:#1877F2; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer; font-weight:bold;">Facebook</button></a>""", unsafe_allow_html=True)

# 5. Bombos (Referencia - Abajo)
st.markdown("---")
st.subheader("🎟 Pots (Remaining)")
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