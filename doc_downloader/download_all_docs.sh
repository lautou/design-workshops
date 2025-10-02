#!/bin/bash

# ==============================================================================
# Red Hat Docs Archiver - Bulk Downloader
#
# Description:
#   This script reads URLs from download_config.yaml, finds all documentation
#   guides for each, and downloads the full PDF to the central
#   'source_documents' directory. It skips files that already exist.
#
# Usage:
#   ./download_all_docs.sh [--no-cache]
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status.

# --- Configuration ---
CONFIG_FILE="download_config.yaml"
# Output directory is now the main project's source folder
OUTPUT_DIRECTORY="../source_documents"
CACHE_MODE="true"

# --- Argument Parsing ---
if [[ "$1" == "--no-cache" ]]; then
  CACHE_MODE="false"
  echo "ℹ️ Caching is DISABLED. All files will be re-downloaded."
fi

# --- Function to process a single HTML URL and download its PDF ---
process_url() {
    local html_url=$1
    local output_dir=$2
    local cache_enabled=$3

    local product=$(echo "$html_url" | awk -F'/' '{print $6}')
    local version=$(echo "$html_url" | awk -F'/' '{print $7}')
    local topic=$(basename "$html_url")
    local product_formatted=$(echo "$product" | tr '_' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1' | tr ' ' '_')
    local local_file_path="${output_dir}/${product_formatted}_${version}_-_${topic}.pdf"

    if [[ "$cache_enabled" == "true" && -f "$local_file_path" ]]; then
        echo "➡️  Skipping (file already exists): $(basename "$local_file_path")"
        return
    fi

    echo "--- Downloading PDF for: $topic ---"
    local topic_formatted=$(echo "$topic" | tr '_' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1' | tr ' ' '_')
    local pdf_filename="${product_formatted}-${version}-${topic_formatted}-en-US.pdf"
    local pdf_url="https://docs.redhat.com/en/documentation/${product}/${version}/pdf/${topic}/${pdf_filename}"

    echo "   Source: $pdf_url"

    http_code=$(curl --silent --location --output "$local_file_path" --write-out "%{http_code}" "$pdf_url")

    if [[ "$http_code" -eq 200 ]]; then
        echo "✅ Download successful: $(basename "$local_file_path")"
    else
        echo "❌ Download failed (HTTP: $http_code) for: $(basename "$local_file_path")"
        rm -f "$local_file_path"
    fi
}

# --- Main Script Logic ---
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Error: Configuration file '$CONFIG_FILE' not found." >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIRECTORY"
echo "✅ Files will be saved in the directory: '$OUTPUT_DIRECTORY'"

# Read URLs from YAML file (basic parsing, requires yq for robustness in future)
URLS=$(grep -E '^\s*-\s*' "$CONFIG_FILE" | sed 's/^\s*-\s*//' | tr -d '"'\'')

if [ -z "$URLS" ]; then
    echo "⚠️ Warning: No URLs found in '$CONFIG_FILE'." >&2
    exit 0
fi

for URL in $URLS; do
    echo ""
    echo "=========================================================="
    echo "🔎 Processing Product URL: $URL"
    echo "=========================================================="
    
    FINAL_URL=$(curl -s -L -o /dev/null -w '%{url_effective}' "$URL")
    echo "✅ Final URL is: $FINAL_URL"

    PRODUCT_SLUG=$(echo "$FINAL_URL" | awk -F'/' '{print $6}')

    curl -s -L "$FINAL_URL" | \
        grep -o "href=\"/en/documentation/${PRODUCT_SLUG}/[^\" ]*/html/[^\" ]*\"" | \
        sed 's/href="\([^"]*\)"/\1/' | \
        sed 's|/index$||' | \
        sort -u | \
        while read -r relative_url; do
            full_url="https://docs.redhat.com${relative_url}"
            process_url "$full_url" "$OUTPUT_DIRECTORY" "$CACHE_MODE"
        done
done

echo ""
echo "✅ All downloads attempted."