#!/bin/bash

# This script provides a convenient wrapper for the downstream build and
# extraction processes. It activates the virtual environment and then
# runs the specified Python script.

# --- Usage ---
# ./run_build.sh extract   -> Runs the image extraction script
# ./run_build.sh build     -> Runs the JSON-to-Slides build script

# Navigate to the script's directory
cd "$(dirname "$0")"

# Activate the Python virtual environment
source .venv/bin/activate

if [ "$1" == "extract" ]; then
    echo "--- Running Image Extraction ---"
    python3 extract_images.py
elif [ "$1" == "build" ]; then
    echo "--- Running Slide Generation from JSON ---"
    python3 build_slides_from_json.py
else
    echo "Usage: $0 [extract|build]"
    echo "  extract: Runs the image extraction script."
    echo "  build  : Runs the JSON-to-Slides build script."
    exit 1
fi

echo "--- Process Finished ---"
