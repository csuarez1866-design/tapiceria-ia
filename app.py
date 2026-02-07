import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite Design", page_icon="✂️", layout="wide")

# --- 2. FONDO DE ASIENTO DETALLADO Y ESTILOS (CSS) ---
# Imagen enfocada solo en el asiento y sus texturas
fondo_asiento = "https://images.unsplash.com/photo-1594939584408-0193987071f0?q=80&w=2000"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
        url("{fondo_asiento}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    .lema-bonito {{
        font-family: 'Playfair Display', serif;
        font-size: 42px;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        font-style: italic;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}

    /* Ocultar elementos innecesarios */
    header, footer, #MainMenu {{visibility: hidden !important;}}
    .stAppDeployButton, .viewerBadge_container__1QS1n {{display: none !important;}}
    
    /* Cuadros de control semitransparentes */
    [data-testid="stVerticalBlock"] > div {{
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(191, 149, 63, 0.3);
    }}
    
    h1, h2, h3, p, label, .stMarkdown {{ color: white !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Token no configurado."); st.stop()

# --- 4. ACCESO ---
codigos_activos = {"ADMIN-MASTER": "Desarrollador", "TALLER-VIP-01": "Tapicería Central"}
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<p class="lema-bonito">Protap IA</p>', unsafe_allow_html=True)
    clave = st.text_input("Credencial de Acceso:", type="password")
    if st.button("Validar Licencia"):
        if clave in codigos_activos:
            st.session_state.autenticado = True
            st.session_state.cliente = codigos_activos[clave]
            st.rerun()
    st.stop()

# --- 5. INTERFAZ ---
st.markdown('<p class="lema-bonito">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.subheader("📸 Captura de Imagen")
    foto = st.camera_input("Foto del asiento")
    if not foto: foto = st.file_uploader("Sube la foto del cliente", type=["jpg", "png", "jpeg"])

    st.divider()
    
    st.markdown("### 🪡 Configuración por Zonas")
    tab1, tab2 = st.tabs(["Materiales", "Costuras"])
    
    with tab1:
        m_centro = st.selectbox("Centro", ["Alcántara", "Microperforado", "Fibra de Carbono", "Cuero Liso"])
        col_c = st.color_picker("Color del Centro", "#222222")
        m_lat = st.selectbox("Laterales", ["Cuero Liso", "Cuero Premium", "Carbon Fiber Look"])
        col_l = st.color_picker("Color de Laterales", "#111111")

    with tab2:
        estilo_c = st.selectbox("Estilo", ["Sencilla", "Doble Deportiva", "Diamante (Luxury)"])
        col_h = st.color_picker("Color del Hilo", "#FF0000")
        detalles = st.text_input("Extras (Logos, franjas...)")

with col_der:
    st.subheader("🖼️ Propuesta IA")
    if foto and st.button("🚀 GENERAR DISEÑO"):
        with st.spinner("Creando propuesta..."):
            try:
                prompt_ia = (f"Close up of a professional car seat upholstery. Center: {m_centro} in {col_c}. "
                             f"Side bolsters: {m_lat} in {col_l}. Stitching: {estilo_c} in {col_h}. "
                             f"Detailed leather grain, realistic fabric textures, 8k.")
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": foto, "prompt": prompt_ia, "image_guidance_scale": 1.5}
                )
                st.image(output, use_container_width=True)
            except:
                st.error("Error de conexión con la IA.")
