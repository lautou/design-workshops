import os
import sys
import logging
import json
import glob
import yaml
import re
import uuid
import time
from dotenv import load_dotenv
import fitz  # PyMuPDF

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
TABLE_HEIGHT_SAFETY_MARGIN_PERCENT = 0.05 # 5% margin to prevent overlap

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
def fit_table_to_area(slides_service, presentation_id, slide_id, table_id, target_width_emu, target_height_emu, start_font_pt=12):
    """
    Calculates the optimal font size for a table by estimating row wraps, then applies it in a single update.
    """
    MIN_FONT_PT = 8
    FONT_STEP = 1
    # Adjusted ratio for a more accurate height estimation per font point.
    FONT_HEIGHT_RATIO = 25500 
    # Average characters per line before wrapping. This is an estimate and may need tuning.
    CHARS_PER_LINE_ESTIMATE = 45 

    try:
        fields = 'pageElements(objectId,table(rows,columns,tableRows(tableCells(text))))'
        page = slides_service.presentations().pages().get(presentationId=presentation_id, pageObjectId=slide_id, fields=fields).execute()
        table_element = next((el for el in page.get('pageElements', []) if el.get('objectId') == table_id), None)
        
        if not table_element or not table_element.get('table'):
            logging.error(f"  - Could not find table '{table_id}' to start fitting process.")
            return

        table_info = table_element.get('table', {})
        num_rows = table_info.get('rows', 0)
        num_cols = table_info.get('columns', 0)
        table_rows = table_info.get('tableRows', [])

        non_empty_cells = [
            {"rowIndex": r, "columnIndex": c}
            for r, row in enumerate(table_rows)
            for c, cell in enumerate(row.get('tableCells', []))
            if cell.get('text', {}).get('textElements')
        ]
        
        # --- Pre-calculate estimated number of lines per row ---
        estimated_lines_per_row = []
        for r_idx, row in enumerate(table_rows):
            max_lines_in_row = 1
            for c_idx, cell in enumerate(row.get('tableCells', [])):
                text_content = ""
                text_elements = cell.get('text', {}).get('textElements', [])
                for elem in text_elements:
                    if 'textRun' in elem:
                        text_content += elem['textRun']['content']
                
                # Estimate lines based on character count
                lines_in_cell = max(1, len(text_content) // (CHARS_PER_LINE_ESTIMATE / num_cols))
                if lines_in_cell > max_lines_in_row:
                    max_lines_in_row = lines_in_cell
            estimated_lines_per_row.append(max_lines_in_row)

    except HttpError as e:
        logging.error(f"  - Failed to get initial table info for fitting. Error: {e}")
        return

    # --- Mathematical Calculation Loop with Wrapping Estimation ---
    final_font_pt = start_font_pt
    for font_pt in range(start_font_pt, MIN_FONT_PT - 1, -FONT_STEP):
        estimated_row_height = font_pt * FONT_HEIGHT_RATIO
        
        # Calculate total height based on estimated lines for each row
        estimated_total_height = sum(estimated_row_height * lines for lines in estimated_lines_per_row)
        
        logging.info(f"  - [Calc] Font: {font_pt}pt -> Estimated Weighted Height: {int(estimated_total_height)} EMU")
        
        if estimated_total_height <= target_height_emu:
            final_font_pt = font_pt
            logging.info(f"  - Found suitable font size based on wrapping estimation: {final_font_pt}pt.")
            break
        else:
            final_font_pt = MIN_FONT_PT

    # --- Apply the final calculated font size in a single batch ---
    requests = []
    for cell_loc in non_empty_cells:
        requests.append({"updateTextStyle": {
            "objectId": table_id,
            "style": {"fontSize": {"magnitude": final_font_pt, "unit": "PT"}},
            "fields": "fontSize",
            "cellLocation": cell_loc
        }})
    
    try:
        if requests:
            slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
            logging.info(f"  ✅ Successfully applied final font size of {final_font_pt}pt to table '{table_id}'.")
    except HttpError as e:
        logging.error(f"  - Failed to apply final font size. Error: {e}")


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
    if not isinstance(text, str):
        return text
    # This regex finds and removes all variations of [cite...] tags.
    return re.sub(r'\[cite.*?\]', '', text).strip()

def get_rich_text_requests(object_id, body_lines):
    requests, plain_text_lines, formatted_lines = [], [], []
    for line in body_lines:
        cleaned_line = clean_text_content(line)
        stripped = cleaned_line.lstrip()
        is_bullet = stripped.startswith('- ')
        text_for_fmt = stripped.lstrip('- ').strip()
        plain_text = text_for_fmt.replace('**', '')
        plain_text_lines.append(plain_text)
        formatted_lines.append({'text': plain_text, 'original': text_for_fmt, 'is_bullet': is_bullet, 'level': (len(cleaned_line) - len(stripped)) // 2})
    
    full_text = "\n".join(plain_text_lines)
    if not full_text: return []
    requests.append({"insertText": {"objectId": object_id, "text": full_text}})
    offset = 0
    for line_info in formatted_lines:
        line_text, original, is_bullet, level = line_info.values()
        line_end = offset + len(line_text)
        if is_bullet:
            requests.append({"createParagraphBullets": {"objectId": object_id, "textRange": {"type": "FIXED_RANGE", "startIndex": offset, "endIndex": line_end}}})
            if level > 0:
                requests.append({"updateParagraphStyle": {"objectId": object_id, "textRange": {"type": "FIXED_RANGE", "startIndex": offset, "endIndex": line_end}, "style": {"indentStart": {"magnitude": 18 * level, "unit": "PT"}}, "fields": "indentStart"}})
        for match in re.finditer(r'\*\*(.*?)\*\*', original):
            try:
                start = offset + line_text.index(match.group(1))
                requests.append({"updateTextStyle": {"objectId": object_id, "textRange": {"type": "FIXED_RANGE", "startIndex": start, "endIndex": start + len(match.group(1))}, "style": {"bold": True}, "fields": "bold"}})
            except ValueError: pass
        offset = line_end + 1
    return requests

# --- AWS S3 Image Upload ---
def upload_image_to_s3(s3_client, image_path, slide_index):
    try:
        object_name = f"presentations/{uuid.uuid4()}-{os.path.basename(image_path)}"
        s3_client.upload_file(image_path, S3_BUCKET_NAME, object_name, ExtraArgs={'ACL': 'public-read'})
        time.sleep(1) # Add a delay to allow for S3 object propagation
        return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{object_name}"
    except Exception as e:
        logging.error(f"  - Failed to upload image for slide {slide_index+1} to S3. Error: {e}")

# --- INTELLIGENT SIZING AND POSITIONING ---
def get_placeholder_bounds(placeholders):
    bounds = {}
    for p_type, p_list in placeholders.items():
        if p_list:
            # Sort by vertical position to correctly identify header/footer from multiple SUBTITLE placeholders
            p_list.sort(key=lambda p: p['transform'].get('translateY', 0))
            
            p = p_list[0] # Use the first element for the primary placeholder type
            transform = p.get('transform', {})
            size = p.get('size', {})
            scale_x = abs(transform.get('scaleX', 1.0))
            scale_y = abs(transform.get('scaleY', 1.0))
            effective_width = size.get('width', {}).get('magnitude', 0) * scale_x
            effective_height = size.get('height', {}).get('magnitude', 0) * scale_y
            x = transform.get('translateX', 0)
            y = transform.get('translateY', 0)
            bounds[p_type] = {'x': x, 'y': y, 'width': effective_width, 'height': effective_height}
            
            # Find HEADER and FOOTER from SUBTITLE placeholders if more than one exists
            if p_type == 'SUBTITLE' and len(p_list) > 1:
                header, footer = p_list[0], p_list[-1]
                
                header_transform = header.get('transform', {})
                header_size = header.get('size', {})
                header_scale_x = abs(header_transform.get('scaleX', 1.0)); header_scale_y = abs(header_transform.get('scaleY', 1.0))
                header_width = header_size.get('width', {}).get('magnitude', 0) * header_scale_x
                header_height = header_size.get('height', {}).get('magnitude', 0) * header_scale_y
                bounds['HEADER'] = {'x': header_transform.get('translateX', 0), 'y': header_transform.get('translateY', 0), 'width': header_width, 'height': header_height}

                footer_transform = footer.get('transform', {})
                footer_size = footer.get('size', {})
                footer_scale_x = abs(footer_transform.get('scaleX', 1.0)); footer_scale_y = abs(footer_transform.get('scaleY', 1.0))
                footer_width = footer_size.get('width', {}).get('magnitude', 0) * footer_scale_x
                footer_height = footer_size.get('height', {}).get('magnitude', 0) * footer_scale_y
                bounds['FOOTER'] = {'x': footer_transform.get('translateX', 0), 'y': footer_transform.get('translateY', 0), 'width': footer_width, 'height': footer_height}
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

    try:
        with fitz.open(image_path) as img_doc:
            img = img_doc[0]
            img_width, img_height = img.rect.width, img.rect.height
            img_aspect_ratio = img_width / img_height if img_height > 0 else 1
    except Exception as e:
        logging.error(f"  - Could not get image dimensions for {image_path}. Using default 4:3. Error: {e}")
        img_aspect_ratio = 4 / 3

    bounds = get_placeholder_bounds(placeholders)
    page_width, page_height = page_size['width']['magnitude'], page_size['height']['magnitude']

    if position == 'fullscreen':
        title_bottom = bounds.get('TITLE', {}).get('y', 0) + bounds.get('TITLE', {}).get('height', 0)
        footer_top = bounds.get('FOOTER', {}).get('y', page_height)
        
        available_height = footer_top - title_bottom
        logging.info(f"  - Calculated target area for '{position}' image: x=0, y={int(title_bottom)}, width={int(page_width)}, height={int(available_height)} (EMU)")
        final_height = available_height
        final_width = final_height * img_aspect_ratio

        if final_width > page_width:
            final_width = page_width
            final_height = final_width / img_aspect_ratio
        
        pos_x = (page_width - final_width) / 2
        pos_y = title_bottom
    else:  # left_half for image_right
        title_bottom = bounds.get('TITLE', {}).get('y', 0) + bounds.get('TITLE', {}).get('height', 0)
        
        main_content_subtitle = next((p for p in placeholders.get('SUBTITLE', []) if p['transform'].get('translateY', 0) > title_bottom), None)
        
        if main_content_subtitle:
             main_content_bounds = get_placeholder_bounds({'SUBTITLE': [main_content_subtitle]})['SUBTITLE']
        elif placeholders.get('BODY'):
             main_content_bounds = get_placeholder_bounds({'BODY': placeholders['BODY']})['BODY']
        else:
             main_content_bounds = {'x': 0, 'y': title_bottom, 'width': page_width, 'height': page_height - title_bottom}
        
        available_height = main_content_bounds['height']
        
        title_left = bounds.get('TITLE', {}).get('x', 0)
        main_content_left = main_content_bounds['x']
        available_width = main_content_left - title_left

        final_height = available_height
        logging.info(f"  - Calculated target area for '{position}' image: x={int(title_left)}, y={int(main_content_bounds['y'])}, width={int(available_width)}, height={int(available_height)} (EMU)")
        final_width = final_height * img_aspect_ratio
        
        if final_width > available_width:
            final_width = available_width
            final_height = final_width / img_aspect_ratio

        pos_x = title_left
        pos_y = main_content_bounds['y'] + (main_content_bounds['height'] - final_height) / 2

    logging.info(f"  - Calculated image properties: ratio={img_aspect_ratio:.2f}, width={int(final_width)}, height={int(final_height)}, x={int(pos_x)}, y={int(pos_y)}")
    return {"createImage": {"url": image_url, "elementProperties": {"pageObjectId": slide_id, "size": {"width": {"magnitude": int(final_width), "unit": "EMU"}, "height": {"magnitude": int(final_height), "unit": "EMU"}}, "transform": {"scaleX": 1, "scaleY": 1, "translateX": int(pos_x), "translateY": int(pos_y), "unit": "EMU"}}}}

def create_fullscreen_table(slide_id, table_data, page_size, target_width_emu, target_height_emu, top_y_offset):
    page_width = page_size['width']['magnitude']
    pos_x = (page_width - target_width_emu) / 2
    pos_y = top_y_offset

    rows, cols = len(table_data.get('rows', [])) + 1, len(table_data.get('headers', []))
    if not (rows > 1 and cols > 0): return [], None

    table_id = str(uuid.uuid4())
    requests = [{"createTable": {"objectId": table_id, "elementProperties": {"pageObjectId": slide_id, "size": {"width": {"magnitude": int(target_width_emu), "unit": "EMU"}, "height": {"magnitude": int(target_height_emu), "unit": "EMU"}}, "transform": {"scaleX": 1, "scaleY": 1, "translateX": int(pos_x), "translateY": int(pos_y), "unit": "EMU"}}, "rows": rows, "columns": cols}}]
    
    # Headers with conditional insert/style and font size
    for c, header in enumerate(table_data['headers']):
        header_text = clean_text_content(header)
        if header_text:
            requests.append({"insertText": {"objectId": table_id, "cellLocation": {"rowIndex": 0, "columnIndex": c}, "text": header_text}})
            requests.append({"updateTextStyle": {"objectId": table_id, "cellLocation": {"rowIndex": 0, "columnIndex": c}, "style": {"bold": True}, "fields": "bold"}})
    
    # Body cells
    for r, row_data in enumerate(table_data.get('rows', [])):
        for c, cell_text in enumerate(row_data):
            cell_text_clean = clean_text_content(str(cell_text))
            if cell_text_clean:
                requests.append({"insertText": {"objectId": table_id, "cellLocation": {"rowIndex": r + 1, "columnIndex": c}, "text": cell_text_clean}})
    
    # Set middle content alignment for all cells
    requests.append({
        "updateTableCellProperties": {
            "objectId": table_id, "tableCellProperties": {"contentAlignment": "MIDDLE"}, "fields": "contentAlignment",
            "tableRange": {"location": {"rowIndex": 0, "columnIndex": 0}, "rowSpan": rows, "columnSpan": cols}
        }
    })
    
    return requests, table_id

# --- Main Slide Creation Logic ---
def add_slide_to_presentation(slides_service, drive_service, s3_client, presentation_id, slide_index, slide_data, layout_map, class_to_layout_name_map, placeholder_map, page_size, globals_config, default_table_font_size=12):
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

    if layout_class in ['image_right', 'image_fullscreen', 'table_fullscreen']:
        # Detailed logging for placeholders on complex slides
        bounds_for_logging = get_placeholder_bounds(placeholders)
        for p_type, bound in bounds_for_logging.items():
            logging.info(f"  - Placeholder '{p_type}' bounds: "
                         f"x={int(bound['x'])}, y={int(bound['y'])}, "
                         f"width={int(bound['width'])}, height={int(bound['height'])}")

    content_requests, image_ref = [], slide_data.get("imageReference")
    if image_ref: image_ref["json_file_base"] = slide_data.get("json_file_base")
    body_placeholder_type = placeholder_map.get(layout_class, {}).get('body_placeholder', 'BODY')
    table_to_check = None

    if 'title' in slide_data and placeholders.get('TITLE'):
        content_requests.append({"insertText": {"objectId": placeholders['TITLE'][0]['objectId'], "text": clean_text_content(slide_data['title'])}})

    if placeholders.get('SUBTITLE'):
        placeholders['SUBTITLE'].sort(key=lambda x: x['transform'].get('translateY', 0))
        subs = placeholders['SUBTITLE']
        
        # Check if subtitle from JSON exists
        if slide_data.get('subtitle'):
            # The main subtitle is usually the one that is NOT a header or footer. Find it.
            title_bottom = get_placeholder_bounds(placeholders).get('TITLE', {}).get('y', 0)
            main_sub = next((s for s in subs if s['transform'].get('translateY', 0) > title_bottom), subs[0])
            content_requests.append({"insertText": {"objectId": main_sub['objectId'], "text": clean_text_content(slide_data['subtitle'])}})

        # Handle global header/footer, avoiding overwriting the main subtitle
        if layout_class not in ['title', 'closing']:
            if globals_config.get('header') and len(subs) > 0: content_requests.append({"insertText": {"objectId": subs[0]['objectId'], "text": globals_config['header']}})
            footer_id = (placeholders.get('FOOTER') or [{}])[0].get('objectId') or (subs[-1]['objectId'] if len(subs) > 1 else None)
            if globals_config.get('footer') and footer_id: content_requests.append({"insertText": {"objectId": footer_id, "text": globals_config['footer']}})
    
    if layout_class == 'columns':
        body_content = slide_data.get('body', [])
        bold_titles = [i for i, line in enumerate(body_content) if line.strip().startswith('**')]
        split_index = bold_titles[1] if len(bold_titles) > 1 else -1
        
        left_body, right_body = (body_content[:split_index], body_content[split_index:]) if split_index != -1 else (body_content, [])
        body_placeholders = sorted(placeholders.get('BODY', []), key=lambda p: p['transform'].get('translateX', 0))

        if len(body_placeholders) > 0 and left_body:
            content_requests.extend(get_rich_text_requests(body_placeholders[0]['objectId'], left_body))
        if len(body_placeholders) > 1 and right_body:
            content_requests.extend(get_rich_text_requests(body_placeholders[1]['objectId'], right_body))

    elif layout_class == "image_fullscreen" and image_ref:
        if img_req := create_image_on_slide(s3_client, slide_id, slide_index, image_ref, page_size, placeholders, 'fullscreen'): content_requests.append(img_req)
    elif layout_class == 'image_right':
        if 'body' in slide_data and placeholders.get(body_placeholder_type):
            rightmost_subtitle = sorted(placeholders[body_placeholder_type], key=lambda x: x['transform'].get('translateX', 0), reverse=True)[0]
            content_requests.extend(get_rich_text_requests(rightmost_subtitle['objectId'], slide_data['body']))
        if image_ref:
            if img_req := create_image_on_slide(s3_client, slide_id, slide_index, image_ref, page_size, placeholders, 'left_half'): content_requests.append(img_req)
    elif layout_class == "table_fullscreen" and 'table' in slide_data:
        bounds = get_placeholder_bounds(placeholders)
        page_width, page_height = page_size['width']['magnitude'], page_size['height']['magnitude']

        target_width_emu = page_width - (2 * 360000) # Standard side margins
        title_bounds = bounds.get('TITLE')
        footer_bounds = bounds.get('FOOTER')
        
        top_y_offset = 0; target_height_emu = page_height
        if title_bounds: top_y_offset = title_bounds.get('y', 0) + title_bounds.get('height', 0)
        if footer_bounds: target_height_emu = footer_bounds.get('y', page_height) - top_y_offset
        else: target_height_emu = page_height - top_y_offset # Fallback if no footer
        
        pos_x = (page_width - target_width_emu) / 2

        # Apply safety margin
        effective_target_height = target_height_emu * (1 - TABLE_HEIGHT_SAFETY_MARGIN_PERCENT)
        logging.info(f"  - Calculated target area for table: "
                     f"x={int(pos_x)}, y={int(top_y_offset)}, "
                     f"width={int(target_width_emu)}, height={int(target_height_emu)} (EMU)")
        logging.info(f"  - Applying {TABLE_HEIGHT_SAFETY_MARGIN_PERCENT*100}% safety margin. Effective height: {int(effective_target_height)} EMU")


        table_requests, table_id = create_fullscreen_table(slide_id, slide_data['table'], page_size, target_width_emu, effective_target_height, top_y_offset)
        if table_requests:
            content_requests.extend(table_requests)
            table_to_check = (slide_id, table_id, target_width_emu, effective_target_height, default_table_font_size)
    else:
        if 'body' in slide_data and placeholders.get(body_placeholder_type) and placeholders[body_placeholder_type]:
            content_requests.extend(get_rich_text_requests(placeholders[body_placeholder_type][0]['objectId'], slide_data['body']))
            
    if 'speakerNotes' in slide_data:
        notes_page = slides_service.presentations().pages().get(presentationId=presentation_id, pageObjectId=slide_id).execute()
        if notes_id := notes_page.get('slideProperties', {}).get('notesPage', {}).get('notesProperties', {}).get('speakerNotesObjectId'):
            content_requests.append({"insertText": {"objectId": notes_id, "text": clean_text_content(slide_data['speakerNotes'])}})

    if content_requests:
        try:
            slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": content_requests}).execute()
        except HttpError as err:
            logging.error(f"  - Failed to populate slide {slide_index+1}. Error: {err}")

    if table_to_check:
        s_id, t_id, target_w, target_h, start_font = table_to_check
        
        # Log initial table size before attempting to fit
        time.sleep(0.7) # Give API a moment to process creation
        try:
            fields = 'pageElements(objectId,table(tableRows(rowHeight),tableColumns(columnWidth)))'
            page = slides_service.presentations().pages().get(presentationId=presentation_id, pageObjectId=s_id, fields=fields).execute()
            table_element = next((el for el in page.get('pageElements', []) if el.get('objectId') == t_id), None)
            if table_element:
                table = table_element['table']
                width_emu = sum(col.get('columnWidth', {}).get('magnitude', 0) for col in table.get('tableColumns', []))
                
                height_emu = 0
                for i, row in enumerate(table.get('tableRows', [])):
                    row_height = row.get('rowHeight', {}).get('magnitude', 0)
                    logging.info(f"    - Initial Row {i+1} height: {row_height} EMU")
                    height_emu += row_height
                
                logging.info(f"  - Initial table size: width={int(width_emu)} EMU x height={int(height_emu)} EMU.")
                
                if height_emu > target_h or width_emu > target_w:
                    logging.info(f"  - Starting auto-fit for table '{t_id}' into target area: width={int(target_w)} EMU x height={int(target_h)} EMU.")
                    fit_table_to_area(slides_service, presentation_id, s_id, t_id, target_w, target_h, start_font)
                else:
                    logging.info("  - Table fits within target area. No auto-fitting needed.")

        except HttpError as e:
            logging.error(f"  - Could not get initial table size for fitting. Error: {e}")


def get_default_font_size(slides_service, presentation_id, layout_map, class_to_layout_name_map):
    """Creates a temporary slide to determine default table font size and returns it."""
    
    table_layout_name = class_to_layout_name_map.get('table_fullscreen')
    if not table_layout_name or not layout_map.get(table_layout_name):
        logging.warning("Could not find layout for 'table_fullscreen'. Skipping default font size check.")
        return 12 # Fallback font size

    logging.info("Determining default table font size via smoke test...")
    slide_id = f"temp_slide_{uuid.uuid4()}"
    table_id = f"temp_table_{uuid.uuid4()}"
    default_font_size = 12 # Fallback
    
    try:
        requests = [
            {"createSlide": {"objectId": slide_id, "slideLayoutReference": {"layoutId": layout_map[table_layout_name]}}},
            {"createTable": {"objectId": table_id, "elementProperties": {"pageObjectId": slide_id}, "rows": 1, "columns": 1}},
            {"insertText": {"objectId": table_id, "cellLocation": {"rowIndex": 0, "columnIndex": 0}, "text": "test"}}
        ]
        slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()

        fields = "pageElements(objectId,table(tableRows(tableCells(text(textElements(textRun(style(fontSize))))))))"
        page = slides_service.presentations().pages().get(presentationId=presentation_id, pageObjectId=slide_id, fields=fields).execute()
        table_element = next((el for el in page.get('pageElements', []) if el.get('objectId') == table_id), None)
        
        if table_element:
            cell = table_element.get('table', {}).get('tableRows', [{}])[0].get('tableCells', [{}])[0]
            text_element = cell.get('text', {})
            text_runs = [te.get('textRun') for te in text_element.get('textElements', []) if te.get('textRun')]
            if text_runs:
                font_size = text_runs[0].get('style', {}).get('fontSize', {}).get('magnitude')
                if font_size:
                    logging.info(f"✅ Default table font size detected: {font_size} PT")
                    default_font_size = font_size
    except Exception as e:
        logging.error(f"Could not determine default font size. Using fallback. Error: {e}")
    finally:
        try:
            slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": [{"deleteObject": {"objectId": slide_id}}]}).execute()
        except Exception as e:
            logging.warning(f"Could not delete temporary slide. Please remove it manually. Error: {e}")
            
    return default_font_size


def main():
    logging.info("--- Initializing JSON to Slides Builder ---")
    
    slides_service, drive_service = authenticate_google()
    s3_client = get_s3_client()
    if not all([slides_service, drive_service, s3_client]): sys.exit(1)

    config = load_config()
    if not config: sys.exit(1)
    
    class_to_layout_name_map, placeholder_map, globals_config = config.get('layout_mapping', {}), config.get('placeholder_mapping', {}), config.get('globals', {})
    default_table_font_size = 12

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

            if any(slide.get('layoutClass') == 'table_fullscreen' for slide in slides):
                default_table_font_size = get_default_font_size(slides_service, presentation_id, layout_map, class_to_layout_name_map)
            
            json_file_base = os.path.splitext(os.path.basename(json_file))[0]
            for i, slide_data in enumerate(slides):
                slide_data['total_slides'], slide_data['json_file_base'] = len(slides), json_file_base
                add_slide_to_presentation(slides_service, drive_service, s3_client, presentation_id, i, slide_data, layout_map, class_to_layout_name_map, placeholder_map, page_size, globals_config, default_table_font_size)

            logging.info(f"✅ Successfully created presentation: https://docs.google.com/presentation/d/{presentation_id}/")
        except Exception as e:
            logging.error(f"❌ An unexpected error occurred while processing {json_file}. Error: {e}", exc_info=True)

    logging.info("\n--- Batch Processing Complete ---")

if __name__ == "__main__":
    main()

