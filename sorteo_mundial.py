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
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

def guardar_simulacion_en_bd(grupos):
    if not supabase: return
    try:
        payload = { "datos": grupos }
        supabase.table("simulaciones").insert(payload).execute()
        st.toast("Simulation saved! ✔️")
    except Exception as e:
        pass

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="WC2026 Draw Simulator", layout="wide")

# --- CSS (ESTILOS VISUALES) ---
st.markdown("""
<style>
    /* Guía de Colores */
    .conf-guide {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin-bottom: 20px;
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
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
    .conf-color-box {
        width: 15px;
        height: 15px;
        margin-right: 8px;
        border-radius: 3px;
    }
    
    /* GRID DE BOMBOS (POTS) - PARTE INFERIOR */
    .pots-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr); /* Escritorio: 2 columnas */
        gap: 15px;
        margin-top: 10px;
    }
    
    .pot-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .pot-title {
        font-weight: bold;
        font-size: 16px;
        text-align: center;
        margin-bottom: 10px;
        border-bottom: 2px solid #f0f2f6;
        padding-bottom: 5px;
        color: #333;
    }

    .country-item {
        display: flex;
        align-items: center;
        font-size: 14px;
        margin-bottom: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        padding: 2px 0;
    }

    /* RESPONSIVE MOVIL */
    @media (max-width: 768px) {
        h1 { font-size: 1.8rem !important; text-align: center; }
        .stButton button { width: 100%; }
        
        /* En móvil, los bombos se ponen en 1 sola columna */
        .pots-grid {
            grid-template-columns: 1fr; 
        }
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

# --- DATOS MAESTROS ---
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
    {"pais": "DR Congo Path", "confederacion": "Variable1"}, 
    {"pais": "Iraq Path", "confederacion": "Variable2"},     
    {"pais": "Italy Path", "confederacion": "UEFA"},         
    {"pais": "Ukraine Path", "confederacion": "UEFA"},       
    {"pais": "Turkey Path", "confederacion": "UEFA"},        
    {"pais": "Denmark Path", "confederacion": "UEFA"}        
]

# --- MAPAS ---
country_conf = {}
for b in (DATA_BOMBO_1 + DATA_BOMBO_2 + DATA_BOMBO_3 + DATA_BOMBO_4):
    country_conf[b["pais"]] = b["confederacion"]

iso_map = {
    "Mexico":"mx","Canada":"ca","USA":"us","Spain":"es","Argentina":"ar",
    "France":"fr","England":"gb","Portugal":"pt","Netherlands":"nl","Brazil":"br",
    "Belgium":"be","Germany":"de","Croatia":"hr","Morocco":"ma","Colombia":"co",
    "Uruguay":"uy","Switzerland":"ch","Senegal":"sn","Japan":"jp","Iran":"ir",
    "South Korea":"kr","Austria":"at","Ecuador":"ec","Australia":"au","Norway":"no",
    "Panama":"pa","Egypt":"eg","Algeria":"dz","Scotland":"gb","Paraguay":"py",
    "Ivory Coast":"ci","Tunisia":"tn","South Africa":"za","Qatar":"qa","Uzbekistan":"uz",
    "Saudi Arabia":"sa","Jordan":"jo","Curacao":"cw","New Zealand":"nz","Haiti":"ht",
    "Ghana":"gh","Cape Verde":"cv",
    "Italy Path": "eu",
    "Ukraine Path": "eu",
    "Turkey Path": "eu",
    "Denmark Path": "eu",
    "DR Congo Path": "PLANET",
    "Iraq Path": "PLANET"
}

# --- FUNCIONES HELPER ---
PLANET_ICON_URL = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f30d.png"

def flag_url_for(country):
    code = iso_map.get(country)
    if not code: return ""
    if code == "PLANET": return PLANET_ICON_URL
    return f"https://flagcdn.com/w40/{code}.png"

flag_cache = {}
def get_flag_image(country_code, size=(20, 15)):
    if country_code not in flag_cache:
        url = PLANET_ICON_URL if country_code == "PLANET" else f"https://flagcdn.com/w40/{country_code}.png"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img_data = response.content
            flag_img = Image.open(io.BytesIO(img_data)).convert("RGBA")
            flag_img = flag_img.resize(size, Image.LANCZOS)
            flag_cache[country_code] = flag_img
        except Exception:
            flag_cache[country_code] = None
    return flag_cache[country_code]

# --- GENERADOR HTML PARA BOMBOS (Mover aquí para evitar error de definición) ---
def generar_html_bombo(nombre_bombo, lista_paises):
    # Inicia la tarjeta
    html = f"<div class='pot-card'><div class='pot-title'>{nombre_bombo}</div>"
    
    if not lista_paises:
        html += "<div style='text-align:center; color:#ccc; font-size:13px; padding:10px;'><i>Empty / Drawn</i></div>"
    else:
        for item in lista_paises:
            color = conf_colors.get(item["confederacion"], "#FFFFFF")
            bandera_url = flag_url_for(item["pais"])
            
            # Imagen de la bandera
            img_tag = ""
            if bandera_url:
                img_tag = f"