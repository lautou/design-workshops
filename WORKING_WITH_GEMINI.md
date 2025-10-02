This document outlines the best practices for working with me, Gemini, to maintain and enhance the "AI-Powered Presentation Generation Pipeline" project. Following these guidelines will help us work together efficiently and ensure the best results.

### **1\. Starting a New Conversation**

To ensure I have the complete picture of the project, **always start a new conversation by providing the contents of the gemini-prompt-generate-workshop-decks.md file.**

This file serves as my "memory" and bootstrapping guide, immediately giving me the necessary context about the project's architecture, my role as a maintainer, and the key files involved.

**Example:**

"Hi Gemini, let's work on the presentation pipeline. Here is the project context to get you started: \[paste content of gemini-prompt-generate-workshop-decks.md\]"

### **2\. Making Change Requests**

* **Be Specific:** The more specific your request, the better I can assist you. Instead of "the script is broken," try "When I run ./run.sh \--show-prompt, I get a KeyError. It seems to be happening in the validate\_layouts\_in\_template function in run\_pipeline.py. Can you look at the logs and the script to fix it?"  
* **Provide All Relevant Files:** If a change spans multiple files or requires context from another file, please provide all of them. For example, if you want to add a new layout to layouts.yaml and use it in build\_slides\_from\_json.py, provide both files.  
* **Work Iteratively:** For complex changes, it's best to work in small steps. Request one or two modifications, review the files I provide, and then request the next set of changes. This allows us to course-correct easily and ensures the final result meets your expectations.

### **3\. My Response Format**

I will always provide my changes within structured file blocks. This makes it easy for you to see exactly what has changed and to copy the content back into your project.

Each file block will have a clear title and the correct filename.

### **4\. Example Workflows**

**Modifying a Script:**

**You:** "In `build_slides_from_json.py`, I'd like to change the font size for the slide titles. Can you find where the title is added and add a request to set the font size to 18pt?" **Me:** "Certainly. I've located the title population logic and will add an `updateTextStyle` request. Here is the updated `build_slides_from_json.py` file:" \[Provides the updated file in a code block\]

**Updating the Core Gemini Prompt:**

**You:** "Let's refine the main prompt. In `gemini-prompt-generate-json.md`, I want to add a rule that the `speakerNotes` field should always start with a one-sentence summary of the slide. Please add this to the 'Content & Style Rules' section." **Me:** "Understood. That's a great rule for consistency. I've updated the prompt to include this instruction. Here is the new version of `gemini-prompt-generate-json.md`:" \[Provides the updated file in a markdown block\]

By following these patterns, we can establish an efficient workflow to keep your project running smoothly. I'm ready for your first request\!

