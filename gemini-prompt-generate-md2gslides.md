Generate a complete, single-file Python script named md2gslides.py. This script will function as a robust command-line tool to convert a directory of Markdown files into fully formatted Google Slides presentations.

Core Functionality:  
The script should process all files ending in .md from a source directory. For each Markdown file, it will create a new, separate Google Slides presentation in a specified Google Drive folder, which MUST be located within a Shared Drive.  
**Authentication and Configuration:**

1. **Authentication**: The script MUST use a non-interactive Google Cloud **Service Account** for all API authentication.  
2. **Configuration**: All configuration parameters MUST be managed in an external .env file. The script should read the following keys:  
   * GOOGLE\_APPLICATION\_CREDENTIALS: Path to the service account's JSON key file.  
   * TEMPLATE\_PRESENTATION\_ID: The ID of the Google Slides template to use.  
   * LAYOUT\_SHEET\_ID: The ID of the Google Sheet containing the layout mapping.  
   * SOURCE\_DIRECTORY: The path to the directory containing the source .md files.  
   * OUTPUT\_FOLDER\_ID: The ID of the Google Drive folder (inside a Shared Drive) where generated presentations will be saved.

**Templating and Layout:**

1. **Template**: Each new presentation must be created by making a copy of the presentation specified by TEMPLATE\_PRESENTATION\_ID.  
2. **Layout Mapping**: The script must read a mapping from the Google Sheet specified by LAYOUT\_SHEET\_ID. It must **dynamically determine the name of the first visible sheet** instead of assuming a hardcoded name like "Sheet1".  
3. **Default Slide Removal**: After creating all new slides, the script must delete the initial slide(s) that came from the template.

Markdown Parsing Rules:  
The script must parse the Markdown content with the following specific rules:

1. **File Structure**: Slides within a Markdown file are separated by \---.  
2. **Metadata Blocks**: All metadata is defined within custom comment tags: \_COMMENT\_START\_ and \_COMMENT\_END\_. These tags must be parsed directly; do not convert them to standard HTML comments.  
3. **Global Header/Footer**: The first comment block in the file can contain header: and footer: declarations. This text must be inserted into SUBTITLE placeholders on every slide.  
   * The script should identify two SUBTITLE placeholders on a slide's layout.  
   * The header text goes into the placeholder with the higher vertical position (lower Y-coordinate).  
   * The footer text goes into the placeholder with the lower vertical position.  
4. **Slide-Level Metadata**: Other comment blocks within a slide's content define:  
   * \_class:: The layout to use for that slide, which maps to the Google Sheet.  
   * Speaker notes:: The text to be placed in the slide's speaker notes area.  
5. **Content Parsing**:  
   * The first line of a slide's content that starts with a markdown heading (\#) should be used as the text for the TITLE placeholder.  
   * All remaining text is considered the BODY content.  
6. **Rich Text Formatting (Body Content)**: The script MUST parse the BODY content for Markdown syntax and apply rich text formatting in Google Slides. This includes:  
   * **Bold** (\*\*text\*\*)  
   * **Italic** (\*text\*)  
   * **Bulleted Lists** (- item)  
   * **Nested Lists**: Must correctly render multiple levels of indentation.  
   * **Content Compaction**: Unnecessary blank lines between paragraphs and list items must be removed to create a compact, clean layout on the slide.  
7. **Tag Removal**:  
   * All \_COMMENT\_START\_...\_COMMENT\_END\_ blocks must be removed from the final visible content on the slides.  
   * The script must remove \`\` and \[cite: XX\] tags. This specific removal operation MUST be performed using a regular expression composed **only of Unicode character codes** (e.g., \\uXXXX).

**Robustness and Error Handling:**

1. **API Scopes**: The script must use the broad https://www.googleapis.com/auth/drive scope to ensure it can access shared templates and folders.  
2. **Shared Drive Support**: All Google Drive API calls that interact with files (like copying and checking permissions) MUST include the supportsAllDrives=True parameter to prevent storage quota errors with the service account.  
3. **Pre-Checks**: Before processing files, the script must:  
   * Verify that the SOURCE\_DIRECTORY exists.  
   * Verify it has "Editor" (or canAddChildren) permissions on the OUTPUT\_FOLDER\_ID. If not, it should exit with a fatal error.  
4. **Graceful Handling**: If no .md files are found in the source directory, the script should log a warning and exit gracefully without an error.  
5. **Batch Processing**: When processing multiple files, an error in one file must not stop the entire process. The script should log the error for the failed file and continue to the next one.  
6. **Logging**: The script must implement comprehensive logging using Python's logging module, outputting timestamped messages to both the console and a file named generation.log.