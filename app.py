import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite Design", page_icon="✂️", layout="wide")

# --- 2. ESTILO VISUAL Y LEMA (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
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

    header, footer, #MainMenu {visibility: hidden !important;}
    .stAppDeployButton, .viewerBadge_container__1QS1n {display: none !important;}
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
        url("https://images.unsplash.com/photo-1517524206127-48bbd362f39e?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    
    h1, h2, h3, p, label { color: white !important; }
    .stSelectbox label, .stColorPicker label { font-weight: bold; font-size: 14px; }
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
    st.title("🛡️ Protap IA")
    clave = st.text_input("Credencial de Acceso:", type="password")
    if st.button("Validar"):
        if clave in codigos_activos:
            st.session_state.autenticado = True
            st.session_state.cliente = codigos_activos[clave]
            st.rerun()
    st.stop()

# --- 5. INTERFAZ PROFESIONAL ---
st.markdown('<p class="lema-bonito">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.subheader("1. Captura de Imagen")
    foto = st.camera_input("Capturar asiento")
    if not foto: foto = st.file_uploader("O subir archivo:", type=["jpg", "png", "jpeg"])

    st.divider()
    
    # --- SECCIÓN A: EL CENTRO ---
    st.subheader("🛋️ Configuración del Centro")
    c1, c2 = st.columns(2)
    with c1:
        mat_centro = st.selectbox("Material Centro:", ["Alcántara", "Cuero Microperforado", "Cuero Liso", "Fibra de Carbono"], key="m_c")
    with c2:
        col_centro = st.color_picker("Color Centro:", "#333333", key="c_c")
    
    # --- SECCIÓN B: LOS LATERALES (OREJAS) ---
    st.subheader("🏎️ Configuración de Laterales")
    c3, c4 = st.columns(2)
    with c3:
        mat_lat = st.selectbox("Material Lateral:", ["Cuero Liso", "Cuero Sintético", "Fibra de Carbono"], key="m_l")
    with c4:
        col_lat = st.color_picker("Color Lateral:", "#1E1E1E", key="c_l")

    # --- SECCIÓN C: COSTURAS Y DETALLES ---
    st.subheader("🧵 Costuras y Acabados")
    c5, c6 = st.columns(2)
    with c5:
        estilo_hilo = st.selectbox("Estilo Costura:", ["Sencilla", "Doble Sport", "Diamante (Diamond)", "Hexagonal"], key="e_h")
    with c6:
        col_hilo = st.color_picker("Color de Hilo:", "#FF0000", key="c_h")
    
    detalles = st.text_input("Personalización adicional (ej: Bordado de marca, franjas):")

with col_der:
    st.subheader("2. Resultado del Diseño")
    if foto and st.button("🚀 GENERAR PROPUESTA POR SECCIONES"):
        with st.spinner("La IA está combinando los materiales..."):
            try:
                # Prompt avanzado que divide las instrucciones por zonas
                prompt_ia = (
                    f"Professional car seat design. "
                    f"CENTRAL PART: {mat_centro} texture in color {col_centro}. "
                    f"SIDE BOLSTERS AND EDGES: {mat_lat} texture in color {col_lat}. "
                    f"STITCHING: {estilo_hilo} pattern throughout the seat in color {col_hilo}. "
                    f"High quality upholstery, realistic leather and fabric textures, 4k, {detalles}"
                )
                
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": foto, "prompt": prompt_ia, "image_guidance_scale": 1.5}
                )
                st.image(output, caption="Propuesta de Diseño Personalizada", use_container_width=True)
                st.success("¡Diseño generado con éxito!")
            except Exception as e:
                st.error("Error en la generación. Intente nuevamente.")
    elif not foto:
        st.info("Suba o tome una foto para comenzar a diseñar por secciones.")

