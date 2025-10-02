import os
import sys
import re
import logging
import yaml
import argparse
from dotenv import load_dotenv

# Import Google Cloud libraries for layout validation
from google.oauth2 import service_account
from googleapiclient.discovery import build
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
    # Configs required for layout validation and prompt generation
    TEMPLATE_PRESENTATION_ID = os.environ['TEMPLATE_PRESENTATION_ID']
    SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    TARGET_THEME_NAME = os.environ['TARGET_THEME_NAME']
    PROMPT_TEMPLATE_FILE = "gemini-prompt-generate-json.md"
    WORKSHOPS_FILE = "workshops.yaml"
    LAYOUTS_FILE = "layouts.yaml"
    GENERATED_PROMPT_FILE = "generated-prompt.md"
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
    sys.exit(1)

# Initialize API Services ONLY for layout validation
try:
    SCOPES = [
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/presentations.readonly"
    ]
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    slides_service = build("slides", "v1", credentials=creds)
except Exception as e:
    logging.critical(f"FATAL: Could not initialize Google Slides API for validation. Error: {e}")
    sys.exit(1)


# --- Validation & Config Functions ---
def validate_layouts_in_template(layout_config):
    """Validates that the layouts defined in the config exist in the Google Slides template."""
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
    """Loads a YAML file and handles errors."""
    try:
        with open(filepath, 'r') as f: return yaml.safe_load(f)
    except FileNotFoundError:
        logging.critical(f"FATAL: Configuration file not found at '{filepath}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.critical(f"FATAL: Error parsing YAML file '{filepath}': {e}")
        sys.exit(1)

# --- Main Execution ---
if __name__ == "__main__":
    logging.info("--- Starting Prompt Generation ---")
    
    workshops = load_yaml_config(WORKSHOPS_FILE).get('workshops', [])
    layout_config = load_yaml_config(LAYOUTS_FILE)
    
    # Perform pre-flight validation before generating the prompt
    validate_layouts_in_template(layout_config)
    
    logging.info("Building the prompt for manual execution...")
    
    enabled_workshops = [w for w in workshops if w.get('enabled', False)]
    if not enabled_workshops:
        logging.error("No enabled workshops found in workshops.yaml. Exiting.")
        sys.exit(1)
    
    # Select the first enabled workshop to generate the prompt for
    workshop = enabled_workshops[0]
    title = workshop['title']
    
    try:
        with open(PROMPT_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            base_prompt_template = f.read()
    except FileNotFoundError:
        logging.critical(f"FATAL: Prompt template not found: '{PROMPT_TEMPLATE_FILE}'")
        sys.exit(1)
        
    all_workshop_titles = [f"* {w['title']}" for w in workshops]
    workshop_roadmap_str = "\n".join(all_workshop_titles)
    base_prompt = base_prompt_template.replace("{{WORKSHOP_ROADMAP}}", workshop_roadmap_str)
    task_prompt = f"\nCurrent Task:\nGenerate the slide deck for the workshop: \"{title}\"."
    
    final_prompt = base_prompt + task_prompt
    
    prompt_header = (
        f"# -- PROMPT FOR: {title} --\n\n"
        f"## REQUIRED FILES TO UPLOAD MANUALLY TO THE GEMINI UI:\n"
    )
    for pattern in workshop.get('source_files', []):
        prompt_header += f"- `{pattern}`\n"
    prompt_header += "\n---\n\n"

    full_prompt_content = prompt_header + final_prompt

    try:
        with open(GENERATED_PROMPT_FILE, 'w', encoding='utf-8') as f:
            f.write(full_prompt_content)
        logging.info(f"✅ Prompt successfully saved to '{GENERATED_PROMPT_FILE}'")
    except IOError as e:
        logging.error(f"❌ Could not write prompt to file: {e}")

    logging.info("--- Prompt Generation Finished ---")
