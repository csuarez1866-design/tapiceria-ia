import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Protap IA - Elite", layout="wide")

# --- 2. CONFIGURACIÓN DE IMÁGENES REFORZADAS ---
# He actualizado estos links a servidores más estables (Unsplash y Wikimedia)
url_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Car_seat_icon_-_Noun_Project_33100.svg/512px-Car_seat_icon_-_Noun_Project_33100.svg.png"
url_fondo = "https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=2000"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&display=swap');
    
    /* 1. BLINDAJE CONTRA IMÁGENES ROTAS: Si la imagen no existe, no muestra el icono de error */
    img:not([src]), img[src=""] {{ display: none !important; }}
    
    .stApp {{
        background-color: #1a1a1a;
        background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: -20px;
        padding: 10px;
        min-height: 100px;
    }}
    
    .logo-img {{
        width: 120px;
        height: auto;
        filter: invert(1) drop-shadow(0px 0px 12px rgba(191, 149, 63, 0.7));
    }}

    .lema-gigante {{
        font-family: 'Playfair Display', serif;
        font-size: clamp(30px, 7vw, 60px); 
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        font-style: italic;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
    }}

    header, footer, #MainMenu {{ visibility: hidden !important; }}
    .stAppDeployButton {{ display: none !important; }}
    
    label, p, .stMarkdown {{ 
        color: #fcf6ba !important; 
        font-weight: bold !important;
        text-shadow: 2px 2px 4px black !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD DE TOKEN ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.warning("Falta configurar el Token en Secrets."); st.stop()

# --- 4. LOGIN ---
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    # Agregado onerror para eliminar el logo si falla el link
    st.markdown(f'<div class="logo-container"><img src="{url_logo}" class="logo-img" onerror="this.style.display=\'none\'"></div>', unsafe_allow_html=True)
    st.markdown('<p class="lema-gigante">PROTAP IA</p>', unsafe_allow_html=True)
    with st.columns([1,1.5,1])[1]:
        clave = st.text_input("Acceso Maestro:", type="password")
        if st.button("INGRESAR"):
            if clave in ["ADMIN", "TALLER01"]:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- 5. PANEL DE DISEÑO ---
# Agregado onerror para eliminar el logo si falla el link
st.markdown(f'<div class="logo-container"><img src="{url_logo}" class="logo-img" onerror="this.style.display=\'none\'"></div>', unsafe_allow_html=True)
st.markdown('<p class="lema-gigante">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    foto = st.camera_input("📷 CAPTURAR")
    if not foto: foto = st.file_uploader("📂 SUBIR", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    m_centro = st.selectbox("MATERIAL CENTRO", ["Alcántara", "Cuero Microperforado", "Fibra de Carbono"])
    c_centro = st.color_picker("COLOR CENTRO", "#333333")
    
    m_lat = st.selectbox("MATERIAL LATERAL", ["Cuero Liso", "Cuero Premium", "Carbon Fiber Look"])
    c_lat = st.color_picker("COLOR LATERAL", "#111111")
    
    hilo = st.color_picker("COLOR HILO", "#E60000")

with col2:
    if foto:
        if st.button("🚀 GENERAR DISEÑO"):
            with st.spinner("PERSONALIZANDO..."):
                try:
                    p = f"Professional automotive upholstery photography, luxury car seat, center in {m_centro} color {c_centro}, sides in {m_lat} color {c_lat}, stitching details in {hilo}, 8k resolution, realistic lighting."
                    out = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": p, "image_guidance_scale": 1.5}
                    )
                    st.image(out, caption="Diseño Propuesto", use_container_width=True)
                except Exception as e:
                    st.error("Servidor ocupado. Por favor, intenta de nuevo en unos segundos.")

