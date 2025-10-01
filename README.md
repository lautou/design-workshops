# **AI-Powered Presentation Generation Pipeline**

This project provides a powerful, semi-automated pipeline to generate branded Google Slides presentations from a collection of source documents. It uses Gemini to act as a technical content curator, generating a structured JSON representation of the slide deck, which is then used by local scripts to build the final presentation.

The pipeline is designed to be robust and developer-friendly, with a "prompt-builder" mode to accommodate environments where direct API access is not available.

## **Features**

- **Semi-Automated Workflow**: Includes a "prompt builder" mode that generates the perfect, context-rich prompt for manual execution in the Gemini web UI.
- **Structured JSON Workflow**: The AI generates a clean, structured JSON file, making the pipeline reliable and eliminating parsing errors.
- **AI-Powered Content & Image Curation**: Leverages Gemini to generate all slide text and to identify relevant diagrams in your source PDFs, creating references to them in the generated JSON.
- **Automated Image Extraction**: A separate utility script reads the generated JSON and automatically extracts the referenced images from your source PDFs.
- **Code-Based Validation**: Performs validation of your slide layouts against your Google Slides template _before_ you run the prompt, preventing errors.
- **Secure & Unified Authentication**: Uses a single Google Cloud Service Account for all necessary API interactions (layout validation, slide building).

## **Pipeline Overview**

The project is now split into a manual generation step and an automated build step.

**Stage 1: Prompt Generation & Manual Execution**

\+---------------------------+ \+-------------------------+ \+---------------------------+  
| run_pipeline.py |-----\>| User Console |-----\>| Gemini Web UI |  
| (with \--show-prompt) | | (Displays full prompt) | | (User uploads files |  
\+---------------------------+ \+-------------------------+ | & pastes prompt) |  
 \+-------------+-------------+  
 |  
 | (User copies JSON output)  
 V  
 \+---------------------------+  
 | JSON Files |  
 | (User saves to json_source/) |  
 \+---------------------------+

**Stage 2: Automated Build & Extraction (./run.sh or manual script calls)**

\+-------------------------+ \+---------------------------+ \+---------------------------+  
| JSON Files |-----\>| extract_images.py |-----\>| Extracted Images |  
| (in json_source/) | | (Reads imageReference) | | (in extracted_images/) |  
\+-------------------------+ \+---------------------------+ \+---------------------------+

\+-------------------------+ \+---------------------------+ \+---------------------------+  
| JSON Files |-----\>| build_slides_from_json.py |-----\>| Generated Presentations |  
| (in json_source/) | | (Builds slides) | | (In Google Drive) |  
\+-------------------------+ \+---------------------------+ \+---------------------------+

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

## **Usage: The Semi-Automated Workflow**

Due to limitations on programmatic API access, this workflow allows you to leverage the pipeline's intelligence by preparing a perfect prompt for manual execution.

### **Step 1: Prepare the Prompt**

Use the \--show-prompt flag. The script will read your workshops.yaml file, construct the full, context-rich prompt for the first enabled workshop, and print it to your console.

\# Make sure the virtual environment is active  
source .venv/bin/activate

\# Generate the prompt for the first enabled workshop in workshops.yaml  
./run.sh \--show-prompt

### **Step 2: Generate JSON in the Gemini UI**

1. Go to your corporate Gemini web UI (e.g., gemini.google.com).
2. **Upload your source files.** Use the file attachment feature to upload all the relevant .pdf and .adoc documents.
3. **Copy and paste** the entire prompt from your console output into the Gemini chat box.
4. Submit the prompt. Gemini will process your files and generate the JSON output.

### **Step 3: Save the JSON Output**

1. **Copy** the complete JSON code block from the Gemini UI.
2. **Save** this content to a new file inside your local json_source/ directory. Give it a descriptive name (e.g., 01-basic-concepts.json).

### **Step 4: Extract Images and Build Slides**

Now that you have the curated JSON locally, you can use the automated downstream scripts.

1. **Extract Images:**  
   python3 extract_images.py

   Check the extracted_images/ directory to ensure the diagrams were pulled correctly.

2. **Build the Final Slides:** Run the build_slides_from_json.py script.  
   python3 build_slides_from_json.py
