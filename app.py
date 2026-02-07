import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite Design", page_icon="✂️", layout="wide")

# --- 2. FONDO DE ASIENTO PREMIUM Y ESTILOS (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    /* IMAGEN DE FONDO DE ASIENTO DE ALTA CALIDAD */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url("https://images.unsplash.com/photo-1631553127988-34757788437d?q=80&w=2000");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    .lema-bonito {
        font-family: 'Playfair Display', serif;
        font-size: 45px;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 25px;
        font-style: italic;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Ocultar botones técnicos */
    header, footer, #MainMenu {visibility: hidden !important;}
    .stAppDeployButton, .viewerBadge_container__1QS1n {display: none !important;}
    
    /* Estilo para los bloques de selección */
    [data-testid="stVerticalBlock"] > div {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(191, 149, 63, 0.2);
    }
    
    h1, h2, h3, p, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Error: Token no configurado."); st.stop()

# --- 4. ACCESO ---
codigos_activos = {"ADMIN-MASTER": "Desarrollador", "TALLER-VIP-01": "Tapicería Central"}
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<p class="lema-bonito">Protap IA</p>', unsafe_allow_html=True)
    clave = st.text_input("Credencial de Acceso:", type="password")
    if st.button("Validar"):
        if clave in codigos_activos:
            st.session_state.autenticado = True
            st.session_state.cliente = codigos_activos[clave]
            st.rerun()
    st.stop()

# --- 5. INTERFAZ TIPO CATÁLOGO ---
st.markdown('<p class="lema-bonito">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.subheader("📸 Captura de Base")
    foto = st.camera_input("Foto del asiento actual")
    if not foto: foto = st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])

    st.divider()
    
    # SECCIONES DE DISEÑO
    st.markdown("### 🛠️ Configuración de Materiales")
    
    tab1, tab2 = st.tabs(["Centro y Laterales", "Costuras"])
    
    with tab1:
        m_centro = st.selectbox("Material Centro", ["Alcántara", "Microperforado", "Cuero Liso", "Fibra de Carbono"], key="mc")
        col_c = st.color_picker("Color Central", "#333333", key="cc")
        m_lat = st.selectbox("Material Lateral", ["Cuero Liso", "Cuero Premium", "Carbon Fiber Look"], key="ml")
        col_l = st.color_picker("Color Lateral", "#111111", key="cl")

    with tab2:
        estilo_c = st.selectbox("Estilo", ["Sencilla", "Doble Sport", "Diamante (Diamond)"], key="ec")
        col_h = st.color_picker("Color Hilo", "#FF0000", key="ch")
        detalles = st.text_input("Extras (ej: Franja central, logo)")

with col_der:
    st.subheader("🖼️ Propuesta IA")
    if foto and st.button("✨ GENERAR DISEÑO"):
        with st.spinner("Creando propuesta..."):
            try:
                prompt_ia = (
                    f"Professional car seat upholstery. Center: {m_centro} in {col_c}. "
                    f"Sides: {m_lat} in {col_l}. Stitching: {estilo_c} in {col_h}. "
                    f"Realistic textures, luxury automotive photography style, 4k."
                )
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": foto, "prompt": prompt_ia, "image_guidance_scale": 1.5}
                )
                st.image(output, use_container_width=True)
            except:
                st.error("Error de conexión.")
