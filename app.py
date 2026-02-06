import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite Design", page_icon="✂️", layout="wide")

# --- 2. BLOQUEO TOTAL DE INTERFAZ (CSS) ---
# Este código oculta la barra lateral de desarrollo, el botón de GitHub, 
# el menú de edición y las leyendas de "Made with Streamlit".
st.markdown("""
    <style>
    /* Ocultar barra de estado y menús superiores */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* Bloquear el visualizador de código y el icono de GitHub */
    .viewerBadge_container__1QS1n {display: none !important;}
    .stAppDeployButton {display: none !important;}
    .st-emotion-cache-zq5wmm {display: none !important;}
    
    /* Fondo profesional del taller */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), 
        url("https://images.unsplash.com/photo-1517524206127-48bbd362f39e?q=80&w=2000");
        background-size: cover;
    }
    
    /* Estilo para los textos */
    h1, h2, h3, p, label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD (TOKEN REPLICATE) ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ Error de sistema: Token no configurado.")
    st.stop()

# --- 4. GESTIÓN DE CLAVES COMERCIALES ---
# Aquí es donde generas tus "tokens" para vender. 
# Añade una línea nueva para cada taller que te pague.
codigos_activos = {
    "ADMIN-MASTER": "Desarrollador",
    "TALLER-VIP-01": "Tapicería Central",
    "PRO-AUTO-123": "Auto-Diseños Pro"
}

# --- 5. SISTEMA DE LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🛡️ Sistema de Diseño Protap IA")
    st.write("Bienvenido. Ingrese su credencial de taller para activar las herramientas de IA.")
    
    clave = st.text_input("Credencial de Acceso:", type="password")
    if st.button("Validar Licencia"):
        if clave in codigos_activos:
            st.session_state.autenticado = True
            st.session_state.cliente = codigos_activos[clave]
            st.rerun()
        else:
            st.error("Credencial inválida. Contacte al administrador para soporte.")
    st.stop()

# --- 6. APLICACIÓN PARA EL CLIENTE ---
st.title(f"✂️ Panel de Diseño: {st.session_state.cliente}")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Configuración")
    archivo = st.file_uploader("1. Subir foto original:", type=["jpg", "png", "jpeg"])
    estilo = st.selectbox("2. Seleccionar material/estilo:", [
        "Cuero Rojo Diamond Stitching",
        "Cuero Negro Perforado",
        "Alcántara Gris con costura Amarilla",
        "Cuero Vintage Tabaco"
    ])
    
    if st.sidebar.button("🔒 Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

with col2:
    if archivo and st.button("🚀 GENERAR PROPUESTA"):
        with st.spinner("La IA está procesando el diseño..."):
            try:
                # Prompt optimizado para realismo
                prompt_ia = f"Automotive interior, professional car seat upholstery, {estilo}, high quality, 4k"
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": archivo, "prompt": prompt_ia}
                )
                st.image(output, caption="Propuesta de Diseño Finalizada")
            except Exception as e:
                st.error("Servidor ocupado. Intente nuevamente en unos segundos.")
