**INPUT:** Take the full Markdown slide deck content generated in the previous step (from Prompt 1).

**INSTRUCTIONS:** Now, perform these two final actions **on that existing content**:

1.  **SoW CHECK & INTEGRATION**:

    - Review the entire Markdown content generated previously.
    - Identify which specific items from the **"Facilitating workshops and/or discussions for:"** sections within the SoW PDF are covered in the generated "Explain" and "Decide" slides.
    - For **each "Decide" slide**, add a dedicated section within its `<div data-speaker-notes>` block titled "**SoW Items Covered:**". List the specific SoW bullet points addressed by the preceding "Explain" slide and the AD on the "Decide" slide itself.
    - **CRITICAL AD FORMATTING:** While adding the SoW check, ensure the full AD content preceding it **strictly maintains** the format specified in Prompt 1 Rule #7 (bold labels **AND blank lines** between ALL items: ID, Title, Question, Issue, Assumptions, Alternatives, Justification, Implications, Agreeing Parties). **Do NOT remove blank lines.**
    - After modifying all relevant speaker notes, add a final check summary comment **at the very end of the entire Markdown output**: ``

2.  **AD SUMMARY SLIDE**:
    - Append a **new, final slide** to the end of the existing Markdown content.
    - Use the `section` layout class for this slide.
    - The title of this slide should be "## Architecture Decision Summary".
    - The body of this slide MUST contain only a Markdown table listing **all ADs** included in the generated deck.
    - The table must have exactly three columns: "**ID**", "**Architectural Question**", and "**Decision**".
    - Populate the "ID" and "Architectural Question" columns based on the ADs used in the "Decide" slides.
    - Fill the "**Decision**" column with `#TODO#` for each AD listed.

**OUTPUT:** Provide the _complete, modified_ Markdown content for the entire slide deck, incorporating the SoW checks in speaker notes (with correct AD formatting including blank lines) and adding the final AD summary slide.
