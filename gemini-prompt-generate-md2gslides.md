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

**Core Functionality:** The script must process all files ending in .md from a source directory. For each Markdown file, it will create a new, separate Google Slides presentation in a specified Google Drive folder, which MUST be located within a Shared Drive.

**Authentication and Configuration:**

1. **Authentication**: The script MUST use a non-interactive Google Cloud **Service Account** for all API authentication.  
2. **Configuration**: All configuration parameters MUST be managed in an external .env file. The script should read the following keys:  
   * GOOGLE\_APPLICATION\_CREDENTIALS: Path to the service account's JSON key file.  
   * TEMPLATE\_PRESENTATION\_ID: The ID of the Google Slides template to use.  
   * SOURCE\_DIRECTORY: The path to the directory containing the source .md files.  
   * OUTPUT\_FOLDER\_ID: The ID of the Google Drive folder (inside a Shared Drive) where generated presentations will be saved.  
   * TARGET\_THEME\_NAME: The exact "Display name" of the theme (master) to use from the template.  
   * **LOG\_LEVEL**: A string to control the logging verbosity (e.g., "DEBUG", "INFO"). The script must default to "INFO" if the variable is missing or invalid.

**Templating and Layout:**

1. **Template**: Each new presentation must be created by making a copy of the presentation specified by TEMPLATE\_PRESENTATION\_ID.  
2. **Intelligent Theme Handling**: The script must correctly identify and use layouts from a specific theme, even in complex templates. The logic must be:  
   a. Find all themes (masters) in the template that exactly match the TARGET\_THEME\_NAME.  
   b. If duplicates are found, determine the correct one by counting which of these themes is used by the most slides within the template file. This heuristic identifies the "active" or primary theme.  
   c. Extract the layouts only from this single, most-used theme. The script must return both the layout map and the ID of this master theme.  
3. **Master Slide Text Replacement**: After copying the presentation, the script must find the selected master slide and perform text replacements on it. Specifically, it must find a text box containing "CONFIDENTIAL designator" and change its text to "CONFIDENTIAL", and another one containing "V0000000" and change its text to "V1.0".  
4. **Layout Mapping**: The script must read a mapping from a local YAML file named layouts.yaml. This file maps a \_class name to the official "Display name" of a layout within the selected theme.  
5. **Template Slide Cleanup**: After creating all new slides, the script must delete **ALL** of the initial slides that came from the template copy, ensuring the final presentation is clean.

**Markdown Parsing Rules:**

1. **Marpit Front-Matter Handling**: The script MUST identify and remove the Marpit YAML front-matter (the content between the first two \--- separators) *before* splitting the file into slides. This prevents an unwanted, blank first slide from being created.  
2. **Advanced Placeholder Population Logic**: The script must handle SUBTITLE placeholders with a nuanced, two-step logic to correctly assign slide-specific subtitles, global headers, and global footers.  
   Step 1: Role Identification  
   For each layout, the script must first analyze the SUBTITLE placeholders to determine their potential role.  
   * If a layout has **two or more** SUBTITLE placeholders, their roles are determined by vertical order: the topmost is the header, the bottommost is the footer, and any in between are for main\_content.  
   * If a layout has **only one** SUBTITLE placeholder, its role is determined by its position *relative to the TITLE placeholder*. If the subtitle is vertically above the title, it is a header. Otherwise, it is for main\_content.

   Step 2: Prioritized Content AssignmentThe script must then assign content to these roles in a strict order of priority, using a tracking mechanism to ensure a placeholder is only used once.

   1. **Slide-Specific Subtitle**: First, if the Markdown for a slide contains \#\# Subtitle content, assign it to an available main\_content subtitle placeholder. This is the highest priority.  
   2. **Global Header**: Second, if a placeholder was identified as a header and it has *not* already been assigned content, assign the global header: text to it.  
   3. **Global Footer**: Third, if a placeholder was identified as a footer and it has *not* already been assigned content, assign the global footer: text to it.  
   4. **Body Fallback**: Finally, use any remaining, unassigned main\_content subtitle placeholders as a fallback destination for the main body content if a dedicated BODY placeholder is not found. If no suitable placeholder exists, log a warning.  
3. **Rich Text Formatting (Body Content)**: The script MUST parse the BODY content for Markdown syntax and apply rich text formatting in Google Slides, including **Bold**, *Italic*, **Bulleted Lists**, and **Nested Lists**. Unnecessary blank lines must be removed.  
4. **Other Parsing Rules**: The script must handle slide separation (---), custom comment blocks (\_COMMENT\_START\_...\_END\_), and slide-level metadata (\_class:, Speaker notes:).  
5. **Tag Removal**: All comment blocks and citation tags (cite\_start  
   ,cite:XX  
   ) must be removed from the final visible content. The citation tag removal must use a regex composed **only of Unicode character codes**.

**Robustness and Error Handling:**

1. **API Scopes & Shared Drive**: Use the .../auth/drive scope and include supportsAllDrives=True in all relevant Drive API calls.  
2. **Pre-Checks**: Verify the source directory exists and the script has permissions for the output folder.  
3. **Graceful Handling**: Handle cases where no .md files are found, and continue processing the next file if one fails.  
4. **Logging**: Implement comprehensive, configurable logging to both console and a generation.log file, controlled by the LOG\_LEVEL environment variable.

### **Detailed Requirements for README.md and Other Files**

* **README.md**: Must be comprehensive, explaining all features and a setup guide based on a git workflow. It should instruct the user to clone, run install.sh, and configure the layouts.yaml and .env files (including the new TARGET\_THEME\_NAME and LOG\_LEVEL variables).  
* **install.sh**: Must automate the creation of a virtual environment, installation of dependencies, and creation of config files from examples.  
* **requirements.txt**: Must include PyYAML and all other necessary packages.  
* **.env.example**: Must include placeholders for TARGET\_THEME\_NAME and LOG\_LEVEL.