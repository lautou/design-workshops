# Red Hat Docs Archiver

A collection of scripts to automatically download the complete PDF documentation for a specific Red Hat OpenShift Container Platform version and upload it to your Google Drive.

## Features

-   **Automatic Scraping**: Discovers all official documentation guides from a single URL.
-   **Handles Redirects**: Correctly resolves version-specific URLs even when you provide a `latest` link.
-   **Efficient Caching**: Efficient Caching: By default, the script will not re-download PDFs that already exist in the local directory, saving time and bandwidth on subsequent runs.
-   **Flexible Google Drive Integration**:
    -   Upload all PDFs individually (default).
    -   **Merge**: Combine all PDFs into a single document. If the combined file exceeds 100 MB, it is automatically split into multiple parts.
    -   **Split**: Upload all PDFs into numbered sub-folders (10 files per folder) for better organization.

## Requirements

-   **Shell Environment**: A bash-compatible shell.
-   **Command-line Tools**: `curl`, `grep`, `sed`, `awk`, `sort`.
-   **Python**: Python 3.6+ and `pip`.
-   **Python Libraries**: `PyPDF2` and Google API Client libraries.

## How to Use

The entire process is managed by the main `run_archiver.sh` script.

### Step 1: First-Time Setup

Before you can run the main script, you must perform a one-time setup to install dependencies and authorize Google Drive access.

**Follow the detailed instructions in the [google_drive_setup.md](./google_drive_setup.md) file.** This is a critical step.

### Step 2: Run the Archiver

Use the `run_archiver.sh` script to fetch the PDFs and upload them to Google Drive.

1.  Make the main script executable:
    ```bash
    chmod +x run_archiver.sh
    ```

2.  Run the script with the URL of the documentation and any optional flags.

    **Default (Upload all files, using local cache)**
    ```bash
    ./run_archiver.sh "[https://docs.redhat.com/en/documentation/openshift_container_platform/latest](https://docs.redhat.com/en/documentation/openshift_container_platform/latest)"
    ```

    **Merge into a Single PDF**
    ```bash
    ./run_archiver.sh "[https://docs.redhat.com/en/documentation/openshift_container_platform/latest](https://docs.redhat.com/en/documentation/openshift_container_platform/latest)" --merge
    ```

    **Disable Caching (Force re-download of all files)**
    ```bash
    ./run_archiver.sh "[https://docs.redhat.com/en/documentation/openshift_container_platform/latest](https://docs.redhat.com/en/documentation/openshift_container_platform/latest)" --no-cache
    ```

The script will first download all the documents into a local folder (e.g., `openshift_container_platform_4.19_Docs`) and then perform the specified upload action to your Google Drive.
