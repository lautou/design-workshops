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
import fnmatch # Import for wildcard matching
from dotenv import load_dotenv

# Import Google Cloud libraries
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# --- Configuration & Setup ---
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log", mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)

try:
    # Configs
    PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
    LOCATION = os.environ.get('GOOGLE_CLOUD_LOCATION')
    SOURCE_DOCS_DRIVE_FOLDER_ID = os.environ.get('SOURCE_DOCUMENTS_DRIVE_FOLDER_ID')
    TEMPLATE_PRESENTATION_ID = os.environ['TEMPLATE_PRESENTATION_ID']
    SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    TARGET_THEME_NAME = os.environ['TARGET_THEME_NAME']
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
try:
    if PROJECT_ID and LOCATION:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        json_model_config = GenerationConfig(response_mime_type="application/json")
        model = GenerativeModel("gemini-1.5-flash-001", generation_config=json_model_config)
    else:
        model = None
except Exception:
    model = None

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/presentations.readonly"
]
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)
slides_service = build("slides", "v1", credentials=creds)


# --- Caching & Metadata Functions ---
def get_local_folder_state_hash():
    logging.info("Checking state of local source_documents/ folder for caching...")
    if not os.path.isdir(LOCAL_DOCS_DIR):
        return None
    hasher = hashlib.sha256()
    files = sorted(os.listdir(LOCAL_DOCS_DIR))
    for filename in files:
        filepath = os.path.join(LOCAL_DOCS_DIR, filename)
        if os.path.isfile(filepath):
            mod_time = os.path.getmtime(filepath)
            hasher.update(filename.encode('utf-8'))
            hasher.update(str(mod_time).encode('utf-8'))
    return hasher.hexdigest()

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

# --- File Helper Functions ---
def load_local_files():
    logging.info("Loading source documents from local source_documents/ directory...")
    loaded_files = []
    if not os.path.isdir(LOCAL_DOCS_DIR):
        logging.warning("Local 'source_documents/' directory not found.")
        return []
    
    for filename in sorted(os.listdir(LOCAL_DOCS_DIR)):
        filepath = os.path.join(LOCAL_DOCS_DIR, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
                mime_type = 'application/pdf' if filename.lower().endswith('.pdf') else 'text/plain'
                loaded_files.append({"mime_type": mime_type, "data": content, "name": filename})
                logging.info(f"  - Loaded '{filename}'")
            except IOError as e:
                logging.error(f"  - Could not read file '{filename}'. Error: {e}")
    return loaded_files

# --- Validation & Config Functions ---
def validate_layouts_in_template(layout_config):
    logging.info(f"Validating layouts in '{LAYOUTS_FILE}' against template '{TEMPLATE_PRESENTATION_ID}'...")
    try:
        presentation = slides_service.presentations().get(presentationId=TEMPLATE_PRESENTATION_ID).execute()
        target_master = next((m for m in presentation.get('masters', []) if m.get('masterProperties', {}).get('displayName') == TARGET_THEME_NAME), None)
        if not target_master:
            logging.critical(f"FATAL: Target theme '{TARGET_THEME_NAME}' not found in the template.")
            sys.exit(1)
        target_master_id = target_master.get('objectId')
        available_layout_names = {
            layout.get('layoutProperties', {}).get('displayName')
            for layout in presentation.get('layouts', [])
            if layout.get('layoutProperties', {}).get('masterObjectId') == target_master_id
        }
        required_layout_names = set(layout_config.get('layout_mapping', {}).values())
        missing_layouts = required_layout_names - available_layout_names
        if missing_layouts:
            logging.critical("FATAL: Layout validation failed! The following layouts are missing from the template's specified theme:")
            for layout in sorted(list(missing_layouts)):
                logging.critical(f"  - '{layout}'")
            sys.exit(1)
        logging.info("✅ Layout validation successful.")
        return True
    except HttpError as err:
        logging.critical(f"FATAL: Google API error during layout validation: {err.reason}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        logging.critical(f"FATAL: An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)

def load_yaml_config(filepath):
    try:
        with open(filepath, 'r') as f: return yaml.safe_load(f)
    except FileNotFoundError:
        logging.critical(f"FATAL: Configuration file not found at '{filepath}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.critical(f"FATAL: Error parsing YAML file '{filepath}': {e}")
        sys.exit(1)

def clean_json_source_directory():
    if not os.path.exists(JSON_SOURCE_DIR): os.makedirs(JSON_SOURCE_DIR)
    logging.info(f"Cleaning the '{JSON_SOURCE_DIR}' directory...")
    for f in os.listdir(JSON_SOURCE_DIR):
        if f.endswith((".json", ".error.txt")):
            os.remove(os.path.join(JSON_SOURCE_DIR, f))

# --- Main Pipeline Functions ---

def generate_json_files(all_source_documents, workshops):
    """
    Loops through workshops, filters for relevant source documents,
    calls Gemini, and saves the output.
    """
    if not model:
        logging.critical("FATAL: Vertex AI model not initialized.")
        sys.exit(1)

    logging.info("--- Starting JSON Generation via Gemini (Vertex AI) ---")
    try:
        with open(PROMPT_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            base_prompt_template = f.read()
    except FileNotFoundError:
        logging.critical(f"FATAL: Prompt template not found: '{PROMPT_TEMPLATE_FILE}'"); sys.exit(1)

    all_workshop_titles = [f"* {w['title']}" for w in workshops]
    workshop_roadmap_str = "\n".join(all_workshop_titles)
    base_prompt = base_prompt_template.replace("{{WORKSHOP_ROADMAP}}", workshop_roadmap_str)
    
    enabled_workshops = [w for w in workshops if w.get('enabled', False)]
    
    for i, workshop in enumerate(enabled_workshops):
        title = workshop['title']
        clean_title = re.sub(r'[^a-z0-9\s-]', '', title.lower()).replace(' ', '-')
        base_filename = f"{i+1:02d}-{clean_title}"
        json_output_path = os.path.join(JSON_SOURCE_DIR, f"{base_filename}.json")
        error_output_path = os.path.join(JSON_SOURCE_DIR, f"{base_filename}.error.txt")

        logging.info(f"\nGenerating JSON for: '{title}'")
        
        # --- NEW: Document Filtering Logic ---
        required_patterns = workshop.get('source_files', [])
        if not required_patterns:
            logging.warning(f"  - No 'source_files' defined for workshop '{title}'. Skipping.")
            continue
            
        relevant_docs = []
        for doc in all_source_documents:
            for pattern in required_patterns:
                if fnmatch.fnmatch(doc['name'], pattern):
                    relevant_docs.append(doc)
                    break # Avoid adding the same doc twice
        
        if not relevant_docs:
            logging.warning(f"  - No matching source files found for workshop '{title}'. Skipping.")
            continue

        logging.info(f"  - Found {len(relevant_docs)} relevant source documents:")
        for doc in relevant_docs:
            logging.info(f"    - {doc['name']}")
            
        file_parts = [Part.from_data(d['data'], mime_type=d['mime_type']) for d in relevant_docs]
        
        task_prompt = f"\nCurrent Task:\nGenerate the slide deck for the workshop: \"{title}\"."
        prompt_parts = [base_prompt, task_prompt] + file_parts
        
        try:
            logging.info(f"  - Calling Vertex AI Gemini API...")
            response = model.generate_content(prompt_parts)
            json_content = response.text
            
            json.loads(json_content) 
            
            with open(json_output_path, 'w', encoding='utf-8') as f:
                f.write(json_content)
            logging.info(f"  - Successfully saved JSON to {json_output_path}")

        except Exception as e:
            logging.error(f"  - ❌ Failed to generate or parse JSON for '{title}'. Error: {e}")
            if 'response' in locals() and hasattr(response, 'text'):
                with open(error_output_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                logging.info(f"  - Saved raw, invalid output to '{error_output_path}'.")
            else:
                logging.error("  - No response content was received from the API.")
            continue

    logging.info("\n--- JSON generation complete. ---")


# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate workshop slides from source documents.")
    parser.add_argument("--force", action="store_true", help="Force regeneration of JSON files, ignoring cache.")
    parser.add_argument("--json-only", action="store_true", help="Stop after generating JSON files.")
    parser.add_argument("--show-prompt", action="store_true", help="Build and print the prompt, then exit.")
    args = parser.parse_args()

    logging.info("--- Starting Generation Pipeline ---")
    
    workshops = load_yaml_config(WORKSHOPS_FILE).get('workshops', [])
    layout_config = load_yaml_config(LAYOUTS_FILE)
    
    validate_layouts_in_template(layout_config)
    
    # --- --show-prompt Logic ---
    if args.show_prompt:
        logging.info("✅ --show-prompt flag detected. Building the prompt for manual execution...")
        
        enabled_workshops = [w for w in workshops if w.get('enabled', False)]
        if not enabled_workshops:
            logging.error("No enabled workshops in workshops.yaml."); sys.exit(1)
        
        workshop = enabled_workshops[0]
        title = workshop['title']
        
        try:
            with open(PROMPT_TEMPLATE_FILE, 'r', encoding='utf-8') as f: base_prompt_template = f.read()
        except FileNotFoundError:
            logging.critical(f"FATAL: Prompt template not found: '{PROMPT_TEMPLATE_FILE}'"); sys.exit(1)
            
        all_workshop_titles = [f"* {w['title']}" for w in workshops]
        workshop_roadmap_str = "\n".join(all_workshop_titles)
        base_prompt = base_prompt_template.replace("{{WORKSHOP_ROADMAP}}", workshop_roadmap_str)
        task_prompt = f"\nCurrent Task:\nGenerate the slide deck for the workshop: \"{title}\"."
        
        final_prompt = base_prompt + task_prompt
        
        print("\n" + "="*80)
        print("COPY AND PASTE THE FOLLOWING PROMPT INTO THE GEMINI UI")
        print(f"WORKSHOP: {title}")
        print("\nREQUIRED FILES TO UPLOAD MANUALLY:")
        for pattern in workshop.get('source_files', []):
            print(f"  - {pattern}")
        print("="*80 + "\n")
        print(final_prompt)
        print("\n" + "="*80)
        
        logging.info("Prompt printed. Exiting.")
        sys.exit(0)
    
    # --- Main Pipeline Logic ---
    all_source_documents = load_local_files()
    if not all_source_documents:
        logging.warning("No source documents found in local cache directory. Ensure they are downloaded.")

    new_hash = get_local_folder_state_hash()
    cached_hash = read_cached_hash()

    if new_hash == cached_hash and not args.force:
        logging.info("✅ Source content has not changed. Skipping AI generation.")
    else:
        if not all_source_documents:
            logging.warning("No source documents found to process.")
        else:
            clean_json_source_directory()
            generate_json_files(all_source_documents, workshops)
            write_cache_hash(new_hash)
    
    if args.json_only:
        logging.info("✅ --json-only flag detected. Halting pipeline.")
    elif any(w.get('enabled', False) for w in workshops):
        logging.info("JSON generation complete. To build slides, run './run_build.sh build'")
    else:
        logging.info("No workshops enabled. Skipping slide generation step.")
    
    logging.info("--- Pipeline Finished ---")

