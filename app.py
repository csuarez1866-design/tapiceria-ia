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
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEGURIDAD ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Error: Token no configurado.")
    st.stop()

# --- 4. ACCESO ---
codigos_activos = {"ADMIN-MASTER": "Desarrollador", "TALLER-VIP-01": "Tapicería Central"}

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

# --- 5. CONFIGURADOR POR ZONAS ---
st.markdown('<p class="lema-bonito">"Diseñemos juntos el asiento de sus sueños"</p>', unsafe_allow_html=True)
st.write(f"💼 **Taller:** {st.session_state.cliente}")

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.subheader("1. Captura de Imagen")
    foto = st.camera_input("Capturar asiento")
    if not foto: foto = st.file_uploader("O subir archivo:", type=["jpg", "png", "jpeg"])

    st.divider()
    st.subheader("2. Mapa de Materiales")
    
    # NUEVA FUNCIÓN: SELECCIÓN DE ZONA
    zona = st.radio("¿Qué parte desea modificar?", 
                    ["Asiento Completo", "Solo el Centro", "Laterales (Orejas)", "Cabezal y Respaldos"])
    
    c1, c2 = st.columns(2)
    with c1:
        material = st.selectbox("Material Principal:", ["Cuero Liso", "Fibra de Carbono", "Alcántara", "Microperforado"])
        color_mat = st.color_picker("Color Base:", "#1E1E1E")
    with c2:
        costura = st.selectbox("Estilo Costura:", ["Sencilla", "Diamante", "Doble Sport"])
        color_h = st.color_picker("Color Hilo:", "#FF0000")
    
    detalles = st.text_input("Personalización extra (ej: Franja central azul):")

with col_der:
    st.subheader("3. Resultado")
    if foto and st.button("🚀 GENERAR DISEÑO POR ZONAS"):
        with st.spinner("Procesando materiales..."):
            try:
                # Prompt inteligente que usa la 'zona' seleccionada
                prompt_ia = (
                    f"In this car seat, modify ONLY the {zona}. "
                    f"Apply {material} texture in color {color_mat}. "
                    f"Add {costura} stitching with thread color {color_h}. "
                    f"Maintain the rest of the seat original. High detail, 4k, {detalles}"
                )
                
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": foto, "prompt": prompt_ia, "image_guidance_scale": 1.5}
                )
                st.image(output, caption="Propuesta Personalizada")
            except Exception as e:
                st.error("Error en servidor. Verifique créditos.")
