import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA Y FONDO PROFESIONAL ---
st.set_page_config(page_title="Protap IA - Elite Design", page_icon="✂️", layout="wide")

# Estilo CSS corregido para fondo elegante y ocultar menús de edición
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url("https://images.unsplash.com/photo-1517524206127-48bbd362f39e?q=80&w=2000");
        background-size: cover;
    }
    /* ESTO BLOQUEA LA VISUALIZACIÓN DEL CÓDIGO Y MENÚS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QS1n {display: none !important;}
    </style>
    """, unsafe_allow_html=True) # <-- AQUÍ ESTABA EL ERROR, YA ESTÁ CORREGIDO

# --- 2. VERIFICACIÓN DE TOKEN ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ Configuración incompleta en Secrets.")
    st.stop()

# --- 3. GENERADOR DE CLAVES (Aquí creas tus accesos para vender) ---
# Para vender una clave nueva, solo añade una línea más aquí:
codigos_activos = {
    "TALLER-VIP-01": "Acceso Premium",
    "LUJO-AUTO-77": "Acceso Empresa",
    "DEMO-GRATIS": "Prueba 24h",
    "NUEVA-LLAVE-2024": "Cliente Nuevo" # Ejemplo de cómo agregar más
}

# --- 4. INTERFAZ DE LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🛡️ Protap IA: Sistema de Gestión Visual")
    st.subheader("Acceso exclusivo para talleres autorizados")
    
    clave = st.text_input("Ingrese su Clave de Acceso Profesional:", type="password")
    if st.button("Activar Licencia"):
        if clave in codigos_activos:
            st.session_state.autenticado = True
            st.session_state.cliente = codigos_activos[clave]
            st.rerun()
        else:
            st.error("Clave inválida o vencida. Contacte al desarrollador.")
    st.stop()

# --- 5. APLICACIÓN DESBLOQUEADA ---
st.title(f"✂️ Diseñador de Tapicería: {st.session_state.cliente}")
st.sidebar.button("Cerrar Sesión", on_click=lambda: st.session_state.update({"autenticado": False}))

col1, col2 = st.columns(2)

with col1:
    archivo = st.file_uploader("Subir foto del interior", type=["jpg", "png", "jpeg"])
    estilo = st.selectbox("Estilo de Tapicería:", [
        "Cuero Rojo Diamond Stitching",
        "Cuero Negro Perforado Sport",
        "Alcántara Gris Premium",
        "Cuero Cognac Vintage"
    ])

with col2:
    if archivo and st.button("✨ GENERAR PREVISUALIZACIÓN"):
        with st.spinner("La IA está confeccionando el diseño..."):
            try:
                p = f"Professional car upholstery, {estilo}, highly detailed, 4k"
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": archivo, "prompt": p}
                )
                st.image(output, caption="Resultado Final")
            except Exception as e:
                st.error("Error en el servidor de diseño. Verifique su crédito en Replicate.")
