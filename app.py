import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---

st.set_page_config(page_title="Protap IA - Elite Design", page_icon="✂️", layout="wide")

# --- 2. BLOQUEO DE INTERFAZ Y ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    /* Ocultar elementos de administración de Streamlit y GitHub */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stAppDeployButton {display: none !important;}
    .viewerBadge_container__1QS1n {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    
    /* Fondo de taller profesional con oscurecimiento para lectura */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
        url("https://images.unsplash.com/photo-1517524206127-48bbd362f39e?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Estilo para los textos y etiquetas */
    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
    }
    
    /* Personalización de la barra lateral */
    section[data-testid="stSidebar"] {
        background-color: rgba(20, 20, 20, 0.9) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD (TOKEN DE REPLICATE) ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ Error: Configure el API Token en los Secrets de Streamlit.")
    st.stop()

# --- 4. GESTIÓN DE CLAVES DE VENTA ---
# Aquí puedes agregar todas las claves que quieras vender
codigos_activos = {
    "ADMIN-MASTER": "Desarrollador Principal",
    "TALLER-VIP-01": "Tapicería Central",
    "LUJO-AUTO-2024": "Diseños Elite",
    "DEMO-GRATIS": "Acceso de Prueba"
}

# --- 5. SISTEMA DE LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🛡️ Protap IA: Sistema de Gestión Visual")
    st.write("Ingrese su clave de taller para activar las herramientas de diseño.")
    
    clave = st.text_input("Credencial de Acceso:", type="password")
    if st.button("Validar Licencia"):
        if clave in codigos_activos:
            st.session_state.autenticado = True
            st.session_state.cliente = codigos_activos[clave]
            st.rerun()
        else:
            st.error("Credencial inválida o cuenta suspendida.")
    st.stop()

# --- 6. APLICACIÓN DESBLOQUEADA (CONFIGURADOR) ---
st.title(f"✂️ Panel de Diseño: {st.session_state.cliente}")
st.sidebar.button("🔒 Cerrar Sesión", on_click=lambda: st.session_state.update({"autenticado": False}))

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.subheader("1. Captura de Imagen")
    # Intentar usar cámara primero, si no, subir archivo
    foto = st.camera_input("Tomar foto del asiento")
    if not foto:
        foto = st.file_uploader("O subir desde galería:", type=["jpg", "png", "jpeg"])

    st.divider()
    
    st.subheader("2. Personalización Detallada")
    
    c1, c2 = st.columns(2)
    with c1:
        tipo_material = st.selectbox("Material:", ["Cuero Liso", "Cuero Microperforado", "Alcántara", "Tela Sport"])
        color_material = st.color_picker("Color de Material:", "#1E1E1E")
        
    with c2:
        tipo_costura = st.selectbox("Costuras:", ["Sencilla", "Doble Deportiva", "Diamante (Diamond)", "Hexagonal"])
        color_hilo = st.color_picker("Color de Hilo:", "#FF0000")
        
    detalles_extra = st.text_input("Notas adicionales (ej: logo bordado, franjas):")

with col_der:
    st.subheader("3. Previsualización IA")
    if foto and st.button("🚀 GENERAR DISEÑO PERSONALIZADO"):
        with st.spinner("Confeccionando diseño digital..."):
            try:
                # Construcción del Prompt inteligente
                prompt_ia = (
                    f"Professional automotive interior, car seat upholstered in {tipo_material} "
                    f"color {color_material}, with {tipo_costura} stitching in color {color_hilo}. "
                    f"Realistic texture, high detail, 4k, {detalles_extra}"
                )
                
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": foto, "prompt": prompt_ia, "image_guidance_scale": 1.5}
                )
                st.image(output, caption="Propuesta Final para el Cliente", use_container_width=True)
                st.success("¡Diseño completado con éxito!")
            except Exception as e:
                st.error("El servidor de diseño no respondió. Verifique sus créditos.")
    elif not foto:
        st.info("Suba o tome una foto para comenzar el diseño.")


