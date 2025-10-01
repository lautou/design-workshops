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
# All setup remains the same, as we need the services for layout validation etc.
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
    # All configs are still needed for validation and downstream steps
    PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT_ID']
    LOCATION = os.environ['GOOGLE_CLOUD_LOCATION']
    SOURCE_DOCS_DRIVE_FOLDER_ID = os.environ.get('SOURCE_DOCUMENTS_DRIVE_FOLDER_ID')
    TEMPLATE_PRESENTATION_ID = os.environ['TEMPLATE_PRESENTATION_ID']
    SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    PROMPT_TEMPLATE_FILE = "gemini-prompt-generate-json.md"
    WORKSHOPS_FILE = "workshops.yaml"
    LAYOUTS_FILE = "layouts.yaml"
    JSON_SOURCE_DIR = "json_source"
    LOCAL_DOCS_DIR = "source_documents"
    CACHE_INFO_FILE = ".cache_info.json"
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
    sys.exit(1)

# Initialize API Services
# We still initialize VertexAI to catch the billing error gracefully if not using --show-prompt
try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    json_model_config = GenerationConfig(response_mime_type="application/json")
    model = GenerativeModel("gemini-1.5-flash-001", generation_config=json_model_config)
except Exception:
    model = None # If it fails, we can still run in --show-prompt mode

SCOPES = ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/presentations.readonly"]
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)
slides_service = build("slides", "v1", credentials=creds)

# --- Caching & Metadata Functions ---

def get_drive_folder_state_hash(folder_id):
    """Fetches file metadata from a Drive folder and returns a hash of that metadata."""
    logging.info("Checking state of Google Drive source folder for caching...")
    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = drive_service.files().list(
            q=query,
            fields="files(id, name, modifiedTime)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
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

def get_local_folder_state_hash():
    """Calculates a hash based on file names and modification times in the local source_documents/ directory."""
    logging.info("Checking state of local source_documents/ folder for caching...")
    if not os.path.isdir(LOCAL_DOCS_DIR):
        return None
    
    hasher = hashlib.sha256()
    # Sort files by name for a consistent hash
    files = sorted(os.listdir(LOCAL_DOCS_DIR))
    
    for filename in files:
        filepath = os.path.join(LOCAL_DOCS_DIR, filename)
        if os.path.isfile(filepath):
            # Include filename and modification time in the hash
            mod_time = os.path.getmtime(filepath)
            hasher.update(filename.encode('utf-8'))
            hasher.update(str(mod_time).encode('utf-8'))
            
    return hasher.hexdigest()

def read_cached_hash():
    """Reads the cached metadata hash."""
    if not os.path.exists(CACHE_INFO_FILE): return None
    try:
        with open(CACHE_INFO_FILE, 'r') as f: return json.load(f).get('metadata_hash')
    except (json.JSONDecodeError, IOError): return None

def write_cache_hash(new_hash):
    """Writes the new metadata hash."""
    try:
        with open(CACHE_INFO_FILE, 'w') as f:
            json.dump({'metadata_hash': new_hash}, f, indent=2)
            logging.info(f"Updated cache with new hash: {new_hash[:10]}...")
    except IOError as e: logging.error(f"Could not write to cache file: {e}")

# --- Google API & File Helper Functions ---

def download_and_cache_drive_files(folder_id):
    """
    Downloads files from Drive, saves them to a local cache directory for image
    extraction, and returns them in-memory for the AI.
    """
    downloaded_files_in_memory = []
    logging.info(f"Change detected. Downloading source documents from Google Drive...")
    os.makedirs(LOCAL_DOCS_DIR, exist_ok=True)
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
            file_content = file_stream.getvalue()
            downloaded_files_in_memory.append({"mime_type": item['mimeType'], "data": file_content, "name": item['name']})
            local_path = os.path.join(LOCAL_DOCS_DIR, item['name'])
            with open(local_path, 'wb') as f: f.write(file_content)
        return downloaded_files_in_memory
    except Exception as e:
        logging.error(f"Failed to download files from Google Drive: {e}", exc_info=True)
        return []

def load_local_files():
    """Loads files from the local source_documents/ directory into memory."""
    logging.info("Loading source documents from local source_documents/ directory...")
    loaded_files = []
    if not os.path.isdir(LOCAL_DOCS_DIR):
        logging.warning("Local 'source_documents/' directory not found.")
        return []
    
    for filename in os.listdir(LOCAL_DOCS_DIR):
        filepath = os.path.join(LOCAL_DOCS_DIR, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
                # Determine mime type, default to text/plain
                mime_type = 'application/pdf' if filename.lower().endswith('.pdf') else 'text/plain'
                loaded_files.append({"mime_type": mime_type, "data": content, "name": filename})
                logging.info(f"  - Loaded '{filename}'")
            except IOError as e:
                logging.error(f"  - Could not read file '{filename}'. Error: {e}")
    return loaded_files

# --- Other Helper & Main Pipeline Functions ---

def validate_layouts(layout_mapping):
    """Compares layouts in layouts.yaml with the Google Slides template."""
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
    """Loads a YAML file."""
    try:
        with open(filepath, 'r') as f: return yaml.safe_load(f)
    except FileNotFoundError:
        logging.critical(f"FATAL: Configuration file not found at '{filepath}'")
        sys.exit(1)

def clean_json_source_directory():
    """Removes old .json and .error.txt files."""
    if not os.path.exists(JSON_SOURCE_DIR): os.makedirs(JSON_SOURCE_DIR)
    logging.info(f"Cleaning the '{JSON_SOURCE_DIR}' directory...")
    for f in os.listdir(JSON_SOURCE_DIR):
        if f.endswith(".json") or f.endswith(".error.txt"):
            os.remove(os.path.join(JSON_SOURCE_DIR, f))

# --- Main Pipeline Functions ---

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
        json_output_path = os.path.join(JSON_SOURCE_DIR, f"{base_filename}.json")
        error_output_path = os.path.join(JSON_SOURCE_DIR, f"{base_filename}.error.txt")

        logging.info(f"Generating JSON for: '{title}' -> {base_filename}.json")
        task_prompt = f"\nCurrent Task:\nGenerate the slide deck for the workshop: \"{title}\"."
        prompt_parts = [base_prompt, task_prompt] + file_parts
        
        try:
            logging.info(f"Calling Vertex AI Gemini API with {len(file_parts)} source documents...")
            response = model.generate_content(prompt_parts)
            json_content = response.text
            json.loads(json_content) # Validate that the response is valid JSON
            with open(json_output_path, 'w', encoding='utf-8') as f: f.write(json_content)
            logging.info(f"Successfully saved JSON to {json_output_path}\n")
        except Exception as e:
            logging.error(f"❌ Failed to generate or parse JSON for '{title}'. Error: {e}")
            if 'response' in locals() and hasattr(response, 'text'):
                logging.info(f"   Saving the raw, invalid output to '{error_output_path}' for debugging.")
                with open(error_output_path, 'w', encoding='utf-8') as f: f.write(response.text)
            else:
                logging.error("   No response content was received from the API.")
            continue

    logging.info("--- JSON generation complete. ---")

def run_slides_generation_from_json():
    """Executes the build_slides_from_json.py script."""
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
    parser.add_argument("--force-download", action="store_true", help="Force re-download of files from Google Drive.")
    parser.add_argument("--json-only", action="store_true", help="Stop after generating JSON files; do not create Google Slides.")
    # --- NEW FEATURE ---
    parser.add_argument("--show-prompt", action="store_true", help="Build and print the full prompt for manual use, then exit.")
    args = parser.parse_args()

    logging.info("--- Starting Generation Pipeline ---")
    
    workshops = load_yaml_config(WORKSHOPS_FILE).get('workshops', [])
    
    # --- NEW: --show-prompt Logic ---
    if args.show_prompt:
        logging.info("✅ --show-prompt flag detected. Building the prompt for manual execution...")
        
        enabled_workshops = [w for w in workshops if w.get('enabled', False)]
        if not enabled_workshops:
            logging.error("No workshop is enabled in workshops.yaml. Cannot build prompt.")
            sys.exit(1)
        if len(enabled_workshops) > 1:
            logging.warning("Multiple workshops enabled. The prompt will be built for the first one only.")
        
        workshop = enabled_workshops[0]
        title = workshop['title']
        
        try:
            with open(PROMPT_TEMPLATE_FILE, 'r', encoding='utf-8') as f: base_prompt_template = f.read()
        except FileNotFoundError:
            logging.critical(f"FATAL: Prompt template not found at '{PROMPT_TEMPLATE_FILE}'"); sys.exit(1)
            
        all_workshop_titles = [f"* {w['title']}" for w in workshops]
        workshop_roadmap_str = "\n".join(all_workshop_titles)
        base_prompt = base_prompt_template.replace("{{WORKSHOP_ROADMAP}}", workshop_roadmap_str)
        task_prompt = f"\nCurrent Task:\nGenerate the slide deck for the workshop: \"{title}\"."
        
        final_prompt = base_prompt + task_prompt
        
        print("\n" + "="*80)
        print("COPY AND PASTE THE FOLLOWING PROMPT INTO THE GEMINI UI")
        print("Make sure you have uploaded your source PDF/ADOC files first.")
        print("="*80 + "\n")
        print(final_prompt)
        print("\n" + "="*80)
        
        logging.info("Prompt has been printed to the console. Exiting.")
        sys.exit(0)
    
    # --- Existing Pipeline Logic ---
    layout_mapping = load_yaml_config(LAYOUTS_FILE)
    validate_layouts(layout_mapping)

    source_docs_in_memory = []
    
    # --- NEW: Branching logic for Local vs. Google Drive Mode ---
    if SOURCE_DOCS_DRIVE_FOLDER_ID:
        # --- Google Drive Mode ---
        logging.info("Google Drive Folder ID detected. Running in Google Drive Mode.")
        new_hash = get_drive_folder_state_hash(SOURCE_DOCS_DRIVE_FOLDER_ID)
        cached_hash = read_cached_hash()

        if new_hash == cached_hash and not args.force_download and not args.force:
            logging.info("✅ Google Drive folder has not changed. Loading documents from local cache.")
            source_docs_in_memory = load_local_files()
        else:
            if args.force_download: logging.info("--force-download flag detected.")
            source_docs_in_memory = download_and_cache_drive_files(SOURCE_DOCS_DRIVE_FOLDER_ID)
            # We get a new hash from the freshly downloaded local files
            new_hash = get_local_folder_state_hash()
    else:
        # --- Local Mode (Default) ---
        logging.info("No Google Drive Folder ID found. Running in Local Mode.")
        new_hash = get_local_folder_state_hash()
        cached_hash = read_cached_hash()
        source_docs_in_memory = load_local_files()

    # --- Caching and Generation Logic ---
    if new_hash == cached_hash and not args.force:
        logging.info("✅ Source content has not changed. Skipping AI generation.")
        logging.info("   To override, run with the --force flag.")
    else:
        if not source_docs_in_memory:
            logging.warning("No source documents found. Cannot proceed with generation.")
        else:
            clean_json_source_directory()
            generate_json_files(source_docs_in_memory, workshops)
            write_cache_hash(new_hash)
    
    if args.json_only:
        logging.info("✅ --json-only flag detected. Halting pipeline before slide generation.")
    elif any(w.get('enabled', False) for w in workshops):
        run_slides_generation_from_json()
    else:
        logging.info("No workshops enabled in workshops.yaml. Skipping slide generation.")
    
    logging.info("--- Pipeline Finished ---")

