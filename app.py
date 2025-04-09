import streamlit as st
import json
import os
import unicodedata
from PIL import Image
from rapidfuzz import fuzz

# Función para normalizar texto (elimina acentos y pasa a minúsculas)
def normalizar(texto):
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8').lower()

# Rutas
OCR_JSON_PATH = "contenido_extraido/texto_slides_ocr.json"
SLIDES_DIR = "contenido_extraido/slides"

# Cargar datos OCR
with open(OCR_JSON_PATH, "r", encoding="utf-8") as f:
    slides_data = json.load(f)

# Configuración de la app
st.set_page_config(
    page_title="Jorge Salvatella Digital",
    layout="wide",
    initial_sidebar_state="auto"
)

# Estilo personalizado (fondo negro y texto más grande)
st.markdown(
    """
    <style>
    body {
        background-color: #111 !important;
        color: #EEE !important;
    }
    .stTextInput input {
        color: #EEE;
        font-size: 18px !important;
    }
    .stCaption, .stMarkdown, .stTitle {
        font-size: 20px !important;
    }
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    .logo-container img {
        max-height: 60px;
    }
    @media (max-width: 600px) {
        .logo-container {
            flex-direction: column;
            align-items: flex-start;
            text-align: left;
        }
        .logo-container img {
            margin-bottom: 10px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Logo + título
st.markdown(
    """
    <div class="logo-container">
        <img src="https://imagenes.jorgesalvatella.com/logo.png" alt="Logo">
        <h1 style="color: #EEE; font-size: 32px;">Jorge Salvatella Digital Services – Asistente Educativo</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Entrada de búsqueda personalizada
st.markdown("<h4 style='color:#EEE; font-size: 22px;'>¿Qué deseas consultar hoy?<br>Escribe una palabra clave para buscar la diapositiva relacionada.</h4>", unsafe_allow_html=True)
query = st.text_input("")

# Búsqueda y despliegue de slides (con tolerancia a errores y sin tildes)
if query:
    resultados = []
    query_norm = normalizar(query)

    for slide, texto in slides_data.items():
        texto_norm = normalizar(texto)
        score = fuzz.partial_ratio(query_norm, texto_norm)
        if score >= 70:
            resultados.append(slide)

    if resultados:
        for slide_img in resultados:
            st.image(os.path.join(SLIDES_DIR, slide_img), use_container_width=True)
    else:
        st.warning("❌ No encontré ninguna slide relacionada con esa palabra.")


# Footer legal
st.markdown(
    """
    <hr style="margin-top: 3rem; margin-bottom: 1rem; border: 1px solid #333;">
    <p style="font-size: 14px; color: #888; text-align: center;">
        Esta presentación ha sido desarrollada con fines de muestra y demostración para clientes en procesos de venta.<br>
        Jorge Salvatella o Jorge Salvatella Digital Services no hacen uso comercial ni difunden el contenido de las presentaciones incluidas.
    </p>
    """,
    unsafe_allow_html=True
)
