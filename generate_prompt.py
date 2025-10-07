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
    CONSOLIDATE_PROMPT_FILE = "gemini-prompt-consolidate-sources.md"
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
        id_prefix = workshop.get('id_prefix', 'GENERAL')
        consolidation_needed = workshop.get('consolidation_needed', False)
        sanitized_title = sanitize_filename(title)

        logging.info(f"  - Generating prompt for: '{title}' (Consolidation needed: {consolidation_needed})")
        
        # --- Always generate the main JSON generation prompt ---
        prompt_with_roadmap = base_prompt_template.replace("{{WORKSHOP_ROADMAP}}", workshop_roadmap_str)
        prompt_with_prefix = prompt_with_roadmap.replace("{{ID_PREFIX}}", id_prefix)
        task_prompt = f"\nCurrent Task:\nGenerate the slide deck for the workshop: \"{title}\"."
        final_json_prompt = prompt_with_prefix + task_prompt
        
        prompt_header_title = f"(Step 2: Generate JSON)" if consolidation_needed else ""
        prompt_header = f"# -- PROMPT FOR: {title} {prompt_header_title} --\n\n"
        
        if consolidation_needed:
            prompt_header += "## REQUIRED FILES TO UPLOAD MANUALLY TO THE GEMINI UI:\n"
            prompt_header += f"- `consolidated_sources/{workshop.get('consolidated_source_file', 'consolidated-sources.md')}`\n"
            prompt_header += "- `*.adoc`\n"
        else:
            prompt_header += "## REQUIRED FILES TO UPLOAD MANUALLY TO THE GEMINI UI:\n"
            if workshop.get('source_files'):
                for pattern in workshop['source_files']:
                    prompt_header += f"- `{pattern}`\n"
            # If not consolidating, list optional files here
            if workshop.get('option_odf_source_files'):
                prompt_header += "\n## OPTIONAL ODF-RELATED FILES TO UPLOAD:\n"
                prompt_header += "### (Upload these ONLY if the workshop should include ODF-specific content)\n"
                for pattern in workshop['option_odf_source_files']:
                    prompt_header += f"- `{pattern}`\n"

        prompt_header += "\n---\n\n"
        full_json_prompt_content = prompt_header + final_json_prompt
        
        json_prompt_filename_base = f"prompt-json-generation-{sanitized_title}.md" if consolidation_needed else f"prompt-{sanitized_title}.md"
        json_prompt_filename = os.path.join(OUTPUT_DIR, json_prompt_filename_base)

        try:
            with open(json_prompt_filename, 'w', encoding='utf-8') as f:
                f.write(full_json_prompt_content)
            logging.info(f"    ✅ JSON prompt saved to '{json_prompt_filename}'")
        except IOError as e:
            logging.error(f"    ❌ Could not write JSON prompt file: {e}")

        # --- Generate and save the consolidation prompt (Step 1) IF NEEDED ---
        if consolidation_needed:
            try:
                with open(CONSOLIDATE_PROMPT_FILE, 'r', encoding='utf-8') as f:
                    consolidate_template = f.read()
                
                final_consolidate_prompt = consolidate_template.replace("{{WORKSHOP_TITLE}}", title)
                
                consolidate_header = f"# -- PROMPT FOR: {title} (Step 1: Consolidate Sources) --\n\n"
                
                source_files = workshop.get('source_files', [])
                odf_files = workshop.get('option_odf_source_files', [])
                all_files_to_consolidate = source_files + odf_files

                consolidate_header += "## INSTRUCTIONS:\n"
                consolidate_header += "This workshop has more than 10 source files. You must consolidate them in batches.\n\n"
                consolidate_header += "1.  For **each batch** of files listed below, start a **new chat** in the Gemini UI.\n"
                consolidate_header += "2.  Upload the files for that specific batch.\n"
                consolidate_header += "3.  Copy and paste the entire prompt from the bottom of this file.\n"
                consolidate_header += "4.  Append the markdown output from each batch into a single temporary text file.\n"
                consolidate_header += f"5.  Save the final combined file as `{workshop.get('consolidated_source_file', 'consolidated-sources.md')}` in the `consolidated_sources/` directory.\n\n"
                
                batch_size = 10
                for i in range(0, len(all_files_to_consolidate), batch_size):
                    batch_num = i // batch_size + 1
                    batch_files = all_files_to_consolidate[i:i + batch_size]
                    consolidate_header += f"### BATCH {batch_num} FILES TO UPLOAD:\n"
                    for file in batch_files:
                        consolidate_header += f"- `{file}`\n"
                    consolidate_header += "\n"

                full_consolidate_prompt_content = consolidate_header + "\n---\n\n" + final_consolidate_prompt
                consolidation_prompt_filename = os.path.join(OUTPUT_DIR, f"prompt-consolidation-{sanitized_title}.md")

                with open(consolidation_prompt_filename, 'w', encoding='utf-8') as f:
                    f.write(full_consolidate_prompt_content)
                logging.info(f"    ✅ Consolidation prompt saved to '{consolidation_prompt_filename}'")

            except FileNotFoundError:
                logging.error(f"    ❌ Consolidation prompt template not found: '{CONSOLIDATE_PROMPT_FILE}'. Skipping.")
            except IOError as e:
                logging.error(f"    ❌ Could not write consolidation prompt file: {e}")

    logging.info("--- Prompt Generation Finished ---")