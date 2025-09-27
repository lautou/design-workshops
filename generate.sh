#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# Activate the Python virtual environment
source .venv/bin/activate

# Run the Python script
python3 md2gslides.py

echo "✅ Slide generation process finished."