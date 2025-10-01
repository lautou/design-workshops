import os
import sys
import subprocess
import re
import logging
import io
import yaml
from dotenv import load_dotenv

# Import Google Cloud libraries
import vertexai
from vertexai.generative_models import GenerativeModel, Part
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
    # Vertex AI Config
    PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT_ID']
    LOCATION = os.environ['GOOGLE_CLOUD_LOCATION']
    # Google Drive & Slides Config
    SOURCE_DOCS_FOLDER_ID = os.environ['SOURCE_DOCUMENTS_DRIVE_FOLDER_ID']
    TEMPLATE_PRESENTATION_ID = os.environ['TEMPLATE_PRESENTATION_ID']
    SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    # Script Config
    PROMPT_TEMPLATE_FILE = "gemini-prompt-generate-md-files.md"
    WORKSHOPS_FILE = "workshops.yaml"
    LAYOUTS_FILE = "layouts.yaml"
    SOURCE_DIR = os.environ.get('SOURCE_DIRECTORY', 'markdown_source')
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
    sys.exit(1)

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-1.5-flash-001")

# Initialize Google API Services
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/presentations.readonly"
]
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)
slides_service = build("slides", "v1", credentials=creds)

# --- Google API Helper Functions ---

def download_files_from_drive_folder(folder_id):
    """Downloads all files from a Google Drive folder into memory."""
    downloaded_files = []
    logging.info(f"Fetching source documents from Google Drive folder: {folder_id}...")
    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = drive_service.files().list(
            q=query,
            fields="files(id, name, mimeType)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        items = results.get('files', [])

        if not items:
            logging.warning("No files found in the specified Google Drive folder.")
            return []

        for item in items:
            logging.info(f"  - Downloading '{item['name']}'...")
            request = drive_service.files().get_media(fileId=item['id'], supportsAllDrives=True)
            file_stream = io.BytesIO()
            downloader = MediaIoBaseDownload(file_stream, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            downloaded_files.append({
                "mime_type": item['mimeType'],
                "data": file_stream.getvalue(),
                "name": item['name']
            })
        return downloaded_files
    except Exception as e:
        logging.error(f"Failed to download files from Google Drive: {e}", exc_info=True)
        return []

def validate_layouts(layout_mapping):
    """
    Connects to the Google Slides API to validate that layouts in the YAML
    file exist in the master template.
    """
    logging.info(f"Validating layouts in '{LAYOUTS_FILE}' against template '{TEMPLATE_PRESENTATION_ID}'...")
    try:
        presentation = slides_service.presentations().get(presentationId=TEMPLATE_PRESENTATION_ID).execute()
        template_layouts = presentation.get('layouts', [])
        
        # Create a set of available layout names for efficient lookup
        available_layout_names = {
            layout.get('layoutProperties', {}).get('displayName')
            for layout in template_layouts
        }

        mapped_layout_names = set(layout_mapping.values())
        missing_layouts = mapped_layout_names - available_layout_names

        if missing_layouts:
            logging.critical("FATAL: Layout validation failed!")
            logging.critical(f"The following layouts are defined in '{LAYOUTS_FILE}' but were NOT FOUND in the Google Slides template:")
            for layout in sorted(list(missing_layouts)):
                logging.critical(f"  - {layout}")
            sys.exit(1)
        
        logging.info("✅ Layout validation successful. All mapped layouts exist in the template.")
        return True

    except Exception as e:
        logging.critical(f"FATAL: An error occurred during layout validation: {e}")
        sys.exit(1)


# --- Main Pipeline Functions ---

def load_yaml_config(filepath):
    """Loads a specified YAML file."""
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.critical(f"FATAL: Configuration file not found at '{filepath}'")
        sys.exit(1)

def clean_source_directory():
    """Removes old markdown files from the source directory."""
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)
    for f in os.listdir(SOURCE_DIR):
        if f.endswith(".md"):
            os.remove(os.path.join(SOURCE_DIR, f))

def generate_markdown_files(source_documents, workshops):
    logging.info("--- Starting Markdown Generation via Gemini (Vertex AI) ---")
    try:
        with open(PROMPT_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            base_prompt_template = f.read()
    except FileNotFoundError:
        logging.critical(f"FATAL: Prompt template not found: '{PROMPT_TEMPLATE_FILE}'")
        sys.exit(1)

    all_workshop_titles = [f"* {w['title']}" for w in workshops]
    workshop_roadmap_str = "\n".join(all_workshop_titles)
    base_prompt = base_prompt_template.replace("{{WORKSHOP_ROADMAP}}", workshop_roadmap_str)

    file_parts = [Part.from_data(d['data'], mime_type=d['mime_type']) for d in source_documents]
    enabled_workshops = [w for w in workshops if w.get('enabled', False)]
    
    for i, workshop in enumerate(enabled_workshops):
        title = workshop['title']
        clean_title = re.sub(r'[^a-z0-9\s-]', '', title.lower()).replace(' ', '-')
        filename = f"{i+1:02d}-{clean_title}.md"
        output_path = os.path.join(SOURCE_DIR, filename)

        logging.info(f"Generating markdown for: '{title}' -> {filename}")
        task_prompt = f"\nCurrent Task:\nGenerate the slide deck for the workshop: \"{title}\"."
        prompt_parts = [base_prompt, task_prompt] + file_parts

        try:
            logging.info(f"Calling Vertex AI Gemini API with {len(file_parts)} source documents...")
            response = model.generate_content(prompt_parts)
            markdown_content = response.text
            markdown_content = re.sub(r'^```markdown\n', '', markdown_content)
            markdown_content = re.sub(r'\n```$', '', markdown_content)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            logging.info(f"Successfully saved markdown to {output_path}\n")
        except Exception as e:
            logging.error(f"Error calling Vertex AI for '{title}': {e}", exc_info=True)
            logging.warning(f"Skipping file creation for '{title}'.\n")
            continue
    logging.info("--- Markdown generation complete for all enabled workshops. ---")


def run_slides_generation():
    """Executes the md2gslides.py script."""
    script_to_run = "md2gslides.py"
    logging.info(f"--- Starting Google Slides Generation by running '{script_to_run}' ---")
    if not os.path.exists(script_to_run):
        logging.critical(f"FATAL: The script '{script_to_run}' was not found.")
        sys.exit(1)
    try:
        process = subprocess.run(
            [sys.executable, script_to_run], capture_output=True, text=True, check=True
        )
        logging.info("md2gslides.py output:\n" + process.stdout)
        if process.stderr:
            logging.warning("md2gslides.py logged errors:\n" + process.stderr)
    except subprocess.CalledProcessError as e:
        logging.error(f"The '{script_to_run}' script failed with exit code {e.returncode}.")
        logging.error("--- STDOUT ---\n" + e.stdout)
        logging.error("--- STDERR ---\n" + e.stderr)

# --- Main Execution ---
if __name__ == "__main__":
    logging.info("--- Starting Generation Pipeline ---")
    
    # Stage 1: Load configurations
    workshops = load_yaml_config(WORKSHOPS_FILE).get('workshops', [])
    layout_mapping = load_yaml_config(LAYOUTS_FILE)
    
    # Stage 2: Validate configuration before proceeding
    validate_layouts(layout_mapping)
    
    # Stage 3: Download source documents
    source_docs = download_files_from_drive_folder(SOURCE_DOCS_FOLDER_ID)
    
    if not source_docs:
        logging.warning("No source documents found. Markdown generation will rely on the model's general knowledge.")

    # Stage 4: Generate Markdown
    clean_source_directory()
    generate_markdown_files(source_docs, workshops)
    
    # Stage 5: Generate Slides
    if any(w.get('enabled', False) for w in workshops):
        run_slides_generation()
    else:
        logging.info("No workshops were enabled in workshops.yaml. Skipping slide generation.")
    
    logging.info("--- Pipeline Finished ---")

