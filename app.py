import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Protap IA - Elite", page_icon="✂️", layout="wide")

# --- 2. FONDO ---
url_fondo = "https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=2000"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&display=swap');
    
    /* Eliminar iconos de error */
    img {{ display: none !important; }}
    .stImage img {{ display: block !important; }}

    .stApp {{
        background-color: #1a1a1a;
        background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    .lema-gigante {{
        font-family: 'Playfair Display', serif;
        font-size: clamp(30px, 7vw, 55px); 
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
    }}

    /* Estilo para los contenedores de secciones */
    .stExpander {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid #bf953f !important;
        border-radius: 10px !important;
    }}

    header, footer, #MainMenu {{ visibility: hidden !important; }}
    
    label, p, .stMarkdown {{ 
        color: #fcf6ba !important; 
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Configura el TOKEN en Secrets"); st.stop()

# --- 4. LOGIN ---
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<p class="lema-gigante">PROTAP IA</p>', unsafe_allow_html=True)
    with st.columns([1,1.5,1])[1]:
        clave = st.text_input("Acceso Maestro:", type="password")
        if st.button("INGRESAR"):
            if clave in ["ADMIN", "TALLER01"]:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- 5. PANEL DE DISEÑO ---
st.markdown('<p class="lema-gigante">Personalizador de Tapicería Elite</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown("### 📸 Paso 1: Cargar Base")
    foto = st.camera_input("Capturar Asiento")
    if not foto: foto = st.file_uploader("O subir archivo", type=["jpg", "png", "jpeg"])
    
    st.markdown("### 🛠️ Paso 2: Configurar Secciones")
    
    # SECCIÓN: CENTRO DEL ASIENTO
    with st.expander("💎 SECCIÓN CENTRAL", expanded=True):
        m_centro = st.selectbox("Tipo de Material (Centro)", ["Alcántara", "Cuero Microperforado", "Cuero Liso", "Diseño Diamante"])
        c_centro = st.color_picker("Color del Centro", "#333333")
    
    # SECCIÓN: LATERALES
    with st.expander("🏎️ SECCIÓN LATERAL"):
        m_lat = st.selectbox("Tipo de Material (Laterales)", ["Cuero Premium", "Carbon Fiber Look", "Cuero Napa"])
        c_lat = st.color_picker("Color de Laterales", "#111111")
    
    # SECCIÓN: COSTURAS Y DETALLES
    with st.expander("🧵 COSTURAS Y ESTILO"):
        hilo = st.color_picker("Color de Hilo (Costuras)", "#E60000")
        estilo_costura = st.selectbox("Estilo de Costura", ["Doble Costura", "Costura Simple", "Punto de Cruz", "Estilo Hexagonal"])
        piping = st.checkbox("¿Añadir vivo (Piping) en los bordes?")

with col2:
    st.markdown("### 🚀 Paso 3: Generar Resultado")
    if foto:
        if st.button("GENERAR DISEÑO DE LUJO"):
            with st.spinner("La IA está trabajando en su diseño..."):
                try:
                    # Creamos un prompt detallado basado en las secciones
                    p = (f"Upholstery car seat redesign. Center part: {m_centro} in color {c_centro}. "
                         f"Side bolsters: {m_lat} in color {c_lat}. "
                         f"Stitching style: {estilo_costura} using {hilo} thread. "
                         f"{'Include contrast piping on edges' if piping else ''}. "
                         "8k resolution, professional automotive interior photography, hyper-realistic.")
                    
                    out = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": p, "image_guidance_scale": 1.5}
                    )
                    st.image(out, caption="Propuesta de Tapicería Finalizada", use_container_width=True)
                except:
                    st.error("Error en la conexión. Intenta de nuevo.")
    else:
        st.info("Esperando captura de imagen para comenzar el diseño.")
