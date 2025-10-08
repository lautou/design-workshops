#!/bin/bash
# ==============================================================================
# Red Hat Docs Downloader
#
# Description:
#   This script reads product documentation URLs from a YAML config file,
#   scrapes those pages to find all related PDF guides, and downloads them.
#   It supports caching, cleanup, and provides user-friendly output.
#
# Usage:
#   ./run.sh download-docs [--no-cache] [--cleanup]
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status.

# --- Configuration ---
CONFIG_FILE="doc_downloader/download_config.yaml"
DEST_DIR="source_documents/pdf"
LOG_FILE="pipeline.log"
CACHE_MODE="true"
CLEANUP_ENABLED="false"

# --- Argument Parsing ---
for arg in "$@"; do
  case $arg in
    --no-cache)
      CACHE_MODE="false"
      shift # Remove --no-cache from processing
      ;;
    --cleanup)
      CLEANUP_ENABLED="true"
      shift # Remove --cleanup from processing
      ;;
  esac
done

# --- Dependency Check ---
if ! command -v curl &> /dev/null; then
    echo "❌ ERROR: curl is not installed. Please install it to continue." >&2
    exit 1
fi
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ ERROR: Configuration file '$CONFIG_FILE' not found." >&2
    exit 1
fi

# --- Function to process a single HTML URL and download its PDF ---
process_pdf_url() {
    local pdf_url=$1
    local local_file_path=$2
    local cache_enabled=$3

    if [[ "$cache_enabled" == "true" && -f "$local_file_path" ]]; then
        echo "➡️  Skipping (file already exists): $(basename "$local_file_path")" | tee -a "$LOG_FILE"
        return
    fi

    echo "--- Downloading PDF for: $(basename "$local_file_path") ---" | tee -a "$LOG_FILE"
    echo "   Source: $pdf_url" | tee -a "$LOG_FILE"

    # Use curl with a progress bar for better user experience
    curl --progress-bar --location --output "$local_file_path" "$pdf_url"

    # Check if the download was successful by checking if the file has a size greater than zero
    if [[ -s "$local_file_path" ]]; then
        echo "✅ Download successful: $(basename "$local_file_path")" | tee -a "$LOG_FILE"
    else
        echo "❌ Download failed for: $(basename "$local_file_path")" | tee -a "$LOG_FILE"
        rm -f "$local_file_path" # Clean up failed (zero-byte) download
    fi
}

# --- Main Script Logic ---
mkdir -p "$DEST_DIR"

echo "====================================================================" | tee -a "$LOG_FILE"
echo "INFO: Starting document download process..." | tee -a "$LOG_FILE"

if [[ "$CACHE_MODE" == "false" ]]; then
  echo "INFO: Caching is DISABLED by command line. All files will be re-downloaded." | tee -a "$LOG_FILE"
else
  echo "INFO: Caching is ENABLED. Only existing files will be skipped." | tee -a "$LOG_FILE"
fi

# --- Step 1: Generate the complete list of expected files first ---
EXPECTED_FILES_LIST="/tmp/expected_files_$$.txt"
> "$EXPECTED_FILES_LIST" # Create or truncate the file

# This function populates the expected files list.
generate_expected_files() {
    local base_url=$1
    local expected_list_file=$2

    local FINAL_URL=$(curl -s -L -o /dev/null -w '%{url_effective}' "$base_url")
    local PRODUCT_SLUG=$(echo "$FINAL_URL" | awk -F'/' '{print $6}')

    curl -s -L "$FINAL_URL" | \
        grep -o "href=\"/en/documentation/${PRODUCT_SLUG}/[^\" ]*/html/[^\" ]*\"" | \
        sed 's/href="\([^"]*\)"/\1/' | \
        sed 's|/index$||' | \
        sort -u | \
        while read -r relative_url; do
            if [ -z "$relative_url" ]; then continue; fi
            
            local product=$(echo "$relative_url" | awk -F'/' '{print $4}')
            local version=$(echo "$relative_url" | awk -F'/' '{print $5}')
            local topic_path=$(echo "$relative_url" | awk -F'/' '{print $7}')
            local topic=$(basename "$topic_path")
            
            local product_formatted=$(echo "$product" | tr '_' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1' | tr ' ' '_')
            
            local local_filename="${product_formatted}_${version}_-_${topic}.pdf"
            echo "$local_filename" >> "$expected_list_file"
        done
}

# Populate the list from all URLs in the config
sed -n '/^urls:/,$p' "$CONFIG_FILE" | grep -E '^\s*-\s*https://' | sed 's/^\s*-\s*//' | while read -r BASE_URL; do
    generate_expected_files "$BASE_URL" "$EXPECTED_FILES_LIST"
done

# Sort the final list to ensure it's correct for `comm`
sort -u "$EXPECTED_FILES_LIST" -o "$EXPECTED_FILES_LIST"

# --- Step 2: Download the files ---
sed -n '/^urls:/,$p' "$CONFIG_FILE" | grep -E '^\s*-\s*https://' | sed 's/^\s*-\s*//' | while read -r BASE_URL; do
    if [ -z "$BASE_URL" ]; then continue; fi
    echo "" | tee -a "$LOG_FILE"
    echo "==========================================================" | tee -a "$LOG_FILE"
    echo "🔎 Processing Product URL: $BASE_URL" | tee -a "$LOG_FILE"
    echo "==========================================================" | tee -a "$LOG_FILE"

    FINAL_URL=$(curl -s -L -o /dev/null -w '%{url_effective}' "$BASE_URL")
    PRODUCT_SLUG=$(echo "$FINAL_URL" | awk -F'/' '{print $6}')

    curl -s -L "$FINAL_URL" | \
        grep -o "href=\"/en/documentation/${PRODUCT_SLUG}/[^\" ]*/html/[^\" ]*\"" | \
        sed 's/href="\([^"]*\)"/\1/' | \
        sed 's|/index$||' | \
        sort -u | \
        while read -r relative_url; do
            if [ -z "$relative_url" ]; then continue; fi
            
            product=$(echo "$relative_url" | awk -F'/' '{print $4}')
            version=$(echo "$relative_url" | awk -F'/' '{print $5}')
            topic_path=$(echo "$relative_url" | awk -F'/' '{print $7}')
            topic=$(basename "$topic_path")
            
            product_formatted=$(echo "$product" | tr '_' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1' | tr ' ' '_')
            topic_formatted=$(echo "$topic" | tr '_' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1' | tr ' ' '_')
            
            pdf_filename="${product_formatted}-${version}-${topic_formatted}-en-US.pdf"
            pdf_url="https://docs.redhat.com/en/documentation/${product}/${version}/pdf/${topic}/${pdf_filename}"
            local_filename="${product_formatted}_${version}_-_${topic}.pdf"
            local_filepath="${DEST_DIR}/${local_filename}"

            process_pdf_url "$pdf_url" "$local_filepath" "$CACHE_MODE"
        done
done

echo "" | tee -a "$LOG_FILE"
echo "INFO: All downloads attempted." | tee -a "$LOG_FILE"

# --- Step 3: Cleanup Process ---
if [[ "$CLEANUP_ENABLED" == "true" ]]; then
  echo "====================================================================" | tee -a "$LOG_FILE"
  echo "INFO: Starting cleanup of orphan documents..." | tee -a "$LOG_FILE"

  # Safety check: ensure the expected files list is not empty
  if [ ! -s "$EXPECTED_FILES_LIST" ]; then
    echo "❌ ERROR: The list of expected files is empty. Aborting cleanup to prevent data loss." | tee -a "$LOG_FILE"
    rm -f "$EXPECTED_FILES_LIST"
    exit 1
  fi

  ACTUAL_FILES_LIST="/tmp/actual_files_$$.txt"
  find "$DEST_DIR" -maxdepth 1 -type f -name "*.pdf" -printf "%f\n" | sort > "$ACTUAL_FILES_LIST"

  ORPHAN_FILES=$(comm -13 "$EXPECTED_FILES_LIST" "$ACTUAL_FILES_LIST")

  if [ -z "$ORPHAN_FILES" ]; then
    echo "INFO: No orphan files found. Directory is clean." | tee -a "$LOG_FILE"
  else
    echo "$ORPHAN_FILES" | while read -r orphan; do
      if [ -n "$orphan" ]; then
        echo "🗑️  Deleting orphan file: $orphan" | tee -a "$LOG_FILE"
        rm -f "$DEST_DIR/$orphan"
      fi
    done
    echo "INFO: Cleanup complete." | tee -a "$LOG_FILE"
  fi

  rm -f "$EXPECTED_FILES_LIST" "$ACTUAL_FILES_LIST"
else
  echo "INFO: Skipping cleanup. To enable, run with the --cleanup flag." | tee -a "$LOG_FILE"
fi

echo "====================================================================" | tee -a "$LOG_FILE"