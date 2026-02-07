import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Protap IA - Elite", page_icon="✂️", layout="wide")

# --- 2. CONFIGURACIÓN DE IMÁGENES REFORZADAS ---
# He seleccionado links que permiten el uso en aplicaciones externas
url_logo = "https://i.imgur.com/83p1yAn.png" # Icono de asiento de alta calidad
url_fondo = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?q=80&w=2000" # Primer plano de cuero premium

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&display=swap');
    
    .stApp {{
        background-color: #1a1a1a;
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* DISEÑO DEL LOGO REFORZADO */
    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: -20px;
        padding: 10px;
    }}
    .logo-img {{
        width: 140px; /* Tamaño del logo */
        height: auto;
        filter: drop-shadow(0px 0px 12px rgba(191, 149, 63, 0.7));
    }}

    .lema-gigante {{
        font-family: 'Playfair Display', serif;
        font-size: clamp(38px, 9vw, 68px); 
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
        font-style: italic;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.6);
        line-height: 1.1;
    }}

    header, footer, #MainMenu {{ visibility: hidden !important; }}
    .stAppDeployButton {{ display: none !important; }}
    [data-testid="stVerticalBlock"] {{ background: none !important; border: none !important; }}
    
    label, p, .stMarkdown {{ 
        color: #fcf6ba !important; 
        font-size: 20px !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 4px black !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Token no configurado."); st.stop()

# --- 4. LOGIN ---
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown(f'<div class="logo-container"><img src="{url_logo}" class="logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p class="lema-gigante">PROTAP IA</p>', unsafe_allow_html=True)
    with st.columns([1,1.5,1])[1]:
        clave = st.text_input("Acceso Maestro:", type="password")
        if st.button("INGRESAR"):
            if clave in ["ADMIN", "TALLER01"]:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- 5. PANEL DE DISEÑO ---
st.markdown(f'<div class="logo-container"><img src="{url_logo}" class="logo-img"></div>', unsafe_allow_html=True)
st.markdown('<p class="lema-gigante">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    foto = st.camera_input("📷 CAPTURAR")
    if not foto: foto = st.file_uploader("📂 SUBIR", type=["jpg", "png", "jpeg"])
    
    st.markdown("<br>", unsafe_allow_html=True)
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
                    st.error("Error.")
