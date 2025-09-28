# **Markdown to Google Slides Generator (md2gslides)**

This project provides a powerful command-line tool to automate the creation of branded, fully-formatted Google Slides presentations directly from Markdown files.

It's designed for batch processing, allowing you to convert an entire directory of Markdown files into professional-looking presentations with a single command, enforcing brand consistency through the use of a master template.

## **Features**

* **Batch Processing**: Converts an entire directory of .md files into separate Google Slides presentations.  
* **Template-Based**: Enforces brand consistency by creating all presentations from a master Google Slides template.  
* **Dynamic Layouts**: Maps a \_class tag in Markdown to a specific slide layout from your template via a Google Sheet.  
* **Rich Text Formatting**: Automatically converts Markdown syntax into formatted text on the slides, including:  
  * **Bold** and *Italic* text.  
  * Bulleted lists.  
  * Multi-level nested lists with correct indentation.  
* **Header & Footer Automation**: Parses global header: and footer: declarations and populates them into subtitle placeholders on every slide.  
* **Secure & Automated**: Uses a Google Cloud Service Account for secure, non-interactive authentication.  
* **Robust & Reliable**: Includes pre-checks for permissions, graceful error handling, and comprehensive logging.

## **Setup Guide**

Follow these steps to set up the environment and configure the tool.

### **Step 1: Google Cloud Project**

1. **Create a Google Cloud Project**: If you don't have one, create a new project in the [Google Cloud Console](https://console.cloud.google.com/).  
2. **Enable APIs**: For your project, enable the following three APIs:  
   * Google Drive API  
   * Google Sheets API  
   * Google Slides API  
3. **Create a Service Account**:  
   * In your project, navigate to **IAM & Admin \> Service Accounts**.  
   * Click **Create Service Account**.  
   * Give it a name (e.g., slides-generator) and click **Done**.  
   * Find your new service account, click the **Actions** menu (⋮), and select **Manage keys**.  
   * Click **Add Key \> Create new key**, choose **JSON**, and click **Create**.  
   * A JSON key file will be downloaded. Rename it to service-account.json and place it in your project folder. **Treat this file as a password.**

### **Step 2: Google Drive Setup (Crucial)**

To avoid storage quota errors, all work must be done within a **Shared Drive**.

1. **Create a Shared Drive**: In Google Drive, right-click on "Shared drives" and create a new one (e.g., "Automated Presentations").  
2. **Add Service Account as Member**:  
   * Open your service-account.json file and copy the client\_email address.  
   * Go to your new Shared Drive, click **Manage members** at the top.  
   * Paste the service account's email address.  
   * Assign it the role of **Content manager** and click **Send**.  
3. **Prepare Assets**:  
   * Create a folder inside the Shared Drive to store the final presentations (e.g., "Generated Slides").  
   * Place your **Google Slides Template** and your **Layout Mapping Google Sheet** anywhere inside this Shared Drive (or ensure they are shared with the service account's email with "Viewer" access).

### **Step 3: Local Project Setup**

1. **Folder Structure**: Organize your project folder as follows:  
   your-project/  
   ├── md2gslides.py  
   ├── .env  
   ├── requirements.txt  
   ├── service-account.json  
   └── markdown\_source/  
       └── presentation1.md

2. **Create a Virtual Environment**:  
   python3 \-m venv .venv

3. **Activate the Environment**:  
   source .venv/bin/activate

4. **Install Dependencies**: Create a requirements.txt file with the content below, then run the install command.  
   **requirements.txt**:  
   google-api-python-client  
   google-auth-httplib2  
   google-auth-oauthlib  
   python-dotenv  
   markdown-it-py

   **Install Command**:  
   pip install \-r requirements.txt

### **Step 4: Configuration**

Create a file named .env and populate it with the required IDs and paths.

**.env**:

\# \--- Authentication \---  
\# Path to your service account's JSON key file  
GOOGLE\_APPLICATION\_CREDENTIALS="service-account.json"

\# \--- Input Files (from your Shared Drive) \---  
\# ID of the Google Slides template presentation  
TEMPLATE\_PRESENTATION\_ID="YOUR\_TEMPLATE\_PRESENTATION\_ID"

\# ID of the Google Sheet with the layout mapping  
LAYOUT\_SHEET\_ID="YOUR\_LAYOUT\_GOOGLE\_SHEET\_ID"

\# \--- Source & Output \---  
\# Path to the LOCAL directory containing your .md files  
SOURCE\_DIRECTORY="markdown\_source"

\# ID of the Google Drive folder (inside the Shared Drive) where slides will be saved  
OUTPUT\_FOLDER\_ID="YOUR\_OUTPUT\_FOLDER\_ID"

*You can get the ID for any file or folder by opening it in Google Drive and copying the string from the URL.*

## **Usage**

1. **Add Markdown Files**: Place one or more .md files into your source directory (e.g., markdown\_source/).  
2. **Run the Script**: Execute the script from your terminal.  
   python3 md2gslides.py

3. **Check the Output**: The script will log its progress to the console and to a generation.log file. Upon successful completion, it will print a link to each generated presentation. The files will also appear in your specified output folder in Google Drive.

## **Markdown File Format**

Your Markdown files should follow this structure:

\_COMMENT\_START\_  
header: 'My Presentation Header'  
footer: 'My Presentation Footer'  
\_COMMENT\_END\_

\---

\_COMMENT\_START\_  
\_class: title  
\_COMMENT\_END\_

\# Slide 1 Title

\#\# A Subtitle for the Title Slide

\---

\_COMMENT\_START\_  
\_class: default  
Speaker notes:  
This is a note for the presenter. It will not be visible on the slide.  
\_COMMENT\_END\_

\# Slide 2 Title

This is a regular paragraph.

This text will be \*\*bold\*\* and this will be \*italic\*.

\- This is a list item.  
\- This is another item.  
  \- This is a nested item (level 2).  
    \- And this is even deeper (level 3).  
\- Back to the first level.  
