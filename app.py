import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite Design", page_icon="✂️", layout="wide")

# --- 2. ESTILO VISUAL, LEMA Y FONDO PREMIUM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url("https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=2070");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .lema-bonito {
        font-family: 'Playfair Display', serif;
        font-size: 45px;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
        font-style: italic;
    }

    /* Estilo de Tarjetas de Configuración */
    .config-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(191, 149, 63, 0.3);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    header, footer, #MainMenu {visibility: hidden !important;}
    .stAppDeployButton, .viewerBadge_container__1QS1n {display: none !important;}
    h1, h2, h3, p, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Error: Token no configurado."); st.stop()

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

# --- 5. INTERFAZ TIPO CATÁLOGO ---
st.markdown('<p class="lema-bonito">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col_izq, col_der = st.columns([1, 1.3])

with col_izq:
    st.subheader("📸 Captura de Base")
    foto = st.camera_input("Foto del asiento actual")
    if not foto: foto = st.file_uploader("Subir imagen de referencia", type=["jpg", "png", "jpeg"])

    st.divider()
    
    # SECCIONES DIVIDIDAS COMO EN TU REFERENCIA
    st.markdown("### 🛠️ Especificaciones de Tapicería")
    
    with st.container():
        st.markdown("**🛡️ PARTE CENTRAL (INSERTS)**")
        c1, c2 = st.columns(2)
        m_centro = c1.selectbox("Material", ["Alcántara", "Microperforado", "Cuero Liso", "Fibra de Carbono"], key="mc")
        col_c = c2.color_picker("Color", "#222222", key="cc")

    with st.container():
        st.markdown("**🏎️ BORDES Y LATERALES (BOLSTERS)**")
        c3, c4 = st.columns(2)
        m_lat = c3.selectbox("Material", ["Cuero Liso", "Cuero Premium", "Sintético", "Carbon Fiber Look"], key="ml")
        col_l = c4.color_picker("Color", "#111111", key="cl")

    with st.container():
        st.markdown("**🧵 ACABADOS Y COSTURAS**")
        c5, c6 = st.columns(2)
        estilo_c = c5.selectbox("Estilo", ["Sencilla", "Doble Sport", "Diamante (Diamond)", "Hexagonal"], key="ec")
        col_h = c6.color_picker("Color Hilo", "#E60000", key="ch")

    detalles = st.text_input("✍️ Observaciones (ej: Logo bordado en cabezal)")

with col_der:
    st.subheader("🖼️ Visualización 3D IA")
    if foto and st.button("✨ GENERAR PROPUESTA DIGITAL"):
        with st.spinner("Procesando materiales y costuras..."):
            try:
                prompt_ia = (
                    f"Professional car interior modification. Focus on the seat. "
                    f"Center part: {m_centro} in color {col_c}. "
                    f"Side bolsters: {m_lat} in color {col_l}. "
                    f"Stitching pattern: {estilo_c} with thread color {col_h}. "
                    f"Ultra-realistic textures, 8k, automotive studio lighting, {detalles}"
                )
                
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": foto, "prompt": prompt_ia, "image_guidance_scale": 1.5}
                )
                st.image(output, caption="Resultado del Catálogo Digital", use_container_width=True)
                st.success("Diseño cargado exitosamente.")
            except:
                st.error("Error al conectar con el servidor de diseño.")
