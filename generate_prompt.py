import os
import sys
import logging
import yaml
import re
from dotenv import load_dotenv

# --- Configuration & Setup ---
load_dotenv()

LOG_LEVEL_STR = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_LEVELS = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR}
log_level = LOG_LEVELS.get(LOG_LEVEL_STR, logging.INFO)

logging.basicConfig(level=log_level, format="%(asctime)s [%(levelname)s] - %(message)s", handlers=[logging.FileHandler("pipeline.log", mode='a'), logging.StreamHandler(sys.stdout)])

try:
    # Configs required for prompt generation
    PROMPT_TEMPLATE_FILE = "gemini-prompt-generate-json.md"
    WORKSHOPS_FILE = "workshops.yaml"
    OUTPUT_DIR = "generated_prompts"
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
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

def sanitize_filename(name):
    """Sanitizes a string to be used as a valid filename."""
    s = name.strip().replace(" ", "_")
    s = re.sub(r'(?u)[^-\w.]', '', s)
    return s

# --- Main Execution ---
if __name__ == "__main__":
    logging.info("--- Starting Prompt Generation for Enabled Workshops ---")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logging.info(f"Ensured output directory exists: {OUTPUT_DIR}")

    workshops_config = load_yaml_config(WORKSHOPS_FILE)
    all_workshops = workshops_config.get('workshops', [])
    
    try:
        with open(PROMPT_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            base_prompt_template = f.read()
    except FileNotFoundError:
        logging.critical(f"FATAL: Prompt template not found: '{PROMPT_TEMPLATE_FILE}'")
        sys.exit(1)

    enabled_workshops = [w for w in all_workshops if w.get('enabled', False)]
    
    if not enabled_workshops:
        logging.warning("No enabled workshops found in workshops.yaml. Nothing to generate.")
        sys.exit(0)

    logging.info(f"Found {len(enabled_workshops)} enabled workshop(s) to process.")

    all_workshop_titles_for_roadmap = [f"* {w['title']}" for w in all_workshops]
    workshop_roadmap_str = "\n".join(all_workshop_titles_for_roadmap)
    
    for workshop in enabled_workshops:
        title = workshop['title']
        id_prefix = workshop.get('id_prefix', 'GENERAL') # Get the prefix from yaml
        logging.info(f"  - Generating prompt for: '{title}' (Prefix: {id_prefix})")
        
        # Replace placeholders in the base template
        prompt_with_roadmap = base_prompt_template.replace("{{WORKSHOP_ROADMAP}}", workshop_roadmap_str)
        prompt_with_prefix = prompt_with_roadmap.replace("{{ID_PREFIX}}", id_prefix)

        task_prompt = f"\nCurrent Task:\nGenerate the slide deck for the workshop: \"{title}\"."
        final_prompt = prompt_with_prefix + task_prompt
        
        prompt_header = (
            f"# -- PROMPT FOR: {title} --\n\n"
            f"## REQUIRED FILES TO UPLOAD MANUALLY TO THE GEMINI UI:\n"
        )
        for pattern in workshop.get('source_files', []):
            prompt_header += f"- `{pattern}`\n"
        prompt_header += "\n---\n\n"

        full_prompt_content = prompt_header + final_prompt

        # Create a sanitized, unique filename for each prompt
        sanitized_title = sanitize_filename(title)
        output_filename = os.path.join(OUTPUT_DIR, f"prompt-{sanitized_title}.md")

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(full_prompt_content)
            logging.info(f"    ✅ Prompt successfully saved to '{output_filename}'")
        except IOError as e:
            logging.error(f"    ❌ Could not write prompt to file: {e}")

    logging.info("--- Prompt Generation Finished ---")