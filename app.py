import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite Design", page_icon="✂️", layout="wide")

# --- 2. ESTILO VISUAL, LEMA Y FONDO PREMIUM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    /* FONDO CON IMAGEN DE ASIENTO PREMIUM */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
        url("https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=2070"); /* Imagen de interior de lujo */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .lema-bonito {
        font-family: 'Playfair Display', serif;
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        font-style: italic;
    }

    /* OCULTAR ELEMENTOS TÉCNICOS */
    header, footer, #MainMenu {visibility: hidden !important;}
    .stAppDeployButton, .viewerBadge_container__1QS1n {display: none !important;}
    
    h1, h2, h3, p, label, .stSelectbox label { color: white !important; text-shadow: 1px 1px 2px black; }
    
    /* Ajuste de contenedores para que no se vean totalmente negros */
    [data-testid="stVerticalBlock"] {
        background-color: rgba(0, 0, 0, 0.4);
        padding: 20px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Error: Token no configurado.")
    st.stop()

# --- 4. ACCESO ---
codigos_activos = {"ADMIN": "Desarrollador", "TALLER-VIP-01": "Tapicería Central"}

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

# --- 5. INTERFAZ PROFESIONAL POR SECCIONES ---
st.markdown('<p class="lema-bonito">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.subheader("1. Captura de Imagen")
    foto = st.camera_input("Capturar asiento")
    if not foto: foto = st.file_uploader("O subir archivo:", type=["jpg", "png", "jpeg"])

    st.divider()
    
    # CONFIGURACIÓN POR SECCIONES (Lo que pediste antes)
    st.subheader("🛋️ Configuración por Partes")
    
    with st.expander("Detalles del Centro", expanded=True):
        mat_centro = st.selectbox("Material Centro:", ["Alcántara", "Cuero Microperforado", "Cuero Liso", "Fibra de Carbono"])
        col_centro = st.color_picker("Color Centro:", "#333333")
    
    with st.expander("Detalles de Laterales", expanded=True):
        mat_lat = st.selectbox("Material Lateral:", ["Cuero Liso", "Cuero Sintético", "Fibra de Carbono"])
        col_lat = st.color_picker("Color Lateral:", "#1E1E1E")

    with st.expander("Costuras y Extras", expanded=True):
        estilo_hilo = st.selectbox("Estilo Costura:", ["Sencilla", "Doble Sport", "Diamante (Diamond)", "Hexagonal"])
        col_hilo = st.color_picker("Color de Hilo:", "#FF0000")
        detalles = st.text_input("Notas adicionales:")

with col_der:
    st.subheader("2. Resultado del Diseño")
    if foto and st.button("🚀 GENERAR PROPUESTA MAESTRA"):
        with st.spinner("La IA está confeccionando su diseño premium..."):
            try:
                prompt_ia = (
                    f"Professional car seat luxury upholstery. "
                    f"CENTRAL PART: {mat_centro} texture in color {col_centro}. "
                    f"SIDE BOLSTERS: {mat_lat} texture in color {col_lat}. "
                    f"STITCHING: {estilo_hilo} in color {col_hilo}. "
                    f"Realistic leather textures, studio lighting, 4k, {detalles}"
                )
                
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": foto, "prompt": prompt_ia, "image_guidance_scale": 1.5}
                )
                st.image(output, caption="Diseño de Alta Gama Generado", use_container_width=True)
                st.success("¡Diseño finalizado!")
            except Exception as e:
                st.error("Error en la conexión. Intente de nuevo.")
