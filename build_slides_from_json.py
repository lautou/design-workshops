import os
import sys
import logging
import json
import glob
import yaml
import re
import uuid
from dotenv import load_dotenv

# Google Auth and API Libraries
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# AWS SDK for Python
import boto3

# --- SCRIPT SETUP: LOGGING AND CONFIGURATION ---
load_dotenv()

LOG_LEVEL_STR = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_LEVELS = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR}
log_level = LOG_LEVELS.get(LOG_LEVEL_STR, logging.INFO)

logging.basicConfig(level=log_level, format="%(asctime)s [%(levelname)s] - %(message)s", handlers=[logging.FileHandler("generation.log", mode='a'), logging.StreamHandler(sys.stdout)])

try:
    CREDENTIALS_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    TEMPLATE_ID = os.environ['TEMPLATE_PRESENTATION_ID']
    OUTPUT_FOLDER_ID = os.environ['OUTPUT_FOLDER_ID']
    TARGET_THEME_NAME = os.environ['TARGET_THEME_NAME']
    SOURCE_DIRECTORY = "json_source"
    IMAGE_DIRECTORY = "extracted_images"
    LAYOUTS_FILE = "layouts.yaml"
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
    AWS_REGION = os.environ['AWS_REGION']
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
    sys.exit(1)

SCOPES = ["https://www.googleapis.com/auth/presentations", "https://www.googleapis.com/auth/drive"]
TOKEN_FILE = 'token.json'

# --- AUTHENTICATION ---
def authenticate_google():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    try:
        slides_service = build('slides', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        logging.info("✅ Successfully authenticated to Google APIs as user.")
        return slides_service, drive_service
    except Exception as error:
        logging.critical(f'An error occurred building Google services: {error}')
        return None, None

def get_s3_client():
    try:
        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
        logging.info("✅ Successfully created AWS S3 client.")
        return s3_client
    except Exception as e:
        logging.critical(f"FATAL: Failed to create AWS S3 client: {e}")

# --- CORE HELPER FUNCTIONS ---
def load_config():
    try:
        with open(LAYOUTS_FILE, 'r') as f: return yaml.safe_load(f)
    except FileNotFoundError:
        logging.critical(f"FATAL: Config file not found: '{LAYOUTS_FILE}'.")

def copy_template_presentation(drive_service, new_title):
    try:
        copy_body = {'name': new_title, 'parents': [OUTPUT_FOLDER_ID]}
        copied_file = drive_service.files().copy(fileId=TEMPLATE_ID, body=copy_body, supportsAllDrives=True).execute()
        return copied_file.get('id')
    except HttpError as err:
        logging.error(f"Failed to copy template: {err}")

def get_theme_and_layouts(slides_service, presentation_id):
    try:
        presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
        target_master = next((m for m in presentation.get('masters', []) if m.get('masterProperties', {}).get('displayName') == TARGET_THEME_NAME), None)
        if not target_master:
            logging.error(f"FATAL: Theme '{TARGET_THEME_NAME}' not found.")
            return None, None, None
        target_master_id = target_master.get('objectId')
        layouts = {l.get('layoutProperties', {}).get('displayName'): l.get('objectId') for l in presentation.get('layouts', []) if l.get('layoutProperties', {}).get('masterObjectId') == target_master_id}
        return target_master_id, layouts, presentation.get('pageSize')
    except HttpError as err:
        logging.error(f"Could not fetch theme info: {err}")

def replace_master_slide_text(slides_service, presentation_id, master_id, replacements):
    requests = []
    for key, value in replacements.items():
        if isinstance(value, dict) and 'find' in value and 'replace' in value:
            requests.append({"replaceAllText": {"replaceText": value['replace'], "pageObjectIds": [master_id], "containsText": {"text": value['find'], "matchCase": False}}})
    if requests:
        try: slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
        except HttpError as err: logging.warning(f"Could not perform master slide replacements: {err}")

def clean_text_content(text):
    if not isinstance(text, str): return text
    return re.sub(r'\[cite(_start|:[\d,\s]+)\]', '', text).strip()

def get_rich_text_requests(object_id, body_lines):
    """Generates API requests for populating a shape with richly formatted text, handling markdown."""
    requests = []
    
    plain_text_lines = []
    formatted_lines = []
    for line in body_lines:
        stripped_line = line.lstrip()
        indentation = len(line) - len(stripped_line)
        nesting_level = indentation // 2
        is_bullet = stripped_line.startswith('- ')
        
        text_for_formatting = stripped_line.lstrip('- ').strip()
        plain_text = text_for_formatting.replace('**', '')
        
        plain_text_lines.append(plain_text)
        formatted_lines.append({'text': plain_text, 'original': text_for_formatting, 'is_bullet': is_bullet, 'level': nesting_level})
        
    full_text = "\n".join(plain_text_lines)
    if not full_text: return []

    requests.append({"insertText": {"objectId": object_id, "text": full_text}})

    current_offset = 0
    for line_info in formatted_lines:
        line_text, original_text, is_bullet, nesting_level = line_info.values()
        line_end = current_offset + len(line_text)

        if is_bullet:
            requests.append({"createParagraphBullets": {"objectId": object_id, "textRange": {"type": "FIXED_RANGE", "startIndex": current_offset, "endIndex": line_end}}})
            if nesting_level > 0:
                requests.append({"updateParagraphStyle": {"objectId": object_id, "textRange": {"type": "FIXED_RANGE", "startIndex": current_offset, "endIndex": line_end}, "style": {"indentStart": {"magnitude": 18 * nesting_level, "unit": "PT"}}, "fields": "indentStart"}})

        for match in re.finditer(r'\*\*(.*?)\*\*', original_text):
            bold_text = match.group(1)
            try:
                start_index_in_line = line_text.index(bold_text)
                start, end = current_offset + start_index_in_line, current_offset + start_index_in_line + len(bold_text)
                requests.append({"updateTextStyle": {"objectId": object_id, "textRange": {"type": "FIXED_RANGE", "startIndex": start, "endIndex": end}, "style": {"bold": True}, "fields": "bold"}})
            except ValueError:
                pass 
        
        current_offset = line_end + 1
    
    return requests

# --- AWS S3 Image Upload ---
def upload_image_to_s3(s3_client, image_path, slide_index):
    try:
        object_name = f"presentations/{uuid.uuid4()}-{os.path.basename(image_path)}"
        s3_client.upload_file(image_path, S3_BUCKET_NAME, object_name, ExtraArgs={'ACL': 'public-read'})
        return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{object_name}"
    except Exception as e:
        logging.error(f"  - Failed to upload image for slide {slide_index+1} to S3. Error: {e}")

# --- INTELLIGENT SIZING AND POSITIONING ---
def get_placeholder_bounds(placeholders):
    bounds = {}
    for p_type, p_list in placeholders.items():
        if p_list:
            p = p_list[0]
            transform, size = p.get('transform', {}), p.get('size', {})
            bounds[p_type] = {'x': transform.get('translateX', 0), 'y': transform.get('translateY', 0), 'width': size.get('width', {}).get('magnitude', 0), 'height': size.get('height', {}).get('magnitude', 0)}
            # Special handling for header/footer from subtitles
            if p_type == 'SUBTITLE' and len(p_list) > 1:
                p_list.sort(key=lambda p: p['transform'].get('translateY', 0))
                header, footer = p_list[0], p_list[-1]
                bounds['HEADER'] = {'y': header['transform'].get('translateY', 0), 'height': header['size']['height']['magnitude']}
                bounds['FOOTER'] = {'y': footer['transform'].get('translateY', 0), 'height': footer['size']['height']['magnitude']}
    return bounds

def create_image_on_slide(s3_client, slide_id, slide_index, image_ref, page_size, placeholders, position='fullscreen'):
    json_base_name = image_ref.get("json_file_base")
    image_pattern = f"{json_base_name}-slide_{slide_index+1:02d}.*"
    found_images = glob.glob(os.path.join(IMAGE_DIRECTORY, image_pattern))
    if not found_images: return None

    image_path = found_images[0]
    logging.info(f"  - Uploading '{os.path.basename(image_path)}' to S3 for {position} placement...")
    
    image_url = upload_image_to_s3(s3_client, image_path, slide_index)
    if not image_url: return None

    bounds = get_placeholder_bounds(placeholders)
    page_width, page_height = page_size['width']['magnitude'], page_size['height']['magnitude']
    img_width, img_height = 1200, 900 
    margin = 360000

    top_bound = bounds.get('TITLE', {}).get('y', 0) + bounds.get('TITLE', {}).get('height', 0)
    bottom_bound = bounds.get('FOOTER', {}).get('y', page_height - margin)
    
    available_y = top_bound + (margin / 4)
    available_height = bottom_bound - available_y

    if position == 'fullscreen':
        available_x = margin
        available_width = page_width - (2 * margin)
    else: # left_half
        available_x = margin
        right_text_bound_x = next((p['transform']['translateX'] for p in placeholders.get('SUBTITLE', []) if p['transform'].get('translateX', 0) > page_width / 2), page_width - margin)
        available_width = right_text_bound_x - margin - (margin / 2)

    scale = min(available_width / img_width, available_height / img_height)
    final_width, final_height = img_width * scale, img_height * scale
    
    pos_x = available_x + (available_width - final_width) / 2
    pos_y = available_y + (available_height - final_height) / 2

    return {"createImage": {"url": image_url, "elementProperties": {"pageObjectId": slide_id, "size": {"width": {"magnitude": final_width, "unit": "EMU"}, "height": {"magnitude": final_height, "unit": "EMU"}}, "transform": {"scaleX": 1, "scaleY": 1, "translateX": pos_x, "translateY": pos_y, "unit": "EMU"}}}}

def create_fullscreen_table(slide_id, table_data, page_elements, page_size):
    title_placeholder = next((el for el in page_elements if el.get('shape', {}).get('placeholder', {}).get('type') == 'TITLE'), None)
    top_margin = 360000 
    if title_placeholder:
        title_transform, title_size = title_placeholder.get('transform', {}), title_placeholder.get('size', {})
        top_margin = title_transform.get('translateY', 0) + title_size.get('height', {}).get('magnitude', 0) + 180000
    page_width, page_height = page_size['width']['magnitude'], page_size['height']['magnitude']
    available_width, available_height = page_width - (2 * 360000), page_height - top_margin - 360000
    rows, cols = len(table_data.get('rows', [])) + 1, len(table_data.get('headers', []))
    if not (rows > 1 and cols > 0): return []
    table_id = str(uuid.uuid4())
    requests = [{"createTable": {"objectId": table_id, "elementProperties": {"pageObjectId": slide_id, "size": {"width": {"magnitude": available_width, "unit": "EMU"}, "height": {"magnitude": available_height, "unit": "EMU"}}, "transform": {"scaleX": 1, "scaleY": 1, "translateX": 360000, "translateY": top_margin, "unit": "EMU"}}, "rows": rows, "columns": cols}}]
    for c, header in enumerate(table_data['headers']):
        requests.extend([{"insertText": {"objectId": table_id, "cellLocation": {"rowIndex": 0, "columnIndex": c}, "text": clean_text_content(header)}}, {"updateTextStyle": {"objectId": table_id, "cellLocation": {"rowIndex": 0, "columnIndex": c}, "style": {"bold": True}, "fields": "bold"}}])
    for r, row_data in enumerate(table_data['rows']):
        for c, cell_text in enumerate(row_data):
            requests.append({"insertText": {"objectId": table_id, "cellLocation": {"rowIndex": r + 1, "columnIndex": c}, "text": clean_text_content(str(cell_text))}})
    return requests

# --- Main Slide Creation Logic ---
def add_slide_to_presentation(slides_service, drive_service, s3_client, presentation_id, slide_index, slide_data, layout_map, class_to_layout_name_map, placeholder_map, page_size, globals_config):
    layout_class, layout_name = slide_data.get('layoutClass', 'default'), class_to_layout_name_map.get(slide_data.get('layoutClass', 'default'))
    if not (layout_id := layout_map.get(layout_name)): return

    slide_id = f"slide_{slide_index}_{uuid.uuid4()}"
    try:
        slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": [{"createSlide": {"objectId": slide_id, "slideLayoutReference": {"layoutId": layout_id}}}]}).execute()
        logging.info(f"  - Created slide {slide_index+1}/{slide_data.get('total_slides')} (class: {layout_class})")
    except HttpError as err:
        logging.error(f"  - Failed to create slide {slide_index+1}. Error: {err}")
        return

    page_elements = slides_service.presentations().pages().get(presentationId=presentation_id, pageObjectId=slide_id).execute().get('pageElements', [])
    
    placeholders = {p_type: [] for p_type in ['TITLE', 'SUBTITLE', 'BODY', 'PICTURE', 'FOOTER']}
    for el in page_elements:
        if ph := el.get('shape', {}).get('placeholder'):
            if (p_type := ph.get('type')) in placeholders:
                placeholders[p_type].append({'objectId': el.get('objectId'), 'transform': el.get('transform', {}), 'size': el.get('size', {})})
    
    if placeholders['SUBTITLE']:
        placeholders['SUBTITLE'].sort(key=lambda x: x['transform'].get('translateY', 0))

    content_requests, image_ref = [], slide_data.get("imageReference", {})
    image_ref["json_file_base"] = slide_data.get("json_file_base")
    body_placeholder_type = placeholder_map.get(layout_class, {}).get('body_placeholder', 'BODY')

    if 'title' in slide_data and placeholders['TITLE']:
        content_requests.append({"insertText": {"objectId": placeholders['TITLE'][0]['objectId'], "text": clean_text_content(slide_data['title'])}})

    if placeholders['SUBTITLE']:
        subs = placeholders['SUBTITLE']
        if slide_data.get('subtitle'):
            content_requests.append({"insertText": {"objectId": subs[0]['objectId'], "text": clean_text_content(slide_data['subtitle'])}})
        elif layout_class not in ['title', 'closing']:
            if globals_config.get('header') and len(subs) > 0: content_requests.append({"insertText": {"objectId": subs[0]['objectId'], "text": globals_config['header']}})
            footer_id = (placeholders.get('FOOTER') or [{}])[0].get('objectId') or (subs[-1]['objectId'] if len(subs) > 1 else None)
            if globals_config.get('footer') and footer_id: content_requests.append({"insertText": {"objectId": footer_id, "text": globals_config['footer']}})
    
    if layout_class == "image_fullscreen" and "imageReference" in slide_data:
        if img_req := create_image_on_slide(s3_client, slide_id, slide_index, image_ref, page_size, placeholders, 'fullscreen'): content_requests.append(img_req)
    elif layout_class == 'image_right':
        if 'body' in slide_data and placeholders.get(body_placeholder_type):
            rightmost_subtitle = sorted(placeholders[body_placeholder_type], key=lambda x: x['transform'].get('translateX', 0), reverse=True)[0]
            content_requests.extend(get_rich_text_requests(rightmost_subtitle['objectId'], slide_data['body']))
        if 'imageReference' in slide_data:
            if img_req := create_image_on_slide(s3_client, slide_id, slide_index, image_ref, page_size, placeholders, 'left_half'): content_requests.append(img_req)
    elif layout_class == "table_fullscreen" and 'table' in slide_data:
        content_requests.extend(create_fullscreen_table(slide_id, slide_data['table'], page_elements, page_size))
    else:
        if 'body' in slide_data and placeholders.get(body_placeholder_type) and placeholders[body_placeholder_type]:
            content_requests.extend(get_rich_text_requests(placeholders[body_placeholder_type][0]['objectId'], slide_data['body']))
            
    if 'speakerNotes' in slide_data:
        notes_page = slides_service.presentations().pages().get(presentationId=presentation_id, pageObjectId=slide_id).execute()
        if notes_id := notes_page.get('slideProperties', {}).get('notesPage', {}).get('notesProperties', {}).get('speakerNotesObjectId'):
            content_requests.append({"insertText": {"objectId": notes_id, "text": clean_text_content(slide_data['speakerNotes'])}})

    if content_requests:
        try: slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": content_requests}).execute()
        except HttpError as err: logging.error(f"  - Failed to populate slide {slide_index+1}. Error: {err}")

def main():
    logging.info("--- Initializing JSON to Slides Builder ---")
    
    slides_service, drive_service = authenticate_google()
    s3_client = get_s3_client()
    if not all([slides_service, drive_service, s3_client]): sys.exit(1)

    config = load_config()
    if not config: sys.exit(1)
    
    class_to_layout_name_map, placeholder_map, globals_config = config.get('layout_mapping', {}), config.get('placeholder_mapping', {}), config.get('globals', {})

    for json_file in glob.glob(os.path.join(SOURCE_DIRECTORY, '*.json')):
        logging.info(f"\n--- Processing file: {os.path.basename(json_file)} ---")
        try:
            with open(json_file, 'r', encoding='utf-8') as f: presentation_data = json.load(f)
            workshop_title, slides = presentation_data.get("workshopTitle", "Untitled"), presentation_data.get("slides", [])
            if not slides: continue

            globals_config['header'] = workshop_title
            presentation_id = copy_template_presentation(drive_service, f"Generated - {workshop_title}")
            if not presentation_id: raise Exception("Failed to copy template.")

            master_id, layout_map, page_size = get_theme_and_layouts(slides_service, presentation_id)
            if not master_id: raise Exception("Could not find target theme.")
            
            replace_master_slide_text(slides_service, presentation_id, master_id, globals_config)

            pres = slides_service.presentations().get(presentationId=presentation_id).execute()
            if slide_ids := [s['objectId'] for s in pres.get('slides', [])]:
                slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": [{"deleteObject": {"objectId": sid}} for sid in slide_ids]}).execute()
                logging.info(f"Removed {len(slide_ids)} template slides.")
            
            json_file_base = os.path.splitext(os.path.basename(json_file))[0]
            for i, slide_data in enumerate(slides):
                slide_data['total_slides'], slide_data['json_file_base'] = len(slides), json_file_base
                add_slide_to_presentation(slides_service, drive_service, s3_client, presentation_id, i, slide_data, layout_map, class_to_layout_name_map, placeholder_map, page_size, globals_config)

            logging.info(f"✅ Successfully created presentation: https://docs.google.com/presentation/d/{presentation_id}/")
        except Exception as e:
            logging.error(f"❌ An unexpected error occurred while processing {json_file}. Error: {e}", exc_info=True)

    logging.info("\n--- Batch Processing Complete ---")

if __name__ == "__main__":
    main()

