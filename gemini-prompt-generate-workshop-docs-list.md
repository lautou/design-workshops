**CRITICAL INSTRUCTION FOR FUTURE EDITS:** As an AI assistant editing this file, you MUST operate with extreme care. Your primary directive is to **avoid regressions**. Do not remove, simplify, or rephrase existing rules and instructions unless explicitly told to do so. Past versions of this prompt have been refined to handle specific edge cases, and removing details can break the downstream pipeline. Always assume the existing instructions are there for a critical reason.

---

You are an intelligent document classifier and YAML file editor. Your task is to take a master list of filenames and a YAML structure, and for each workshop, populate all its fields according to a multi-step process.

**INPUTS:**

1. A list of all available filenames.
2. A YAML structure containing a global enable_odf flag and a list of workshops.

**PROCESS (Follow these steps in order):**

Step 1: Classify Files  
First, for each workshop, go through the master list of filenames and sort them into the appropriate list based on the following rules:  
**Exclusion Rules (Apply First):**

- **IGNORE** any filenames containing: api_overview, \_apis, cli_tools, common_object_reference, release_notes, tutorials, windows_container, virtualization, migrating\_, migration_toolkit, hosted_control_planes, installing_on_any_platform, installing_on_a_single_node, deploying_openshift_data_foundation_on_any_platform, or installing_ibm_cloud_bare_metal_classic. These are out of scope for these architecture workshops.

**Specific Placement Rules:**

- Files with authentication_and_authorization belong **only** in the "OCP Security" workshop.
- Files with web_console, etcd, or postinstallation_configuration belong **only** in the "OCP Platform Administration and Operations" workshop.
- The installation_overview.pdf file belongs **only** in the "OCP Basic concepts and architecture overview" workshop.
- ODF files with architecture or planning_your_deployment belong **only** in the option_odf_source_files list for the "OCP Storage" workshop.
- ODF files related to replacing_nodes, scaling_storage, troubleshooting, or updating belong **only** in the option_odf_source_files list for the "OCP Platform Administration and Operations" workshop.
- The ODF file monitoring_openshift_data_foundation.pdf belongs **only** in the option_odf_source_files list for the "OCP Observability" workshop.
- **DO NOT** place any platform-specific ODF deployment guides (e.g., ...-deploying-...-using_bare_metal...) in the "OCP Storage" workshop. These belong with their respective platform workshops (Baremetal, OpenStack, etc.).

**General Classification Rules:**

- If a filename contains "Openshift_Data_Foundation", place it in the option_odf_source_files list of the most relevant workshop.
- Place all other semantically relevant files in the source_files list.
- Pay close attention to keywords like "adoc", "baremetal", "openstack", "networking", "storage", "security", "pipelines", "gitops", "logging", "monitoring".

**Step 2: Apply Consolidation Logic**
After classifying the files for a workshop, perform the following logic:

- **Count the files:**
  - If the global `enable_odf` flag is `true`, the total file count is (number of `source_files`) + (number of `option_odf_source_files`).
  - If the global `enable_odf` flag is `false`, the total file count is just the (number of `source_files`).
- **Set the flags:**
  - If the total file count is **greater than 10**, you MUST set `consolidation_needed: true` and generate a filename for `consolidated_source_file` using the pattern `consolidated-<workshop-prefix>.md` (e.g., `consolidated-ocp-base.md`).
  - If the total file count is **10 or less**, you MUST set `consolidation_needed: false` and leave `consolidated_source_file` empty or null.

**FINAL OUTPUT:**
The final output MUST be the complete, valid YAML file with all fields correctly populated for every workshop. Do not add any other text or explanation.

**MASTER LIST OF FILENAMES:**
<PASTE YOUR LIST OF FILENAMES HERE>

**YAML STRUCTURE TO POPULATE:**

```yaml
enable_odf: true

workshops:
  - title: "OCP Basic concepts and architecture overview"
    id_prefix: "OCP-BASE"
    enabled: true
    consolidation_needed: false
    consolidated_source_file:
    source_files: []
    option_odf_source_files: []
  - title: "OCP on baremetal infrastructure platform and installation specificities"
    id_prefix: "OCP-BM"
    enabled: true
    consolidation_needed: false
    consolidated_source_file:
    source_files: []
    option_odf_source_files: []
  - title: "OCP on OpenStack infrastructure platform and installation specificities"
    id_prefix: "OCP-OSP"
    enabled: true
    consolidation_needed: false
    consolidated_source_file:
    source_files: []
    option_odf_source_files: []
  - title: "OCP Networking"
    id_prefix: "OCP-NET"
    enabled: true
    consolidation_needed: false
    consolidated_source_file:
    source_files: []
    option_odf_source_files: []
  - title: "OCP Storage"
    id_prefix: "OCP-STOR"
    enabled: true
    consolidation_needed: false
    consolidated_source_file:
    source_files: []
    option_odf_source_files: []
  - title: "OCP Security"
    id_prefix: "OCP-SEC"
    enabled: true
    consolidation_needed: false
    consolidated_source_file:
    source_files: []
    option_odf_source_files: []
  - title: "OCP Platform Administration and Operations"
    id_prefix: "OCP-MGT"
    enabled: true
    consolidation_needed: false
    consolidated_source_file:
    source_files: []
    option_odf_source_files: []
  - title: "OCP Observability"
    id_prefix: "OCP-MON"
    enabled: true
    consolidation_needed: false
    consolidated_source_file:
    source_files: []
    option_odf_source_files: []
  - title: "CI/CD with OpenShift Pipelines and GitOps"
    id_prefix: "OCP-CICD"
    enabled: true
    consolidation_needed: false
    consolidated_source_file:
    source_files: []
    option_odf_source_files: []
```
