# **AI-Powered Presentation Generation Pipeline**

This project provides a powerful, semi-automated pipeline to generate branded Google Slides presentations from a collection of source documents. It uses Gemini to act as a technical content curator, generating a structured JSON representation of the slide deck, which is then used by local scripts to build the final presentation.

The pipeline is designed to be robust and developer-friendly, focusing on a manual "prompt-builder" workflow that does not require direct API access.

## **Features**

- **Automated Document Retrieval**: Downloads all required source PDFs from product documentation sites with a single command.
- **File-based Prompt Generation**: Creates a clean markdown file containing the perfect, context-rich prompt for manual execution in the Gemini web UI.
- **Structured JSON Workflow**: The AI generates a clean, structured JSON file, making the pipeline reliable and eliminating parsing errors.
- **AI-Powered Content & Image Curation**: Leverages Gemini to generate all slide text and to identify relevant diagrams in your source PDFs.
- **Automated Image Extraction & Cloud Upload**: Automatically extracts referenced images and uploads them to a public AWS S3 bucket for seamless integration into Google Slides.
- **User-Based Authentication**: Securely authenticates to Google APIs using a standard OAuth 2.0 flow, allowing the script to act on your behalf.

## **Setup Guide**

Follow these steps for a one-time setup of the project.

### **1\. Prerequisite: Google Cloud Setup**

Follow the instructions in **OAUTH_SETUP.md** to create a Google Cloud `credentials.json` file. This allows the script to authenticate as you to create and edit Google Slides. Place the downloaded `credentials.json` in the project's root directory.

### **2\. Project Installation (A Two-Step Process)**

The installation is a two-step process to ensure credentials are in place before creating cloud resources.

**Step 2a: Initial Setup**

First, run the installation script. It will create a Python virtual environment, install the required dependencies, and create a `.env` file for you.

```bash
./install.sh
```

The script will stop and prompt you to configure the newly created `.env` file.

**Step 2b: Configure Your `.env` File**

Open the `.env` file and fill in all the required values:

- `TEMPLATE_PRESENTATION_ID`
- `OUTPUT_FOLDER_ID`
- `TARGET_THEME_NAME`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `S3_BUCKET_NAME` (choose a globally unique name)
- `AWS_REGION`

**Step 2c: Finalize Setup**

Run the installation script again. This time, it will detect your configuration and proceed to automatically create and configure your S3 bucket.

Bash

```
./install.sh
```

The project is now fully configured and ready to run.

## **The Final Workflow**

The entire process is managed through a series of simple commands.

### **Step 1: Download Source Documents**

This step uses the `doc_downloader` utility to read the URLs from `doc_downloader/download_config.yaml` and download all the necessary PDF documentation into the `source_documents/` directory.

Bash

```
# Download all documents defined in the config
./run.sh download-docs

# Force a re-download of all documents, ignoring the cache
./run.sh download-docs --no-cache
```

### **Step 2: Generate the Prompt File**

This command reads your `workshops.yaml` file, constructs the full prompt for the first enabled workshop, and saves it to `generated-prompt.md`.

Bash

```
# Generate the prompt for the first enabled workshop
./run.sh generate-prompt
```

### **Step 3: Generate JSON in the Gemini UI**

1. Go to your corporate Gemini web UI (e.g., gemini.google.com).
2. **Open** the `generated-prompt.md` file. It will tell you exactly which source documents you need to upload.
3. **Upload the required source files** using the file attachment feature.
4. **Copy and paste** the entire prompt from `generated-prompt.md` into the Gemini chat box and submit it.

### **Step 4: Save the JSON Output**

1. **Copy** the complete JSON code block from the Gemini UI.
2. **Save** this content to a new file inside your local `json_source/` directory (e.g., `result.json`).

### **Step 5: Extract Images and Build Slides**

1. **Extract Images:**  
   Bash

```
 ./run_build.sh extract
```

2.  This script reads your new JSON file and extracts the referenced images into the `extracted_images/` directory.
3.  **Build the Final Slides:**  
    Bash

```
 ./run_build.sh build
```

4.  The first time you run this, it will open a browser for you to log in and authorize the script. On subsequent runs, it will use a saved `token.json` file. This script will:

- Authenticate with your Google and AWS accounts.
- Create a new Google Slides presentation in your specified output folder.
- Upload the extracted images to your AWS S3 bucket.
- Build the slides, inserting text and the public S3 image URLs.
