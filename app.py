import streamlit as st
import replicate
import os

# 1. Configuración de seguridad (Secrets)
# El token se lee automáticamente de la configuración que hiciste en el paso anterior
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ['REPLICATE_API_TOKEN'] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Error de configuración: Falta el Token en Secrets.")
    st.stop()

st.set_page_config(page_title="Protap - Sistema de Diseño", page_icon="✂️")

# --- SISTEMA DE ACCESO PARA TALLERES ---
with st.sidebar:
    st.header("🔑 Acceso Clientes")
    # Aquí es donde el taller pone la clave que TÚ le vendes
    codigo_acceso = st.text_input("Código de Taller:", type="password")

# Base de datos de clientes (Aquí añades los códigos que quieras vender)
codigos_validos = ["TALLER01", "PRO-AUTO-2024", "PRUEBA-GRATIS"]

if codigo_acceso in codigos_validos:
    st.sidebar.success("Acceso Concedido")
    
    st.title("✂️ Diseñador de Tapicería Profesional")
    st.write("Herramienta exclusiva para talleres asociados.")

    archivo = st.file_uploader("Subir foto del asiento", type=["jpg", "png", "jpeg"])
    
    estilo = st.selectbox("Seleccione el nuevo diseño:", [
        "Cuero rojo con costura diamante",
        "Cuero negro microperforado",
        "Alcántara gris con bordes amarillos",
        "Cuero café estilo vintage"
    ])

    prompts = {
        "Cuero rojo con costura diamante": "Change the seat to red leather with luxury diamond stitching pattern",
        "Cuero negro microperforado": "Change the seat to black perforated leather",
        "Alcántara gris con bordes amarillos": "Change the seat to gray alcantara with yellow piping",
        "Cuero café estilo vintage": "Change the seat to vintage brown leather"
    }

    if archivo and st.button("🚀 GENERAR DISEÑO"):
        with st.spinner("Procesando imagen..."):
            try:
                output = replicate.run(
                    "timbrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": archivo, "prompt": prompts[estilo]}
                )
                st.image(output, caption="Propuesta Visual", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.title("🔓 Sistema Bloqueado")
    st.info("Para activar esta herramienta en su taller, contacte al proveedor del servicio.")
    st.warning("Ingrese un código de taller válido en el menú de la izquierda.")
