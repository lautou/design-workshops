import os
import sys
import logging
import re
import uuid
import glob
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from markdown_it import MarkdownIt

# --- 1. SCRIPT SETUP: LOGGING AND CONFIGURATION ---

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("generation.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

load_dotenv()

try:
    SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    TEMPLATE_ID = os.environ['TEMPLATE_PRESENTATION_ID']
    SHEET_ID = os.environ['LAYOUT_SHEET_ID']
    SOURCE_DIRECTORY = os.environ['SOURCE_DIRECTORY']
    OUTPUT_FOLDER_ID = os.environ['OUTPUT_FOLDER_ID']
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]


# --- 2. AUTHENTICATION & PRE-CHECKS ---

def authenticate():
    """Authenticates using the service account file specified in .env."""
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        slides_service = build("slides", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)
        sheets_service = build("sheets", "v4", credentials=creds)
        logging.info("✅ Successfully authenticated using service account.")
        return slides_service, drive_service, sheets_service
    except FileNotFoundError:
        logging.critical(f"FATAL: Service account key file not found at '{SERVICE_ACCOUNT_FILE}'")
    except Exception as e:
        logging.critical(f"FATAL: An unexpected error occurred during authentication: {e}")
    return None, None, None

def check_drive_folder_permissions(drive_service, folder_id):
    """Verifies that the service account can create files in the target folder."""
    try:
        logging.info(f"Verifying permissions for target folder ID: {folder_id}...")
        # Add supportsAllDrives=True to work with Shared Drives
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

def get_template_layouts(service, template_id):
    """Gets all layout names and IDs from the template presentation."""
    try:
        presentation = service.presentations().get(presentationId=template_id).execute()
        layouts = {
            layout.get("layoutProperties", {}).get("displayName"): layout.get("objectId")
            for layout in presentation.get("layouts", [])
            if layout.get("layoutProperties", {}).get("displayName")
        }
        logging.info("Fetched layouts from the template presentation.")
        return layouts
    except HttpError as err:
        logging.error(f"Could not fetch template presentation with ID '{template_id}': {err}"); return None

def load_layout_mapping_from_sheet(service, spreadsheet_id):
    """Loads the class-to-layout mapping from the first visible sheet in a Google Sheet."""
    try:
        spreadsheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = spreadsheet_metadata.get('sheets', '')
        if not sheets:
            logging.error(f"No sheets found in Google Sheet with ID '{spreadsheet_id}'.")
            return None
        
        first_sheet_name = sheets[0].get('properties', {}).get('title', 'Sheet1')
        logging.info(f"Found first sheet named '{first_sheet_name}'. Reading data from it.")
        
        sheet_range = f"'{first_sheet_name}'!A2:B"
        
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_range).execute()
        values = result.get('values', [])
        if not values:
            logging.warning(f"No data found in sheet '{first_sheet_name}'.")
            return {}
        mapping = {row[0].strip(): row[1].strip() for row in values if len(row) >= 2 and row[0].strip()}
        logging.info(f"Layout mapping loaded successfully.")
        return mapping
    except HttpError as err:
        logging.error(f"Failed to fetch layout mapping from Google Sheet '{spreadsheet_id}': {err}"); return None

def copy_template_presentation(drive_service, template_id, new_title, folder_id):
    """Copies the template to the specified output folder."""
    try:
        logging.info(f"Copying template to create new presentation '{new_title}'...")
        copy_body = {'name': new_title, 'parents': [folder_id]}
        # Add supportsAllDrives=True to work with Shared Drives
        copied_file = drive_service.files().copy(
            fileId=template_id, body=copy_body, supportsAllDrives=True
        ).execute()
        presentation_id = copied_file.get('id')
        logging.info(f"✅ Template copied successfully. New Presentation ID: {presentation_id}")
        return presentation_id
    except HttpError as err:
        logging.error(f"Failed to copy template presentation: {err}")
    return None

def preprocess_markdown(raw_markdown_content):
    """Cleans up the markdown content by removing custom citation tags using Unicode regex."""
    cite_start_regex = r'\u005B\u0063\u0069\u0074\u0065\u005F\u0073\u0074\u0061\u0072\u0074\u005D'
    content = re.sub(cite_start_regex, '', raw_markdown_content)
    cite_xx_regex = r'\u005B\u0063\u0069\u0074\u0065\u003A\u0020[\u0030-\u0039]+\u005D'
    content = re.sub(cite_xx_regex, '', content)
    return content

def parse_global_headers(raw_markdown_content):
    """Parses header and footer from the first _COMMENT_START_ block."""
    header_text, footer_text = "", ""
    first_comment_match = re.search(r'_COMMENT_START_(.*?)_COMMENT_END_', raw_markdown_content, re.DOTALL)
    if first_comment_match:
        comment_content = first_comment_match.group(1)
        header_match = re.search(r"header:\s*'(.*?)'", comment_content)
        footer_match = re.search(r"footer:\s*'(.*?)'", comment_content)
        if header_match:
            header_text = header_match.group(1).strip()
        if footer_match:
            footer_text = footer_match.group(1).strip()
    return header_text, footer_text

def parse_markdown_to_slides(processed_content):
    """Parses the markdown file content into a list of slide data objects."""
    slides_data = []
    content_without_header = re.sub(r'_COMMENT_START_(.*?)_COMMENT_END_', '', processed_content, count=1, flags=re.DOTALL)
    raw_slides = content_without_header.split("\n---\n")
    for slide_text in raw_slides:
        if not slide_text.strip(): continue
        speaker_notes, layout_class = "", "default"
        notes_match = re.search(r'_COMMENT_START_\s*Speaker notes:(.*?)_COMMENT_END_', slide_text, re.IGNORECASE | re.DOTALL)
        if notes_match:
            speaker_notes = notes_match.group(1).strip()
            slide_text = slide_text.replace(notes_match.group(0), "")
        class_match = re.search(r'_COMMENT_START_\s*_class:\s*([\w\s-]+)_COMMENT_END_', slide_text, re.IGNORECASE)
        if class_match:
            layout_class = class_match.group(1).strip().split()[0]
            slide_text = slide_text.replace(class_match.group(0), "")
        
        slide_content = re.sub(r'_COMMENT_START_.*?_COMMENT_END_', '', slide_text, flags=re.DOTALL).strip()
        slides_data.append({"content": slide_content, "notes": speaker_notes, "class": layout_class})
    logging.info(f"Markdown file parsed into {len(slides_data)} slides.")
    return slides_data

def populate_body_with_rich_text(service, presentation_id, body_id, markdown_text):
    """Parses markdown and applies rich text formatting to a placeholder."""
    if not markdown_text.strip():
        return

    md = MarkdownIt()
    tokens = md.parse(markdown_text)

    plain_text_parts = []
    formatting_styles = []
    list_requests = []
    
    char_cursor = 0
    style_stack = []

    for token in tokens:
        if token.type == 'paragraph_open':
            para_start = char_cursor
        elif token.type == 'inline':
            for child in token.children:
                if child.type == 'text':
                    plain_text_parts.append(child.content)
                    char_cursor += len(child.content)
                elif child.type in ['strong_open', 'em_open']:
                    style_stack.append({'type': child.type, 'start': char_cursor})
                elif child.type in ['strong_close', 'em_close']:
                    if not style_stack: continue
                    style = style_stack.pop()
                    formatting_styles.append({
                        'type': style['type'],
                        'range': (style['start'], char_cursor)
                    })
        elif token.type == 'paragraph_close':
            is_last_token = (token == tokens[-1])
            if not is_last_token and char_cursor > 0 and char_cursor > para_start:
                plain_text_parts.append('\n')
                char_cursor += 1
            
            if token.level > 0:
                end_index = char_cursor - 1 if not is_last_token else char_cursor
                list_requests.append({
                    "createParagraphBullets": {
                        "objectId": body_id,
                        "textRange": {"type": "FIXED_RANGE", "startIndex": para_start, "endIndex": end_index },
                        "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                        "nestingLevel": token.level - 1
                    }
                })

    plain_text = "".join(plain_text_parts)
    if not plain_text: return
    
    all_requests = [{"insertText": {"objectId": body_id, "text": plain_text}}]
    all_requests.extend(list_requests)

    for style in formatting_styles:
        style_update = {}
        if style['type'] == 'strong_open': style_update['bold'] = True
        if style['type'] == 'em_open': style_update['italic'] = True
        
        all_requests.append({
            "updateTextStyle": {
                "objectId": body_id,
                "textRange": {"type": "FIXED_RANGE", "startIndex": style['range'][0], "endIndex": style['range'][1]},
                "style": style_update,
                "fields": ",".join(style_update.keys())
            }
        })
    
    if len(all_requests) > 0:
        service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": all_requests}).execute()

def add_slide_to_presentation(service, presentation_id, slide_data, class_to_layout_map, template_layouts_map, header_text, footer_text):
    """Creates a slide and populates its placeholders with parsed content."""
    layout_class = slide_data['class']
    layout_name = class_to_layout_map.get(layout_class, class_to_layout_map.get('default'))
    layout_id = template_layouts_map.get(layout_name)
    if not layout_id:
        logging.warning(f"Layout '{layout_name}' for class '{layout_class}' not found. Using default.")

    slide_content = slide_data['content']
    title, body_text_md = "", ""
    lines = slide_content.split('\n')
    title_found = False
    for i, line in enumerate(lines):
        if line.strip().startswith("#"):
            title = line.lstrip('# ').strip()
            body_text_md = "\n".join(lines[i+1:]).strip()
            title_found = True
            break
    if not title_found:
        body_text_md = slide_content
    
    try:
        response = service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": [{"createSlide": {"objectId": str(uuid.uuid4()), "slideLayoutReference": {"layoutId": layout_id}}}]}
        ).execute()
        slide_info = response['replies'][0]['createSlide']
        
        text_requests, subtitle_placeholders, body_id = [], [], None
        
        for element in slide_info.get('pageElements', []):
            placeholder = element.get('shape', {}).get('placeholder', {})
            object_id = element.get('objectId')
            
            if placeholder.get('type') in ('TITLE', 'CENTERED_TITLE') and title:
                text_requests.append({"insertText": {"objectId": object_id, "text": title}})
            elif placeholder.get('type') == 'BODY':
                body_id = object_id
            elif placeholder.get('type') == 'SUBTITLE':
                subtitle_placeholders.append({'id': object_id, 'y': element.get('transform', {}).get('translateY', 0)})

        if len(subtitle_placeholders) >= 2:
            subtitle_placeholders.sort(key=lambda p: p['y'])
            if header_text: text_requests.append({"insertText": {"objectId": subtitle_placeholders[0]['id'], "text": header_text}})
            if footer_text: text_requests.append({"insertText": {"objectId": subtitle_placeholders[1]['id'], "text": footer_text}})
        elif len(subtitle_placeholders) == 1 and header_text:
            text_requests.append({"insertText": {"objectId": subtitle_placeholders[0]['id'], "text": header_text}})

        if slide_data['notes']:
            notes_page_id = slide_info.get("slideProperties", {}).get("notesPage", {}).get("notesProperties", {}).get("speakerNotesObjectId")
            if notes_page_id: text_requests.append({"insertText": {"objectId": notes_page_id, "text": slide_data['notes']}})
        
        if text_requests:
            service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": text_requests}).execute()

        if body_id and body_text_md:
            populate_body_with_rich_text(service, presentation_id, body_id, body_text_md)

    except HttpError as err:
        logging.error(f"An error occurred while adding a slide: {err}", exc_info=True)
    except (KeyError, IndexError) as e:
        logging.error(f"Could not parse response after creating slide: {e}", exc_info=True)


# --- 4. MAIN EXECUTION LOGIC ---

def main():
    """Main execution flow of the script."""
    logging.info("--- Initializing Script ---")
    
    slides_service, drive_service, sheets_service = authenticate()
    if not all([slides_service, drive_service, sheets_service]): sys.exit(1)

    if not check_drive_folder_permissions(drive_service, OUTPUT_FOLDER_ID): sys.exit(1)
        
    class_to_layout_map = load_layout_mapping_from_sheet(sheets_service, SHEET_ID)
    if class_to_layout_map is None: sys.exit(1)

    template_layouts_map = get_template_layouts(slides_service, TEMPLATE_ID)
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
            
            try:
                initial_slide_id = slides_service.presentations().get(presentationId=presentation_id).execute()['slides'][0]['objectId']
            except (HttpError, KeyError, IndexError):
                initial_slide_id = None

            for i, slide_data in enumerate(slides):
                logging.info(f"  - Creating slide {i+1}/{len(slides)} (class: {slide_data['class']})...")
                add_slide_to_presentation(slides_service, presentation_id, slide_data, class_to_layout_map, template_layouts_map, header_text, footer_text)
            
            if initial_slide_id:
                slides_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": [{"deleteObject": {"objectId": initial_slide_id}}]}).execute()
                logging.info("Removed initial template slide.")

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

