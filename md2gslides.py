import os
import sys
import logging
import re
import uuid
import glob
import yaml
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from markdown_it import MarkdownIt

# --- 1. SCRIPT SETUP: LOGGING AND CONFIGURATION ---

load_dotenv()

# Set up tunable logging
LOG_LEVEL_STR = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
log_level = LOG_LEVELS.get(LOG_LEVEL_STR, logging.INFO)

logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("generation.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

try:
    SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    TEMPLATE_ID = os.environ['TEMPLATE_PRESENTATION_ID']
    SOURCE_DIRECTORY = os.environ['SOURCE_DIRECTORY']
    OUTPUT_FOLDER_ID = os.environ['OUTPUT_FOLDER_ID']
    TARGET_THEME_NAME = os.environ['TARGET_THEME_NAME']
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]


# --- 2. AUTHENTICATION & PRE-CHECKS ---

def authenticate():
    """Authenticates using the service account file specified in .env."""
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        slides_service = build("slides", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)
        logging.info("✅ Successfully authenticated using service account.")
        return slides_service, drive_service
    except FileNotFoundError:
        logging.critical(f"FATAL: Service account key file not found at '{SERVICE_ACCOUNT_FILE}'")
    except Exception as e:
        logging.critical(f"FATAL: An unexpected error occurred during authentication: {e}")
    return None, None

def check_drive_folder_permissions(drive_service, folder_id):
    """Verifies that the service account can create files in the target folder."""
    try:
        logging.info(f"Verifying permissions for target folder ID: {folder_id}...")
        folder_metadata = drive_service.files().get(
            fileId=folder_id, fields='capabilities', supportsAllDrives=True
        ).execute()
        
        if folder_metadata.get('capabilities', {}).get('canAddChildren'):
            logging.info("✅ Permission check passed.")
            return True
        else:
            logging.critical("FATAL: Permission denied. Service account cannot create files in the target folder.")
            return False
    except HttpError as err:
        logging.critical(f"FATAL: API error checking folder permissions (ID: '{folder_id}'). Check the ID and sharing settings. Error: {err}")
        return False
    return True


# --- 3. CORE HELPER FUNCTIONS ---

def get_template_theme_info(service, template_id, target_theme_name):
    """
    Identifies the most-used master theme and returns its ID, a detailed layout map,
    and the presentation's page size.
    """
    try:
        presentation = service.presentations().get(presentationId=template_id).execute()
        
        page_size = presentation.get('pageSize')
        slides = presentation.get('slides', [])
        masters = presentation.get('masters', [])
        all_layouts = presentation.get('layouts', [])
        
        candidate_masters = [m for m in masters if m.get('masterProperties', {}).get('displayName') == target_theme_name]
        if not candidate_masters:
            logging.error(f"FATAL: No theme (master) named '{target_theme_name}' found.")
            return None, None, None

        logging.info(f"Found {len(candidate_masters)} master theme(s) named '{target_theme_name}'. Determining the most used one...")
        master_usage_count = {m.get('objectId'): 0 for m in candidate_masters}
        
        for slide in slides:
            layout_id = slide.get('slideProperties', {}).get('layoutObjectId')
            if not layout_id: continue
            parent_master_id = next((l.get('layoutProperties', {}).get('masterObjectId') for l in all_layouts if l.get('objectId') == layout_id), None)
            if parent_master_id in master_usage_count:
                master_usage_count[parent_master_id] += 1
        
        most_used_master_id = None
        if any(master_usage_count.values()):
             most_used_master_id = max(master_usage_count, key=master_usage_count.get)
        elif candidate_masters:
             most_used_master_id = candidate_masters[0].get('objectId')

        if not most_used_master_id:
            logging.error(f"Could not determine a primary master for theme '{target_theme_name}'.")
            return None, None, None

        logging.info(f"Selected master theme with ID: {most_used_master_id}.")
        
        final_layouts = {}
        for layout in all_layouts:
            if layout.get('layoutProperties', {}).get('masterObjectId') == most_used_master_id:
                display_name = layout.get('layoutProperties', {}).get('displayName')
                logging.debug(f"--- Inspecting Layout: '{display_name}' ---")
                layout_details = {'id': layout.get('objectId'), 'placeholders': {}}
                for element in layout.get('pageElements', []):
                    if 'placeholder' in element.get('shape', {}):
                        ph = element['shape']['placeholder']
                        ph_type = ph.get('type', 'BODY')
                        ph_index = ph.get('index', 0)
                        
                        logging.debug(f"  -> Found placeholder -> Type: {ph_type}, Index: {ph_index}")
                        
                        transform = element.get('transform', {})
                        x_pos = transform.get('translateX', 0)
                        y_pos = transform.get('translateY', 0)
                        height = element.get('size', {}).get('height', {}).get('magnitude', 0)

                        ph_details = {'id': element.get('objectId'), 'index': ph_index, 'type': ph_type, 'x': x_pos, 'y': y_pos, 'height': height}
                        
                        if ph_type not in layout_details['placeholders']:
                            layout_details['placeholders'][ph_type] = []
                        layout_details['placeholders'][ph_type].append(ph_details)
                
                if 'SUBTITLE' in layout_details['placeholders']:
                    layout_details['placeholders']['SUBTITLE'].sort(key=lambda p: p['y'])
                if 'BODY' in layout_details['placeholders']:
                    # Sort body placeholders by X position (left-to-right) for two-column layouts
                    layout_details['placeholders']['BODY'].sort(key=lambda p: p['x'])


                display_name = layout.get('layoutProperties', {}).get('displayName')
                if display_name:
                    final_layouts[display_name] = layout_details

        logging.info("Fetched and processed layouts from the selected master theme.")
        return most_used_master_id, final_layouts, page_size

    except HttpError as err:
        logging.error(f"Could not fetch and process template presentation: {err}")
        return None, None, None


def update_master_slide_text(service, presentation_id, master_id):
    """Finds and replaces specific text strings on the master slide."""
    try:
        logging.info(f"Checking master slide '{master_id}' for text to update...")
        replacements = {"CONFIDENTIAL designator": "CONFIDENTIAL", "V0000000": "V1.0"}
        update_requests = []
        for search_text, replace_text in replacements.items():
            update_requests.append({
                'replaceAllText': {
                    'replaceText': replace_text, 'pageObjectIds': [master_id],
                    'containsText': {'text': search_text, 'matchCase': False}
                }
            })
        
        if update_requests:
            service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": update_requests}).execute()
            logging.info("✅ Successfully updated text on the master slide.")
    except HttpError as err:
        logging.error(f"An error occurred while updating the master slide: {err}")

def load_layout_mapping_from_yaml(file_path="layouts.yaml"):
    try:
        with open(file_path, 'r') as f:
            mapping = yaml.safe_load(f)
            logging.info(f"Layout mapping loaded successfully from '{file_path}'.")
            return mapping
    except FileNotFoundError:
        logging.critical(f"FATAL: Layout mapping file not found at '{file_path}'. Please create it.")
    except yaml.YAMLError as e:
        logging.critical(f"FATAL: Error parsing YAML file '{file_path}': {e}")
    return None

def copy_template_presentation(drive_service, template_id, new_title, folder_id):
    try:
        logging.info(f"Copying template to create new presentation '{new_title}'...")
        copy_body = {'name': new_title, 'parents': [folder_id]}
        copied_file = drive_service.files().copy(
            fileId=template_id, body=copy_body, supportsAllDrives=True
        ).execute()
        return copied_file.get('id')
    except HttpError as err:
        logging.error(f"Failed to copy template presentation: {err}")
    return None

def preprocess_markdown(raw_markdown_content):
    cite_start_regex = r'\u005B\u0063\u0069\u0074\u0065\u005F\u0073\u0074\u0061\u0072\u0074\u005D'
    content = re.sub(cite_start_regex, '', raw_markdown_content)
    # Updated regex to handle multiple, comma-separated numbers. e.g., [cite: 70, 71]
    cite_xx_regex = r'\u005B\u0063\u0069\u0074\u0065\u003A\u0020[\u0030-\u0039]+(?:,\s*[\u0030-\u0039]+)*\u005D'
    content = re.sub(cite_xx_regex, '', content)
    return content

def parse_global_headers(raw_markdown_content):
    header_text, footer_text = "", ""
    first_comment_match = re.search(r'_COMMENT_START_(.*?)_COMMENT_END_', raw_markdown_content, re.DOTALL)
    if first_comment_match:
        comment_content = first_comment_match.group(1)
        header_match = re.search(r"header:\s*'(.*?)'", comment_content)
        footer_match = re.search(r"footer:\s*'(.*?)'", comment_content)
        if header_match: header_text = header_match.group(1).strip()
        if footer_match: footer_text = footer_match.group(1).strip()
    return header_text, footer_text

def parse_slide_content(slide_text):
    """
    Parses a slide's text into title, subtitle, body and table components.
    The first heading of any level (#, ##, ###) is considered the title.
    """
    title, subtitle, body, table = "", "", "", None
    lines = slide_text.strip().split('\n')
    
    body_lines = []
    table_lines = []
    is_table = False
    
    title_found = False
    
    # Find the first heading of any level to be the title
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if not title_found and stripped_line.startswith('#'):
            title = stripped_line.lstrip('# ').strip()
            title_found = True
            body_lines = lines[i+1:] # The rest of the lines become the body
            break
        elif not title_found:
             body_lines.append(line) # If no heading found yet, it's part of the body

    # If a title was found, process the rest for subtitles and body
    if title_found:
        subtitle_lines = []
        final_body_lines = []
        for body_line in body_lines:
            stripped_body_line = body_line.strip()
            # Only consider '##' as a subtitle, not '###' etc.
            if stripped_body_line.startswith('## '):
                 subtitle_lines.append(stripped_body_line.lstrip('## ').strip())
            # Table detection
            elif stripped_body_line.startswith('|') and stripped_body_line.endswith('|'):
                is_table = True
                table_lines.append(stripped_body_line)
            else:
                 final_body_lines.append(body_line)
        subtitle = "\n".join(subtitle_lines)
        body = "\n".join(final_body_lines).strip()
    else:
        # If no heading was found at all, check for a table in the body
        final_body_lines = []
        for line in body_lines:
            stripped_line = line.strip()
            if stripped_line.startswith('|') and stripped_line.endswith('|'):
                is_table = True
                table_lines.append(stripped_line)
            else:
                final_body_lines.append(line)
        body = "\n".join(final_body_lines).strip()

    if is_table:
        table_rows = []
        for line in table_lines:
            if not re.match(r'\|-*\|', line): # Skip separator line
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                table_rows.append(cells)
        if table_rows:
            table = table_rows

    return title, subtitle, body, table


def parse_markdown_to_slides(processed_content):
    """
    Parses the full markdown file content into a list of slide data dictionaries,
    correctly handling and removing Marpit front-matter.
    """
    slides_data = []
    
    # Remove the global header/footer comment block first
    content_without_globals = re.sub(r'_COMMENT_START_(.*?)_COMMENT_END_', '', processed_content, count=1, flags=re.DOTALL)
    
    # Remove the Marpit YAML front-matter
    content_without_marpit = re.sub(r'^\s*---\s*.*?---\s*', '', content_without_globals, flags=re.DOTALL).strip()
    
    raw_slides = content_without_marpit.split("\n---\n")
    
    for slide_text in raw_slides:
        if not slide_text.strip(): continue
        speaker_notes, layout_class = "", "default"
        notes_match = re.search(r'_COMMENT_START_\s*Speaker notes:(.*?)_COMMENT_END_', slide_text, re.IGNORECASE | re.DOTALL)
        if notes_match: speaker_notes = notes_match.group(1).strip(); slide_text = slide_text.replace(notes_match.group(0), "")
        class_match = re.search(r'_COMMENT_START_\s*_class:\s*([\w\s-]+)\\?_COMMENT_END_', slide_text, re.IGNORECASE)
        if class_match: layout_class = class_match.group(1).strip().split()[0]; slide_text = slide_text.replace(class_match.group(0), "")
        
        slide_content = re.sub(r'_COMMENT_START_.*?\\?_COMMENT_END_', '', slide_text, flags=re.DOTALL).strip()
        title, subtitle, body, table = parse_slide_content(slide_content)
        
        slides_data.append({
            "title": title, "subtitle": subtitle, "body": body, "table": table,
            "notes": speaker_notes, "class": layout_class
        })
    logging.info(f"Markdown file parsed into {len(slides_data)} slides.")
    return slides_data

def get_rich_text_requests(object_id, rich_text):
    """
    Generates a list of requests for populating a shape with richly formatted text.
    Does NOT execute the requests.
    """
    all_requests = []
    
    # --- Step 1: Prepare the text and metadata for each paragraph ---
    paragraph_metadata = []
    final_text_lines = []
    current_offset = 0

    lines = [line for line in rich_text.split('\n') if line.strip()]

    for line in lines:
        leading_spaces = len(line) - len(line.lstrip(' '))
        level = leading_spaces // 2
        
        content_part = line.lstrip(' ')
        is_list_item = False
        
        if re.match(r'^\d+\.\s', content_part):
            cleaned_content = re.sub(r'^\d+\.\s', '', content_part)
            is_list_item = True
        elif re.match(r'^[-*]\s', content_part):
            cleaned_content = re.sub(r'^[-*]\s', '', content_part)
            is_list_item = True
        else:
            cleaned_content = content_part

        plain_text, bold_ranges, italic_ranges = remove_formatting(cleaned_content)
        line_text_to_insert = ('\t' * level) + plain_text
        final_text_lines.append(line_text_to_insert)
        
        start_index = current_offset
        end_index = start_index + len(line_text_to_insert)
        
        tab_offset = len('\t' * level)
        adjusted_bold = [(start + tab_offset, end + tab_offset) for start, end in bold_ranges]
        adjusted_italic = [(start + tab_offset, end + tab_offset) for start, end in italic_ranges]

        paragraph_metadata.append({
            'is_list': is_list_item,
            'level': level,
            'range': (start_index, end_index),
            'bold_ranges': adjusted_bold,
            'italic_ranges': adjusted_italic
        })
        current_offset = end_index + 1

    # --- Step 2: Phase 1 - Insert Text and Apply Character Styles ---
    full_text = '\n'.join(final_text_lines)
    
    if full_text:
        all_requests.append({"insertText": {"objectId": object_id, "text": full_text}})

    for meta in paragraph_metadata:
        for start, end in meta['bold_ranges']:
            all_requests.append({
                "updateTextStyle": {
                    "objectId": object_id,
                    "textRange": {"type": "FIXED_RANGE", "startIndex": meta['range'][0] + start, "endIndex": meta['range'][0] + end},
                    "style": {"bold": True}, "fields": "bold"
                }
            })
        for start, end in meta['italic_ranges']:
            all_requests.append({
                "updateTextStyle": {
                    "objectId": object_id,
                    "textRange": {"type": "FIXED_RANGE", "startIndex": meta['range'][0] + start, "endIndex": meta['range'][0] + end},
                    "style": {"italic": True}, "fields": "italic"
                }
            })

    # --- Step 3: Phase 2 - Apply Bullets to Contiguous List Items ---
    i = 0
    while i < len(paragraph_metadata):
        if paragraph_metadata[i]['is_list']:
            list_block_start_index = paragraph_metadata[i]['range'][0]
            j = i
            while j < len(paragraph_metadata) and paragraph_metadata[j]['is_list']:
                list_block_end_index = paragraph_metadata[j]['range'][1]
                j += 1
            
            all_requests.append({
                "createParagraphBullets": {
                    "objectId": object_id,
                    "textRange": {
                        "type": "FIXED_RANGE",
                        "startIndex": list_block_start_index,
                        "endIndex": list_block_end_index
                    }
                }
            })
            i = j
        else:
            i += 1
    
    return all_requests


def remove_formatting(line):
    bold_ranges = []
    italic_ranges = []
    
    temp_plain = line
    temp_offset = 0
    
    bold_matches = list(re.finditer(r'\*\*(.*?)\*\*', temp_plain))
    for m in bold_matches:
        start_index = m.start() - temp_offset
        end_index = m.end() - temp_offset
        
        content_start = start_index 
        content_end = start_index + len(m.group(1))
        bold_ranges.append((content_start, content_end))
        
        temp_plain = temp_plain[:start_index] + m.group(1) + temp_plain[end_index:]
        
        removed_length = 4
        temp_offset += removed_length

    plain = temp_plain
    
    temp_plain = plain
    temp_offset = 0
    
    italic_matches = list(re.finditer(r'\*(.*?)\*', temp_plain))
    for m in italic_matches:
        start_index = m.start() - temp_offset
        end_index = m.end() - temp_offset

        content_start = start_index
        content_end = start_index + len(m.group(1))
        italic_ranges.append((content_start, content_end))
        
        temp_plain = temp_plain[:start_index] + m.group(1) + temp_plain[end_index:]
        
        removed_length = 2
        temp_offset += removed_length

    plain = temp_plain

    return plain, bold_ranges, italic_ranges

def add_slide_to_presentation(service, presentation_id, slide_data, class_to_layout_map, template_layouts_map, page_size, header_text, footer_text):
    """Creates a slide using placeholder mappings and populates it with parsed content."""
    layout_class = slide_data['class']
    layout_name = class_to_layout_map.get(layout_class, class_to_layout_map.get('default'))
    layout_details = template_layouts_map.get(layout_name)
    if not layout_details:
        logging.error(f"FATAL: Layout name '{layout_name}' for class '{layout_class}' not found. Check layouts.yaml.")
        raise Exception(f"Layout not found: {layout_name}")

    try:
        all_update_requests = []
        placeholder_mappings = []
        new_ids = {}
        assigned_placeholder_ids = set()
        layout_placeholders = layout_details.get('placeholders', {})
        
        part1_text = ""
        part2_text = ""
        
        logging.debug(f"Processing slide with layout '{layout_name}' (class: {layout_class})")
        
        all_subtitle_phs = list(layout_placeholders.get('SUBTITLE', []))
        
        header_ph, footer_ph = None, None
        main_subtitle_candidates = []
        
        logging.debug(f"  Layout '{layout_name}': Found {len(all_subtitle_phs)} SUBTITLE placeholder(s).")

        if len(all_subtitle_phs) >= 2:
            header_ph = all_subtitle_phs.pop(0)
            footer_ph = all_subtitle_phs.pop(-1)
            main_subtitle_candidates = all_subtitle_phs
            logging.debug(f"  -> Classified as Multi-Subtitle Layout. Header: {header_ph['id']}, Footer: {footer_ph['id']}")
        elif len(all_subtitle_phs) == 1:
            candidate = all_subtitle_phs[0]
            title_ph_list = (layout_placeholders.get('TITLE', []) or layout_placeholders.get('CENTERED_TITLE', []))
            title_y = title_ph_list[0]['y'] if title_ph_list else candidate['y'] + 1 
            
            logging.debug(f"  -> Single SUBTITLE candidate: id={candidate['id']}, y={candidate['y']}. Title y={title_y}")
            if candidate['y'] < title_y:
                header_ph = candidate
                logging.debug("     ...classified as HEADER (above title).")
            else:
                main_subtitle_candidates.append(candidate)
                logging.debug("     ...classified as MAIN CONTENT (below or at title level).")
        
        title_ph = (layout_placeholders.get('TITLE', []) or layout_placeholders.get('CENTERED_TITLE', []))
        body_phs = list(layout_placeholders.get('BODY', []))

        if title_ph and slide_data['title']:
            new_ids['title'] = str(uuid.uuid4())
            placeholder_mappings.append({'layoutPlaceholder': {'type': title_ph[0]['type'], 'index': title_ph[0]['index']}, 'objectId': new_ids['title']})

        if slide_data['subtitle'] and main_subtitle_candidates:
            subtitle_ph = main_subtitle_candidates.pop(0)
            new_ids['subtitle'] = str(uuid.uuid4())
            placeholder_mappings.append({'layoutPlaceholder': {'type': 'SUBTITLE', 'index': subtitle_ph['index']}, 'objectId': new_ids['subtitle']})
            assigned_placeholder_ids.add(subtitle_ph['id'])
            logging.debug(f"  -> Assigned slide subtitle to MAIN placeholder {subtitle_ph['id']}")

        if header_text and header_ph and header_ph['id'] not in assigned_placeholder_ids:
            new_ids['header'] = str(uuid.uuid4())
            placeholder_mappings.append({'layoutPlaceholder': {'type': 'SUBTITLE', 'index': header_ph['index']}, 'objectId': new_ids['header']})
            assigned_placeholder_ids.add(header_ph['id'])
            logging.debug(f"  -> Assigned global header to HEADER placeholder {header_ph['id']}")

        final_footer_text = footer_text if footer_text else "Red Hat Consulting"
        if final_footer_text and footer_ph and footer_ph['id'] not in assigned_placeholder_ids:
            new_ids['footer'] = str(uuid.uuid4())
            placeholder_mappings.append({'layoutPlaceholder': {'type': 'SUBTITLE', 'index': footer_ph['index']}, 'objectId': new_ids['footer']})
            assigned_placeholder_ids.add(footer_ph['id'])
            logging.debug(f"  -> Assigned global footer to FOOTER placeholder {footer_ph['id']}")
        
        if len(body_phs) == 2 and slide_data['body']:
            logging.debug("  -> Detected Two-Column Body Layout.")
            body_parts = re.split(r'(\n\s*\*\*.*?\*\*\s*\n)', slide_data['body'], maxsplit=1)
            
            if len(body_parts) >= 3:
                part1_text = body_parts[0].strip()
                part2_text = (body_parts[1] + body_parts[2]).strip()
                logging.debug(f"  -> Split body content into two columns.")
            else:
                part1_text = slide_data['body'].strip()
                logging.debug("  -> No splitter found, placing all body content in the left column.")
            
            new_ids['body1'] = str(uuid.uuid4())
            placeholder_mappings.append({'layoutPlaceholder': {'type': 'BODY', 'index': body_phs[0]['index']}, 'objectId': new_ids['body1']})
            
            new_ids['body2'] = str(uuid.uuid4())
            placeholder_mappings.append({'layoutPlaceholder': {'type': 'BODY', 'index': body_phs[1]['index']}, 'objectId': new_ids['body2']})
        
        # If there is body text (but no table), map the body placeholder.
        elif body_phs and slide_data['body'] and not slide_data['table']:
            new_ids['body1'] = str(uuid.uuid4())
            placeholder_mappings.append({'layoutPlaceholder': {'type': 'BODY', 'index': body_phs[0]['index']}, 'objectId': new_ids['body1']})
            part1_text = slide_data['body']
            logging.debug("  -> Assigned body text to single BODY placeholder.")
        # If there is a table, we don't map the body placeholder. The table will be created in its place.
        elif body_phs and slide_data['table']:
             logging.debug("  -> Found table content. Body placeholder will be used for table placement, not text.")
            
        elif not body_phs and slide_data['body'] and main_subtitle_candidates:
            body_fallback_ph = main_subtitle_candidates.pop(0)
            new_ids['body1'] = str(uuid.uuid4())
            placeholder_mappings.append({'layoutPlaceholder': {'type': 'SUBTITLE', 'index': body_fallback_ph['index']}, 'objectId': new_ids['body1']})
            assigned_placeholder_ids.add(body_fallback_ph['id'])
            part1_text = slide_data['body']
            logging.debug(f"  -> Assigned body to fallback MAIN placeholder {body_fallback_ph['id']}")
            logging.info(f"   -> No 'BODY' placeholder found, using a 'SUBTITLE' as fallback.")
            
        create_slide_request = {"createSlide": {"objectId": str(uuid.uuid4()), "slideLayoutReference": {"layoutId": layout_details['id']}, "placeholderIdMappings": placeholder_mappings}}
        response = service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": [create_slide_request]}).execute()
        new_slide_id = response['replies'][0]['createSlide']['objectId']

        if 'title' in new_ids and slide_data['title']: all_update_requests.append({"insertText": {"objectId": new_ids['title'], "text": slide_data['title']}})
        if 'subtitle' in new_ids and slide_data['subtitle']: all_update_requests.append({"insertText": {"objectId": new_ids['subtitle'], "text": slide_data['subtitle']}})
        if 'header' in new_ids and header_text: all_update_requests.append({"insertText": {"objectId": new_ids['header'], "text": header_text}})
        if 'footer' in new_ids: all_update_requests.append({"insertText": {"objectId": new_ids['footer'], "text": final_footer_text}})

        if 'body1' in new_ids and part1_text:
            all_update_requests.extend(get_rich_text_requests(new_ids['body1'], part1_text))
        if 'body2' in new_ids and part2_text:
            all_update_requests.extend(get_rich_text_requests(new_ids['body2'], part2_text))
            
        if slide_data['table']:
            table_id = str(uuid.uuid4())
            rows = len(slide_data['table'])
            cols = len(slide_data['table'][0])
            
            content_placeholder = None
            if body_phs:
                layout_page = service.presentations().pages().get(presentationId=TEMPLATE_ID, pageObjectId=layout_details['id']).execute()
                for element in layout_page.get('pageElements', []):
                    if 'placeholder' in element.get('shape', {}):
                        if element['shape']['placeholder'].get('type') == 'BODY' and element['shape']['placeholder'].get('index') == body_phs[0]['index']:
                            content_placeholder = element
                            break
            
            if not content_placeholder and main_subtitle_candidates:
                 layout_page = service.presentations().pages().get(presentationId=TEMPLATE_ID, pageObjectId=layout_details['id']).execute()
                 for element in layout_page.get('pageElements', []):
                    if 'placeholder' in element.get('shape', {}):
                        if element['shape']['placeholder'].get('type') == 'SUBTITLE' and element['shape']['placeholder'].get('index') == main_subtitle_candidates[0]['index']:
                            content_placeholder = element
                            break
            
            # --- 1. Calculate Table and Column Widths ---
            if content_placeholder:
                table_width = content_placeholder['size']['width']['magnitude']
            else:
                table_width = page_size['width']['magnitude'] * 0.9

            max_chars_per_column = [0] * cols
            for row in slide_data['table']:
                for i, cell in enumerate(row):
                    if len(cell) > max_chars_per_column[i]:
                        max_chars_per_column[i] = len(cell)
            
            total_chars = sum(max_chars_per_column)
            column_widths = [int((1/cols) * table_width)] * cols
            if total_chars > 0:
                column_widths = [int((max_chars / total_chars) * table_width) for max_chars in max_chars_per_column]
            
            # --- 2. Estimate Table Height and Adjust Font Size ---
            font_size = 10  # Start with a default font size
            table_height = 0

            while font_size > 5: # Minimum font size of 5
                table_height = 0
                base_row_height_emu = int(font_size * 20000)
                extra_line_height_emu = int(font_size * 15000)
                
                for row_idx, row in enumerate(slide_data['table']):
                    max_lines_in_row = 1
                    for col_idx, cell in enumerate(row):
                        plain_text, _, _ = remove_formatting(cell)
                        col_width_emu = column_widths[col_idx]
                        chars_per_line = (col_width_emu / 1000000) * (28 - font_size) if col_width_emu > 0 else 1
                        
                        lines_for_cell = 1
                        if chars_per_line > 0:
                            lines_for_cell = -(-len(plain_text) // chars_per_line) if len(plain_text) > 0 else 1
                        
                        if lines_for_cell > max_lines_in_row:
                            max_lines_in_row = lines_for_cell
                    
                    table_height += base_row_height_emu + ((max_lines_in_row - 1) * extra_line_height_emu)

                if content_placeholder and table_height > content_placeholder['size']['height']['magnitude']:
                    font_size -= 1
                else:
                    break

            logging.debug(f"  -> Final Font Size: {font_size}pt, Estimated Table Height: {table_height} EMU")
            
            # --- 3. Calculate Centered Position and Define Element Properties ---
            if content_placeholder and 'transform' in content_placeholder:
                placeholder_width = content_placeholder['size']['width']['magnitude']
                placeholder_height = content_placeholder['size']['height']['magnitude']
                placeholder_translate_x = content_placeholder['transform']['translateX']
                placeholder_translate_y = content_placeholder['transform']['translateY']

                logging.debug(f"  -> Content Placeholder Coords: X={placeholder_translate_x}, Y={placeholder_translate_y}, W={placeholder_width}, H={placeholder_height}")

                centered_translateX = placeholder_translate_x + (placeholder_width - table_width) / 2
                centered_translateY = placeholder_translate_y + (placeholder_height - table_height) / 2

                if centered_translateY < placeholder_translate_y:
                    centered_translateY = placeholder_translate_y

                logging.debug(f"  -> Calculated Table Coords: X={int(centered_translateX)}, Y={int(centered_translateY)}, W={table_width}, H={table_height}")

                transform = {
                    'scaleX': 1, 'scaleY': 1,
                    'translateX': centered_translateX,
                    'translateY': centered_translateY,
                    'unit': 'EMU'
                }
                
                element_properties = {
                    'pageObjectId': new_slide_id,
                    'size': { 'width': {'magnitude': table_width, 'unit': 'EMU'}, 'height': {'magnitude': table_height, 'unit': 'EMU'} },
                    'transform': transform
                }
            else:
                centered_translateX = (page_size['width']['magnitude'] - table_width) / 2
                element_properties = {
                    'pageObjectId': new_slide_id,
                    'size': { 'height': {'magnitude': table_height, 'unit': 'EMU'}, 'width': {'magnitude': table_width, 'unit': 'EMU'}},
                    'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': centered_translateX, 'translateY': 1000000, 'unit': 'EMU'}
                }

            # --- 4. Build Requests ---
            all_update_requests.append({
                'createTable': {
                    'objectId': table_id,
                    'elementProperties': element_properties,
                    'rows': rows,
                    'columns': cols
                }
            })
            
            for i, width in enumerate(column_widths):
                all_update_requests.append({
                    'updateTableColumnProperties': {
                        'objectId': table_id,
                        'columnIndices': [i],
                        'tableColumnProperties': {
                            'columnWidth': {
                                'magnitude': width,
                                'unit': 'EMU'
                            }
                        },
                        'fields': 'columnWidth'
                    }
                })

            for row_idx, row in enumerate(slide_data['table']):
                for col_idx, cell in enumerate(row):
                    plain_text, bold_ranges, _ = remove_formatting(cell)
                    
                    # Only add requests if there is text to prevent styling empty cells
                    if plain_text:
                        all_update_requests.extend([{
                            'insertText': {
                                'objectId': table_id,
                                'cellLocation': {'rowIndex': row_idx, 'columnIndex': col_idx},
                                'text': plain_text
                            }},{
                            'updateTextStyle': {
                                'objectId': table_id,
                                'cellLocation': {'rowIndex': row_idx, 'columnIndex': col_idx},
                                'style': {'fontSize': {'magnitude': font_size, 'unit': 'PT'}},
                                'fields': 'fontSize'
                            }
                        }])
                        if bold_ranges:
                            all_update_requests.append({
                                'updateTextStyle': {
                                    'objectId': table_id,
                                    'cellLocation': {'rowIndex': row_idx, 'columnIndex': col_idx},
                                    'style': {'bold': True},
                                    'fields': 'bold'
                                }
                            })


        if slide_data['notes']:
            slide_page = service.presentations().pages().get(presentationId=presentation_id, pageObjectId=new_slide_id).execute()
            notes_page_props = slide_page.get('slideProperties', {}).get('notesPage', {})
            if notes_page_props:
                notes_properties = notes_page_props.get('notesProperties', {})
                speaker_notes_object_id = notes_properties.get('speakerNotesObjectId')
                if speaker_notes_object_id:
                    cleaned_notes = preprocess_markdown(slide_data['notes'])
                    all_update_requests.extend(get_rich_text_requests(speaker_notes_object_id, cleaned_notes))

        if all_update_requests:
            service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": all_update_requests}).execute()
        
        if not ('body1' in new_ids or 'body2' in new_ids or slide_data['table']) and slide_data['body']:
             logging.warning(f"   -> No suitable placeholder found for body content on slide with class '{layout_class}'. Body was not inserted.")

    except HttpError as err:
        logging.error(f"An error occurred while adding a slide: {err}", exc_info=True)
    except Exception as e:
        logging.error(f"An unexpected error occurred in add_slide_to_presentation: {e}", exc_info=True)


# --- 4. MAIN EXECUTION LOGIC ---

def main():
    """Main execution flow of the script."""
    logging.info("--- Initializing Script ---")
    
    slides_service, drive_service = authenticate()
    if not all([slides_service, drive_service]): sys.exit(1)

    if not check_drive_folder_permissions(drive_service, OUTPUT_FOLDER_ID): sys.exit(1)
        
    class_to_layout_map = load_layout_mapping_from_yaml()
    if class_to_layout_map is None: sys.exit(1)

    most_used_master_id, template_layouts_map, page_size = get_template_theme_info(slides_service, TEMPLATE_ID, TARGET_THEME_NAME)
    if not template_layouts_map: sys.exit(1)

    if not os.path.isdir(SOURCE_DIRECTORY):
        logging.critical(f"FATAL: Source directory not found at '{SOURCE_DIRECTORY}'"); sys.exit(1)
        
    markdown_files = glob.glob(os.path.join(SOURCE_DIRECTORY, '*.md'))
    if not markdown_files:
        logging.warning(f"No markdown (.md) files found in '{SOURCE_DIRECTORY}'. Exiting."); sys.exit(0)

    logging.info(f"Found {len(markdown_files)} markdown file(s) to process.")
    success_count, failure_count = 0, 0

    for md_file_path in markdown_files:
        logging.info(f"\n--- Processing file: {os.path.basename(md_file_path)} ---")
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                raw_markdown = f.read()
            
            processed_markdown = preprocess_markdown(raw_markdown)
            header_text, footer_text = parse_global_headers(processed_markdown)
            
            slides = parse_markdown_to_slides(processed_markdown)
            if not slides:
                logging.warning("No slides found in this file. Skipping."); continue

            new_title = os.path.splitext(os.path.basename(md_file_path))[0]
            presentation_id = copy_template_presentation(drive_service, TEMPLATE_ID, f"Generated - {new_title}", OUTPUT_FOLDER_ID)
            if not presentation_id:
                raise Exception("Failed to copy template and create new presentation.")
            
            if most_used_master_id:
                update_master_slide_text(slides_service, presentation_id, most_used_master_id)
            
            initial_slide_ids = []
            try:
                presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
                initial_slide_ids = [slide.get('objectId') for slide in presentation.get('slides', [])]
            except HttpError as e:
                logging.warning(f"Could not get initial slide IDs to delete. Error: {e}")

            for i, slide_data in enumerate(slides):
                logging.info(f"  - Creating slide {i+1}/{len(slides)} (class: {slide_data['class']})...")
                add_slide_to_presentation(slides_service, presentation_id, slide_data, class_to_layout_map, template_layouts_map, page_size, header_text, footer_text)
            
            if initial_slide_ids:
                logging.info(f"Removing {len(initial_slide_ids)} slides that came from the template...")
                try:
                    delete_requests = [{"deleteObject": {"objectId": slide_id}} for slide_id in initial_slide_ids]
                    slides_service.presentations().batchUpdate(
                        presentationId=presentation_id,
                        body={"requests": delete_requests}
                    ).execute()
                    logging.info("Removed all initial template slides.")
                except HttpError as err:
                    logging.warning(f"Could not remove all initial template slides. They may need to be removed manually. Error: {err}")

            presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/"
            logging.info(f"✅ Successfully finished processing {os.path.basename(md_file_path)}")
            logging.info(f"   View presentation here: {presentation_url}")
            success_count += 1

        except Exception as e:
            logging.error(f"❌ Failed to process file {os.path.basename(md_file_path)}. Error: {e}", exc_info=True)
            failure_count += 1
            continue

    logging.info("\n--- Batch Processing Complete ---")
    logging.info(f"Summary: {success_count} succeeded, {failure_count} failed.")

if __name__ == "__main__":
    main()



