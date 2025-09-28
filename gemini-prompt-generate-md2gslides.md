Generate a complete, multi-file project for a command-line tool named md2gslides. This tool's purpose is to automate the conversion of Markdown files into fully-formatted Google Slides presentations.

The project should be structured for management in a git repository and include an installation script for easy setup.

Please generate the following files:

1. md2gslides.py: The main Python script.
2. README.md: The project's documentation.
3. install.sh: A shell script to automate local environment setup.
4. requirements.txt: The list of Python dependencies.
5. .env.example: An example configuration file.
6. layouts.yaml.example: An example layout mapping file.

### **Detailed Requirements for md2gslides.py**

Core Functionality:  
The script must process all files ending in .md from a source directory. For each Markdown file, it will create a new, separate Google Slides presentation in a specified Google Drive folder, which MUST be located within a Shared Drive.  
**Authentication and Configuration:**

1. **Authentication**: The script MUST use a non-interactive Google Cloud **Service Account** for all API authentication.
2. **Configuration**: All configuration parameters MUST be managed in an external .env file. The script should read the following keys:
   - GOOGLE_APPLICATION_CREDENTIALS: Path to the service account's JSON key file.
   - TEMPLATE_PRESENTATION_ID: The ID of the Google Slides template to use.
   - SOURCE_DIRECTORY: The path to the directory containing the source .md files.
   - OUTPUT_FOLDER_ID: The ID of the Google Drive folder (inside a Shared Drive) where generated presentations will be saved.

**Templating and Layout:**

1. **Template**: Each new presentation must be created by making a copy of the presentation specified by TEMPLATE_PRESENTATION_ID.
2. **Layout Mapping**: The script must read a mapping from a local YAML file named layouts.yaml. This file maps a \_class name to the official "Display name" of a layout in the Google Slides template.
3. **Default Slide Removal**: After creating all new slides, the script must delete the initial slide(s) that came from the template.

Markdown Parsing Rules:  
The script must parse the Markdown content with the following specific rules:

1. **File Structure**: Slides within a Markdown file are separated by \---.
2. **Metadata Blocks**: All metadata is defined within custom comment tags: \_COMMENT_START\_ and \_COMMENT_END\_. These tags must be parsed directly; do not convert them to standard HTML comments. The parser must be robust enough to handle an optional backslash (\\) before the closing tag (e.g., \\\_COMMENT_END\_).
3. **Global Header/Footer**: The first comment block in the file can contain header: and footer: declarations. This text must be inserted into SUBTITLE placeholders on every slide.
   - The script should identify two SUBTITLE placeholders on a slide's layout.
   - The header text goes into the placeholder with the higher vertical position (lower Y-coordinate).
   - The footer text goes into the placeholder with the lower vertical position.
4. **Slide-Level Metadata**: Other comment blocks within a slide's content define:
   - \_class:: The layout to use for that slide, which maps to the layouts.yaml file.
   - Speaker notes:: The text to be placed in the slide's speaker notes area.
5. **Content Parsing**:
   - The first line of a slide's content that starts with a markdown heading (\#) should be used as the text for the TITLE placeholder.
   - All remaining text is considered the BODY content.
6. **Rich Text Formatting (Body Content)**: The script MUST parse the BODY content for Markdown syntax and apply rich text formatting in Google Slides. This includes:
   - **Bold** (\*\*text\*\*)
   - **Italic** (\*text\*)
   - **Bulleted Lists** (- item)
   - **Nested Lists**: Must correctly render multiple levels of indentation.
   - **Content Compaction**: Unnecessary blank lines between paragraphs and list items must be removed to create a compact, clean layout on the slide.
7. **Tag Removal**:
   - All \_COMMENT_START\_...\_COMMENT_END\_ blocks must be removed from the final visible content on the slides.
   - The script must remove \[cite_start\] and \[cite: XX\] tags. This specific removal operation MUST be performed using a regular expression composed **only of Unicode character codes** (e.g., \\uXXXX).

**Robustness** and **Error Handling:**

1. **API Scopes**: The script must use the broad https://www.googleapis.com/auth/drive scope to ensure it can access shared templates and folders.
2. **Shared Drive Support**: All Google Drive API calls that interact with files (like copying and checking permissions) MUST include the supportsAllDrives=True parameter to prevent storage quota errors with the service account.
3. **Pre-Checks**: Before processing files, the script must:
   - Verify that the SOURCE_DIRECTORY exists.
   - Verify it has "Editor" (or canAddChildren) permissions on the OUTPUT_FOLDER_ID. If not, it should exit with a fatal error.
4. **Graceful Handling**: If no .md files are found in the source directory, the script should log a warning and exit gracefully without an error.
5. **Batch Processing**: When processing multiple files, an error in one file must not stop the entire process. The script should log the error for the failed file and continue to the next one.
6. **Logging**: The script must implement comprehensive logging using Python's logging module, outputting timestamped messages to both the console and a file named generation.log.

### **Detailed Requirements for README.md**

Generate a comprehensive README file that explains the project for other users. It should follow a professional format and include:

1. A brief introduction to the project's purpose.
2. A "Features" section in a bulleted list.
3. A "Setup Guide" section optimized for a git-based workflow. It should instruct the user to:
   - Complete the one-time setup on Google Cloud and Google Drive (creating service account, shared drive, etc.).
   - Clone the repository.
   - Run the install.sh script.
   - Configure the project by editing the .env and layouts.yaml files.
4. A "Usage" section explaining how to run the generator.

### **Detailed Requirements for install.sh**

Generate a shell script named install.sh that automates the local setup process. It should:

1. Check if python3 and python3-venv are available.
2. Create a Python virtual environment named .venv.
3. Activate the virtual environment.
4. Install all dependencies from requirements.txt.
5. Create layouts.yaml and .env by copying them from layouts.yaml.example and .env.example, but only if they don't already exist.
6. Print clear instructions for the user on the final manual configuration steps.

### **Detailed Requirements for Other Files**

- **requirements.txt**: Should contain all necessary Python packages (google-api-python-client, google-auth-httplib2, google-auth-oauthlib, python-dotenv, markdown-it-py, PyYAML).
