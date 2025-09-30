Generate a complete, multi-file project for a command-line tool named md2gslides. This tool's purpose is to automate the conversion of Markdown files into fully-formatted Google Slides presentations.

The project should be structured for management in a git repository and include an installation script for easy setup.

Please generate the following files:

1. **md2gslides.py**: The main Python script.  
2. **README.md**: The project's documentation.  
3. **install.sh**: A shell script to automate local environment setup.  
4. **requirements.txt**: The list of Python dependencies.  
5. **.env.example**: An example configuration file.  
6. **layouts.yaml.example**: An example layout mapping file.

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
   * LOG\_LEVEL: A string to control the logging verbosity (e.g., "DEBUG", "INFO"). The script must default to "INFO" if the variable is missing or invalid.

**Templating and Layout:**

1. **Template**: Each new presentation must be created by making a copy of the presentation specified by TEMPLATE\_PRESENTATION\_ID.  
2. **Template Slide Cleanup**: Immediately after copying the template, the script must delete **ALL** of the initial slides that came from the template. This "pre-cleaning" strategy ensures that the script can reliably identify the single surviving theme and its associated layouts for the rest of the process.  
3. **Theme Identification**: After the cleanup, the script must analyze the now-empty presentation to find the single master theme that matches the TARGET\_THEME\_NAME from the .env file. All layouts used for slide creation will be derived from this master.  
4. **Master Slide Text Replacement**: After identifying the correct master slide, the script must perform text replacements on it. Specifically, it must find a text box containing "CONFIDENTIAL designator" and change its text to "CONFIDENTIAL", and another one containing "V0000000" and change its text to "V1.0".  
5. **Layout Mapping**: The script must read a mapping from a local YAML file named layouts.yaml. This file maps a \_class name (from Markdown) to the official "Display name" of a layout within the selected theme.

**Markdown Parsing & Content Rendering Rules:**

1. **Marpit Front-Matter Handling**: The script MUST identify and remove the Marpit YAML front-matter (the content between the first two \--- separators) *before* splitting the file into slides.  
2. **Flexible Title Detection**: The script must identify the **first heading on a slide, regardless of its level** (\#, \#\#, \#\#\#, etc.), and treat it as the slide's main title. All subsequent text and headings will be treated as the subtitle or body.  
3. **Rich Text Formatting**: The script MUST parse body content for Markdown syntax and apply rich text formatting in Google Slides, including **Bold**, *Italic*, **Bulleted Lists**, and **Nested Lists** with correct indentation.  
4. **Advanced Placeholder Population**: The script must handle SUBTITLE placeholders with a nuanced logic to correctly assign slide-specific subtitles, global headers, and global footers.  
   * **Role Identification**: For each layout, it must analyze SUBTITLE placeholders. If there are two or more, the topmost is the header and the bottommost is the footer. If there is only one, its role (header vs. main content) is determined by its vertical position relative to the TITLE placeholder.  
   * **Prioritized Assignment**: It must then assign content to these placeholders in a strict order, ensuring a placeholder is only used once: slide-specific subtitle first, then global header, then global footer. Any remaining SUBTITLE placeholders can be used as a fallback for body content.  
5. **Two-Column Body Handling**: For layouts with exactly two BODY placeholders, the script must split the body content. It should scan for a splitter (a bolded line of text). Content *before* the splitter goes into the left column; content *including and after* the splitter goes into the right column.  
6. **Body Text Autofit Algorithm**: Since the API disables autofit on text insertion, the script MUST implement a heuristic algorithm to manually fit text into BODY placeholders.  
   * For a given text block and placeholder, the script will start with a default font size (e.g., 11pt).  
   * It will estimate the number of lines the text will occupy based on the placeholder's width.  
   * It will calculate the total estimated text height based on the number of lines and a line-height factor.  
   * If the estimated height exceeds the placeholder's actual height, it will decrement the font size and repeat the calculation until the text fits.  
   * The final calculated font size will be applied to the text shape.  
7. **Table Rendering and Centering Algorithm**: The script must parse Markdown tables and render them with advanced formatting.  
   * **Column Sizing**: Column widths must be calculated proportionally based on the character length of the content in each column.  
   * **Height Calculation**: It must implement a font-size reduction loop (similar to the body text autofit) to calculate a final font size and total table height that fits within the body placeholder's vertical space.  
   * **Perfect Centering**: The script MUST calculate the final translateX and translateY coordinates for the table. This is done by finding the center point of the BODY placeholder and subtracting half of the table's calculated width and height. This ensures the table is perfectly centered both horizontally and vertically.  
8. **Tag Removal**: All comment blocks (\_COMMENT\_START\_...\_END\_) and citation tags (\[cite\_start\], \[cite: XX\]) must be removed from the final visible content on the slides. The citation tag removal must use a regex composed **only of Unicode character codes**.

**Robustness and Error Handling:**

1. **API Scopes & Shared Drive**: Use the .../auth/drive scope and include supportsAllDrives=True in all relevant Drive API calls.  
2. **Pre-Checks**: Verify the source directory exists and the script has permissions for the output folder before starting.  
3. **Graceful Handling**: Handle cases where no .md files are found, and continue processing the next file if one fails.  
4. **Logging**: Implement comprehensive, configurable logging to both console and a generation.log file, controlled by the LOG\_LEVEL environment variable.