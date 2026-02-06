import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite Design", page_icon="✂️", layout="wide")

# --- 2. BLOQUEO DE INTERFAZ Y ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    /* Importar fuente elegante */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    /* ESTILO DEL LEMA SUPERIOR */
    .lema-bonito {
        font-family: 'Playfair Display', serif;
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
        font-style: italic;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stAppDeployButton {display: none !important;}
    .viewerBadge_container__1QS1n {display: none !important;}
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
        url("https://images.unsplash.com/photo-1517524206127-48bbd362f39e?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    
    h1, h2, h3, p, label, .stMarkdown { color: white !important; }
    section[data-testid="stSidebar"] { background-color: rgba(20, 20, 20, 0.9) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ Error de configuración en Secrets.")
    st.stop()

# --- 4. CLAVES DE VENTA ---
codigos_activos = {
    "ADMIN": "Desarrollador",
    "TALLER-VIP-01": "Tapicería Central",
    "PRO-AUTO-2024": "Diseños Elite"
}

# --- 5. SISTEMA DE LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🛡️ Protap IA")
    clave = st.text_input("Credencial de Acceso:", type="password")
    if st.button("Validar Licencia"):
        if clave in codigos_activos:
            st.session_state.autenticado = True
            st.session_state.cliente = codigos_activos[clave]
            st.rerun()
        else:
            st.error("Clave incorrecta.")
    st.stop()

# --- 6. APLICACIÓN CON LEMA BONITO ---
# AQUÍ APARECE TU LEMA PERSONALIZADO
st.markdown('<p class="lema-bonito">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

st.write(f"💼 **Panel de Diseño:** {st.session_state.cliente}")

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.subheader("1. Captura de Imagen")
    foto = st.camera_input("Tomar foto del asiento")
    if not foto:
        foto = st.file_uploader("O subir desde galería:", type=["jpg", "png", "jpeg"])

    st.divider()
    st.subheader("2. Personalización")
    c1, c2 = st.columns(2)
    with c1:
        tipo_material = st.selectbox("Material:", ["Cuero Liso", "Cuero Microperforado", "Alcántara", "Tela Sport"])
        color_material = st.color_picker("Color de Material:", "#1E1E1E")
    with c2:
        tipo_costura = st.selectbox("Costuras:", ["Sencilla", "Doble Deportiva", "Diamante (Diamond)", "Hexagonal"])
        color_hilo = st.color_picker("Color de Hilo:", "#FF0000")
    detalles_extra = st.text_input("Peticiones especiales (ej: logos, franjas):")

with col_der:
    st.subheader("3. Resultado Final")
    if foto and st.button("🚀 GENERAR DISEÑO"):
        with st.spinner("La IA está trabajando..."):
            try:
                prompt_ia = (
                    f"Professional car upholstery, seat made of {tipo_material} color {color_material}, "
                    f"with {tipo_costura} stitching in color {color_hilo}. Realistic texture, 4k, {detalles_extra}"
                )
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": foto, "prompt": prompt_ia, "image_guidance_scale": 1.5}
                )
                st.image(output, caption="Diseño Exclusivo", use_container_width=True)
            except Exception as e:
                st.error("Verifique su crédito en Replicate.")

