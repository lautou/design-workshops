#!/bin/bash

# This script is the main entry point for the presentation generation pipeline.
# It provides commands for the entire workflow, from downloading source
# documents to building the final presentation.

# Navigate to the script's directory to ensure correct file paths
cd "$(dirname "$0")"

# Activate the Python virtual environment
source .venv/bin/activate

COMMAND=$1
shift # Remove the command from the arguments list

case "$COMMAND" in
  "build-slides")
    echo "--- Running Slide Generation from JSON ---"
    python3 build_slides_from_json.py
    ;;

  "download-docs")
  echo "===================================================================="
  echo "INFO: Downloading all documentation from config..."
  echo "===================================================================="
  ./doc_downloader/download_all_docs.sh "$@"
  ;;

  "extract-images")
    echo "--- Running Image Extraction ---"
    python3 extract_images.py
    ;;

  "generate-prompt")
    echo "--- Starting Prompt Generation ---"
    python3 generate_prompt.py
    echo "--- Prompt Generation Finished ---"
    ;;

  "map-kb")
    echo "===================================================================="
    echo "INFO: Mapping Knowledge Base to workshops.yaml..."
    echo "===================================================================="
    python3 map_kb.py
    ;;

  "prepare-kb")
    echo "===================================================================="
    echo "INFO: Preparing Knowledge Base by converting all PDFs to Markdown..."
    echo "===================================================================="
    python3 prepare_kb.py
    ;;
  *)
    echo "Usage: $0 [generate-prompt|download-docs|extract-images|build-slides]"
    echo "  generate-prompt: Builds the prompt file (generated-prompt.md)."
    echo "  download-docs  : Downloads source PDFs from the config (accepts --no-cache)."
    echo "  extract-images : Extracts image references from the generated JSON file."
    echo "  build-slides   : Builds the Google Slides presentation from the JSON file."
    exit 1
    ;;
esac

echo "--- Process Finished ---"