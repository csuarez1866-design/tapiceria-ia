import streamlit as st
import replicate
import os

st.set_page_config(page_title="Protap IA", page_icon="✂️", layout="wide")

# CSS para ocultar TODO lo técnico y poner fondo
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden !important;}
    .stAppDeployButton, .viewerBadge_container__1QS1n {display: none !important;}
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
        url("https://images.unsplash.com/photo-1517524206127-48bbd362f39e?q=80&w=2000");
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

# Seguridad
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Falta Token")
    st.stop()

# Claves de venta
codigos = {"TALLER01": "Premium", "ADMIN": "Master"}

if "auth" not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    clave = st.text_input("Clave de Acceso:", type="password")
    if st.button("Entrar"):
        if clave in codigos:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- INTERFAZ DE TRABAJO ---
st.title("✂️ Diseñador en Vivo")

# OPCIÓN DE CÁMARA DIRECTA
foto = st.camera_input("1. Captura el asiento del cliente")

if not foto:
    foto = st.file_uploader("O sube una imagen guardada:", type=["jpg", "png", "jpeg"])

estilo = st.selectbox("2. Elige el nuevo estilo:", ["Cuero Rojo Diamante", "Cuero Negro Sport", "Cuero Café Vintage"])

if foto and st.button("🚀 VER RESULTADO"):
    with st.spinner("Diseñando..."):
        try:
            p = f"Professional car seat upholstery, {estilo}, high quality"
            out = replicate.run("timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                                input={"image": foto, "prompt": p})
            st.image(out, caption="Propuesta para el Cliente")
        except:
            st.error("Error. Verifica créditos en Replicate.")
