# **AI-Powered Presentation Generation Pipeline**

This project provides a powerful, semi-automated pipeline to generate branded Google Slides presentations from a collection of source documents. It uses Gemini to act as a technical content curator, generating a structured JSON representation of the slide deck, which is then used by local scripts to build the final presentation.

The pipeline is designed to be robust and developer-friendly, focusing on a manual "prompt-builder" workflow that does not require direct API access.

## **Features**

- **Automated Document Retrieval**: Downloads all required source PDFs from product documentation sites with a single command.
- **Batch Prompt Generation**: Creates a separate, clean markdown prompt file in the `generated_prompts/` directory for every workshop enabled in `workshops.yaml`.
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

The project is now fully configured and ready to run.

## **The Final Workflow**

The entire process is managed through a series of simple commands using a single script.

### **Step 1: Download Source Documents**

This step uses the `doc_downloader` utility to download all necessary PDF documentation into the `source_documents/` directory.

```bash
# Download all documents defined in the config
./run.sh download-docs
```

### **Step 2: Generate the Prompt File**

This command reads your `workshops.yaml` file and creates a unique, `prompt-WORKSHOP_NAME.md`, file in the `generated_prompts` directory for every workshop that has `enabled: true`.

```bash
# Generate prompts for all enabled workshops
./run.sh generate-prompt
```

### **Step 3: Generate JSON in the Gemini UI**

For each prompt file in the `generated_prompts/` directory.

1. Go to your corporate Gemini web UI (e.g., gemini.google.com).
2. **Open** one of the `prompt-*.md` files. It will tell you exactly which source documents you need to upload for that specific workshop.
3. **Upload those specific source files** using the file attachment feature.
4. **Copy and paste** the entire prompt from the file into the Gemini chat box and submit it.

### **Step 4: Save the JSON Output**

1. **Copy** the complete JSON code block from the Gemini UI.
2. **Save** this content to a new file inside your local `json_source/` directory. It's best practice to name the JSON file after the workshop (e.g., `ocp-baremetal.json`).

Repeat steps 3 and 4 for each prompt section in the consolidated file.

### **Step 5: Extract Images and Build Slides**

1. **Extract Images:**

```bash
./run.sh extract-images
```

2.  This script reads **all** JSON files in the `json_source` directory and extracts the referenced images.
3.  **Build the Final Slides:**

```bash
./run.sh build-slides
```

4.  This script reads **all** JSON files in the `json_source` directory and creates a separate Google Slides presentation for each one.
