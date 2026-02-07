import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite", page_icon="✂️", layout="wide")

# --- 2. CONFIGURACIÓN DE FONDO ---
url_fondo = "https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=2000"

st.markdown(f"""
    <style>
    /* Importamos una alternativa Serif Vintage potente de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Unna:ital,wght@0,700;1,700&display=swap');
    
    img {{
        display: none !important;
    }}
    .stImage img {{
        display: block !important;
    }}

    .stApp {{
        background-color: #1a1a1a;
        background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* ESTILO BLACK HOLIST VINTAGE - MÁS GRANDE */
    .protap-logo {{
        font-family: 'Black Holist', 'Unna', serif; /* Prioriza Black Holist si está instalada */
        font-size: clamp(60px, 15vw, 110px); /* Tamaño masivo */
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to bottom, #bf953f 0%, #fcf6ba 50%, #b38728 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        margin-bottom: 0px;
        text-shadow: 4px 4px 15px rgba(0,0,0,0.8);
        letter-spacing: 2px;
        text-transform: uppercase;
    }}

    .subtitulo-vintage {{
        color: #fcf6ba;
        text-align: center;
        font-family: 'Unna', serif;
        font-style: italic;
        font-size: 26px !important;
        margin-top: -10px;
        margin-bottom: 40px;
        text-shadow: 2px 2px 4px black;
    }}

    header, footer, #MainMenu {{ visibility: hidden !important; }}
    
    label, p, .stMarkdown {{ 
        color: #fcf6ba !important; 
        font-weight: bold !important;
        text-shadow: 2px 2px 4px black !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD (TOKEN) ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Configura el TOKEN en Secrets"); st.stop()

# --- 4. LOGIN ---
if "autenticado" not in st.session_state: 
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<p class="protap-logo">PROTAP IA</p>', unsafe_allow_html=True)
    with st.columns([1,1.5,1])[1]:
        clave = st.text_input("Acceso Maestro:", type="password")
        if st.button("INGRESAR"):
            if clave in ["ADMIN", "TALLER01"]:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- 5. PANEL DE DISEÑO ---
st.markdown('<p class="protap-logo">PROTAP IA</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo-vintage">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    foto = st.camera_input("📷 CAPTURAR")
    if not foto: 
        foto = st.file_uploader("📂 SUBIR", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    m_centro = st.selectbox("MATERIAL CENTRO", ["Alcántara", "Cuero Microperforado", "Fibra de Carbono"])
    c_centro = st.color_picker("COLOR CENTRO", "#333333")
    
    m_lat = st.selectbox("MATERIAL LATERAL", ["Cuero Liso", "Cuero Premium", "Carbon Fiber Look"])
    c_lat = st.color_picker("COLOR LATERAL", "#111111")
    
    hilo = st.color_picker("COLOR HILO", "#E60000")

with col2:
    if foto:
        if st.button("🚀 GENERAR DISEÑO"):
            with st.spinner("PROCESANDO..."):
                try:
                    p = f"Luxury car seat. Center: {m_centro} in {c_centro}. Sides: {m_lat} in {c_lat}. Stitching: {hilo}. 8k realistic."
                    out = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": p, "image_guidance_scale": 1.5}
                    )
                    st.image(out, use_container_width=True)
                except:
                    st.error("Error de conexión. Reintenta.")
