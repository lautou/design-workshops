#!/bin/bash

# This script is the main entry point for the presentation generation pipeline.
# It activates the Python virtual environment and then executes the
# main pipeline orchestrator script (run_pipeline.py) or the new
# document downloader.
#
# Any arguments passed to this script (e.g., --force, --json-only)
# will be forwarded directly to the Python script.

# Navigate to the script's directory to ensure correct file paths
cd "$(dirname "$0")"

# Activate the Python virtual environment
source .venv/bin/activate

COMMAND=$1
shift # Remove the command from the arguments list

case "$COMMAND" in
  "generate")
    echo "--- Starting Presentation Generation Pipeline ---"
    # Run the main Python orchestrator, passing all remaining arguments
    python3 run_pipeline.py "$@"
    echo "--- Pipeline Finished ---"
    ;;

  "download-docs")
    echo "--- Starting Document Download and Archiving Process ---"
    # Navigate to the downloader directory and execute its script, passing along any flags like --no-cache
    (cd doc_downloader && ./download_all_docs.sh "$@")
    echo "--- Document Download Finished ---"
    ;;

  *)
    echo "Usage: $0 [generate|download-docs]"
    echo "  generate       : Runs the main slide generation pipeline."
    echo "                   (accepts flags like --generate-prompt, --force)"
    echo "  download-docs  : Runs the script to download source PDFs from the config."
    echo "                   (accepts flags like --no-cache)"
    exit 1
    ;;
esac