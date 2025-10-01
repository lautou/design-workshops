import os
import sys
import logging
import json
import glob
import fitz  # PyMuPDF
import re

# --- Configuration ---
JSON_SOURCE_DIR = "json_source"
IMAGE_OUTPUT_DIR = "extracted_images"
SOURCE_DOCS_DIR = "source_documents"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("extraction.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def clean_and_parse_json(file_path):
    """
    Reads a file, cleans invalid citation placements that break JSON syntax,
    and then parses it into a Python dictionary. The cleaned content is
    written back to the original file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()

        # This regex finds [cite...] tags that are followed by whitespace and then a double-quoted key.
        # This is the pattern that breaks the JSON parsing.
        # It removes these misplaced tags.
        cleaned_content = re.sub(r'(\[cite_start\]|\+\])\s*(")', r'\2', raw_content)

        # Overwrite the original file with the cleaned content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        # Now, parse the cleaned content
        data = json.loads(cleaned_content)
        logging.info(f"  - Successfully cleaned and parsed {os.path.basename(file_path)}.")
        return data

    except json.JSONDecodeError as e:
        logging.error(f"  - Invalid JSON in {os.path.basename(file_path)} even after cleaning. Skipping. Error: {e}")
        return None
    except Exception as e:
        logging.error(f"  - An unexpected error occurred while processing {file_path}. Error: {e}")
        return None


def clean_text_content(text):
    """
    Removes citation tags from a string value *within* the JSON, 
    using the same Unicode-based regex for consistency.
    """
    if not isinstance(text, str):
        return text
    # Regex for 
    text = re.sub(r'\u005B\u0063\u0069\u0074\u0065\u005F\u0073\u0074\u0061\u0072\u0074\u005D', '', text)
    # Regex for or
    text = re.sub(r'\u005B\u0063\u0069\u0074\u0065\u003A\u0020[\d,\s]+\u005D', '', text)
    return text.strip()

def extract_images_from_json():
    """
    Scans JSON files, finds image references, and extracts the images.
    """
    logging.info("--- Starting JSON Curation and Image Extraction Process ---")
    
    os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)
    logging.info(f"Ensured output directory exists: {IMAGE_OUTPUT_DIR}")

    json_files = glob.glob(os.path.join(JSON_SOURCE_DIR, '*.json'))
    if not json_files:
        logging.warning(f"No JSON files found in '{JSON_SOURCE_DIR}'. Nothing to process.")
        return

    extraction_count = 0
    for json_file in json_files:
        logging.info(f"\nProcessing file: {os.path.basename(json_file)}")
        
        # Use the new cleaning and parsing function
        data = clean_and_parse_json(json_file)
        if data is None:
            continue

        slides = data.get("slides", [])
        for i, slide in enumerate(slides):
            if "imageReference" in slide:
                ref = slide["imageReference"]
                source_file = ref.get("sourceFile")
                page_num = ref.get("pageNumber")
                caption = ref.get("caption", "")
                
                # Clean the caption text content
                clean_caption = clean_text_content(caption)

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

    logging.info(f"\n--- Curation and Extraction Complete. Total images extracted: {extraction_count} ---")

if __name__ == "__main__":
    extract_images_from_json()