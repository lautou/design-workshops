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
    OUTPUT_FOLDER_ID = os.environ['OUTPUT_FOLDER_ID']
    TARGET_THEME_NAME = os.environ['TARGET_THEME_NAME']
    LAYOUTS_FILE = "layouts.yaml"
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]

# --- CORE API & HELPER FUNCTIONS (Adapted from md2gslides.py) ---

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

def load_layout_mapping():
    """Loads the class-to-layout mapping from the YAML file."""
    try:
        with open(LAYOUTS_FILE, 'r') as f:
            mapping = yaml.safe_load(f)
            logging.info(f"Layout mapping loaded successfully from '{LAYOUTS_FILE}'.")
            return mapping
    except FileNotFoundError:
        logging.critical(f"FATAL: Layout mapping file not found at '{LAYOUTS_FILE}'.")
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
        return copied_file.get('id')
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

def get_rich_text_requests(object_id, body_lines):
    """Generates API requests for populating a shape with richly formatted text from a list of strings."""
    requests = []
    full_text = "\n".join(body_lines)
    if not full_text:
        return []

    requests.append({"insertText": {"objectId": object_id, "text": full_text}})

    # Process bold formatting and create bullets
    current_offset = 0
    for line in body_lines:
        plain_line = line.replace("**", "")
        line_end = current_offset + len(plain_line)
        
        # Create paragraph bullets for lines that are list items
        if line.lstrip().startswith(('-', '*', '1.')):
             requests.append({"createParagraphBullets": {
                "objectId": object_id,
                "textRange": {"type": "FIXED_RANGE", "startIndex": current_offset, "endIndex": line_end}
            }})

        # Apply bold style
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

def add_slide_to_presentation(slides_service, presentation_id, slide_data, layout_map, class_to_layout_name_map):
    """Creates a new slide and populates it with data from the JSON slide object."""
    layout_class = slide_data.get('layoutClass', 'default')
    layout_name = class_to_layout_name_map.get(layout_class)
    layout_id = layout_map.get(layout_name)

    if not layout_id:
        logging.error(f"Layout '{layout_name}' for class '{layout_class}' not found. Skipping slide.")
        return

    requests = []
    slide_id = str(uuid.uuid4())
    
    # Map placeholders by type
    placeholder_mappings = []
    if slide_data.get('title'): placeholder_mappings.append({'layoutPlaceholder': {'type': 'TITLE'}, 'objectId': str(uuid.uuid4())})
    if slide_data.get('subtitle'): placeholder_mappings.append({'layoutPlaceholder': {'type': 'SUBTITLE'}, 'objectId': str(uuid.uuid4())})
    if slide_data.get('body'): placeholder_mappings.append({'layoutPlaceholder': {'type': 'BODY', 'index': 0}, 'objectId': str(uuid.uuid4())})
    # Add more for columns etc. if needed

    requests.append({"createSlide": {"objectId": slide_id, "slideLayoutReference": {"layoutId": layout_id}}})

    # Execute slide creation
    body = {"requests": requests}
    response = slides_service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
    
    # Get the actual object IDs created by the API
    page_elements = slides_service.presentations().pages().get(presentationId=presentation_id, pageObjectId=slide_id).execute().get('pageElements', [])
    object_ids = {el.get('shape', {}).get('placeholder', {}).get('type'): el.get('objectId') for el in page_elements if 'placeholder' in el.get('shape', {})}

    # Populate content
    text_requests = []
    if 'title' in slide_data and 'TITLE' in object_ids:
        text_requests.append({"insertText": {"objectId": object_ids['TITLE'], "text": slide_data['title']}})
    if 'subtitle' in slide_data and 'SUBTITLE' in object_ids:
        text_requests.append({"insertText": {"objectId": object_ids['SUBTITLE'], "text": slide_data['subtitle']}})
    if 'body' in slide_data and 'BODY' in object_ids:
        text_requests.extend(get_rich_text_requests(object_ids['BODY'], slide_data['body']))
    
    # Handle speaker notes
    if 'speakerNotes' in slide_data:
        notes_page = slides_service.presentations().pages().get(presentationId=presentation_id, pageObjectId=slide_id).execute()
        notes_id = notes_page.get('slideProperties', {}).get('notesPage', {}).get('notesProperties', {}).get('speakerNotesObjectId')
        if notes_id:
            text_requests.append({"insertText": {"objectId": notes_id, "text": slide_data['speakerNotes']}})

    # Create table if it exists
    if 'table' in slide_data and 'BODY' in object_ids:
        table_data = slide_data['table']
        rows = len(table_data.get('rows', [])) + 1 # +1 for header
        cols = len(table_data.get('headers', []))
        if rows > 1 and cols > 0:
            table_id = str(uuid.uuid4())
            text_requests.append({"createTable": {
                "objectId": table_id,
                "elementProperties": {"pageObjectId": slide_id},
                "rows": rows, "columns": cols
            }})
            # Populate header
            for c, header in enumerate(table_data['headers']):
                text_requests.append({"insertText": {"objectId": table_id, "cellLocation": {"rowIndex": 0, "columnIndex": c}, "text": header}})
                text_requests.append({"updateTextStyle": {"objectId": table_id, "cellLocation": {"rowIndex": 0, "columnIndex": c}, "style": {"bold": True}, "fields": "bold"}})
            # Populate rows
            for r, row_data in enumerate(table_data['rows']):
                for c, cell_text in enumerate(row_data):
                    text_requests.append({"insertText": {"objectId": table_id, "cellLocation": {"rowIndex": r + 1, "columnIndex": c}, "text": cell_text}})

    if text_requests:
        slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": text_requests}).execute()

# --- MAIN EXECUTION LOGIC ---
def main():
    """Main execution flow of the script."""
    logging.info("--- Initializing JSON to Slides Builder ---")
    
    slides_service, drive_service = authenticate()
    if not all([slides_service, drive_service]):
        sys.exit(1)

    class_to_layout_name_map = load_layout_mapping()
    if not class_to_layout_name_map:
        sys.exit(1)

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
            
            # 1. Create the new presentation by copying the template
            presentation_id = copy_template_presentation(drive_service, f"Generated - {workshop_title}")
            if not presentation_id:
                raise Exception("Failed to copy template presentation.")

            # 2. Clean template slides
            pres = slides_service.presentations().get(presentationId=presentation_id).execute()
            slide_ids_to_delete = [s['objectId'] for s in pres.get('slides', [])]
            if slide_ids_to_delete:
                delete_requests = [{"deleteObject": {"objectId": sid}} for sid in slide_ids_to_delete]
                slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": delete_requests}).execute()
                logging.info(f"Removed {len(slide_ids_to_delete)} template slides.")

            # 3. Get theme and layout info
            master_id, layout_map, page_size = get_theme_and_layouts(slides_service, presentation_id)
            if not master_id:
                raise Exception("Could not identify target theme in the template.")
            
            # 4. Loop through slides in JSON and create them
            for i, slide_data in enumerate(slides):
                logging.info(f"  - Creating slide {i+1}/{len(slides)} (class: {slide_data.get('layoutClass', 'N/A')})...")
                add_slide_to_presentation(slides_service, presentation_id, slide_data, layout_map, class_to_layout_name_map)

            presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/"
            logging.info(f"✅ Successfully created presentation: {presentation_url}")

        except json.JSONDecodeError as e:
            logging.error(f"❌ Failed to parse JSON file {json_file}. Error: {e}")
        except Exception as e:
            logging.error(f"❌ An unexpected error occurred while processing {json_file}. Error: {e}", exc_info=True)

    logging.info("\n--- Batch Processing Complete ---")

if __name__ == "__main__":
    main()

