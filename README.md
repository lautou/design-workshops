# **AI-Powered Presentation Generation Pipeline**

This project provides a powerful, fully automated pipeline to generate branded Google Slides presentations from a collection of source documents. It uses Gemini via the Vertex AI API to act as a technical content curator, generating a structured JSON representation of the slide deck, including references to relevant images within your documents.

The pipeline is designed to be robust, maintainable, and developer-friendly, with features like efficient caching and fine-grained execution control.

## **Features**

- **Structured JSON Workflow**: The AI generates a clean, structured JSON file, not Markdown. This eliminates parsing errors and creates a reliable "contract" between the AI and the slide generation script.
- **AI-Powered Content & Image Curation**: Leverages Gemini to generate all slide text and to identify relevant diagrams in your source PDFs, creating references to them in the generated JSON.
- **Automated Image Extraction**: A separate utility script reads the generated JSON and automatically extracts the referenced images from your source PDFs into a local directory.
- **Efficient Metadata Caching**: Avoids unnecessary document downloads and expensive API calls by hashing the metadata of your Google Drive source folder. Regeneration only occurs when your source material actually changes.
- **Developer Controls**: Includes command-line flags to \--force regeneration (bypassing the cache) and to run in \--json-only mode for quick content validation.
- **Secure & Unified Authentication**: Uses a single Google Cloud Service Account for secure, non-interactive authentication across all Google Cloud services (Vertex AI, Drive, Slides).

## **Pipeline Overview**

The project is split into two main stages: Content Generation (managed by run.sh and run_pipeline.py) and Image Extraction (managed by extract_images.py).

**Stage 1: Content Generation (./run.sh)**

\+-------------------------+ \+---------------------------+ \+---------------------------+  
| Google Drive Folder |-----\>| run_pipeline.py |-----\>| JSON Files |  
| (Source Docs & PDFs) | | (Checks Metadata Hash) | | (in json_source/) |  
\+-------------------------+ \+---------------------------+ \+---------------------------+  
 ^ |  
 | | (If Hash Mismatch or \--force)  
 | V  
\+-------------------------+ \+---------------------------+  
| workshops.yaml |-----\>| Call Vertex AI Gemini |  
| (Controls which | | (Generates JSON) |  
| workshops to build) | \+---------------------------+  
\+-------------------------+ |  
 | (Executes next step, unless \--json-only)  
 V  
\+-------------------------+ \+---------------------------+ \+---------------------------+  
| build_slides_from_json.py|-----\>| Google Slides & Drive |-----\>| Generated Presentations |  
| (Converts JSON to Slides)| | APIs | | (In Google Drive) |  
\+-------------------------+ \+---------------------------+ \+---------------------------+

**Stage 2: Image Extraction (python3 extract_images.py)**

\+-------------------------+ \+---------------------------+ \+---------------------------+  
| JSON Files |-----\>| extract_images.py |-----\>| Extracted Images |  
| (in json_source/) | | (Reads imageReference) | | (in extracted_images/) |  
\+-------------------------+ \+---------------------------+ \+---------------------------+  
 ^ |  
 | |  
\+-------------------------+ |  
| Source Documents |------------------+  
| (Local copy for speed) |  
\+-------------------------+

## **Setup Guide**

Follow these steps to set up the environment.

### **Step 1: Google Cloud & Drive Setup (One-Time)**

1. **Create a Google Cloud Project**: If you don't have one, create a new project in the [Google Cloud Console](https://console.cloud.google.com/). Note your **Project ID**.
2. **Enable APIs**: In your project, search for and enable the following three APIs:
   - Google Drive API
   - Google Slides API
   - **Vertex AI API**
3. **Create a Service Account**:
   - Navigate to **IAM & Admin \> Service Accounts**.
   - Click **Create Service Account**, give it a name (e.g., slides-generator), and click **Done**.
   - Go to the **IAM** page. Click **Grant Access**, and in the "New principals" field, add the service account's email.
   - Assign it the role of **Vertex AI User**.
   - Back in the **Service Accounts** page, click the **Actions** menu (⋮) for your new account, select **Manage keys**, and then **Add Key \> Create new key**. Choose **JSON**.
   - A JSON key file will be downloaded. This is your authentication key.
4. **Create a Shared Drive**: In Google Drive, create a new **Shared Drive** (e.g., "Automated Presentations"). This is crucial for the service account to have the correct permissions.
5. **Add Service Account as Member**:
   - Open your downloaded JSON key file and copy the client_email address.
   - Go to your new Shared Drive in Google Drive, click **Manage members**, and paste the service account's email.
   - Assign it the role of **Content manager** and click **Send**.
6. **Prepare Assets in Shared Drive**:
   - Create a folder inside the Shared Drive to store the final presentations (e.g., "Generated Slides"). **Note its ID** from the URL.
   - Place your **Google Slides Template** inside the Shared Drive. **Note its ID** from the URL.

### **Step 2: Local Project Setup**

1. **Clone the Repository** and navigate into the directory.
2. **Run the Install Script**: This creates a Python virtual environment and installs all dependencies from requirements.txt, including PyMuPDF for image extraction.  
   chmod \+x install.sh  
   ./install.sh

3. **Configure .env**: Fill in all the required values in your .env file (Project ID, folder IDs, etc.).
4. **Configure workshops.yaml**: Edit this file to control which workshops you want to generate by setting enabled: true or enabled: false.

## **Usage and Development Workflow**

The pipeline is controlled via the new run.sh script, which is a simple wrapper for run_pipeline.py.

### **Recommended Development Workflow**

This workflow allows you to iterate on the AI prompt and curate the content efficiently.

Step 1: Generate the JSON Content  
Use the \--force flag to ensure you're getting fresh output based on your latest prompt changes, and \--json-only to stop before the slower slide-building step.  
\# Make sure the virtual environment is active  
source .venv/bin/activate

\# Force a new AI run and stop after creating the JSON file(s)  
./run.sh \--force \--json-only

Step 2: Review and Curate  
Inspect the generated .json file(s) in the json_source/ directory. Check if the text is correct and if the imageReference blocks are present and accurate. If not, refine your master prompt (gemini-prompt-generate-json.md) and repeat Step 1\.  
Step 3: Extract Images  
Once you are happy with the JSON, run the image extraction script. This step requires a local copy of your source PDFs in a source_documents/ directory for the script to access.  
\# (First, ensure source_documents/ contains your PDFs)  
python3 extract_images.py

Check the extracted_images/ directory to ensure the correct diagrams were pulled.

Step 4: Generate the Final Slides  
When the JSON and images are validated, run the full pipeline without the \--json-only flag. It will use the cached content from your last run to quickly build the final presentations.  
./run.sh
