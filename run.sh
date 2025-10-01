#!/bin/bash

# This script is the main entry point for the presentation generation pipeline.
# It activates the Python virtual environment and then executes the main
# pipeline orchestrator script (run_pipeline.py).
#
# Any arguments passed to this script (e.g., --force, --json-only)
# will be forwarded directly to the Python script.

# Navigate to the script's directory to ensure correct file paths
cd "$(dirname "$0")"

# Activate the Python virtual environment
source .venv/bin/activate

echo "--- Starting Presentation Generation Pipeline ---"

# Run the main Python orchestrator, passing all script arguments
python3 run_pipeline.py "$@"

echo "--- Pipeline Finished ---"
