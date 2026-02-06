import streamlit as st
import replicate
import os

st.set_page_config(page_title="Protap - IA de Diseño", page_icon="✂️")

# Estilo personalizado para que se vea profesional
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("✂️ Diseñador de Tapicería Profesional")
st.write("Muestre al cliente cómo quedará su vehículo antes de empezar a trabajar.")

with st.sidebar:
    st.header("🔑 Acceso")
    api_token = st.text_input("API Token:", type="password")
    st.info("Este token activa el motor de diseño de IA.")

if api_token:
    os.environ['REPLICATE_API_TOKEN'] = api_token
    
    col1, col2 = st.columns(2)
    
    with col1:
        archivo = st.file_uploader("Subir foto del asiento actual", type=["jpg", "png", "jpeg"])
    
    with col2:
        st.subheader("Opciones de Diseño")
        estilo = st.selectbox("Seleccione el material/estilo:", [
            "Cuero rojo con costura diamante (Diamond stitching)",
            "Cuero negro microperforado",
            "Alcántara gris con bordes amarillos",
            "Cuero café estilo vintage / cafe racer",
            "Personalizado..."
        ])
        
        # Traductor automático para la IA
        prompts = {
            "Cuero rojo con costura diamante (Diamond stitching)": "Change the seat to red leather with luxury diamond stitching pattern",
            "Cuero negro microperforado": "Change the seat to black perforated leather, professional upholstery",
            "Alcántara gris con bordes amarillos": "Change the seat to dark gray alcantara fabric with yellow piping on edges",
            "Cuero café estilo vintage / cafe racer": "Change the seat to vintage cognac brown leather, horizontal ribbed pattern"
        }

    if archivo:
        st.image(archivo, caption="Estado Actual", use_container_width=True)
        
        prompt_final = prompts.get(estilo, "Change the seat upholstery")
        if estilo == "Personalizado...":
            prompt_final = st.text_input("Describa el diseño (en inglés):", "Change the seat to...")

        if st.button("🚀 GENERAR PROPUESTA VISUAL"):
            with st.spinner("Diseñando..."):
                try:
                    output = replicate.run(
                        "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                        input={"image": archivo, "prompt": prompt_final, "image_guidance_scale": 1.5}
                    )
                    st.image(output, caption="Propuesta de Diseño", use_container_width=True)
                    st.success("¡Diseño generado! Puede guardar la imagen para enviársela al cliente.")
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("Ingrese el API Token en la barra lateral para comenzar.")