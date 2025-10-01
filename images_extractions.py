import os
import sys
import logging
import json
import glob
import fitz  # PyMuPDF

# --- Configuration ---
JSON_SOURCE_DIR = "json_source"
IMAGE_OUTPUT_DIR = "extracted_images"
# This now correctly points to the directory managed by run_pipeline.py
SOURCE_DOCS_DIR = "source_documents" 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("extraction.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def extract_images_from_json():
    """
    Scans generated JSON files, finds image references, and extracts
    the corresponding images from the locally cached source PDFs.
    """
    logging.info("--- Starting Image Extraction Process ---")
    
    # This safely creates the output directory if it doesn't exist.
    os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)
    logging.info(f"Ensured output directory exists: {IMAGE_OUTPUT_DIR}")

    json_files = glob.glob(os.path.join(JSON_SOURCE_DIR, '*.json'))
    if not json_files:
        logging.warning(f"No JSON files found in '{JSON_SOURCE_DIR}'. Nothing to process.")
        return

    extraction_count = 0
    for json_file in json_files:
        logging.info(f"\nProcessing file: {os.path.basename(json_file)}")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        slides = data.get("slides", [])
        for i, slide in enumerate(slides):
            # The script ONLY acts if this specific block is found.
            if "imageReference" in slide:
                ref = slide["imageReference"]
                source_file = ref.get("sourceFile")
                page_num = ref.get("pageNumber")

                if not source_file or not page_num:
                    logging.warning(f"  - Slide {i+1}: Incomplete image reference. Skipping.")
                    continue

                pdf_path = os.path.join(SOURCE_DOCS_DIR, source_file)
                if not os.path.exists(pdf_path):
                    logging.error(f"  - Slide {i+1}: Source PDF not found locally at '{pdf_path}'. Try running the main pipeline first. Skipping.")
                    continue

                try:
                    doc = fitz.open(pdf_path)
                    if not (0 < page_num <= len(doc)):
                        logging.error(f"  - Slide {i+1}: Page number {page_num} is out of bounds for '{source_file}'. Skipping.")
                        continue
                    
                    page = doc.load_page(page_num - 1)
                    image_list = page.get_images(full=True)

                    if not image_list:
                        logging.warning(f"  - Slide {i+1}: No images found on page {page_num} of '{source_file}'.")
                        continue

                    # Assumes the largest image is the correct one.
                    image_list.sort(key=lambda img: img[4] * img[5], reverse=True)
                    img_info = image_list[0]
                    xref = img_info[0]
                    base_image = doc.extract_image(xref)
                    
                    image_filename = f"{os.path.splitext(os.path.basename(json_file))[0]}-slide_{i+1:02d}.{base_image['ext']}"
                    image_save_path = os.path.join(IMAGE_OUTPUT_DIR, image_filename)

                    with open(image_save_path, "wb") as img_file:
                        img_file.write(base_image["image"])
                    
                    logging.info(f"  - Slide {i+1}: Successfully extracted image to '{image_save_path}'")
                    extraction_count += 1
                except Exception as e:
                    logging.error(f"  - Slide {i+1}: Failed to extract image from '{source_file}' page {page_num}. Error: {e}")

    logging.info(f"\n--- Extraction Complete. Total images extracted: {extraction_count} ---")

if __name__ == "__main__":
    extract_images_from_json()

