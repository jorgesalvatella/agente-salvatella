from pathlib import Path
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import os

# Rutas a los 3 archivos PDF que vas a usar
PDFS = [
    "docs/DS Explainer-4.pdf",
    "docs/Nuestros-Cimientos.pdf",
    "docs/Un-Servicio-Extraordinaro-1.pdf"
]

# Carpetas de salida
OUTPUT_DIR = "contenido_extraido"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "slides")
TEXT_OUTPUT = os.path.join(OUTPUT_DIR, "texto_completo.txt")

# Crear carpetas si no existen
os.makedirs(IMAGES_DIR, exist_ok=True)

# Función para extraer texto de un PDF
def extraer_texto(pdf_path):
    texto = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        texto += page.get_text() + "\n"
    return texto

# Función para extraer imágenes de cada página del PDF
def extraer_imagenes(pdf_path, pdf_name, output_folder):
    images = convert_from_path(pdf_path, dpi=200)
    for i, img in enumerate(images):
        filename = f"{pdf_name.replace('.pdf','')}_slide_{i+1}.png"
        img_path = os.path.join(output_folder, filename)
        img.save(img_path, "PNG")

# Extraer texto de todos los PDFs y combinarlo en un solo archivo
all_text = ""
for pdf in PDFS:
    nombre_archivo = Path(pdf).name
    all_text += f"### CONTENIDO DE: {nombre_archivo}\n\n"
    all_text += extraer_texto(pdf)
    all_text += "\n\n"

# Guardar texto completo extraído
with open(TEXT_OUTPUT, "w", encoding="utf-8") as f:
    f.write(all_text)

# Extraer imágenes slide por slide de cada PDF
for pdf in PDFS:
    nombre = Path(pdf).name
    extraer_imagenes(pdf, nombre, IMAGES_DIR)

print("✅ Extracción completada.")
