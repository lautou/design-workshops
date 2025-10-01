import os
import sys
import subprocess
import re
import logging
import io
import yaml
import hashlib
import json
import argparse
from dotenv import load_dotenv

# Import Google Cloud libraries
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# --- Configuration & Setup ---
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

try:
    # Configs from .env file
    PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT_ID']
    LOCATION = os.environ['GOOGLE_CLOUD_LOCATION']
    SOURCE_DOCS_FOLDER_ID = os.environ['SOURCE_DOCUMENTS_DRIVE_FOLDER_ID']
    TEMPLATE_PRESENTATION_ID = os.environ['TEMPLATE_PRESENTATION_ID']
    SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    # Script file configs
    PROMPT_TEMPLATE_FILE = "gemini-prompt-generate-json.md"
    WORKSHOPS_FILE = "workshops.yaml"
    LAYOUTS_FILE = "layouts.yaml"
    SOURCE_DIR = "json_source"
    CACHE_INFO_FILE = ".cache_info.json"
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
    sys.exit(1)

# Initialize API Services
vertexai.init(project=PROJECT_ID, location=LOCATION)
json_model_config = GenerationConfig(response_mime_type="application/json")
model = GenerativeModel("gemini-1.5-flash-001", generation_config=json_model_config)
SCOPES = ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/presentations.readonly"]
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)
slides_service = build("slides", "v1", credentials=creds)

# --- Caching, Validation, and Helper functions ---
def get_drive_folder_state_hash(folder_id):
    logging.info("Checking state of Google Drive source folder for caching...")
    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = drive_service.files().list(q=query, fields="files(id, name, modifiedTime)", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        items = results.get('files', [])
        if not items:
            logging.warning("No files found in the source Google Drive folder.")
            return None
        items.sort(key=lambda x: x['id'])
        metadata_string = "".join([f"{item['id']}{item['name']}{item['modifiedTime']}" for item in items])
        return hashlib.sha256(metadata_string.encode('utf-8')).hexdigest()
    except Exception as e:
        logging.error(f"Could not get Drive folder state for caching: {e}", exc_info=True)
        return None

def read_cached_hash():
    if not os.path.exists(CACHE_INFO_FILE): return None
    try:
        with open(CACHE_INFO_FILE, 'r') as f: return json.load(f).get('metadata_hash')
    except (json.JSONDecodeError, IOError): return None

def write_cache_hash(new_hash):
    try:
        with open(CACHE_INFO_FILE, 'w') as f:
            json.dump({'metadata_hash': new_hash}, f, indent=2)
            logging.info(f"Updated cache with new hash: {new_hash[:10]}...")
    except IOError as e: logging.error(f"Could not write to cache file: {e}")

def download_files_from_drive_folder(folder_id):
    downloaded_files = []
    logging.info(f"Change detected. Downloading source documents from Google Drive folder: {folder_id}...")
    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = drive_service.files().list(q=query, fields="files(id, name, mimeType)", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        items = results.get('files', [])
        for item in items:
            logging.info(f"  - Downloading '{item['name']}'...")
            request = drive_service.files().get_media(fileId=item['id'], supportsAllDrives=True)
            file_stream = io.BytesIO()
            downloader = MediaIoBaseDownload(file_stream, request)
            done = False
            while not done: status, done = downloader.next_chunk()
            downloaded_files.append({"mime_type": item['mimeType'], "data": file_stream.getvalue(), "name": item['name']})
        return downloaded_files
    except Exception as e:
        logging.error(f"Failed to download files from Google Drive: {e}", exc_info=True)
        return []

def validate_layouts(layout_mapping):
    logging.info(f"Validating layouts in '{LAYOUTS_FILE}' against template '{TEMPLATE_PRESENTATION_ID}'...")
    try:
        presentation = slides_service.presentations().get(presentationId=TEMPLATE_PRESENTATION_ID).execute()
        available_layout_names = {l.get('layoutProperties', {}).get('displayName') for l in presentation.get('layouts', [])}
        missing_layouts = set(layout_mapping.values()) - available_layout_names
        if missing_layouts:
            logging.critical("FATAL: Layout validation failed!")
            for layout in sorted(list(missing_layouts)): logging.critical(f"  - Layout '{layout}' from '{LAYOUTS_FILE}' not found in template.")
            sys.exit(1)
        logging.info("✅ Layout validation successful.")
        return True
    except Exception as e:
        logging.critical(f"FATAL: An error occurred during layout validation: {e}", exc_info=True)
        sys.exit(1)

def load_yaml_config(filepath):
    try:
        with open(filepath, 'r') as f: return yaml.safe_load(f)
    except FileNotFoundError:
        logging.critical(f"FATAL: Configuration file not found at '{filepath}'")
        sys.exit(1)

def clean_json_source_directory():
    if not os.path.exists(SOURCE_DIR): os.makedirs(SOURCE_DIR)
    logging.info(f"Cleaning the '{SOURCE_DIR}' directory...")
    for f in os.listdir(SOURCE_DIR):
        if f.endswith(".json") or f.endswith(".error.txt"):
            os.remove(os.path.join(SOURCE_DIR, f))

# --- Main Pipeline Functions (with Error Handling) ---

def generate_json_files(source_documents, workshops):
    """Loops through workshops, calls Gemini, and saves the output with graceful error handling."""
    logging.info("--- Starting JSON Generation via Gemini (Vertex AI) ---")
    try:
        with open(PROMPT_TEMPLATE_FILE, 'r', encoding='utf-8') as f: base_prompt_template = f.read()
    except FileNotFoundError:
        logging.critical(f"FATAL: Prompt template not found: '{PROMPT_TEMPLATE_FILE}'"); sys.exit(1)

    all_workshop_titles = [f"* {w['title']}" for w in workshops]
    workshop_roadmap_str = "\n".join(all_workshop_titles)
    base_prompt = base_prompt_template.replace("{{WORKSHOP_ROADMAP}}", workshop_roadmap_str)
    
    file_parts = [Part.from_data(d['data'], mime_type=d['mime_type']) for d in source_documents]
    enabled_workshops = [w for w in workshops if w.get('enabled', False)]
    
    for i, workshop in enumerate(enabled_workshops):
        title = workshop['title']
        clean_title = re.sub(r'[^a-z0-9\s-]', '', title.lower()).replace(' ', '-')
        base_filename = f"{i+1:02d}-{clean_title}"
        json_output_path = os.path.join(SOURCE_DIR, f"{base_filename}.json")
        error_output_path = os.path.join(SOURCE_DIR, f"{base_filename}.error.txt")

        logging.info(f"Generating JSON for: '{title}' -> {base_filename}.json")
        task_prompt = f"\nCurrent Task:\nGenerate the slide deck for the workshop: \"{title}\"."
        prompt_parts = [base_prompt, task_prompt] + file_parts
        
        try:
            logging.info(f"Calling Vertex AI Gemini API with {len(file_parts)} source documents...")
            response = model.generate_content(prompt_parts)
            
            # This is the raw text from the AI
            json_content = response.text
            
            # This line validates if the text is valid JSON. It will raise an exception if not.
            json.loads(json_content)
            
            # If validation passes, write the good JSON file
            with open(json_output_path, 'w', encoding='utf-8') as f:
                f.write(json_content)
            logging.info(f"Successfully saved JSON to {json_output_path}\n")

        except Exception as e:
            # Catch ANY exception during the API call or JSON parsing
            logging.error(f"❌ Failed to generate or parse JSON for '{title}'. Error: {e}")
            
            # Check if we have a response from the AI to save for debugging
            if 'response' in locals() and hasattr(response, 'text'):
                logging.info(f"   Saving the raw, invalid output to '{error_output_path}' for debugging.")
                with open(error_output_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
            else:
                logging.error("   No response content was received from the API.")

            # Continue to the next workshop instead of crashing
            continue

    logging.info("--- JSON generation complete. ---")


def run_slides_generation_from_json():
    script_to_run = "build_slides_from_json.py"
    logging.info(f"--- Starting Google Slides Generation by running '{script_to_run}' ---")
    try:
        process = subprocess.run([sys.executable, script_to_run], capture_output=True, text=True, check=True)
        logging.info(f"{script_to_run} output:\n" + process.stdout)
        if process.stderr: logging.warning(f"{script_to_run} logged errors:\n" + process.stderr)
    except FileNotFoundError:
        logging.critical(f"FATAL: The build script '{script_to_run}' was not found.")
    except subprocess.CalledProcessError as e:
        logging.error(f"'{script_to_run}' failed.\n--- STDOUT ---\n{e.stdout}\n--- STDERR ---\n{e.stderr}")

# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate workshop slides from source documents.")
    parser.add_argument("--force", action="store_true", help="Force regeneration of JSON files, ignoring the cache.")
    parser.add_argument("--json-only", action="store_true", help="Stop after generating JSON files; do not create Google Slides.")
    args = parser.parse_args()

    logging.info("--- Starting Generation Pipeline ---")
    
    workshops = load_yaml_config(WORKSHOPS_FILE).get('workshops', [])
    layout_mapping = load_yaml_config(LAYOUTS_FILE)
    
    validate_layouts(layout_mapping)
    
    new_metadata_hash = get_drive_folder_state_hash(SOURCE_DOCS_FOLDER_ID)
    cached_metadata_hash = read_cached_hash()

    if new_metadata_hash == cached_metadata_hash and not args.force:
        logging.info("✅ Source folder has not changed. Skipping download and AI generation.")
        logging.info("   To override, run with the --force flag.")
    else:
        source_docs = download_files_from_drive_folder(SOURCE_DOCS_FOLDER_ID)
        clean_json_source_directory()
        generate_json_files(source_docs, workshops)
        write_cache_hash(new_metadata_hash)
    
    if args.json_only:
        logging.info("✅ --json-only flag detected. Halting pipeline before slide generation.")
    elif any(w.get('enabled', False) for w in workshops):
        run_slides_generation_from_json()
    else:
        logging.info("No workshops enabled in workshops.yaml. Skipping slide generation.")
    
    logging.info("--- Pipeline Finished ---")

