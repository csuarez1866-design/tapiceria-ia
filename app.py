import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Protap IA - Elite", layout="wide")

# --- 2. FONDO (MANTENIDO) ---
url_fondo = "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?q=80&w=2000"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&display=swap');
    
    /* ELIMINACIÓN DE ICONOS DE ERROR */
    img {{
        display: none !important;
    }}
    /* Permitir que solo las imágenes generadas por la IA se muestren */
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

    .lema-gigante {{
        font-family: 'Playfair Display', serif;
        font-size: clamp(30px, 7vw, 60px); 
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 50px; /* Espacio para compensar la falta de logo */
        margin-bottom: 30px;
        font-style: italic;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
    }}

    header, footer, #MainMenu {{ visibility: hidden !important; }}
    
    label, p, .stMarkdown {{ 
        color: #fcf6ba !important; 
        font-weight: bold !important;
        text-shadow: 2px 2px 4px black !important;
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
    # Se eliminó la línea del logo que causaba el error
    st.markdown('<p class="lema-gigante">PROTAP IA</p>', unsafe_allow_html=True)
    with st.columns([1,1.5,1])[1]:
        clave = st.text_input("Acceso Maestro:", type="password")
        if st.button("INGRESAR"):
            if clave in ["ADMIN", "TALLER01"]:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- 5. PANEL DE DISEÑO ---
# Se eliminó la línea del logo aquí también
st.markdown('<p class="lema-gigante">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    foto = st.camera_input("📷 CAPTURAR")
    if not foto: foto = st.file_uploader("📂 SUBIR", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    m_centro = st.selectbox("MATERIAL CENTRO", ["Alcántara", "Cuero Microperforado", "Fibra de Carbono"])
    c_centro = st.color_picker("COLOR CENTRO", "#333333")
    hilo = st.color_picker("COLOR HILO", "#E60000")

with col2:
    if foto:
        if st.button("🚀 GENERAR DISEÑO"):
            with st.spinner("PROCESANDO..."):
                try:
                    p = f"Luxury car seat, {m_centro} texture, color {c_centro}, stitching {hilo}, hyperrealistic."
                    out = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": p}
                    )
                    st.image(out, use_container_width=True)
                except:
                    st.error("Error de conexión. Reintenta.")

