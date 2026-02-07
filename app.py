import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite", layout="wide")

# --- 2. FONDO Y ESTILO DE MARCA ---
url_fondo = "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?q=80&w=2000"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');
    
    /* Ocultar cualquier error residual de imagen */
    img {{ display: none !important; }}
    .stImage img {{ display: block !important; }}

    .stApp {{
        background-color: #1a1a1a;
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* EL LOGO MÁS IMPONENTE: TAMAÑO MONUMENTAL */
    .protap-logo {{
        font-family: 'Great Vibes', cursive; 
        font-size: clamp(150px, 40vw, 300px); /* TAMAÑO MÁXIMO AUMENTADO A 300PX */
        font-weight: 400;
        text-align: center;
        
        /* Efecto de Oro Líquido */
        background: linear-gradient(to right, #bf953f 20%, #fcf6ba 40%, #fcf6ba 60%, #bf953f 80%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        
        margin-top: -80px; 
        margin-bottom: -80px;
        filter: drop-shadow(0px 15px 30px rgba(0,0,0,0.9));
        line-height: 1.1;
        white-space: nowrap;
    }}

    @keyframes shine {{
        to {{ background-position: 200% center; }}
    }}

    .subtitulo-vintage {{
        color: #fcf6ba;
        text-align: center;
        font-family: 'serif';
        font-style: italic;
        font-size: clamp(24px, 6vw, 40px) !important;
        margin-top: -30px;
        margin-bottom: 50px;
        text-shadow: 2px 2px 10px black;
        letter-spacing: 2px;
    }}

    /* Estilo para el botón de ingreso */
    .stButton>button {{
        background: linear-gradient(45deg, #bf953f, #aa771c) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        height: 50px;
        font-size: 20px !important;
    }}

    header, footer, #MainMenu {{ visibility: hidden !important; }}
    label {{ color: #fcf6ba !important; font-size: 20px !important; }}
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
    st.markdown('<p class="protap-logo">Protap IA</p>', unsafe_allow_html=True)
    with st.columns([1,1.5,1])[1]:
        clave = st.text_input("Acceso Maestro:", type="password")
        if st.button("INGRESAR"):
            if clave in ["ADMIN", "TALLER01"]:
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- 5. PANEL DE DISEÑO POR SECCIONES ---
st.markdown('<p class="protap-logo">Protap IA</p>', unsafe_allow_html=True)

col_config, col_viz = st.columns([1, 1.2])

with col_config:
    st.markdown("### 1. Captura de Base")
    foto = st.camera_input("Asiento actual")
    if not foto: foto = st.file_uploader("O sube una imagen", type=["jpg", "png", "jpeg"])

    st.markdown("###  2. Personalización por Zonas")

    # SECCIÓN CENTRO
    with st.expander(" ZONA CENTRAL (Respaldo y Base)"):
        mat_centro = st.selectbox("Material", ["Alcántara", "Cuero Microperforado", "Cuero Liso", "Diseño Diamante", "Tela Premium"])
        col_centro = st.color_picker("Color Principal", "#333333", key="c1")

    # SECCIÓN LATERALES
    with st.expander(" ZONA LATERAL (Soportes)"):
        mat_lat = st.selectbox("Material Lateral", ["Cuero Napa", "Fibra de Carbono", "Cuero Premium"])
        col_lat = st.color_picker("Color Lateral", "#111111", key="c2")

    # SECCIÓN CABEZAL Y LOGO
    with st.expander(" CABEZAL Y BORDADO"):
        mat_head = st.selectbox("Estilo Cabezal", ["A juego con centro", "A juego con laterales", "Contraste liso"])
        bordado = st.checkbox("¿Incluir bordado Protap?")
        if bordado:
            col_bordado = st.color_picker("Color del Hilo Bordado", "#bf953f")

    # SECCIÓN COSTURAS
    with st.expander("🧵 COSTURAS Y VIVOS"):
        estilo_hilo = st.selectbox("Tipo de Punto", ["Doble Costura", "Costura Simple", "Punto Cruz", "Hexagonal"])
        col_hilo = st.color_picker("Color del Hilo", "#E60000", key="c3")
        piping = st.checkbox("¿Añadir vivo (Piping) en bordes?")

with col_viz:
    st.markdown("###  3. Resultado Final")
    if foto:
        if st.button("GENERAR DISEÑO COMPLETO"):
            with st.spinner("La IA está cosiendo su diseño..."):
                try:
                    # Creamos un prompt ultra detallado con todas las variables
                    prompt_final = (
                        f"Professional automotive upholstery photography. "
                        f"Central part of the seat: {mat_centro} texture, color {col_centro}. "
                        f"Side bolsters: {mat_lat} texture, color {col_lat}. "
                        f"Headrest: {mat_head}. "
                        f"Stitching details: {estilo_hilo} style with {col_hilo} thread. "
                        f"{'Add an elegant embroidered logo on the backrest' if bordado else ''} "
                        f"{'Add contrast piping on the edges' if piping else ''}. "
                        f"Luxury car interior, hyper-realistic, 8k resolution."
                    )
                    
                    resultado = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": prompt_final, "image_guidance_scale": 1.5}
                    )
                    st.image(resultado, use_container_width=True)
                except Exception as e:
                    st.error("Error en la generación. Intente con otra foto.")
    else:
        st.info("Cargue una foto para activar la personalización.")



