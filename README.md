# **AI-Powered Presentation Generation Pipeline**

This project provides a powerful, semi-automated pipeline to generate branded Google Slides presentations from a collection of source documents. It uses Gemini to act as a technical content curator, generating a structured JSON representation of the slide deck, which is then used by local scripts to build the final presentation.

The pipeline is designed to be robust and developer-friendly, focusing on a manual "prompt-builder" workflow that does not require direct API access.

## **Features**

- **Automated Document Retrieval**: Downloads all required source PDFs from product documentation sites with a single command.
- **Intelligent Prompt Generation**: Creates tailored prompt files, including a two-step process for workshops that exceed the 10-file upload limit.
- **Flexible Content Scope**: Supports optional, ODF-specific source files to generate tailored content for different customer environments.
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

Open the `.env` file and fill in all the required values.

**Step 2c: Finalize Setup**

Run the installation script again. This time, it will detect your configuration and proceed to automatically create and configure your S3 bucket.

```bash
./install.sh
```

The project is now fully configured and ready to run.

## **The Final Workflow**

The entire process is managed through a series of simple commands using a single script.

### **Step 1: Download Source Documents**

```bash
./run.sh download-docs
```

### **Step 2: Generate the Prompt Files**

This command reads your workshops.yaml file and generates the necessary prompt files in the generated_prompts/ directory for every workshop that has enabled: true.

```bash
./run.sh generate-prompt
```

For workshops with 10 or fewer source files, it will create a single prompt file. For workshops that need consolidation, it will create two: a "Step 1" for consolidation and a "Step 2" for JSON generation.

### **Step 3: Generate JSON in the Gemini UI**

You will now process the files from the generated_prompts/ directory.

#### **For Standard Workshops (Fewer than 10 source files):**

1. Open the prompt-WORKSHOP_NAME.md file.
2. Go to the Gemini UI, upload the required and any optional files listed in the prompt's header.
3. Copy and paste the entire prompt and save the resulting JSON to the json_source/ directory.

#### **For Large Workshops (More than 10 source files):**

This is a two-step process that requires batching to overcome the 10-file limit.

**Step 3a: Consolidate Sources (in Batches)**

1. Open the prompt-consolidation-WORKSHOP_NAME.md file. The header contains critical instructions and lists the source files in numbered batches.
2. For **each batch**, start a new chat in the Gemini UI, upload the files for that batch, and run the consolidation prompt from the bottom of the file.
3. Append the markdown output from each run into a single, temporary text file.
4. Once all batches are processed, save the combined markdown text to the consolidated_sources/ directory with the filename specified in the prompt's instructions.

**Step 3b: Generate the Final JSON**

1. Open the prompt-json-generation-WORKSHOP_NAME.md file.
2. In a **new** Gemini chat, upload only the files it requires (the newly created consolidated file and the \*.adoc files).
3. Copy and paste this second prompt and run it.
4. Save the final JSON output to the json_source/ directory.

### **Step 4: Extract Images and Build Slides**

Once all your JSON files are in the json_source/ directory:

1. **Extract Images:**

```bash
./run.sh extract-images
```

2. **Build the Final Slides:**

```bash
./run.sh build-slides
```
