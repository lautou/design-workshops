# OpenShift Pipelines

## PIPELINES-01: Pipeline Strategy and Scope

**Architectural Question**
What is the strategic scope and intended use case for OpenShift Pipelines within the organization?

**Issue or Problem**
A clear domain must be defined for which OpenShift Pipelines will be the standard CI tool. Different workloads, such as traditional application development and data science model training, have distinct CI/CD requirements.

**Assumption**
A CI/CD solution is required for building and deploying applications on the platform.

**Alternatives**

- Unified Pipeline Strategy
- Segregated Pipeline Strategy (Apps vs. Data Science)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Unified Pipeline Strategy:** To standardize on a single, cloud-native CI/CD tool for all workloads, simplifying the toolchain and operational knowledge required.
- **Segregated Pipeline Strategy (Apps vs. Data Science):** To use the best-fit tool for each domain. OpenShift Pipelines (Tekton) is ideal for container-native application CI, while specialized tools (like Kubeflow Pipelines, part of RHOAI) are better suited for the experimental and data-centric nature of MLOps.

**Implications**

- **Unified Pipeline Strategy:** May require extensive customization of Tekton Tasks to accommodate the specific needs of data science workloads. Data science teams may face a steeper learning curve.
- **Segregated Pipeline Strategy (Apps vs. Data Science):** Establishes clear boundaries and provides purpose-built tools for each team. However, it increases the number of tools the platform team must support and requires integration points.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## PIPELINES-02: Pipeline Execution Storage (Workspaces)

**Architectural Question**
What type of storage will be used for pipeline workspaces?

**Issue or Problem**
Pipelines require storage (workspaces) to clone source code, store intermediate artifacts, and share data between tasks. The choice of storage affects performance, cost, and data persistence.

**Assumption**
OpenShift Pipelines will be deployed.

**Alternatives**

- Ephemeral Storage (`emptyDir`)
- Persistent Volume Claims (PVCs)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Ephemeral Storage (`emptyDir`):** To use temporary, node-local storage for pipeline runs. This is the simplest option and is suitable for pipelines where artifacts do not need to be preserved.
- **Persistent Volume Claims (PVCs):** To use persistent storage for workspaces. This is necessary when artifacts (e.g., test reports, binaries) need to be saved and accessed after the pipeline run is complete.

**Implications**

- **Ephemeral Storage (`emptyDir`):** No additional storage configuration is required. However, all data is lost when the pipeline's pod terminates. Performance is dependent on the speed of the node's local disk.
- **Persistent Volume Claims (PVCs):** Requires an underlying storage provider. This adds a dependency on the storage infrastructure but provides data persistence. High-performance storage (e.g., from ODF) may be required for I/O-heavy build jobs.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert

---

## PIPELINES-03: Pipeline Triggering Mechanism

**Architectural Question**
How will pipelines be initiated?

**Issue or Problem**
A strategy is needed to determine how pipelines are triggered. This affects the level of automation, integration with source control, and enabling event-driven workflows.

**Assumption**
OpenShift Pipelines (Tekton) will be used for CI/CD automation.

**Alternatives**

- Manual Triggering (CLI/Console)
- Git Webhooks via Tekton Triggers
- GitOps/ArgoCD Synchronization

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Manual Triggering (CLI/Console):** Simplest implementation, suitable for early development or troubleshooting, requiring no external integration setup.
- **Git Webhooks via Tekton Triggers:** To enable event-driven CI/CD, automatically running pipelines (Builds, Tests) immediately upon source code changes (e.g., git push, pull request open).
- **GitOps/ArgoCD Synchronization:** To enforce a declarative deployment state, allowing the GitOps tool to manage the continuous execution of promotion or synchronization pipelines.

**Implications**

- **Manual Triggering (CLI/Console):** Lack of automation results in manual operational overhead for application release management.
- **Git Webhooks via Tekton Triggers:** Requires securing and managing webhook secrets and configuration, ensuring the cluster is reachable by the Git provider, or leveraging internal Git server integrations.
- **GitOps/ArgoCD Synchronization:** Requires defining pipelines that operate based on repository state rather than transient events. This aligns with GitOps principles but may not support rapid CI/test cycles.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert

---

## PIPELINES-04: Pipelines as Code (PaC) Adoption Strategy

**Architectural Question**
What strategy will be adopted for defining and executing CI/CD workflows using OpenShift Pipelines?

**Issue or Problem**
CI/CD pipelines should be managed declaratively alongside application source code to facilitate GitOps principles and version control of the entire development and deployment process.

**Assumption**
OpenShift Pipelines will be deployed.

**Alternatives**

- Manual Definition of Tekton Resources
- Pipelines as Code (PaC) Integration

**Decision**
#TODO: Document the decision.#

**Justification**

- **Manual Definition of Tekton Resources:** To define and apply `Pipeline` and `PipelineRun` resources directly to the cluster, typically via CLI commands or application manifests. This offers maximum control but lacks the Git integration benefits of PaC.
- **Pipelines as Code (PaC) Integration:** To leverage repository webhooks and in-line comments to trigger and manage Tekton pipelines directly from the Git repository, aligning the CI/CD definition closely with the application source code.

**Implications**

- **Manual Definition of Tekton Resources:** Requires external orchestration (e.g., Jenkins, GitLab CI) to manage pipeline runs, increasing complexity.
- **Pipelines as Code (PaC) Integration:** Requires configuring webhooks on the source control system and deployment of the specialized PaC components within the cluster.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
