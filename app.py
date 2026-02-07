import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite", page_icon="✂️", layout="wide")

# --- 2. FONDO Y ESTILO DE MARCA IMPONENTE ---
url_fondo = "https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=2000"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');
    
    /* Ocultar cualquier error residual de imagen */
    img {{ display: none !important; }}
    .stImage img {{ display: block !important; }}

    .stApp {{
        background-color: #1a1a1a;
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* EL LOGO MÁS IMPONENTE: TAMAÑO MONUMENTAL */
    .protap-logo {{
        font-family: 'Great Vibes', cursive; 
        font-size: clamp(120px, 40vw, 300px); /* TAMAÑO MÁXIMO AUMENTADO A 300PX */
        font-weight: 400;
        text-align: center;
        
        /* Efecto de Oro Líquido */
        background: linear-gradient(to right, #bf953f 20%, #fcf6ba 40%, #fcf6ba 60%, #bf953f 80%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        
        margin-top: -80px; 
        margin-bottom: -80px;
        filter: drop-shadow(0px 15px 30px rgba(0,0,0,0.9));
        line-height: 1.1;
        white-space: nowrap;
    }}

    @keyframes shine {{
        to {{ background-position: 200% center; }}
    }}

    .subtitulo-vintage {{
        color: #fcf6ba;
        text-align: center;
        font-family: 'serif';
        font-style: italic;
        font-size: clamp(24px, 6vw, 40px) !important;
        margin-top: -30px;
        margin-bottom: 50px;
        text-shadow: 2px 2px 10px black;
        letter-spacing: 2px;
    }}

    /* Estilo para el botón de ingreso */
    .stButton>button {{
        background: linear-gradient(45deg, #bf953f, #aa771c) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        height: 50px;
        font-size: 20px !important;
    }}

    header, footer, #MainMenu {{ visibility: hidden !important; }}
    label {{ color: #fcf6ba !important; font-size: 20px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Configura el TOKEN en Secrets"); st.stop()

# --- 4. LOGIN ---
if "autenticado" not in st.session_state: 
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<p class="protap-logo">Protap IA</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitulo-vintage">Elite Design Studio</p>', unsafe_allow_html=True)
    with st.columns([1,1.5,1])[1]:
        clave = st.text_input("Acceso Maestro:", type="password")
        if st.button("INGRESAR AL TALLER"):
            if clave in ["ADMIN", "TALLER01"]:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- 5. PANEL DE DISEÑO ---
st.markdown('<p class="protap-logo">Protap IA</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo-vintage">"El arte de la tapicería en sus manos"</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    foto = st.camera_input("📷 CAPTURAR ASIENTO")
    if not foto: 
        foto = st.file_uploader("📂 O SUBIR FOTO", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    m_centro = st.selectbox("MATERIAL CENTRO", ["Alcántara", "Cuero Microperforado", "Fibra de Carbono"])
    c_centro = st.color_picker("COLOR CENTRO", "#333333")
    hilo = st.color_picker("COLOR HILO", "#E60000")

with col2:
    if foto:
        if st.button("🚀 GENERAR DISEÑO EXCLUSIVO"):
            with st.spinner("CREANDO OBRA MAESTRA..."):
                try:
                    p = f"Luxury car seat. Center: {m_centro} in {c_centro}. Stitching: {hilo}. 8k photorealistic."
                    out = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": p, "image_guidance_scale": 1.5}
                    )
                    st.image(out, use_container_width=True)
                except:
                    st.error("Error de conexión. Reintenta.")
