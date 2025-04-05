import os
import pytesseract
from PIL import Image
import json

# Ruta a las imágenes de las slides
IMAGES_DIR = "contenido_extraido/slides"
OUTPUT_JSON = "contenido_extraido/texto_slides_ocr.json"

# OCR a cada imagen de slide
ocr_data = {}

for filename in sorted(os.listdir(IMAGES_DIR)):
    if filename.endswith(".png"):
        img_path = os.path.join(IMAGES_DIR, filename)
        print(f"🧠 Procesando: {filename}")
        texto = pytesseract.image_to_string(Image.open(img_path), lang="spa")  # 'spa' para español
        ocr_data[filename] = texto.strip()

# Guardar en JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(ocr_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ OCR completado. Texto guardado en: {OUTPUT_JSON}")
