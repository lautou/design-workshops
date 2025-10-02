# **AI-Powered Presentation Generation Pipeline**

This project provides a powerful, semi-automated pipeline to generate branded Google Slides presentations from a collection of source documents. It uses Gemini to act as a technical content curator, generating a structured JSON representation of the slide deck, which is then used by local scripts to build the final presentation.

The pipeline is designed to be robust and developer-friendly, with a "prompt-builder" mode to accommodate environments where direct API access is not available.

## **Features**

- **Automated Document Retrieval**: Downloads all required source PDFs from product documentation sites with a single command.
- **File-based Prompt Generation**: Creates a clean markdown file containing the perfect, context-rich prompt for manual execution in the Gemini web UI.
- **Structured JSON Workflow**: The AI generates a clean, structured JSON file, making the pipeline reliable and eliminating parsing errors.
- **AI-Powered Content & Image Curation**: Leverages Gemini to generate all slide text and to identify relevant diagrams in your source PDFs, creating references to them in the generated JSON.
- **Automated Image Extraction**: A separate utility script reads the generated JSON and automatically extracts the referenced images from your source PDFs.
- **Code-Based Validation**: Performs validation of your slide layouts against your Google Slides template _before_ you run the prompt, preventing errors.
- **Secure & Unified Authentication**: Uses a single Google Cloud Service Account for all necessary API interactions (layout validation, slide building).

## **The Streamlined Workflow**

The entire process is managed through a series of simple commands.

### **Step 1: Download Source Documents**

This step uses the `doc_downloader` utility to read the URLs from `doc_downloader/download_config.yaml` and download all the necessary PDF documentation into the `source_documents/` directory.

```bash
# Download all documents defined in the config
./run.sh download-docs

# Force a re-download of all documents, ignoring the cache
./run.sh download-docs --no-cache
```

### **Step 2: Generate the Prompt File**

Use the --generate-prompt flag. The script will read your workshops.yaml file, construct the full, context-rich prompt for the first enabled workshop, and save it to generated-prompt.md.

```bash
# Make sure the virtual environment is active
source .venv/bin/activate

# Generate the prompt for the first enabled workshop
./run.sh generate --generate-prompt
```

### **Step 3: Generate JSON in the Gemini UI**

Go to your corporate Gemini web UI (e.g., gemini.google.com).

Open the generated-prompt.md file. It will tell you exactly which source documents you need to upload.

Upload the required source files using the file attachment feature.

Copy and paste the entire prompt from generated-prompt.md into the Gemini chat box.

Submit the prompt. Gemini will process your files and generate the JSON output.

### **Step 4: Save the JSON Output**

Copy the complete JSON code block from the Gemini UI.

Save this content to a new file inside your local json_source/ directory. Give it a descriptive name (e.g., 01-basic-concepts.json).

### **Step 5: Extract Images and Build Slides**

Now that you have the curated JSON locally, you can use the automated downstream scripts via the run_build.sh wrapper.

Extract Images:

```bash
./run_build.sh extract
```

Check the extracted_images/ directory to ensure the diagrams were pulled correctly.

Build the Final Slides:

```bash
./run_build.sh build
```

Your final presentation will be created in the Google Drive folder specified in your .env configuration.
