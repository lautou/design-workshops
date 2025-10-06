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
if [ ! -d ".venv" ]; then
    echo "✅ Found Python 3. Creating virtual environment in './.venv'..."
    python3 -m venv .venv
fi
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

# --- Step 5: Check if .env is configured ---
# Source the .env file to check variables
set -a 
source .env
set +a

if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo ""
    echo "🛑 ACTION REQUIRED: Configuration needed."
    echo "   Please edit the '.env' file with your AWS credentials and other settings."
    echo "   Once you have saved your changes, re-run this script './install.sh' to complete the setup."
    echo ""
    exit 0
fi

# --- Step 6: Setup AWS S3 Bucket (only runs if .env is configured) ---
echo "✅ Configuration found. Running S3 bucket setup script..."
python3 create_s3_bucket.py

echo ""
echo "--- ✅ Setup Complete! ---"
echo ""
echo "Next Steps:"
echo "1. If you haven't already, place your Google Cloud 'credentials.json' in this directory."
echo "2. Edit the 'layouts.yaml' file to match your template's layout names if needed."
echo "3. You are now ready to use the './run.sh' and './run_build.sh' scripts."