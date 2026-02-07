import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Protap IA", page_icon="✂️", layout="wide")

# --- 2. CSS PARA INTERFAZ LIMPIA Y FONDO DE ASIENTO ---
# Imagen: Primer plano de costuras de asiento premium
url_fondo = "https://cdn.pixabay.com/photo/2016/11/22/23/44/porsche-1851246_1280.jpg"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    /* FONDO COMPLETO */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* LEMA ELEGANTE */
    .lema-bonito {{
        font-family: 'Playfair Display', serif;
        font-size: 42px;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        font-style: italic;
    }}

    /* ELIMINAR CONTENEDORES Y BORDES */
    [data-testid="stVerticalBlock"] {{ background: none !important; border: none !important; }}
    div[data-testid="stExpander"] {{ background: none !important; border: none !important; }}
    .stTabs {{ background: none !important; }}
    
    /* OCULTAR MENÚS TÉCNICOS */
    header, footer, #MainMenu {{ visibility: hidden !important; }}
    .stAppDeployButton {{ display: none !important; }}

    /* TEXTOS CLAROS */
    h1, h2, h3, p, label, .stMarkdown {{ 
        color: white !important; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Falta Token"); st.stop()

# --- 4. LOGIN ---
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<p class="lema-bonito">Protap IA</p>', unsafe_allow_html=True)
    with st.columns([1,2,1])[1]: # Centrar login
        clave = st.text_input("Contraseña de Acceso:", type="password")
        if st.button("Entrar"):
            if clave in ["TALLER01", "ADMIN"]:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- 5. INTERFAZ LIMPIA ---
st.markdown('<p class="lema-bonito">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    foto = st.camera_input("📸 Captura el asiento")
    if not foto: foto = st.file_uploader("O selecciona un archivo", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    
    # CONFIGURACIÓN SIN CUADROS, SOLO SELECTORES
    st.markdown("### 🛠️ Configuración")
    m_centro = st.selectbox("Centro:", ["Alcántara", "Microperforado", "Cuero Liso", "Fibra de Carbono"])
    c_centro = st.color_picker("Color Centro:", "#333333")
    
    m_lat = st.selectbox("Laterales:", ["Cuero Liso", "Cuero Premium", "Carbon Fiber Look"])
    c_lat = st.color_picker("Color Laterales:", "#111111")
    
    hilo = st.color_picker("Color de Hilo:", "#FF0000")
    extras = st.text_input("Detalle adicional:")

with col2:
    if foto:
        st.markdown("### 🖼️ Propuesta")
        if st.button("🚀 GENERAR NUEVO DISEÑO"):
            with st.spinner("Confeccionando..."):
                try:
                    p = f"Professional car seat upholstery. Center: {m_centro} in {c_centro}. Sides: {m_lat} in {c_lat}. Stitching color: {hilo}. 8k, realistic."
                    out = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": p, "image_guidance_scale": 1.5}
                    )
                    st.image(out, use_container_width=True)
                except:
                    st.error("Error de servidor.")
    else:
        st.info("Esperando captura de imagen...")
