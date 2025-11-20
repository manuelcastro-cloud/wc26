import streamlit as st
import random
import copy
import io
from PIL import Image, ImageDraw, ImageFont
import requests # <--- Nueva importación

# --- Configuración de la página ---
st.set_page_config(page_title="Simulador Sorteo WC2026", layout="wide")
st.title("🌍 Simulador Sorteo WC2026")

# --- COLORES ---
conf_colors = {
    "CONCACAF": "#FFD700",
    "CONMEBOL": "#ADFF2F",
    "UEFA": "#1E90FF",
    "CAF": "#FF6347",
    "AFC": "#FF69B4",
    "OFC": "#9370DB",
    "Variable1": "#D3D3D3", # Gris claro
    "Variable2": "#A9A9A9"  # Gris oscuro
}

# --- DATOS MAESTROS (CONSTANTES) ---
# Estos datos no se tocan, sirven para reiniciar la simulación.

DATA_BOMBO_1 = [
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

DATA_BOMBO_2 = [
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

DATA_BOMBO_3 = [
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

DATA_BOMBO_4 = [
    {"pais": "Jordania", "confederacion": "AFC"},
    {"pais": "Curazao", "confederacion": "CONCACAF"},
    {"pais": "Nueva Zelanda", "confederacion": "OFC"},
    {"pais": "Haití", "confederacion": "CONCACAF"},
    {"pais": "Ghana", "confederacion": "CAF"},
    {"pais": "Cabo Verde", "confederacion": "CAF"},
    {"pais": "ICP1", "confederacion": "Variable1"},
    {"pais": "ICP2", "confederacion": "Variable2"},
    {"pais": "UEFA1", "confederacion": "UEFA"},
    {"pais": "UEFA2", "confederacion": "UEFA"},
    {"pais": "UEFA3", "confederacion": "UEFA"},
    {"pais": "UEFA4", "confederacion": "UEFA"}
]

# --- MAPAS DE REFERENCIA ---
# Mapa país -> confederación
country_conf = {}
for b in (DATA_BOMBO_1 + DATA_BOMBO_2 + DATA_BOMBO_3 + DATA_BOMBO_4):
    country_conf[b["pais"]] = b["confederacion"]

# Mapa ISO alpha-2 para banderas
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
}

# --- Cache para banderas (descarga una vez) ---
flag_cache = {}

def get_flag_image(country_code, size=(20, 15)): # Tamaño optimizado para la imagen de resumen
    if country_code not in flag_cache:
        url = f"https://flagcdn.com/w40/{country_code}.png" # Usamos la versión de 40px para mejor calidad
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status() # Lanza una excepción para errores HTTP
            img_data = response.content
            flag_img = Image.open(io.BytesIO(img_data)).convert("RGBA") # Convertir a RGBA para transparencia
            flag_img = flag_img.resize(size, Image.LANCZOS) # Redimensionar con filtro de alta calidad
            flag_cache[country_code] = flag_img
        except requests.exceptions.RequestException as e:
            st.warning(f"No se pudo cargar la bandera de {country_code}: {e}")
            flag_cache[country_code] = None # Guardar None para no intentar de nuevo
        except Exception as e:
            st.warning(f"Error procesando la bandera de {country_code}: {e}")
            flag_cache[country_code] = None
    return flag_cache[country_code]


# --- INICIALIZAR SESIÓN (ESTADO) ---
if "grupos" not in st.session_state:
    st.session_state.grupos = {chr(65+i): [None]*4 for i in range(12)}

if "botones" not in st.session_state:
    st.session_state.botones = {"b1": True, "b2": False, "b3": False, "b4": False}

# Cargamos los bombos DE TRABAJO en sesión (copias de los datos maestros)
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
            st.markdown(f"<b>Grupo {letra}</b><br>{html_table}", unsafe_allow_html=True)

# --- GENERACIÓN DE IMAGEN (PILLOW) ---
def generar_imagen_resumen():
    W, H = 1200, 800
    bg_color = (240, 242, 246) 
    img = Image.new('RGB', (W, H), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Intentar cargar una fuente, si no usar default.
    try:
        # Rutas comunes para Arial en Windows/Mac. En Linux/Streamlit Cloud puede variar.
        # Si no la encuentra, load_default() es el fallback.
        try: # Windows
            font_title = ImageFont.truetype("arial.ttf", 28) 
            font_group = ImageFont.truetype("arial.ttf", 20)
            font_country = ImageFont.truetype("arial.ttf", 16)
        except IOError: # Mac/Linux o Streamlit Cloud si no está en PATH
            font_title = ImageFont.truetype("Arial.ttf", 28) # A veces es Arial.ttf
            font_group = ImageFont.truetype("Arial.ttf", 20)
            font_country = ImageFont.truetype("Arial.ttf", 16)
    except IOError:
        font_title = ImageFont.load_default()
        font_group = ImageFont.load_default()
        font_country = ImageFont.load_default()
        st.warning("No se encontró una fuente 'Arial'. Usando fuente por defecto. La imagen podría verse diferente.")

    # Título
    text_w, text_h = d.textsize("RESULTADOS SORTEO MUNDIAL", font=font_title)
    d.text(((W - text_w) / 2, 20), "RESULTADOS SORTEO MUNDIAL", fill=(0,0,0), font=font_title)

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
        d.text((x + 10, y + 10), f"GRUPO {letra}", fill="black", font=font_group)
        d.line([x+10, y+35, x + ancho_grupo - 20, y+35], fill="#ddd", width=1)
        
        # Países
        paises = st.session_state.grupos[letra]
        for idx, pais in enumerate(paises):
            y_pais = y + 50 + (idx * 35) # Ajustar la separación vertical para la bandera
            if pais:
                conf = country_conf.get(pais, "Variable")
                hex_color = conf_colors.get(conf, "#000000")
                
                d.rectangle([x + 10, y_pais, x + 15, y_pais + 20], fill=hex_color)
                
                # --- LÓGICA PARA BANDERAS EN LA IMAGEN ---
                country_code = iso_map.get(pais)
                if country_code:
                    flag_img = get_flag_image(country_code)
                    if flag_img:
                        img.paste(flag_img, (int(x + 25), int(y_pais + 2)), flag_img) # Pegar bandera
                        d.text((x + 25 + flag_img.width + 5, y_pais + 2), pais, fill="black", font=font_country) # Texto después de bandera
                    else: # Si bandera no se pudo cargar
                        d.text((x + 25, y_pais + 2), pais, fill="black", font=font_country)
                else: # Si no hay código ISO para el país
                    d.text((x + 25, y_pais + 2), pais, fill="black", font=font_country)
            else:
                d.text((x + 25, y_pais + 2), "---", fill="gray", font=font_country)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# --- LÓGICA DE SORTEO ---

# 1. BOMBO 1 (Cabezas de serie)
def repartir_bombo1_con_restricciones():
    bombo = st.session_state.bombo1
    if not bombo: return
    
    fijas = {"México": "A", "Canadá": "B", "USA": "D"}
    
    # Asignar anfitriones
    for pais, grupo in fijas.items():
        obj = next((x for x in bombo if x["pais"] == pais), None)
        if obj:
            st.session_state.grupos[grupo][0] = obj["pais"]
            bombo.remove(obj)
            
    # Repartir resto
    paises_restantes = bombo.copy()
    grupos_restantes = [l for l in st.session_state.grupos if l not in fijas.values()]
    random.shuffle(paises_restantes)
    
    for i, letra in enumerate(grupos_restantes):
        if i < len(paises_restantes):
            st.session_state.grupos[letra][0] = paises_restantes[i]["pais"]
            
    st.session_state.bombo1.clear()
    st.session_state.botones["b1"] = False
    st.session_state.botones["b2"] = True

# 2. BOMBOS GENERÍCOS (2 y 3) - Backtracking
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
    if key_siguiente: 
        st.session_state.botones[key_siguiente] = True

# 3. BOMBO 4 (Especial ICP)
def repartir_bombo4_especial():
    bombo_list = st.session_state.bombo4
    if not bombo_list: return
    
    # Restricciones compuestas
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
                
                if mi_conf == "Variable1": # ICP1
                    if not any(c in confs_grupo for c in restricciones_icp1):
                        es_valido = True
                        
                elif mi_conf == "Variable2": # ICP2
                    if not any(c in confs_grupo for c in restricciones_icp2):
                        es_valido = True
                        
                elif mi_conf == "UEFA":
                    if uefa_count < 2: es_valido = True
                        
                else: # Resto normal
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


# --- CALLBACKS (BOTONES) ---
def repartir_bombo1_click():
    repartir_bombo1_con_restricciones()

def repartir_bombo2_click():
    repartir_bombo_generico(st.session_state.bombo2, 1, "b2", "b3")

def repartir_bombo3_click():
    repartir_bombo_generico(st.session_state.bombo3, 2, "b3", "b4")

def repartir_bombo4_click():
    repartir_bombo4_especial()

def limpiar_grupos_click():
    # Reiniciar Grupos
    for letra in st.session_state.grupos:
        st.session_state.grupos[letra] = [None] * 4
    # Restaurar Bombos desde MAESTROS
    st.session_state.bombo1 = copy.deepcopy(DATA_BOMBO_1)
    st.session_state.bombo2 = copy.deepcopy(DATA_BOMBO_2)
    st.session_state.bombo3 = copy.deepcopy(DATA_BOMBO_3)
    st.session_state.bombo4 = copy.deepcopy(DATA_BOMBO_4)
    # Restaurar botones
    st.session_state.botones = {"b1": True, "b2": False, "b3": False, "b4": False}


# --- INTERFAZ PRINCIPAL ---

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

st.subheader("🎟 Bombos")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**Bombo 1**")
    mostrar_bombo_objetos(st.session_state.bombo1)
with col2:
    st.markdown("**Bombo 2**")
    mostrar_bombo_objetos(st.session_state.bombo2)
with col3:
    st.markdown("**Bombo 3**")
    mostrar_bombo_objetos(st.session_state.bombo3)
with col4:
    st.markdown("**Bombo 4**")
    mostrar_bombo_objetos(st.session_state.bombo4)

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
    st.button("🔄 Limpiar / Reiniciar", on_click=limpiar_grupos_click)

st.markdown("---")
st.subheader("📋 Grupos")
mostrar_grupos_coloreados()

# --- SECCIÓN DE DESCARGA Y COMPARTIR ---
# Se muestra solo si el bombo 4 ya fue sorteado
if not st.session_state.bombo4 and not st.session_state.botones["b4"]:
    st.markdown("---")
    st.markdown("## 📤 Compartir Resultados")