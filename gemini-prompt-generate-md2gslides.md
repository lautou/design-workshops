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
   * GOOGLE\_APPLICATION\_CREDENTIALS: Path to the service account's JSON key file.  
   * TEMPLATE\_PRESENTATION\_ID: The ID of the Google Slides template to use.  
   * SOURCE\_DIRECTORY: The path to the directory containing the source .md files.  
   * OUTPUT\_FOLDER\_ID: The ID of the Google Drive folder (inside a Shared Drive) where generated presentations will be saved.  
   * TARGET\_THEME\_NAME: The exact "Display name" of the theme (master) to use from the template.

**Templating and Layout:**

1. **Template**: Each new presentation must be created by making a copy of the presentation specified by TEMPLATE\_PRESENTATION\_ID.  
2. Intelligent Theme Handling: The script must correctly identify and use layouts from a specific theme, even in complex templates. The logic must be:  
   a. Find all themes (masters) in the template that exactly match the TARGET\_THEME\_NAME.  
   b. If duplicates are found, determine the correct one by counting which of these themes is used by the most slides within the template file. This heuristic identifies the "active" or primary theme.  
   c. Extract the layouts only from this single, most-used theme.  
3. **Layout Mapping**: The script must read a mapping from a local YAML file named layouts.yaml. This file maps a \_class name to the official "Display name" of a layout within the selected theme.  
4. **Template Slide Cleanup**: After creating all new slides, the script must delete **ALL** of the initial slides that came from the template copy, ensuring the final presentation is clean.

Markdown Parsing Rules:  
The script must parse the Markdown content with the following specific rules:

1. **File Structure**: Slides within a Markdown file are separated by \---.  
2. **Metadata Blocks**: All metadata is defined within custom comment tags: \_COMMENT\_START\_ and \_COMMENT\_END\_. The parser must be robust enough to handle an optional backslash (\\) before the closing tag (e.g., \\\_COMMENT\_END\_).  
3. **Global Header/Footer**: The first comment block can contain header: and footer: declarations. This text must be inserted into SUBTITLE placeholders on every slide based on vertical position.  
4. **Slide-Level Metadata**: Other comment blocks within a slide's content define \_class: and Speaker notes:.  
5. **Content Parsing**: The first line starting with a markdown heading (\#) is the TITLE. All other text is the BODY.  
6. **Rich Text Formatting (Body Content)**: The script MUST parse the BODY content for Markdown syntax and apply rich text formatting in Google Slides, including **Bold**, *Italic*, **Bulleted Lists**, and **Nested Lists**. Unnecessary blank lines must be removed.  
7. **Tag Removal**: All comment blocks and citation tags (\[cite\_start\], \[cite: XX\]) must be removed from the final visible content. The citation tag removal must use a regex composed **only of Unicode character codes**.

**Robustness and Error Handling:**

1. **API Scopes & Shared Drive**: Use the .../auth/drive scope and include supportsAllDrives=True in all relevant Drive API calls.  
2. **Pre-Checks**: Verify the source directory exists and the script has permissions for the output folder.  
3. **Graceful Handling**: Handle cases where no .md files are found, and continue processing the next file if one fails.  
4. **Logging**: Implement comprehensive logging to both console and a generation.log file.

### **Detailed Requirements for README.md and Other Files**

* **README.md**: Must be comprehensive, explaining all features and a setup guide based on a git workflow. It should instruct the user to clone, run install.sh, and configure the layouts.yaml and .env files (including the new TARGET\_THEME\_NAME).  
* **install.sh**: Must automate the creation of a virtual environment, installation of dependencies, and creation of config files from examples.  
* **requirements.txt**: Must include PyYAML and all other necessary packages.  
* **.env.example**: Must include a placeholder for TARGET\_THEME\_NAME.  
* **layouts.yaml.example**: An example mapping file.