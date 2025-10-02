import os
import sys
import logging
import json
import glob
import yaml
import re
import uuid
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build, errors
from googleapiclient.http import MediaFileUpload

# --- SCRIPT SETUP: LOGGING AND CONFIGURATION ---
load_dotenv()

# Set up logging to append to the main pipeline log file
LOG_LEVEL_STR = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_LEVELS = {
    'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
    'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
}
log_level = LOG_LEVELS.get(LOG_LEVEL_STR, logging.INFO)

logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("generation.log", mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)

try:
    SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    TEMPLATE_ID = os.environ['TEMPLATE_PRESENTATION_ID']
    SOURCE_DIRECTORY = "json_source"
    IMAGE_DIRECTORY = "extracted_images"
    OUTPUT_FOLDER_ID = os.environ['OUTPUT_FOLDER_ID']
    TARGET_THEME_NAME = os.environ['TARGET_THEME_NAME']
    LAYOUTS_FILE = "layouts.yaml"
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
    sys.exit(1)

# ---FIX--- Correctly define scopes as a list of strings
SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive" # Add drive scope for image uploads
]

# --- CORE API & HELPER FUNCTIONS ---

def authenticate():
    """Authenticates using the service account and returns API services."""
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        slides_service = build("slides", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)
        logging.info("✅ Successfully authenticated to Google APIs.")
        return slides_service, drive_service
    except Exception as e:
        logging.critical(f"FATAL: An unexpected error occurred during authentication: {e}")
    return None, None

def load_config():
    """Loads the main YAML configuration file."""
    try:
        with open(LAYOUTS_FILE, 'r') as f:
            config = yaml.safe_load(f)
            logging.info(f"Configuration loaded successfully from '{LAYOUTS_FILE}'.")
            return config
    except FileNotFoundError:
        logging.critical(f"FATAL: Configuration file not found at '{LAYOUTS_FILE}'.")
    except yaml.YAMLError as e:
        logging.critical(f"FATAL: Error parsing YAML file '{LAYOUTS_FILE}': {e}")
    return None

def copy_template_presentation(drive_service, new_title):
    """Copies the template presentation and returns the new ID."""
    try:
        logging.info(f"Copying template to create new presentation '{new_title}'...")
        copy_body = {'name': new_title, 'parents': [OUTPUT_FOLDER_ID]}
        copied_file = drive_service.files().copy(
            fileId=TEMPLATE_ID, body=copy_body, supportsAllDrives=True
        ).execute()
        presentation_id = copied_file.get('id')
        logging.info(f"New presentation created with ID: {presentation_id}")
        return presentation_id
    except errors.HttpError as err:
        logging.error(f"Failed to copy template presentation: {err}")
    return None

def get_theme_and_layouts(slides_service, presentation_id):
    """Analyzes a presentation to find the target theme and its layouts."""
    try:
        presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
        target_master = next((m for m in presentation.get('masters', []) if m.get('masterProperties', {}).get('displayName') == TARGET_THEME_NAME), None)

        if not target_master:
            logging.error(f"FATAL: Theme '{TARGET_THEME_NAME}' not found in the template.")
            return None, None, None

        target_master_id = target_master.get('objectId')
        logging.info(f"Identified theme '{TARGET_THEME_NAME}' with ID: {target_master_id}")
        
        final_layouts = {
            layout.get('layoutProperties', {}).get('displayName'): layout.get('objectId')
            for layout in presentation.get('layouts', [])
            if layout.get('layoutProperties', {}).get('masterObjectId') == target_master_id
        }
        return target_master_id, final_layouts, presentation.get('pageSize')
    except errors.HttpError as err:
        logging.error(f"Could not fetch and process presentation theme info: {err}")
        return None, None, None

def replace_master_slide_text(slides_service, presentation_id, master_id, replacements):
    """Performs text replacements on the master slide."""
    requests = []
    for key, value in replacements.items():
        if isinstance(value, dict) and 'find' in value and 'replace' in value:
            requests.append({
                "replaceAllText": {
                    "replaceText": value['replace'],
                    "pageObjectIds": [master_id],
                    "containsText": {"text": value['find'], "matchCase": False}
                }
            })
    if requests:
        try:
            slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
            logging.info("Performed global text replacements on the master slide.")
        except errors.HttpError as err:
            logging.warning(f"Could not perform master slide text replacements: {err}")

def clean_text_content(text):
    """Removes citation tags from a string value *within* the JSON."""
    if not isinstance(text, str):
        return text
    text = re.sub(r'\[cite_start\]|\[cite:[\d,\s]+\]', '', text)
    return text.strip()

def get_rich_text_requests(object_id, body_lines):
    """Generates API requests for populating a shape with richly formatted text."""
    requests = []
    # Clean text content before processing
    cleaned_lines = [clean_text_content(line) for line in body_lines]
    full_text = "\n".join(cleaned_lines)
    
    if not full_text:
        return []

    requests.append({"insertText": {"objectId": object_id, "text": full_text}})

    current_offset = 0
    for line in cleaned_lines:
        plain_line = line.replace("**", "").replace("*", "")
        line_end = current_offset + len(plain_line)
        
        if line.lstrip().startswith(('-', '*', '1.')):
             requests.append({"createParagraphBullets": {
                "objectId": object_id,
                "textRange": {"type": "FIXED_RANGE", "startIndex": current_offset, "endIndex": line_end}
            }})

        bold_matches = re.finditer(r'\*\*(.*?)\*\*', line)
        for match in bold_matches:
            start, end = match.span(1)
            # Adjust indices for removed asterisks
            adjusted_start = current_offset + start - (match.start(0) // 2 * 2)
            adjusted_end = adjusted_start + (end - start)
            requests.append({"updateTextStyle": {
                "objectId": object_id,
                "textRange": {"type": "FIXED_RANGE", "startIndex": adjusted_start, "endIndex": adjusted_end},
                "style": {"bold": True}, "fields": "bold"
            }})
        
        current_offset = line_end + 1
    
    return requests

# --- NEW: Advanced Rendering Logic ---
def create_fullscreen_image(drive_service, slide_id, slide_index, image_ref, page_size):
    """Generates request to create a centered, fullscreen image."""
    json_base_name = image_ref.get("json_file_base")
    image_pattern = f"{json_base_name}-slide_{slide_index+1:02d}.*"
    
    found_images = glob.glob(os.path.join(IMAGE_DIRECTORY, image_pattern))
    if not found_images:
        logging.warning(f"  - Slide {slide_index+1}: Image file not found for pattern '{image_pattern}'. Skipping image.")
        return None

    image_path = found_images[0]
    logging.info(f"  - Uploading and placing image '{os.path.basename(image_path)}'...")
    
    try:
        # Upload image to a temporary folder in Drive to get a URL
        file_metadata = {'name': os.path.basename(image_path), 'parents': [OUTPUT_FOLDER_ID]}
        media = MediaFileUpload(image_path)
        image_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webContentLink').execute()
        
        # Make the image publicly readable so the Slides API can access it
        drive_service.permissions().create(fileId=image_file.get('id'), body={'type': 'anyone', 'role': 'reader'}).execute()
        
        image_url = image_file.get('webContentLink')

        # This part remains a heuristic. For a precise solution, a library like Pillow
        # would be needed to read the image dimensions before uploading.
        # For now, we assume a 4:3 aspect ratio for calculation.
        img_width, img_height = 1200, 900
        
        page_width = page_size['width']['magnitude']
        page_height = page_size['height']['magnitude']
        margin = 360000 # EMU, approx 0.5 inches

        # Calculate final dimensions while maintaining aspect ratio
        scale = min((page_width - 2 * margin) / img_width, (page_height - 2 * margin) / img_height)
        final_width = img_width * scale
        final_height = img_height * scale

        pos_x = (page_width - final_width) / 2
        pos_y = (page_height - final_height) / 2

        return {
            "createImage": {
                "url": image_url,
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": {"magnitude": final_width, "unit": "EMU"}, "height": {"magnitude": final_height, "unit": "EMU"}},
                    "transform": {"scaleX": 1, "scaleY": 1, "translateX": pos_x, "translateY": pos_y, "unit": "EMU"}
                }
            }
        }
    except Exception as e:
        logging.error(f"  - Failed to upload or place image for slide {slide_index+1}. Error: {e}")
        return None


def create_fullscreen_table(slide_id, table_data, page_elements, page_size):
    """Generates requests to create and populate a centered table."""
    # Find the title placeholder to determine available vertical space
    title_placeholder = next((el for el in page_elements if el.get('shape', {}).get('placeholder', {}).get('type') == 'TITLE'), None)
    
    top_margin = 360000 # Default top margin
    if title_placeholder:
        title_transform = title_placeholder.get('transform', {})
        title_size = title_placeholder.get('size', {})
        # Position below the title
        top_margin = title_transform.get('translateY', 0) + title_size.get('height', {}).get('magnitude', 0) + 180000 # plus padding
    
    page_width = page_size['width']['magnitude']
    page_height = page_size['height']['magnitude']
    bottom_margin = 360000
    
    available_width = page_width - (2 * 360000)
    available_height = page_height - top_margin - bottom_margin
    
    rows = len(table_data.get('rows', [])) + 1 # +1 for header
    cols = len(table_data.get('headers', []))
    if not (rows > 1 and cols > 0):
        return []

    table_id = str(uuid.uuid4())
    requests = []
    
    # NOTE: This creates a table that fills the available space. Sizing and centering
    # is complex. This is a simplified approach. A full implementation would
    # calculate text length to set column widths and row heights.
    requests.append({"createTable": {
        "objectId": table_id,
        "elementProperties": {
            "pageObjectId": slide_id,
            "size": {"width": {"magnitude": available_width, "unit": "EMU"}, "height": {"magnitude": available_height, "unit": "EMU"}},
            "transform": {"scaleX": 1, "scaleY": 1, "translateX": 360000, "translateY": top_margin, "unit": "EMU"}
        },
        "rows": rows, "columns": cols
    }})

    # Populate header
    for c, header in enumerate(table_data['headers']):
        requests.append({"insertText": {"objectId": table_id, "cellLocation": {"rowIndex": 0, "columnIndex": c}, "text": clean_text_content(header)}})
        requests.append({"updateTextStyle": {"objectId": table_id, "cellLocation": {"rowIndex": 0, "columnIndex": c}, "style": {"bold": True}, "fields": "bold"}})
    # Populate rows
    for r, row_data in enumerate(table_data['rows']):
        for c, cell_text in enumerate(row_data):
            requests.append({"insertText": {"objectId": table_id, "cellLocation": {"rowIndex": r + 1, "columnIndex": c}, "text": clean_text_content(str(cell_text))}})
            
    return requests

# --- Main Slide Creation Logic ---

def add_slide_to_presentation(slides_service, drive_service, presentation_id, slide_index, slide_data, layout_map, class_to_layout_name_map, page_size, globals_config):
    """Creates a new slide and populates it with data from the JSON slide object."""
    layout_class = slide_data.get('layoutClass', 'default')
    layout_name = class_to_layout_name_map.get(layout_class)
    layout_id = layout_map.get(layout_name)

    if not layout_id:
        logging.error(f"  - Layout '{layout_name}' for class '{layout_class}' not found. Skipping slide.")
        return

    requests = []
    slide_id = f"slide_{slide_index}_{uuid.uuid4()}"
    
    requests.append({"createSlide": {"objectId": slide_id, "slideLayoutReference": {"layoutId": layout_id}}})

    # Execute slide creation first to get element IDs
    try:
        response = slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
        logging.info(f"  - Created slide {slide_index+1}/{slide_data.get('total_slides')} (class: {layout_class})")
    except errors.HttpError as err:
        logging.error(f"  - Failed to create slide {slide_index+1}. Error: {err}")
        return

    page_elements = slides_service.presentations().pages().get(presentationId=presentation_id, pageObjectId=slide_id).execute().get('pageElements', [])
    
    # --- Get all placeholders and their properties ---
    placeholders = {}
    for el in page_elements:
        ph = el.get('shape', {}).get('placeholder')
        if ph:
            ph_type = ph.get('type')
            if ph_type not in placeholders:
                placeholders[ph_type] = []
            placeholders[ph_type].append({
                'objectId': el.get('objectId'),
                'transform': el.get('transform', {})
            })
    
    # Sort subtitle placeholders by vertical position
    if 'SUBTITLE' in placeholders:
        placeholders['SUBTITLE'].sort(key=lambda x: x['transform'].get('translateY', 0))

    # --- Build Content Population Requests ---
    content_requests = []
    
    # 1. Populate Title
    if 'title' in slide_data and 'TITLE' in placeholders:
        title_id = placeholders['TITLE'][0]['objectId']
        content_requests.append({"insertText": {"objectId": title_id, "text": clean_text_content(slide_data['title'])}})

    # 2. Populate Globals (Header/Footer) and Subtitle
    if 'SUBTITLE' in placeholders:
        subtitle_placeholders = placeholders['SUBTITLE']
        if slide_data.get('subtitle'):
            subtitle_id = subtitle_placeholders[0]['objectId']
            content_requests.append({"insertText": {"objectId": subtitle_id, "text": clean_text_content(slide_data['subtitle'])}})
        elif layout_class not in ['title', 'closing']: # Don't add globals to title/closing
            if globals_config.get('header') and len(subtitle_placeholders) > 0:
                header_id = subtitle_placeholders[0]['objectId'] # Topmost
                content_requests.append({"insertText": {"objectId": header_id, "text": globals_config['header']}})
            if globals_config.get('footer') and len(subtitle_placeholders) > 1:
                footer_id = subtitle_placeholders[-1]['objectId'] # Bottommost
                content_requests.append({"insertText": {"objectId": footer_id, "text": globals_config['footer']}})
    
    # 3. Handle different layout classes
    body_id = placeholders.get('BODY', [{}])[0].get('objectId')

    if layout_class == "image_fullscreen":
        image_ref = slide_data.get("imageReference", {})
        image_ref["json_file_base"] = slide_data.get("json_file_base")
        img_req = create_fullscreen_image(drive_service, slide_id, slide_index, image_ref, page_size)
        if img_req: content_requests.append(img_req)

    elif layout_class == "table_fullscreen":
        if 'table' in slide_data:
            content_requests.extend(create_fullscreen_table(slide_id, slide_data['table'], page_elements, page_size))
    
    elif layout_class == 'image_right' and body_id:
        if 'body' in slide_data:
            content_requests.extend(get_rich_text_requests(body_id, slide_data['body']))
        # TODO: Handle image placement in the correct image placeholder
        logging.warning(f"  - image_right layout class does not yet place the image automatically.")


    else: # Default, columns, agenda etc.
        if 'body' in slide_data and body_id:
            content_requests.extend(get_rich_text_requests(body_id, slide_data['body']))
            
    # Handle speaker notes
    if 'speakerNotes' in slide_data:
        notes_page = slides_service.presentations().pages().get(presentationId=presentation_id, pageObjectId=slide_id).execute()
        notes_id = notes_page.get('slideProperties', {}).get('notesPage', {}).get('notesProperties', {}).get('speakerNotesObjectId')
        if notes_id:
            content_requests.append({"insertText": {"objectId": notes_id, "text": clean_text_content(slide_data['speakerNotes'])}})

    if content_requests:
        try:
            slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": content_requests}).execute()
        except errors.HttpError as err:
            logging.error(f"  - Failed to populate slide {slide_index+1}. Error: {err}")


# --- MAIN EXECUTION LOGIC ---
def main():
    """Main execution flow of the script."""
    logging.info("--- Initializing JSON to Slides Builder ---")
    
    slides_service, drive_service = authenticate()
    if not all([slides_service, drive_service]):
        sys.exit(1)

    config = load_config()
    if not config:
        sys.exit(1)
    
    class_to_layout_name_map = config.get('layout_mapping', {})
    globals_config = config.get('globals', {})

    json_files = glob.glob(os.path.join(SOURCE_DIRECTORY, '*.json'))
    if not json_files:
        logging.warning(f"No .json files found in '{SOURCE_DIRECTORY}'. Exiting.")
        return

    for json_file in json_files:
        logging.info(f"\n--- Processing file: {os.path.basename(json_file)} ---")
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                presentation_data = json.load(f)
            
            workshop_title = presentation_data.get("workshopTitle", "Untitled Workshop")
            slides = presentation_data.get("slides", [])
            
            if not slides:
                logging.warning(f"No slides found in {json_file}. Skipping.")
                continue

            # Set the dynamic global header
            globals_config['header'] = workshop_title
            
            # 1. Create the new presentation
            presentation_id = copy_template_presentation(drive_service, f"Generated - {workshop_title}")
            if not presentation_id:
                raise Exception("Failed to copy template presentation.")

            # 2. Get theme info and apply global replacements
            master_id, layout_map, page_size = get_theme_and_layouts(slides_service, presentation_id)
            if not master_id:
                raise Exception("Could not identify target theme in the template.")
            
            replace_master_slide_text(slides_service, presentation_id, master_id, globals_config)

            # 3. Clean template slides
            pres = slides_service.presentations().get(presentationId=presentation_id).execute()
            slide_ids_to_delete = [s['objectId'] for s in pres.get('slides', [])]
            if slide_ids_to_delete:
                delete_requests = [{"deleteObject": {"objectId": sid}} for sid in slide_ids_to_delete]
                slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": delete_requests}).execute()
                logging.info(f"Removed {len(slide_ids_to_delete)} template slides.")
            
            # 4. Loop through slides in JSON and create them
            total_slides = len(slides)
            json_file_base = os.path.splitext(os.path.basename(json_file))[0]
            for i, slide_data in enumerate(slides):
                slide_data['total_slides'] = total_slides
                slide_data['json_file_base'] = json_file_base
                add_slide_to_presentation(slides_service, drive_service, presentation_id, i, slide_data, layout_map, class_to_layout_name_map, page_size, globals_config)

            presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/"
            logging.info(f"✅ Successfully created presentation: {presentation_url}")

        except json.JSONDecodeError as e:
            logging.error(f"❌ Failed to parse JSON file {json_file}. Error: {e}")
        except Exception as e:
            logging.error(f"❌ An unexpected error occurred while processing {json_file}. Error: {e}", exc_info=True)

    logging.info("\n--- Batch Processing Complete ---")

if __name__ == "__main__":
    main()

