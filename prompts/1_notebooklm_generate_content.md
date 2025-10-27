ROLE: Red Hat Architect.
SOURCES: All uploads (Docs, SoW, agenda.md, ad_prefix_dictionary.md, AD md files).
CONTEXT: ODC Noord; Two on-prem clusters (OCP/OpenStack, OCP/BM) in same DC running RHOAI.
ADHERENCE: **CRITICAL**: Generate topics **strictly** following agenda.md ORDER for "{{WORKSHOP_TITLE}}". No reordering/overlap.

RULES:

1.  **AGENDA SLIDE**: First slide: "Agenda" listing ONLY topics for "{{WORKSHOP_TITLE}}" from agenda.md.
2.  **ADs**: Find ADs. Tag reuse/modify/new. Core AD content (incl. Alternatives) MUST be **VERBATIM**, generic, **NO CONTEXT**. Modify core AD only if repo is outdated/incorrect.
3.  **FLOW**: Explain -> Decide pattern per topic, strictly following agenda.md order.
4.  **EXPLAIN SLIDE**: Visible: concise summary/bullets. `<div data-speaker-notes>`: detailed narrative.
5.  **DECIDE SLIDE (VISIBLE)**: ONLY ID, Title, Question, Alternatives. **CRITICAL**: Use **blank lines** between EACH item.
6.  **DECIDE SLIDE (NOTES)**: Start notes with blank line. Include Full AD (per rule 7) then "Workshop Context" paragraph.
7.  **AD FORMATTING (NOTES - CRITICAL)**:
    - Full AD block uses **bold labels**.
    - **Blank lines** MUST separate **EVERY** item AND labels from content (e.g., blank line between **Justification** label and its first bullet).
    - Include ALL fields, this EXACT order: **ID**, **Title**, **Question**, **Issue**, **Assumptions** ("N/A" if none), **Alternatives**, **Justification** (bullets), **Implications** (bullets), **Agreeing Parties**.
8.  **OUTPUT**: Pure Markdown. NO JSON.

INSTRUCTION:
Apply ALL rules meticulously. Generate complete Markdown for "{{WORKSHOP_TITLE}}". Follow **strict agenda.md topic order**. STOP after session.
