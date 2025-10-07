You are an intelligent document classifier and YAML file editor. Your task is to populate the `source_files` and `option_odf_source_files` lists for each workshop in the provided YAML structure based on a master list of filenames.

**INPUTS:**

1.  A list of all available PDF filenames.
2.  A YAML structure containing a list of workshops, each with a `title`.

**RULES:**

1.  For each workshop in the YAML, analyze its `title`.
2.  From the master list of filenames, select all files that are semantically relevant to that workshop's title.
3.  **ODF Rule:** If a filename contains "Openshift_Data_Foundation" or "ODF", place it in the `option_odf_source_files` list for the relevant workshop.
4.  **General Rule:** Place all other relevant files in the `source_files` list.
5.  **ADOC Rule:** The `*.adoc` wildcard should ALWAYS be included in the main `source_files` list for every workshop.
6.  Pay close attention to keywords like "baremetal", "openstack", "networking", "storage", "security", "pipelines", "gitops", "logging", "monitoring", etc.
7.  It is better to include a file that might be slightly related than to miss a critical one. Be inclusive.
8.  The final output MUST be the complete, valid YAML file with all workshops and their populated `source_files` and `option_odf_source_files` lists. Do not add any other text or explanation.

**MASTER LIST OF FILENAMES:**
<PASTE YOUR LIST OF FILENAMES HERE>

**YAML STRUCTURE TO POPULATE:**

```yaml
workshops:
  - title: "OCP Basic concepts and architecture overview"
    id_prefix: "OCP-BASE"
    enabled: true
    source_files: []
    option_odf_source_files: []
  - title: "OCP on baremetal infrastructure platform and installation specificities"
    id_prefix: "OCP-BM"
    enabled: true
    source_files: []
    option_odf_source_files: []
  - title: "OCP on OpenStack infrastructure platform and installation specificities"
    id_prefix: "OCP-OSP"
    enabled: true
    source_files: []
    option_odf_source_files: []
  - title: "OCP Networking"
    id_prefix: "OCP-NET"
    enabled: true
    source_files: []
    option_odf_source_files: []
  - title: "OCP Storage"
    id_prefix: "OCP-STOR"
    enabled: true
    source_files: []
    option_odf_source_files: []
  - title: "OCP Security"
    id_prefix: "OCP-SEC"
    enabled: true
    source_files: []
    option_odf_source_files: []
  - title: "OCP Platform Administration and Operations"
    id_prefix: "OCP-MGT"
    enabled: true
    source_files: []
    option_odf_source_files: []
  - title: "OCP Observability"
    id_prefix: "OCP-MON"
    enabled: true
    source_files: []
    option_odf_source_files: []
  - title: "CI/CD with OpenShift Pipelines and GitOps"
    id_prefix: "OCP-CICD"
    enabled: true
    source_files: []
    option_odf_source_files: []
```
