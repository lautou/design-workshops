#!/bin/bash

echo "--- Setting up md2gslides Environment ---"

# --- Step 1: Check for necessary commands ---
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: python3 is not installed. Please install Python 3 and try again."
    exit 1
fi

if ! command -v python3 -m venv &> /dev/null
then
    echo "❌ Error: python3-venv is not installed. Please install it (e.g., 'sudo dnf install python3-venv' on Fedora) and try again."
    exit 1
fi

# --- Step 2: Create and activate virtual environment ---
echo "✅ Found Python 3. Creating virtual environment in './.venv'..."
python3 -m venv .venv
source .venv/bin/activate

# --- Step 3: Install dependencies ---
if [ -f "requirements.txt" ]; then
    echo "✅ Virtual environment activated. Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "❌ Error: requirements.txt not found. Cannot install dependencies."
    exit 1
fi

# --- Step 4: Create configuration files from examples ---
CONFIG_FILES=(".env" "layouts.yaml")
for file in "${CONFIG_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        if [ -f "$file.example" ]; then
            echo "✅ Creating '$file' from example..."
            cp "$file.example" "$file"
        else
            echo "⚠️ Warning: '$file.example' not found. Please create '$file' manually."
        fi
    else
        echo "✅ '$file' already exists. Skipping creation."
    fi
done

echo ""
echo "--- ✅ Setup Complete! ---"
echo ""
echo "Next Steps:"
echo "1. Place your service account key in this directory and rename it to 'service-account.json'."
echo "2. Edit the '.env' file and fill in your Google Drive IDs and the TARGET_THEME_NAME."
echo "3. Edit the 'layouts.yaml' file to match your template's layout names."
echo "4. Add your Markdown files to the 'markdown_source/' directory."
echo "5. Run the tool using './generate.sh' or 'python3 md2gslides.py'."

