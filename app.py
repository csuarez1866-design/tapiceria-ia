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
st.markdown('<p class="lema-gigante">Diseño de Tapicería Personalizada</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown("### 📸 Paso 1: Imagen Base")
    foto = st.camera_input("Capturar")
    if not foto: foto = st.file_uploader("Subir imagen", type=["jpg", "png", "jpeg"])
    
    st.markdown("### 🛠️ Paso 2: Configuración Detallada")
    
    # SECCIÓN: CABEZAL (NUEVA)
    with st.expander("👤 CABEZAL"):
        m_cabezal = st.selectbox("Material del Cabezal", ["Igual al centro", "Igual a laterales", "Cuero Liso", "Alcántara"])
        c_cabezal = st.color_picker("Color del Cabezal", "#111111")
    
    # SECCIÓN: CENTRO
    with st.expander("💎 SECCIÓN CENTRAL", expanded=True):
        m_centro = st.selectbox("Tipo de Material (Centro)", ["Alcántara", "Cuero Microperforado", "Cuero Liso", "Efecto Diamante", "Fibra de Carbono"])
        c_centro = st.color_picker("Color del Centro", "#333333")
    
    # SECCIÓN: LATERALES
    with st.expander("🏎️ SECCIÓN LATERAL"):
        m_lat = st.selectbox("Tipo de Material (Laterales)", ["Cuero Napa", "Cuero Premium", "Carbon Fiber Look"])
        c_lat = st.color_picker("Color de Laterales", "#111111")
    
    # SECCIÓN: COSTURAS Y BORDADO (ACTUALIZADA)
    with st.expander("🧵 DETALLES Y LOGO"):
        hilo = st.color_picker("Color de Costuras", "#E60000")
        estilo_costura = st.selectbox("Estilo", ["Doble Costura", "Simple", "Punto Hexagonal"])
        bordado_logo = st.checkbox("¿Añadir bordado de logo en el respaldo?")
        if bordado_logo:
            color_logo = st.color_picker("Color del Bordado", "#FFFFFF")
            posicion_logo = st.radio("Posición del logo", ["Centro del respaldo", "Bajo el cabezal"])

with col2:
    st.markdown("### 🚀 Paso 3: Previsualización")
    if foto:
        if st.button("GENERAR DISEÑO EXCLUSIVO"):
            with st.spinner("Creando su diseño personalizado..."):
                try:
                    # PROMPT REFORZADO CON LAS NUEVAS SECCIONES
                    p = (f"Automotive upholstery masterwork. "
                         f"Headrest: {m_cabezal} in {c_cabezal} color. "
                         f"Seat center: {m_centro} texture, color {c_centro}. "
                         f"Sides: {m_lat} in {c_lat}. "
                         f"Stitching: {estilo_costura} with {hilo} thread. "
                         f"{'Add an elegant embroidered logo in ' + color_logo + ' color on ' + posicion_logo if bordado_logo else ''}. "
                         "8k resolution, luxury car interior, highly detailed, realistic materials.")
                    
                    out = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": p, "image_guidance_scale": 1.5}
                    )
                    st.image(out, caption="Resultado del diseño personalizado", use_container_width=True)
                except:
                    st.error("Error al procesar. Intenta con una foto más clara.")
    else:
        st.info("Sube una foto para aplicar la configuración de materiales.")
