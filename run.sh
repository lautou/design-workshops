#!/bin/bash

# This script is the main entry point for the presentation generation pipeline.
# It activates the Python virtual environment and then executes the
# prompt generation script or the document downloader.

# Navigate to the script's directory to ensure correct file paths
cd "$(dirname "$0")"

# Activate the Python virtual environment
source .venv/bin/activate

COMMAND=$1
shift # Remove the command from the arguments list

case "$COMMAND" in
  "generate-prompt")
    echo "--- Starting Prompt Generation ---"
    # Run the Python orchestrator to generate the prompt file. It no longer takes arguments.
    python3 run_pipeline.py
    echo "--- Prompt Generation Finished ---"
    ;;

  "download-docs")
    echo "--- Starting Document Download and Archiving Process ---"
    # Navigate to the downloader directory and execute its script, passing along any flags like --no-cache
    (cd doc_downloader && ./download_all_docs.sh "$@")
    echo "--- Document Download Finished ---"
    ;;

  *)
    echo "Usage: $0 [generate-prompt|download-docs]"
    echo "  generate-prompt: Runs the script to build the prompt file (generated-prompt.md)."
    echo "  download-docs  : Runs the script to download source PDFs from the config."
    echo "                   (accepts flags like --no-cache)"
    exit 1
    ;;
esac
