import streamlit as st
import replicate
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Protap IA - Elite", page_icon="✂️", layout="wide")

# --- 2. CONFIGURACIÓN DE RECURSOS ---
# Links estables y corrección de sintaxis
url_logo = "https://www.svgrepo.com/show/493721/car-seat.svg"
url_fondo = "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?q=80&w=2000"

# --- 3. ESTILOS CSS (ELIMINA ICONOS DE ERROR Y CONFIGURA DISEÑO) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&display=swap');
    
    /* Ocultar iconos de imagen rota en cualquier navegador */
    img:not([src]), img[src=""], img[onerror] {{
        display: none !important;
    }}

    .stApp {{
        background-color: #1a1a1a;
        background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 20px;
    }}
    
    .logo-img {{
        width: 100px;
        filter: invert(80%) sepia(20%) saturate(1000%) hue-rotate(10deg);
    }}

    .lema-gigante {{
        font-family: 'Playfair Display', serif;
        font-size: clamp(30px, 6vw, 50px); 
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
        font-style: italic;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.5);
    }}

    /* Limpieza de interfaz */
    header, footer, #MainMenu {{ visibility: hidden !important; }}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
    
    label, p, .stMarkdown {{ 
        color: #fcf6ba !important; 
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SEGURIDAD DE ACCESO ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Error: Token de Replicate no encontrado en Secrets."); st.stop()

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# --- 5. LÓGICA DE LOGIN ---
if not st.session_state.autenticado:
    st.markdown(f'<div class="logo-container"><img src="{url_logo}" class="logo-img" onerror="this.style.display=\'none\'"></div>', unsafe_allow_html=True)
    st.markdown('<p class="lema-gigante">PROTAP IA</p>', unsafe_allow_html=True)
    
    col_login, _ = st.columns([1, 2])
    with col_login:
        clave = st.text_input("Credencial de Acceso:", type="password")
        if st.button("Validar Licencia"):
            if clave in ["ADMIN", "TALLER01"]:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Acceso denegado.")
    st.stop()

# --- 6. PANEL DE DISEÑO ---
st.markdown(f'<div class="logo-container"><img src="{url_logo}" class="logo-img" onerror="this.style.display=\'none\'"></div>', unsafe_allow_html=True)
st.markdown('<p class="lema-gigante">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.markdown("### 📷 Captura de Base")
    foto = st.camera_input("Foto del asiento actual")
    if not foto:
        foto = st.file_uploader("O sube una imagen", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    st.markdown("### 🎨 Configuración")
    m_centro = st.selectbox("MATERIAL CENTRO", ["Alcántara", "Cuero Microperforado", "Fibra de Carbono"])
    c_centro = st.color_picker("COLOR CENTRO", "#333333")
    hilo = st.color_picker("COLOR HILO", "#E60000")

with col_der:
    st.markdown("### 🖼️ Visualización IA")
    if foto:
        if st.button("🚀 GENERAR DISEÑO"):
            with st.spinner("Transformando tapicería..."):
                try:
                    prompt_ia = f"Luxury car seat, material {m_centro}, color {c_centro}, stitching details in {hilo}, professional upholstery photography, highly detailed."
                    resultado = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": foto, "prompt": prompt_ia, "image_guidance_scale": 1.5}
                    )
                    st.image(resultado, caption="Resultado del Diseño", use_container_width=True)
                except Exception as e:
                    st.error("Hubo un problema con la IA. Intenta subir una foto más clara.")
    else:
        st.info("Por favor, captura o sube una foto para comenzar.")
