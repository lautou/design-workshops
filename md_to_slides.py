import re
import os.path
import argparse
from collections import Counter
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def select_main_theme(service, pres_id):
    presentation = service.presentations().get(presentationId=pres_id, fields='slides,masters').execute()
    slides = presentation.get('slides', [])
    masters = presentation.get('masters', [])
    if not masters: return None, None
    master_usage_count = Counter(slide['slideProperties'].get('masterObjectId') for slide in slides)
    light_themes = [m for m in masters if m.get('masterProperties', {}).get('displayName') == 'Red Hat - Light']
    if not light_themes:
        print("Warning: No theme named 'Red Hat - Light' found. Using the first available theme as a fallback.")
        return masters[0]['objectId'], slides
    main_theme_obj = max(light_themes, key=lambda m: master_usage_count.get(m['objectId'], 0))
    main_theme_id = main_theme_obj['objectId']
    usage = master_usage_count.get(main_theme_id, 0)
    print(f"Selected theme: 'Red Hat - Light' (ID: {main_theme_id}) used by {usage} slides.")
    return main_theme_id, slides

def update_master_placeholders(service, pres_id, master_id):
    print("Updating master slide text boxes (Version and Confidential)...")
    requests = [
        {'replaceAllText': {'replaceText': 'CONFIDENTIAL', 'pageObjectIds': [master_id], 'containsText': {'text': 'CONFIDENTIAL designator', 'matchCase': False}}},
        {'replaceAllText': {'replaceText': 'V0.1', 'pageObjectIds': [master_id], 'containsText': {'text': 'V0000000', 'matchCase': False}}}
    ]
    service.presentations().batchUpdate(presentationId=pres_id, body={'requests': requests}).execute()
    print("...Done.")

def get_layout_details(service, pres_id, master_id, layout_name):
    print(f"Finding details for '{layout_name}' layout...")
    presentation = service.presentations().get(presentationId=pres_id, fields='layouts').execute()
    layouts = presentation.get('layouts', [])
    
    target_layout = next((l for l in layouts if l.get('layoutProperties', {}).get('masterObjectId') == master_id and l.get('layoutProperties', {}).get('displayName') == layout_name), None)

    if not target_layout:
        print(f"Error: Could not find layout '{layout_name}' in the selected theme.")
        return None

    details = {
        'objectId': target_layout['objectId'],
        'placeholders': []
    }

    for element in target_layout.get('pageElements', []):
        if 'placeholder' in element.get('shape', {}):
            ph = element['shape']['placeholder']
            details['placeholders'].append({
                'objectId': element['objectId'],
                'type': ph.get('type'),
                'index': ph.get('index')
            })

    print("...Found layout successfully.")
    return details


def parse_md(md_file):
    with open(md_file, 'r', encoding='utf-8') as f: content = f.read()
    slides = re.split(r'^---$', content, flags=re.MULTILINE)
    parsed = []
    for slide in slides:
        slide = slide.strip()
        if not slide: continue
        notes_match = re.search(r'::: notes\s*\n(.*?)\n:::', slide, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else ''
        slide = slide.replace(notes_match.group(0), '').strip() if notes_match else slide
        lines = slide.split('\n')
        
        title = ""
        header1 = ""
        body_lines = []
        
        h1_found = False
        h2_found = False
        for line in lines:
            if line.startswith('##') and not h2_found:
                title = line.replace('##', '').strip()
                h2_found = True
            elif line.startswith('#') and not line.startswith('##') and not h1_found:
                header1 = line.replace('#', '').strip()
                h1_found = True
            else:
                body_lines.append(line)
        
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
        while body_lines and not body_lines[-1].strip():
            body_lines.pop()
        parsed.append({'title': title, 'header1': header1, 'content_lines': body_lines, 'notes': notes})
    return parsed

def create_slide(service, pres_id, slide_data, layout_details, master_id, insertion_index):
    """Creates a slide, populates it, and correctly formats bullet points and other styling."""

    # 1. CREATE THE SLIDE
    create_slide_req = [{'createSlide': {
        'insertionIndex': insertion_index,
        'slideLayoutReference': {'layoutId': layout_details['objectId']}
    }}]
    response = service.presentations().batchUpdate(presentationId=pres_id, body={'requests': create_slide_req}).execute()
    slide_id = response['replies'][0]['createSlide']['objectId']
    page = service.presentations().pages().get(presentationId=pres_id, pageObjectId=slide_id).execute()

    # 2. FIND PLACEHOLDER IDs
    notes_page = page.get('slideProperties', {}).get('notesPage', {})
    speaker_notes_object_id = notes_page.get('notesProperties', {}).get('speakerNotesObjectId')
    def find_placeholder_in_page(page_obj, placeholder_type):
        for el in page_obj.get('pageElements', []):
            ph = el.get('shape', {}).get('placeholder', {})
            if ph and ph.get('type') == placeholder_type:
                return el['objectId']
        return None
    title_placeholder_id = find_placeholder_in_page(page, 'TITLE')
    body_placeholder_id = find_placeholder_in_page(page, 'BODY')
    subtitle_placeholders = sorted([el for el in page.get('pageElements', []) if el.get('shape', {}).get('placeholder', {}).get('type') == 'SUBTITLE'], key=lambda x: x['transform']['translateY'])
    header_placeholder_id = subtitle_placeholders[0]['objectId'] if len(subtitle_placeholders) > 0 else None
    footer_placeholder_id = subtitle_placeholders[1]['objectId'] if len(subtitle_placeholders) > 1 else None

    # --- First Pass: Insert all text ---
    text_insertion_requests = []
    if slide_data['title'] and title_placeholder_id:
        text_insertion_requests.append({'insertText': {'objectId': title_placeholder_id, 'text': slide_data['title']}})
    
    header_text = slide_data['header1'] if slide_data['header1'] else 'Red Hat OpenShift Container Platform'
    if header_placeholder_id:
        text_insertion_requests.append({'insertText': {'objectId': header_placeholder_id, 'text': header_text}})
    
    if footer_placeholder_id:
        text_insertion_requests.append({'insertText': {'objectId': footer_placeholder_id, 'text': 'Red Hat Consulting'}})
    
    # Execute title/header/footer insertion first
    if text_insertion_requests:
        service.presentations().batchUpdate(presentationId=pres_id, body={'requests': text_insertion_requests}).execute()

    if slide_data['content_lines'] and body_placeholder_id:
        # Filter out any lines that are empty or contain only whitespace
        processed_content_lines = [line for line in slide_data['content_lines'] if line.strip()]

        full_text_lines = []
        bold_spans = []
        bullet_ranges = []
        
        current_cursor = 0
        in_list = False
        list_start_index = -1

        for i, line in enumerate(processed_content_lines):
            line_is_bullet = line.lstrip().startswith('* ')
            indent_level = (len(line) - len(line.lstrip(' '))) // 4
            
            # Remove markdown characters to get the clean text for insertion
            clean_line = line.lstrip()[2:] if line_is_bullet else line
            
            # Handle bold formatting
            processed_line = ""
            last_end = 0
            for match in re.finditer(r'\*\*(.*?)\*\*', clean_line):
                start, end = match.start(), match.end()
                bold_text = match.group(1)
                
                processed_line += clean_line[last_end:start]
                bold_start_in_line = len(processed_line)
                processed_line += bold_text
                
                # Calculate span relative to the whole text body
                span_start = current_cursor + bold_start_in_line
                bold_spans.append({'start': span_start, 'end': span_start + len(bold_text)})
                last_end = end
            processed_line += clean_line[last_end:]

            final_line = ('\t' * indent_level) + processed_line
            full_text_lines.append(final_line)

            # --- Logic for tracking bulleted list ranges ---
            if line_is_bullet and not in_list:
                in_list = True
                list_start_index = current_cursor
            elif not line_is_bullet and in_list:
                in_list = False
                bullet_ranges.append({'start': list_start_index, 'end': current_cursor})
                list_start_index = -1
            
            # Move cursor forward by length of the final line 
            current_cursor += len(final_line)
            # Add 1 for \n if not the last line
            if i < len(processed_content_lines) - 1:
                current_cursor += 1

        # If the presentation ends with a list, close the final range
        if in_list:
            bullet_ranges.append({'start': list_start_index, 'end': current_cursor})

        # Insert the full, processed body text
        full_text = '\n'.join(full_text_lines)
        if full_text:
            service.presentations().batchUpdate(presentationId=pres_id, body={'requests': [
                {'insertText': {'objectId': body_placeholder_id, 'text': full_text}}
            ]}).execute()

            # --- Second Pass: Apply formatting based on calculated ranges ---
            formatting_requests = []
            for brange in bullet_ranges:
                formatting_requests.append({'createParagraphBullets': {
                    'objectId': body_placeholder_id,
                    'textRange': {'type': 'FIXED_RANGE', 'startIndex': brange['start'], 'endIndex': brange['end']}
                }})

            for span in bold_spans:
                formatting_requests.append({'updateTextStyle': {
                    'objectId': body_placeholder_id,
                    'style': {'bold': True},
                    'fields': 'bold',
                    'textRange': {'type': 'FIXED_RANGE', 'startIndex': span['start'], 'endIndex': span['end']}
                }})
            
            if formatting_requests:
                service.presentations().batchUpdate(presentationId=pres_id, body={'requests': formatting_requests}).execute()
                
    # Insert speaker notes if available
    if slide_data['notes'] and speaker_notes_object_id:
        service.presentations().batchUpdate(presentationId=pres_id, body={'requests': [
            {'insertText': {'objectId': speaker_notes_object_id, 'text': slide_data['notes']}}
        ]}).execute()
                
def main(md_file, title, template_id=None):
    creds = get_credentials()
    service_drive = build('drive', 'v3', credentials=creds)
    service_slides = build('slides', 'v1', credentials=creds)

    print("Step 1: Copying template presentation...")
    new_pres = service_drive.files().copy(fileId=template_id, body={'name': title}).execute()
    pres_id = new_pres.get('id')
    print(f'Created presentation: https://docs.google.com/presentation/d/{pres_id}/edit')
    
    original_slide_ids = [s['objectId'] for s in service_slides.presentations().get(presentationId=pres_id, fields='slides.objectId').execute().get('slides', [])]

    print("\nStep 2 & 3: Selecting the main theme...")
    main_theme_id, all_slides = select_main_theme(service_slides, pres_id)
    if not main_theme_id: return

    print("\nStep 4: Updating master slide for the selected theme...")
    update_master_placeholders(service_slides, pres_id, main_theme_id)

    print("\nStep 5: Finding layout and placeholder details...")
    layout_details = get_layout_details(service_slides, pres_id, main_theme_id, 'Interior title and body')
    if not layout_details: return
    
    print("\nStep 6: Generating new slides from markdown file...")
    insertion_index = 0
    for i, slide in enumerate(all_slides):
        if slide.get('slideProperties', {}).get('masterObjectId') == main_theme_id:
            insertion_index = i + 1
            break
    
    parsed_slides = parse_md(md_file)

    main_header = parsed_slides[0].get('header1') if parsed_slides else ''

    for i, slide_data in enumerate(parsed_slides):
        print(f"  - Creating slide {i+1}: {slide_data['title']}")

        if not slide_data.get('header1') and main_header:
          slide_data['header1'] = main_header
        create_slide(service_slides, pres_id, slide_data, layout_details, main_theme_id, insertion_index + i)
    print("...New slides created.")

    print("\nStep 7: Deleting original template slides...")
    if original_slide_ids:
        requests = [{'deleteObject': {'objectId': slide_id}} for slide_id in original_slide_ids]
        service_slides.presentations().batchUpdate(presentationId=pres_id, body={'requests': requests}).execute()
        print(f"...Deleted {len(original_slide_ids)} slides.")
    
    print("\nSlide generation complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Google Slides from a Markdown file using a template.')
    parser.add_argument('md_file', help='The Markdown file to process.')
    parser.add_argument('title', help='The title of the new presentation.')
    parser.add_argument('--template_id', required=True, help='The Google Drive ID of the template presentation.')
    args = parser.parse_args()
    main(args.md_file, args.title, args.template_id)