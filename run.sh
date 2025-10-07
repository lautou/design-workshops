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
  "generate-prompt")
    echo "--- Starting Prompt Generation ---"
    python3 generate_prompt.py
    echo "--- Prompt Generation Finished ---"
    ;;

  "download-docs")
    echo "--- Starting Document Download Process ---"
    (cd doc_downloader && ./download_all_docs.sh "$@")
    echo "--- Document Download Finished ---"
    ;;

  "extract-images")
    echo "--- Running Image Extraction ---"
    python3 extract_images.py
    ;;

  "build-slides")
    echo "--- Running Slide Generation from JSON ---"
    python3 build_slides_from_json.py
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