import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Protap IA", page_icon="✂️", layout="wide")

# --- 2. CSS PARA LOGO, LETRAS GRANDES Y MINIMALISMO ---
# URL de tu logo (Reemplaza este link por el de tu logo real)
url_logo = "https://cdn-icons-png.flaticon.com/512/3039/3039430.png" 
# URL de fondo (Asiento premium de cerca)
url_fondo = "https://images.unsplash.com/photo-1594939584408-0193987071f0?q=80&w=2000"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* DISEÑO DEL LOGO */
    .logo-container {{
        text-align: center;
        margin-top: -50px;
    }}
    .logo-img {{
        width: 120px; /* Tamaño del logo */
        filter: drop-shadow(0px 0px 10px rgba(191, 149, 63, 0.5));
    }}

    /* LETRAS MÁS GRANDES Y ELEGANTES */
    .lema-gigante {{
        font-family: 'Playfair Display', serif;
        font-size: 58px; /* LETRAS MÁS GRANDES */
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 40px;
        font-style: italic;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        line-height: 1.2;
    }}

    /* LIMPIEZA TOTAL */
    header, footer, #MainMenu {{ visibility: hidden !important; }}
    .stAppDeployButton {{ display: none !important; }}
    [data-testid="stVerticalBlock"] {{ background: none !important; }}
    
    /* ESTILO DE TEXTOS DE CONTROL */
    label, p, .stMarkdown {{ 
        color: #fcf6ba !important; /* Color crema/oro suave */
        font-size: 18px !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px black !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Falta Token"); st.stop()

# --- 4. LOGIN MINIMALISTA ---
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown(f'<div class="logo-container"><img src="{url_logo}" class="logo-img"></div>', unsafe_allow_html=True)
    st.markdown('<p class="lema-gigante">Protap IA</p>', unsafe_allow_html=True)
    with st.columns([1,1.5,1])[1]:
        clave = st.text_input("Acceso Maestro:", type="password")
        if st.button("INGRESAR"):
            if clave in ["ADMIN", "TALLER01"]:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- 5. INTERFAZ DE DISEÑO ---
# LOGO Y LEMA GIGANTE EN EL PANEL PRINCIPAL
st.markdown(f'<div class="logo-container"><img src="{url_logo}" class="logo-img"></div>', unsafe_allow_html=True)
st.markdown('<p class="lema-gigante">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    foto = st.camera_input("📷 TOMA LA FOTO")
    if not foto: foto = st.file_uploader("📂 O SUBE UN ARCHIVO", type=["jpg", "png", "jpeg"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CONTROLES LIMPIOS
    m_centro = st.selectbox("MATERIAL CENTRO", ["Alcántara", "Cuero Microperforado", "Fibra de Carbono"])
    c_centro = st.color_picker("COLOR CENTRO", "#333333")
    
    m_lat = st.selectbox("MATERIAL LATERAL", ["Cuero Liso", "Cuero Premium", "Carbon Fiber Look"])
    c_lat = st.color_picker("COLOR LATERAL", "#111111")
    
    hilo = st.color_picker("COLOR DE HILO", "#FF0000")

with col2:
    if foto:
        st.markdown("### 🖼️ VISTA PREVIA DEL DISEÑO")
        if st.button("🚀 GENERAR PROPUESTA ELITE"):
            with st.spinner("CONFECCIONANDO..."):
                try:
                    p = f"Professional luxury car seat. Center: {m_centro} in {c_centro}. Sides: {m_lat} in {c_lat}. Stitching: {hilo}. 8k ultra realistic textures."
                    out = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": p, "image_guidance_scale": 1.5}
                    )
                    st.image(out, use_container_width=True)
                except:
                    st.error("Error de conexión.")
    else:
        st.info("💡 Por favor, captura una imagen para comenzar el diseño.")
