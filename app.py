import streamlit as st
import replicate
import os
import tempfile
import base64

# --- 1. CONFIGURACIÓN ---
st.set_page_config(
    page_title="Protap IA - Elite",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CONFIGURACIÓN DE IMÁGENES (ENLACES DE ALTA ESTABILIDAD) ---
# He cambiado estos links por servidores que NO bloquean tráfico de aplicaciones
url_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Car_seat_icon_-_Noun_Project_33100.svg/512px-Car_seat_icon_-_Noun_Project_33100.svg.png"
url_fondo = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?q=80&w=2000"

# --- 3. ESTILOS CSS (GIGANTES Y LIMPIOS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;600&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    .logo-container {{
        text-align: center;
        padding-top: 20px;
        animation: pulse 4s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    .logo-img {{
        width: 160px;
        filter: invert(1) drop-shadow(0px 0px 15px rgba(191, 149, 63, 0.8));
    }}

    .lema-gigante {{
        font-family: 'Playfair Display', serif;
        font-size: clamp(45px, 9vw, 85px) !important; /* LETRAS REALMENTE GRANDES */
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0 40px 0;
        font-style: italic;
        text-shadow: 4px 4px 15px rgba(0,0,0,0.7);
        line-height: 1.1;
    }}

    /* ELIMINAR CONTENEDORES GRISES PARA MÁXIMA LIMPIEZA */
    [data-testid="stVerticalBlock"] {{ background: none !important; border: none !important; }}
    .stCard {{ background: none !important; border: none !important; box-shadow: none !important; }}
    
    header, footer, #MainMenu {{ visibility: hidden !important; }}
    .stAppDeployButton {{ display: none !important; }}

    label, p, .stMarkdown {{ 
        color: #fcf6ba !important; 
        font-size: 22px !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 4px black !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. LÓGICA DE SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Token faltante"); st.stop()

if "autenticado" not in st.session_state: st.session_state.autenticado = False

# --- 5. PANTALLA DE INGRESO ---
if not st.session_state.autenticado:
    st.markdown(f'<div class="logo-container"><img src="{url_logo}" class="logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p class="lema-gigante">PROTAP IA ELITE</p>', unsafe_allow_html=True)
    
    col_log1, col_log2, col_log3 = st.columns([1, 1.5, 1])
    with col_log2:
        clave = st.text_input("Credencial Maestra:", type="password")
        if st.button("ACCEDER AL TALLER"):
            if clave in ["ADMIN", "TALLER01"]:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- 6. PANEL DE DISEÑO ---
st.markdown(f'<div class="logo-container"><img src="{url_logo}" class="logo-img"></div>', unsafe_allow_html=True)
st.markdown('<p class="lema-gigante">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    foto = st.camera_input("📸 TOMA LA FOTO")
    if not foto: foto = st.file_uploader("📂 SUBIR ARCHIVO", type=["jpg", "png", "jpeg"])
    
    st.markdown("### 🛠️ CONFIGURACIÓN")
    m_centro = st.selectbox("MATERIAL CENTRO", ["Alcántara", "Cuero Microperforado", "Fibra de Carbono"])
    c_centro = st.color_picker("COLOR CENTRO", "#333333")
    
    m_lat = st.selectbox("MATERIAL LATERAL", ["Cuero Liso", "Cuero Premium", "Carbon Fiber Look"])
    c_lat = st.color_picker("COLOR LATERAL", "#111111")
    
    hilo = st.color_picker("COLOR DE HILO", "#E60000")

with col2:
    if foto:
        st.markdown("### 🖼️ RESULTADO")
        if st.button("✨ GENERAR DISEÑO PREMIUM"):
            with st.spinner("CREANDO..."):
                try:
                    p = f"Professional car seat upholstery. Center: {m_centro} in {c_centro}. Sides: {m_lat} in {c_lat}. Stitching: {hilo}. 8k, realistic."
                    # Nota: Aquí usamos el archivo directamente como lo tenías
                    out = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": p, "image_guidance_scale": 1.5}
                    )
                    st.image(out, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")
