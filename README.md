# **Markdown to Google Slides Generator (md2gslides)**

This project provides a powerful, fully automated pipeline to generate branded Google Slides presentations. It uses Gemini via the Vertex AI API to create technical content from a prompt and then converts the resulting Markdown into a polished presentation.

It's designed for batch processing, allowing you to convert an entire list of workshop titles into professional-looking presentations with a single command, enforcing brand consistency through the use of a master Google Slides template.

## **Features**

- **End-to-End Automation**: A single script (run_pipeline.py) manages the entire workflow from prompt to final presentation.
- **AI-Powered Content Generation**: Leverages Gemini through the enterprise-grade Vertex AI API to create the initial Markdown content for each presentation.
- **Efficient Caching**: Avoids unnecessary downloads and API calls by hashing Google Drive file metadata. Regeneration only occurs when source documents actually change.
- **Developer Controls**: Includes command-line flags to \--force regeneration (bypassing the cache) and to run in \--md-only mode for quick content validation.
- **Secure Cloud Authentication**: Uses a single Google Cloud Service Account for secure, non-interactive authentication for all Google Cloud services.
- **Rich Text & Table Formatting**: Automatically converts Markdown into formatted slide content, including bold/italic text, nested lists, and perfectly centered tables.

## **Pipeline Overview**

The tool operates in a two-stage pipeline orchestrated by the main run_pipeline.py script. It checks for changes in your source documents, generates the markdown, and then builds the final slide deck.

\+-------------------------+ \+---------------------------+ \+---------------------------+  
| Google Drive Folder |-----\>| run_pipeline.py |-----\>| Markdown Files |  
| (Source Docs & PDFs) | | (Checks Metadata Hash) | | (source_markdown/) |  
\+-------------------------+ \+---------------------------+ \+---------------------------+  
 ^ |  
 | | (If Hash Mismatch or \--force)  
 | V  
\+-------------------------+ \+---------------------------+  
| workshops.yaml |-----\>| Call Vertex AI Gemini |  
| (Controls which | | (Generates MD Content) |  
| workshops to build) | \+---------------------------+  
\+-------------------------+ |  
 | (Executes next step)  
 V  
\+-------------------------+ \+---------------------------+ \+---------------------------+  
| md2gslides.py |-----\>| Google Slides & Drive |-----\>| Generated Presentations |  
| (Converts MD to Slides) | | APIs | | (In Google Drive) |  
\+-------------------------+ \+---------------------------+ \+---------------------------+

## **Setup Guide**

Follow these steps to set up the environment. This involves a one-time setup on Google Cloud, followed by a simple local installation.

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

1. **Clone the Repository**:  
   git clone \<your-repository-url\>  
   cd \<your-repository-name\>

2. **Run the Install Script**: This script will create a Python virtual environment, install all dependencies from requirements.txt, and create your local configuration files from the examples.  
   chmod \+x install.sh  
   ./install.sh

3. **Configure Your Project**:
   - **Service Account**: Place your downloaded JSON key file into the project's root directory and rename it to service-account.json.
   - **.env file**: Open the newly created .env file and fill in all the required values based on your Google Cloud and Drive setup.
   - **layouts.yaml**: Open layouts.yaml and adjust the mappings to match the "Display names" of the layouts in your specific Google Slides template.

## **Usage**

The pipeline is controlled via the run_pipeline.py script, which now accepts command-line arguments for development flexibility.

### **Basic Run**

This command will use the efficient caching. It will only download documents and run the AI generation if it detects a change in the source Google Drive folder.

\# Ensure your virtual environment is active  
source .venv/bin/activate

\# Run the full pipeline with caching enabled  
python3 run_pipeline.py

### **Development Options**

These flags are essential when you are curating the AI prompt and validating the output.

**1\. Force Regeneration (--force)**

Use this when you have updated your prompt (gemini-prompt-generate-md-files.md) and want to regenerate the Markdown, even if your source documents in Google Drive have not changed.

python3 run_pipeline.py \--force

**2\. Markdown Only (--md-only)**

Use this to run only the AI generation stage and stop before creating the Google Slides. This is very useful for quickly checking the quality of the generated .md files.

python3 run_pipeline.py \--md-only

You can also combine these flags:

\# Force a regeneration of the Markdown, but don't create the slides yet  
python3 run_pipeline.py \--force \--md-only
