import streamlit as st
import replicate
import os
import tempfile
from PIL import Image
import base64

# --- 1. CONFIGURACIÓN MEJORADA ---
st.set_page_config(
    page_title="Protap IA - Elite",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CONFIGURACIÓN DE IMÁGENES CON FALLBACK ---
url_logo = "https://res.cloudinary.com/dze74ofjx/image/upload/v1625503521/car-seat-icon.png"
url_fondo = "https://images.unsplash.com/photo-1583121274602-3e2820c69888?q=80&w=2000"

# URLs de respaldo en caso de fallo
backup_logo = "https://cdn-icons-png.flaticon.com/512/3097/3097140.png"
backup_bg = "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=2070"

# --- 3. ESTILOS CSS MEJORADOS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;600&display=swap');
    
    /* FONDO CON MULTIPLES FALLBACKS */
    .stApp {{
        background: 
            linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.9)),
            url("{url_fondo}"),
            url("{backup_bg}"),
            linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
        min-height: 100vh;
    }}

    /* LOGO CON ANIMACIÓN SUTIL */
    .logo-container {{
        text-align: center;
        padding: 20px 0;
        animation: pulse 4s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    .logo-img {{
        width: 180px;
        height: 180px;
        object-fit: contain;
        filter: drop-shadow(0px 0px 20px rgba(191, 149, 63, 0.8));
        transition: transform 0.3s ease;
    }}
    
    .logo-img:hover {{
        transform: rotate(-5deg);
    }}

    /* TÍTULO PRINCIPAL */
    .lema-gigante {{
        font-family: 'Playfair Display', serif;
        font-size: clamp(40px, 8vw, 70px);
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #bf953f, #fcf6ba, #b38728, #fbf5b7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 20px 0 40px 0;
        font-style: italic;
        text-shadow: 4px 4px 12px rgba(0,0,0,0.7);
        line-height: 1.1;
        padding: 10px;
        letter-spacing: 1px;
    }}

    /* TARJETAS ELEGANTES */
    .stCard {{
        background: rgba(30, 30, 30, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(191, 149, 63, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }}

    /* BOTONES MEJORADOS */
    .stButton > button {{
        background: linear-gradient(45deg, #bf953f, #b38728) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        width: 100%;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(191, 149, 63, 0.4) !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(191, 149, 63, 0.6) !important;
    }}

    /* INPUTS ESTILIZADOS */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {{
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 2px solid rgba(191, 149, 63, 0.5) !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }}
    
    .stColorPicker > div {{
        border: 2px solid rgba(191, 149, 63, 0.5) !important;
        border-radius: 8px !important;
    }}

    /* TEXTO GENERAL */
    .custom-text {{
        color: #fcf6ba !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
        margin-bottom: 8px !important;
    }}

    /* LIMPIEZA DE ELEMENTOS DE STREAMLIT */
    #MainMenu, footer, header, .stDeployButton {{ 
        visibility: hidden !important; 
        display: none !important;
    }}
    
    /* SCROLLBAR PERSONALIZADO */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(30, 30, 30, 0.5);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(#bf953f, #b38728);
        border-radius: 4px;
    }}
    
    /* RESPONSIVE ADJUSTMENTS */
    @media (max-width: 768px) {{
        .lema-gigante {{
            font-size: 32px !important;
        }}
        .logo-img {{
            width: 120px !important;
            height: 120px !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. FUNCIONES AUXILIARES ---
def get_image_base64(image_file):
    """Convierte imagen a base64 para previsualización"""
    if hasattr(image_file, 'read'):
        img_bytes = image_file.read()
        return base64.b64encode(img_bytes).decode()
    return None

def save_uploaded_file(uploaded_file):
    """Guarda archivo temporalmente"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        return tmp_file.name

def generate_prompt(material_centro, color_centro, material_lateral, color_lateral, color_hilo, extras=None):
    """Genera prompt mejorado para el modelo"""
    base_prompt = f"""
    Professional luxury car seat upholstery design. 
    Center material: {material_centro} in {color_centro}. 
    Side material: {material_lateral} in {color_lateral}. 
    Stitching color: {color_hilo}.
    """
    
    if extras:
        base_prompt += f" Additional details: {extras}. "
    
    base_prompt += """
    Ultra realistic 8K render, studio lighting, professional automotive design, 
    detailed textures, premium materials, photorealistic.
    """
    
    return base_prompt

# --- 5. SEGURIDAD MEJORADA ---
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
    replicate_api_key = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("❌ Token de Replicate no configurado en Secrets")
    st.info("Por favor, configura REPLICATE_API_TOKEN en los secrets de Streamlit")
    st.stop()

# --- 6. SISTEMA DE AUTENTICACIÓN MEJORADO ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.design_history = []
    st.session_state.current_design = None

# Contraseñas seguras (en producción, usar variables de entorno)
VALID_PASSWORDS = {
    "ADMIN": "admin_protap",
    "TALLER01": "taller_protap_2024",
    "CLIENTE": "cliente_premium"
}

if not st.session_state.autenticado:
    st.markdown(f'''
        <div class="logo-container">
            <img src="{url_logo}" class="logo-img" onerror="this.src='{backup_logo}'">
        </div>
        <p class="lema-gigante">PROTAP IA ELITE</p>
    ''', unsafe_allow_html=True)
    
    # Login en el centro
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.markdown('<p class="custom-text">🔐 ACCESO RESTRINGIDO</p>', unsafe_allow_html=True)
            
            user_type = st.selectbox(
                "Tipo de usuario:",
                ["ADMIN", "TALLER01", "CLIENTE"],
                key="user_type"
            )
            
            clave = st.text_input(
                "Contraseña:",
                type="password",
                help="Ingrese la contraseña correspondiente",
                key="password_input"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🚪 INGRESAR", use_container_width=True):
                    if clave == VALID_PASSWORDS.get(user_type):
                        st.session_state.autenticado = True
                        st.session_state.user_type = user_type
                        st.rerun()
                    else:
                        st.error("Contraseña incorrecta")
            
            with col_btn2:
                if st.button("ℹ️ INFO", use_container_width=True):
                    st.info("""
                    **Credenciales de prueba:**
                    - ADMIN: admin
                    - TALLER01: taller_protap_2024
                    - CLIENTE: cliente_premium
                    """)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.stop()

# --- 7. PANEL PRINCIPAL ---
st.markdown(f'''
    <div class="logo-container">
        <img src="{url_logo}" class="logo-img" onerror="this.src='{backup_logo}'">
    </div>
    <p class="lema-gigante">"Diseñemos juntos el asiento de sus sueños"</p>
    <p style="text-align: center; color: #bf953f; font-size: 16px; margin-top: -30px;">
        Usuario: {st.session_state.user_type}
    </p>
''', unsafe_allow_html=True)

# --- 8. DISEÑO MEJORADO ---
col1, col2 = st.columns([1, 1.2])

with col1:
    with st.container():
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown('<p class="custom-text">📷 CAPTURA DE ASIENTO</p>', unsafe_allow_html=True)
        
        # Opción de cámara o upload
        option = st.radio(
            "Seleccionar fuente:",
            ["📸 Usar Cámara", "📁 Subir Archivo"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if option == "📸 Usar Cámara":
            foto = st.camera_input("", label_visibility="collapsed")
        else:
            foto = st.file_uploader(
                "Seleccionar imagen",
                type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed"
            )
        
        # Mostrar previsualización
        if foto:
            img_base64 = get_image_base64(foto)
            if img_base64:
                st.markdown(
                    f'<img src="data:image/jpeg;base64,{img_base64}" style="width:100%; border-radius:10px; margin:10px 0;">',
                    unsafe_allow_html=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Especificaciones de diseño
    with st.container():
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown('<p class="custom-text">🎨 ESPECIFICACIONES DEL DISEÑO</p>', unsafe_allow_html=True)
        
        # Materiales mejorados
        materiales_centro = {
            "Alcántara": "Material suave y deportivo",
            "Cuero Microperforado": "Ventilación premium",
            "Fibra de Carbono": "Look deportivo avanzado",
            "Cuero Liso": "Elegancia clásica",
            "Gamuza Italiana": "Lujo máximo",
            "Tela Técnica": "Deportivo/Competición"
        }
        
        materiales_lateral = {
            "Cuero Liso": "Base clásica",
            "Cuero Premium Nappa": "Calidad superior",
            "Carbon Fiber Look": "Estilo deportivo",
            "Alcántara Refuerzo": "Deportivo premium",
            "Cuero Perforado": "Ventilación + estilo"
        }
        
        m_centro = st.selectbox(
            "Material Centro:",
            options=list(materiales_centro.keys()),
            format_func=lambda x: f"{x} - {materiales_centro[x]}",
            key="mat_centro"
        )
        
        c_centro = st.color_picker(
            "Color Centro:",
            "#333333",
            key="color_centro"
        )
        
        m_lat = st.selectbox(
            "Material Lateral:",
            options=list(materiales_lateral.keys()),
            format_func=lambda x: f"{x} - {materiales_lateral[x]}",
            key="mat_lateral"
        )
        
        c_lat = st.color_picker(
            "Color Lateral:",
            "#111111",
            key="color_lateral"
        )
        
        hilo = st.color_picker(
            "Color de Hilo:",
            "#E60000",
            help="Color para costuras y detalles",
            key="color_hilo"
        )
        
        # Características adicionales
        extras = st.text_area(
            "Detalles adicionales:",
            placeholder="Ej: Logotipo bordado, calefacción integrada, ventilación activa...",
            height=100
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown('<p class="custom-text">🚀 VISUALIZACIÓN DEL DISEÑO</p>', unsafe_allow_html=True)
        
        if foto:
            # Botón de generación mejorado
            if st.button("✨ GENERAR DISEÑO PREMIUM", use_container_width=True):
                with st.spinner("🔄 Creando diseño personalizado..."):
                    try:
                        # Guardar imagen temporalmente
                        temp_path = save_uploaded_file(foto)
                        
                        # Generar prompt mejorado
                        prompt = generate_prompt(
                            m_centro, c_centro,
                            m_lat, c_lat,
                            hilo, extras
                        )
                        
                        # Mostrar detalles
                        with st.expander("📋 Ver especificaciones del diseño"):
                            st.write(f"**Material Centro:** {m_centro} ({c_centro})")
                            st.write(f"**Material Lateral:** {m_lat} ({c_lat})")
                            st.write(f"**Color Hilo:** {hilo}")
                            if extras:
                                st.write(f"**Detalles:** {extras}")
                        
                        # Ejecutar modelo
                        output = replicate.run(
                            "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                            input={
                                "image": open(temp_path, "rb"),
                                "prompt": prompt,
                                "image_guidance_scale": 1.5,
                                "guidance_scale": 7.5,
                                "num_inference_steps": 50
                            }
                        )
                        
                        # Guardar en historial
                        design_data = {
                            "materials": {
                                "center": m_centro,
                                "lateral": m_lat,
                                "colors": {
                                    "center": c_centro,
                                    "lateral": c_lat,
                                    "stitch": hilo
                                }
                            },
                            "prompt": prompt,
                            "image_url": output[0] if isinstance(output, list) else output
                        }
                        
                        st.session_state.design_history.append(design_data)
                        st.session_state.current_design = design_data
                        
                        # Mostrar resultado
                        st.success("✅ Diseño generado exitosamente!")
                        st.image(
                            output,
                            caption="🎨 Diseño Protap IA Elite",
                            use_container_width=True
                        )
                        
                        # Opciones de descarga (simuladas)
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            if st.button("💾 Guardar Diseño"):
                                st.info("En versión completa: función de descarga habilitada")
                        
                        with col_dl2:
                            if st.button("🔄 Nuevo Diseño"):
                                st.rerun()
                        
                        # Limpiar archivo temporal
                        os.unlink(temp_path)
                        
                    except Exception as e:
                        st.error(f"❌ Error al generar diseño: {str(e)}")
                        st.info("""
                        **Posibles soluciones:**
                        1. Verifica tu conexión a internet
                        2. Asegúrate que la imagen sea clara
                        3. Intenta con otra imagen
                        """)
            else:
                st.info("📝 Configura los parámetros y haz clic en 'Generar Diseño Premium'")
        else:
            st.warning("⚠️ Sube o captura una imagen para comenzar")
            st.image(
                "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?q=80&w=2000",
                caption="Ejemplo de asiento para personalizar",
                use_container_width=True
            )
        
        # Historial de diseños (si existe)
        if st.session_state.design_history:
            with st.expander("📜 Historial de Diseños", expanded=False):
                for i, design in enumerate(st.session_state.design_history[-3:], 1):
                    st.write(f"**Diseño {i}:** {design['materials']['center']} + {design['materials']['lateral']}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 9. FOOTER MEJORADO ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; color: #666;">
        <hr style="border-color: #333; margin: 30px 0;">
        <p style="font-size: 14px;">
            🛠️ <strong>PROTAP IA ELITE</strong> • Sistema de Diseño de Tapicería Premium • v2.0<br>
            © 2024 • Tecnología de punta para personalización automotriz
        </p>
        <p style="font-size: 12px; margin-top: 10px;">
            <i>Powered by Replicate AI • Streamlit</i>
        </p>
    </div>
""", unsafe_allow_html=True)

