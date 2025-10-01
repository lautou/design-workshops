# **Markdown to Google Slides AI Pipeline**

This project provides a powerful, fully automated pipeline to generate branded Google Slides presentations. It uses Gemini via the Google Cloud Vertex AI API to create technical content from a prompt and then converts the resulting Markdown into a polished presentation using the Google Slides API.

It's designed for batch processing, allowing you to convert an entire list of workshop titles into professional-looking presentations with a single command, enforcing brand consistency through the use of a master Google Slides template.

## **Pipeline Overview**

The tool operates in a two-stage pipeline orchestrated by the main run\_pipeline.py script. This creates a seamless flow from a simple idea to a finished slide deck.

\+--------------------------+      \+--------------------------+      \+---------------------------+  
|      Workshop Titles     |-----\>|     run\_pipeline.py      |-----\>|      Markdown Files       |  
| (Defined in Python list) |      | (Calls Vertex AI Gemini) |      | (Saved in source\_source/) |  
\+--------------------------+      \+--------------------------+      \+---------------------------+  
                                               |  
                                               | (Executes next step)  
                                               V  
\+--------------------------+      \+--------------------------+      \+---------------------------+  
|      md2gslides.py       |-----\>|   Google Slides & Drive  |-----\>|   Generated Presentations |  
|  (Converts MD to Slides) |      |           APIs           |      |    (In Google Drive)      |  
\+--------------------------+      \+--------------------------+      \+---------------------------+

## **Key Features**

* **End-to-End Automation**: A single script (run\_pipeline.py) manages the entire workflow from prompt to final presentation.  
* **AI-Powered Content Generation**: Leverages Gemini through the enterprise-grade **Vertex AI API** to generate the initial Markdown content for each presentation.  
* **Secure Cloud Authentication**: Uses a single **Google Cloud Service Account** for secure, non-interactive authentication for all Google APIs (Drive, Slides, and Vertex AI).  
* **Intelligent Templating**:  
  * Creates all presentations from a master Google Slides template to enforce brand consistency.  
  * Cleans template slides and intelligently identifies the correct theme and layouts to use, even in complex templates.  
* **Rich Text & Table Formatting**: Automatically converts Markdown into formatted slide content, including:  
  * **Bold** and *Italic* text.  
  * Multi-level nested bullet points with correct indentation.  
  * Perfectly centered and auto-sized tables with proportional columns.  
* **Advanced Layout Management**:  
  * Maps Markdown \_class tags to specific slide layouts via a simple layouts.yaml file.  
  * Automatically populates global headers and footers on every slide.  
  * Supports two-column layouts and implements a text autofit algorithm to prevent overflow.

## **Setup Guide**

Follow these steps to set up the environment. This involves a one-time setup on Google Cloud, followed by a simple local installation.

### **Prerequisites**

* A Google Cloud account with an active billing account.  
* A Fedora 42 laptop or a similar Linux environment with python3 and python3-venv installed.

### **Step 1: Google Cloud & Drive Setup (One-Time)**

1. **Create a Google Cloud Project**: If you don't have one, create a new project in the [Google Cloud Console](https://console.cloud.google.com/). Note your **Project ID**.  
2. **Enable APIs**: In your project, search for and enable the following three APIs:  
   * Google Drive API  
   * Google Slides API  
   * **Vertex AI API**  
3. **Create a Service Account**:  
   * Navigate to **IAM & Admin \> Service Accounts**.  
   * Click **Create Service Account**, give it a name (e.g., slides-generator), and click **Done**.  
   * Go to the **IAM** page. Click **Grant Access**, and in the "New principals" field, add the service account's email.  
   * Assign it the role of **Vertex AI User**.  
   * Back in the **Service Accounts** page, click the **Actions** menu (⋮) for your new account, select **Manage keys**, and then **Add Key \> Create new key**. Choose **JSON**.  
   * A JSON key file will be downloaded. This is your authentication key.  
4. **Create a Shared Drive**: In Google Drive, create a new **Shared Drive** (e.g., "Automated Presentations"). This is crucial for the service account to have the correct permissions.  
5. **Add Service Account as Member**:  
   * Open your downloaded JSON key file and copy the client\_email address.  
   * Go to your new Shared Drive in Google Drive, click **Manage members**, and paste the service account's email.  
   * Assign it the role of **Content manager** and click **Send**.  
6. **Prepare Assets in Shared Drive**:  
   * Create a folder inside the Shared Drive to store the final presentations (e.g., "Generated Slides"). **Note its ID** from the URL.  
   * Place your **Google Slides Template** inside the Shared Drive. **Note its ID** from the URL.

### **Step 2: Local Project Setup**

1. **Clone the Repository**:  
   git clone \<your-repository-url\>  
   cd \<your-repository-name\>

2. **Run the Install Script**: This script will create a Python virtual environment, install all dependencies from requirements.txt, and create your local configuration files from the examples.  
   chmod \+x install.sh  
   ./install.sh

3. **Configure Your Project**:  
   * **Service Account**: Place your downloaded JSON key file into the project's root directory and rename it to service-account.json.  
   * **.env file**: Open the newly created .env file and fill in all the required values based on your Google Cloud and Drive setup.  
   * **layouts.yaml**: Open layouts.yaml and adjust the mappings to match the "Display names" of the layouts in your specific Google Slides template.

## **Usage**

1. **Configure Workshops**: Open the run\_pipeline.py script and edit the WORKSHOP\_TITLES list to define which presentations you want to generate.  
2. **Run the Pipeline**: Execute the main script from your terminal.  
   \# Make sure your virtual environment is active  
   source .venv/bin/activate

   \# Run the master Python script  
   python3 run\_pipeline.py

The script will now run the complete pipeline, providing logs in your terminal and in pipeline.log. When it finishes, you will find the generated presentations in the output folder you specified on Google Drive.