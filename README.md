# **Markdown to Google Slides Generator (md2gslides)**

This project provides a powerful command-line tool to automate the creation of branded, fully-formatted Google Slides presentations directly from Markdown files.

It's designed for batch processing, allowing you to convert an entire directory of Markdown files into professional-looking presentations with a single command, enforcing brand consistency through the use of a master template.

## **Features**

* **Batch Processing**: Converts an entire directory of .md files into separate Google Slides presentations.  
* **Intelligent Template Usage**:  
  * Enforces brand consistency by creating all presentations from a master Google Slides template.  
  * **Handles complex templates** with multiple or duplicate themes by intelligently selecting the most-used theme as the source for layouts.  
* **Local Layout Mapping**: Maps a \_class tag in Markdown to a specific slide layout from your template via a simple, local layouts.yaml file.  
* **Rich Text Formatting**: Automatically converts Markdown syntax into formatted text on the slides, including:  
  * **Bold** and *Italic* text.  
  * Bulleted lists.  
  * Multi-level nested lists with correct indentation.  
* **Header & Footer Automation**: Parses global header: and footer: declarations and populates them into subtitle placeholders on every slide.  
* **Secure & Automated**: Uses a Google Cloud Service Account for secure, non-interactive authentication.  
* **Robust & Reliable**: Includes pre-checks for permissions, graceful error handling, and comprehensive logging.

## **Setup Guide**

Follow these steps to set up the environment and configure the tool. The process involves one-time setup on Google Cloud, followed by a simple local installation.

### **Step 1: Google Cloud & Drive Setup (One-Time)**

1. **Create a Google Cloud Project**: If you don't have one, create a new project in the [Google Cloud Console](https://console.cloud.google.com/).  
2. **Enable APIs**: For your project, enable the following two APIs:  
   * Google Drive API  
   * Google Slides API  
3. **Create a Service Account**:  
   * In your project, navigate to **IAM & Admin \> Service Accounts**.  
   * Click **Create Service Account**, give it a name (e.g., slides-generator), and click **Done**.  
   * Find your new service account, click the **Actions** menu (⋮), select **Manage keys**, and then **Add Key \> Create new key**. Choose **JSON**.  
   * A JSON key file will be downloaded. This is your service-account.json key.  
4. **Create a Shared Drive**: In Google Drive, create a new **Shared Drive** (e.g., "Automated Presentations"). This is crucial to avoid storage quota errors.  
5. **Add Service Account as Member**:  
   * Open your downloaded service-account.json file and copy the client\_email address.  
   * Go to your new Shared Drive, click **Manage members**, and paste the service account's email.  
   * Assign it the role of **Content manager** and click **Send**.  
6. **Prepare Assets in Shared Drive**:  
   * Create a folder inside the Shared Drive to store the final presentations (e.g., "Generated Slides").  
   * Place your **Google Slides Template** inside the Shared Drive.

### **Step 2: Local Project Setup**

1. **Clone the Repository**:  
   git clone \<your-repository-url\>  
   cd \<your-repository-name\>

2. **Run the Install Script**: This will create a virtual environment, install all dependencies, and create your configuration files from the examples.  
   chmod \+x install.sh  
   ./install.sh

3. **Configure Your Project**:  
   * **Service Account**: Place your downloaded service-account.json key file into the project's root directory.  
   * **.env file**: Open the newly created .env file and fill in your TEMPLATE\_PRESENTATION\_ID, OUTPUT\_FOLDER\_ID, and the TARGET\_THEME\_NAME.  
   * **layouts.yaml**: Open layouts.yaml and adjust the mappings to match the "Display names" of the layouts in your specific Google Slides template.

## **Usage**

1. **Add Markdown Files**: Place one or more .md files into your source directory (markdown\_source/).  
2. **Run the Generator**: Execute the script from your terminal.  
   \# You can use the helper script  
   ./generate.sh

   \# Or run the Python script directly (ensure venv is active)  
   \# python3 md2gslides.py  
