import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite Design", page_icon="✂️", layout="wide")

# --- 2. BLOQUEO AGRESIVO DE INTERFAZ (CSS) ---
st.markdown("""
    <style>
    /* Ocultar barra superior y menús */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* OCULTAR BOTÓN 'ADMINISTRAR APLICACIÓN' Y MARCAS DE AGUA */
    .stAppDeployButton {display: none !important;}
    .viewerBadge_container__1QS1n {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    
    /* Ocultar el botón de 'Manage App' que aparece abajo a la derecha */
    iframe[title="manage-app"] {display: none !important;}
    button[title="Manage app"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}

    /* Fondo profesional con overlay oscuro */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
        url("https://images.unsplash.com/photo-1517524206127-48bbd362f39e?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Forzar que no haya barras laterales de edición */
    section[data-testid="stSidebar"] {
        background-color: rgba(20, 20, 20, 0.9) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD DE ACCESO ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Error crítico de configuración.")
    st.stop()

# --- 4. TUS CLAVES DE VENTA ---
# Cada vez que un taller te pague, añade su clave aquí
codigos_activos = {
    "TALLER-MASTER-01": "Sede Principal",
    "VIP-DESIGN-PRO": "Estudio Creativo",
    "PRUEBA-77": "Usuario Demo"
}

# --- 5. LÓGICA DE AUTENTICACIÓN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🛡️ Protap IA: Control de Acceso")
    clave = st.text_input("Credencial de Taller:", type="password")
    if st.button("Ingresar al Sistema"):
        if clave in codigos_activos:
            st.session_state.autenticado = True
            st.session_state.cliente = codigos_activos[clave]
            st.rerun()
        else:
            st.error("Clave Incorrecta.")
    st.stop()

# --- 6. APLICACIÓN LIMPIA ---
st.title(f"✂️ Panel de Diseño: {st.session_state.cliente}")
# ... resto de tu código de subida de fotos y generación ...
