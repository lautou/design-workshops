# Red Hat OpenShift AI Self Managed - Architecture Decisions

## RHOAI-SM-01: Red Hat OpenShift AI instances and purposes

**Architectural Question**
How many Red Hat OpenShift AI instances will be installed? What will be the main objective of each Red Hat OpenShift AI instance?

**Issue or Problem**
Determining the number and purpose of OpenShift AI instances impacts resource allocation, operational complexity, and the ability to isolate production, non-production, and testing workloads. Too few instances may lead to conflicts between environments, while too many could strain infrastructure and increase management overhead.

**Assumption**
N/A

**Alternatives**

- Two Instances Model
- Three Instances Model
- Flexible Choice with Sandbox

**Decision**
#TODO#

**Justification**

- **Two Instances Model:** For minimal setup with a sandbox for safe testing and a production instance for operations.
- **Three Instances Model:** For clear separation of production, non-production, and sandbox environments, reducing interference risks.
- **Flexible Choice with Sandbox:** For adaptability to organizational needs, ensuring a sandbox for testing without user impact.

**Implications**

- **Two Instances Model:** Requires moderate management effort; demands two separate deployments with sandbox testing capability, potentially limiting non-production flexibility.
- **Three Instances Model:** Needs robust monitoring processes; involves three deployments with increased resource demands (e.g., 6 nodes minimum) and potential underutilization.
- **Flexible Choice with Sandbox:** Risks inconsistent management; allows variable instances with additional resources, ensuring safe testing but complicating scaling.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-02: Red Hat OpenShift AI host OpenShift clusters

**Architectural Question**
Which OpenShift clusters will be used to host Red Hat OpenShift AI instances?

**Issue or Problem**
Choosing the host clusters for Red Hat OpenShift AI instances affects resource utilization, deployment timelines, and compatibility with existing workloads. Using existing clusters may constrain capacity or conflict with other applications, while creating new clusters increases setup effort and infrastructure costs.

**Assumption**
Red Hat OpenShift AI instances have been defined (RHOAI-SM-01).

**Alternatives**

- Existing Clusters
- New Clusters
- Mixed Approach

**Decision**
#TODO#

**Justification**

- **Existing Clusters:** To leverage current infrastructure, minimizing setup time and costs.
- **New Clusters:** To ensure dedicated resources and isolation, avoiding conflicts with existing workloads.
- **Mixed Approach:** For balancing reuse and capacity, optimizing resource use while addressing needs.

**Implications**

- **Existing Clusters:** May delay rollout if workloads need relocation due to single-instance limits; reuses cluster resources, reducing provisioning effort but risking capacity shortages.
- **New Clusters:** Requires additional admin effort for maintenance; demands additional cluster provisioning, increasing setup time and cost with guaranteed resource availability.
- **Mixed Approach:** Needs careful planning to avoid overload; combines existing and new clusters, requiring hybrid management tools with potential uneven resource distribution.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-03: Environment connectivity

**Architectural Question**
Should Red Hat OpenShift AI Self-Managed be deployed in a connected or disconnected environment?

**Issue or Problem**
The environment’s internet connectivity impacts access to external resources (e.g., container images, updates) and security requirements. A connected environment requires internet access, while a disconnected environment must operate without it. (Aligns with OCP-BASE-07).

**Assumption**
N/A

**Alternatives**

- Connected Environment
- Disconnected Environment

**Decision**
#TODO#

**Justification**

- **Connected Environment:** For simplicity in accessing external resources, ideal for rapid deployment.
- **Disconnected Environment:** To ensure security and compliance, critical for sensitive or isolated setups.

**Implications**

- **Connected Environment:** Increases security monitoring needs; enables direct resource pulls (e.g., images, updates), speeding setup.
- **Disconnected Environment:** Demands manual update processes and skilled admins; requires mirroring resources (e.g., images to local registry), adding setup time. (See RHOAI-SM-04).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-04: Mirror registry (disconnected environment)

**Architectural Question**
If deploying in a disconnected environment, what mirror registry will be used for RHOAI components?

**Issue or Problem**
In a disconnected environment (RHOAI-SM-03), a mirror registry is essential for providing OpenShift AI with access to container images and operators. The choice of registry impacts availability, scalability, and integration. (Aligns with OCP-BASE-08).

**Assumption**
OpenShift cluster is in a disconnected environment.

**Alternatives**

- Use OCP Mirror Registry (Filesystem-based or Dedicated)
- Dedicated RHOAI-Specific Mirror (if different from OCP)

**Decision**
#TODO#

**Justification**

- **Use OCP Mirror Registry:** To leverage the same mirror registry infrastructure used for the underlying OpenShift platform (as decided in OCP-BASE-08), ensuring consistency and simplifying mirror management.
- **Dedicated RHOAI-Specific Mirror:** To maintain a separate mirror registry specifically for RHOAI components, potentially for organizational separation or different update cadences. Generally increases complexity.

**Implications**

- **Use OCP Mirror Registry:** Simplifies overall disconnected setup. Requires ensuring the OCP mirror contains all necessary RHOAI images and catalogs. Update process is unified.
- **Dedicated RHOAI-Specific Mirror:** Increases infrastructure footprint and management overhead. Requires managing two separate mirroring processes and ensuring network connectivity between RHOAI installation sources and its dedicated mirror.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-05: Identity provider Integration

**Architectural Question**
Which OpenShift identity provider (IdP) will be used to authenticate users accessing Red Hat OpenShift AI?

**Issue or Problem**
OpenShift AI relies entirely on the OpenShift platform's configured authentication mechanism (OCP-SEC-03). The choice of IdP affects user login experience, integration with enterprise directories, group management for RBAC, and overall security posture for RHOAI users.

**Assumption**
An appropriate OpenShift IdP must be configured (see OCP-SEC-03).

**Alternatives**

- Leverage Configured OpenShift IdP (HTPasswd, LDAP, OIDC/OAuth)

**Decision**
#TODO#

**Justification**

- **Leverage Configured OpenShift IdP:** RHOAI integrates directly with the IdP configured at the OpenShift cluster level. The justification aligns with the choice made in OCP-SEC-03 (e.g., simplicity for HTPasswd, enterprise integration for LDAP, modern features/SSO for OIDC).

**Implications**

- The implications are inherited from the OCP-SEC-03 decision. RHOAI dashboard and components utilize the OpenShift OAuth proxy flow, meaning user authentication is handled transparently based on the cluster's IdP configuration. Group synchronization (OCP-SEC-04) becomes important for managing RHOAI roles (RHOAI-SM-06).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-06: User/Group Dashboard Access Configuration

**Architectural Question**
How will access to the OpenShift AI dashboard be controlled based on user groups?

**Issue or Problem**
By default, any authenticated OpenShift user can access the RHOAI dashboard. A mechanism is needed to restrict access to specific administrator and standard user groups defined in OpenShift, aligning with RBAC best practices.

**Assumption**
Access to the OpenShift AI dashboard must be restricted based on OpenShift user groups. OpenShift groups are synchronized or defined (OCP-SEC-04). RHOAI IdP integration is confirmed (RHOAI-SM-05).

**Alternatives**

- Configure Access via `Auth` Resource (Recommended)
- Use Default Unrestricted Access (Not Recommended for Production)

**Decision**
#TODO#

**Justification**

- **Configure Access via `Auth` Resource:** To manage RHOAI dashboard administrator and standard user access by defining the corresponding OpenShift group names in the dedicated `Auth` custom resource (`dscinitialization_odscustomizations_console_auth`). This is the standard, supported method.
- **Use Default Unrestricted Access:** To allow any authenticated OpenShift user to access the OpenShift AI dashboard without explicit group membership checks. Simplifies initial setup but lacks role separation.

**Implications**

- **Configure Access via `Auth` Resource:** Requires identifying or creating appropriate OpenShift groups (e.g., `rhods-admins`, `rhods-users`) and configuring the `Auth` resource (typically via GitOps overlay) to reference them. Enforces role separation (admins see admin settings, users see user view). Requires group sync or manual group management in OpenShift.
- **Use Default Unrestricted Access:** Simplest setup, no group configuration needed. Provides limited security segmentation; all authenticated users can log in, potentially seeing inappropriate options or consuming resources without oversight. Not suitable for multi-tenant or production environments.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-07: OpenShift AI Namespace Strategy (Core Components)

**Architectural Question**
What namespace strategy will be used for deploying OpenShift AI core components?

**Issue or Problem**
Red Hat OpenShift AI Self-Managed uses default projects (`redhat-ods-operator`, `redhat-ods-applications`), but enterprise environments often require custom names for standardization or compliance. This decision focuses on the core platform namespaces, distinct from user workload namespaces (RHOAI-SM-13).

**Assumption**
N/A

**Alternatives**

- Use Default RHOAI Namespaces (Core Components)
- Configure Custom Namespaces for RHOAI Core Components

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Use Default RHOAI Namespaces:** To simplify installation and maintenance by accepting the standard naming (`redhat-ods-*`). Aligns directly with documentation and default operator behavior.
- **Configure Custom Namespaces for RHOAI Core:** To adhere to strict organizational naming conventions by specifying custom project names for the core RHOAI operator and application components during installation via the `DataScienceCluster` CR.

**Implications**

- **Use Default Namespaces:** Easiest setup. May not meet strict naming policies.
- **Configure Custom Core Namespaces:** Requires defining custom names via `DataScienceCluster` CR _before_ initial installation. Ensures compliance with naming standards for platform components but adds configuration steps. Does not affect the default `rhods-notebooks` namespace unless also customized.

**Agreeing Parties**

- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-08: CA Certificate management

**Architectural Question**
Which CA certificate bundle will be used for Red Hat OpenShift AI components, and how will its lifecycle be managed?

**Issue or Problem**
OpenShift AI components require trusted CA certificates for secure TLS communication (internal and external). Choosing the bundle and manager affects trust scope, integration effort, and operational consistency.

**Assumption**
Secure communication using TLS is required.

**Alternatives**

- Managed by RHOAI Operator (Legacy/Compatibility Mode)
- Externally Managed (`managementState: Removed`, Recommended)

**Decision**
#TODO#

**Justification**

- **Managed by RHOAI Operator:** To have the OpenShift AI Operator automatically manage a `trusted-ca-bundle` ConfigMap. Simpler initial setup but less control and potentially conflicts with cluster-wide trust.
- **Externally Managed (`managementState: Removed`):** Recommended approach (RHOAI 2.25+). The operator does not manage the CA bundle. Trust is handled externally (e.g., via cluster-wide proxy settings, injected CAs via ConfigMaps referenced by workloads, service mesh trust). Offers better security separation and aligns with standard cluster practices.

**Implications**

- **Managed by RHOAI Operator:** Operator manages `trusted-ca-bundle` ConfigMap. Provides automatic trust injection for managed components but increases operator scope and potential conflicts.
- **Externally Managed/Removed:** Requires administrators to ensure necessary CAs are trusted via other mechanisms (cluster proxy, manual ConfigMaps, service mesh). More initial effort but clearer separation of concerns, less operator complexity. Preferred long-term.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-09: S3 Object Storage Location

**Architectural Question**
Will S3-compatible object storage be used for OpenShift AI, and if so, where will it be hosted?

**Issue or Problem**
OpenShift AI requires S3-compatible object storage for model serving artifacts (KServe) and Data Science Pipelines intermediate data. The choice of provider impacts integration, cost, latency, and management.

**Assumption**
Model serving (RHOAI-SM-27) and/or Data Science Pipelines (RHOAI-SM-33) capabilities are required.

**Alternatives**

- OpenShift Data Foundation (MCG) On-Cluster
- External Cloud Provider S3 Storage (e.g., AWS S3, Azure Blob, GCP)
- External Dedicated S3 Storage (e.g., MinIO, Ceph RGW On-Prem)

**Decision**
#TODO#

**Justification**

- **OpenShift Data Foundation (MCG):** To utilize integrated, on-cluster object storage provided by ODF (if deployed, OCP-STOR-01 / ODF-BASE-02), optimizing data co-location and simplifying platform storage management.
- **External Cloud Provider S3:** To leverage native cloud services for scalability, durability, and managed features (less relevant for on-prem context unless hybrid connectivity exists).
- **External Dedicated S3:** To utilize an existing, dedicated, enterprise-grade S3 solution (on-prem or private cloud) for centralized storage management outside the OCP cluster lifecycle.

**Implications**

- **OpenShift Data Foundation (MCG):** Requires ODF installation/configuration. Ensures low-latency access within cluster. Requires sizing ODF appropriately. Adds MCG resource overhead.
- **External Cloud Provider S3:** Requires external connectivity and secure credential management. Offloads S3 management. Cost based on provider.
- **External Dedicated S3:** Requires configuring external connectivity and secure credentials. Performance depends on network. Offloads S3 management to separate team/system.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert

---

## RHOAI-SM-10: Default storage class for Red Hat OpenShift AI components

**Architectural Question**
Which default storage class (StorageClass) will be configured for use by Red Hat OpenShift AI components requiring dynamic Persistent Volume provisioning?

**Issue or Problem**
Components like workbenches automatically create PVCs and rely on a cluster-defined default `StorageClass`. The selected default affects performance, access modes (RWO/RWX), and capacity management for these components.

**Assumption**
Dynamic volume provisioning is used. Components like Workbenches (RHOAI-SM-14) will require PVCs.

**Alternatives**

- Use Existing Cluster Default StorageClass
- Designate a Specific RHOAI Default StorageClass

**Decision**
#TODO#

**Justification**

- **Use Existing Cluster Default:** Simplest approach, leveraging the pre-configured default `StorageClass` if it meets RHOAI's needs (e.g., provides reliable RWO block storage).
- **Designate a Specific RHOAI Default:** Explicitly choose/create a `StorageClass` (e.g., from ODF, OCP-STOR-01 / ODF-BASE-01) and mark it as default (`storageclass.kubernetes.io/is-default-class: "true"`), ensuring RHOAI components use the desired backend. Requires cluster-admin privilege.

**Implications**

- **Use Existing Cluster Default:** RHOAI storage characteristics depend entirely on the cluster default. May not be optimal (e.g., slow performance). Easiest initial setup.
- **Designate Specific RHOAI Default:** Ensures RHOAI components (like workbench PVCs) use intended storage (e.g., ODF `ocs-storagecluster-ceph-rbd`). Requires administrative action to set default. **Important:** Changing the default affects _all_ workloads cluster-wide that don't specify an explicit `storageClassName`.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert

---

## RHOAI-SM-11: Usage data collection (Telemetry)

**Architectural Question**
Will you enable usage data collection (telemetry) for Red Hat OpenShift AI?

**Issue or Problem**
OpenShift AI Self-Managed can optionally send anonymized usage data to Red Hat to help improve the product. Enabling this affects privacy considerations, connectivity requirements (if connected), and compliance policies.

**Assumption**
N/A

**Alternatives**

- Enable Sending Usage Data to Red Hat
- Disable Sending Usage Data to Red Hat

**Decision**
#TODO#

**Justification**

- **Enable Sending Usage Data:** To contribute usage statistics that help Red Hat understand product usage patterns and prioritize improvements. May facilitate proactive support.
- **Disable Sending Usage Data:** To maintain strict data isolation, comply with privacy regulations, or operate in disconnected environments (RHOAI-SM-03).

**Implications**

- **Enable Sending Usage Data:** Requires outbound internet connectivity (if cluster is connected) to Red Hat's telemetry endpoints. Data is typically anonymized configuration and usage metrics. May require security/privacy review.
- **Disable Sending Usage Data:** Ensures no data leaves the cluster for telemetry. Requires explicitly setting `spec.telemetry.enabled: false` in the `DataScienceCluster` CR. Necessary for disconnected environments.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-12: Red Hat partner solutions integration

**Architectural Question**
Which Red Hat partner software (ISV) components will be enabled or integrated with Red Hat OpenShift AI?

**Issue or Problem**
OpenShift AI supports enabling certified partner software to enhance AI/ML capabilities. Choosing components impacts functionality, licensing, compatibility, resource usage, and complexity.

**Assumption**
N/A

**Alternatives**

- Anaconda Enterprise Notebooks
- IBM Watson Studio
- Intel AI Tools (including OpenVINO)
- NVIDIA AI Enterprise
- Pachyderm
- Starburst Galaxy
- None (Only Red Hat components)

**Decision**
#TODO#

**Justification**

- **Anaconda:** Provide Anaconda's curated package distribution/management.
- **IBM Watson Studio:** Integrate IBM's AI tools/MLOps capabilities.
- **Intel AI Tools:** Leverage Intel-optimized libraries/frameworks (OpenVINO).
- **NVIDIA AI Enterprise:** Utilize NVIDIA's optimized AI/ML software suite (requires NVIDIA GPUs, RHOAI-SM-22).
- **Pachyderm:** Integrate data versioning/pipelining.
- **Starburst Galaxy:** Integrate distributed SQL query engine.
- **None:** Rely solely on Red Hat components for simplicity/minimal dependencies.

**Implications**

- **Enabling ISV Components:** Typically requires separate partner licenses. Consumes additional cluster resources. Requires managing partner operator/component lifecycle. Adds specific functionalities. Compatibility must be maintained.
- **None:** Simplifies licensing/dependency management. Relies on RHOAI built-in features and community integrations.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

**(Start of User Environment Section)**

## RHOAI-SM-13: Data science project allocation strategy (User Namespaces)

**Architectural Question**
How will OpenShift Projects (Kubernetes Namespaces) be allocated and used for data science activities (workbenches, pipelines, models)?

**Issue or Problem**
OpenShift Projects provide isolation (resources, RBAC, network, quotas). The allocation strategy impacts multi-tenancy, resource management, security, and collaboration. (Aligns with OCP-MGT-01).

**Assumption**
Data science workloads need namespace isolation beyond the core RHOAI components (RHOAI-SM-07).

**Alternatives**

- Single Shared Data Science Project (e.g., default `rhods-notebooks`)
- Project per Team/Group
- Project per ML Project/Initiative
- Hybrid (e.g., Shared for experimentation, dedicated for production)

**Decision**
#TODO#

**Justification**

- **Single Shared Project:** Simplest, often uses default `rhods-notebooks`. Users share resources/RBAC. Suitable for small teams/pilots.
- **Project per Team/Group:** Isolation between DS teams. Allows team-specific RBAC, quotas, network policies. Promotes autonomy.
- **Project per ML Project/Initiative:** Highest isolation (per model/problem). Facilitates project-specific resource tracking/security.
- **Hybrid:** Shared space for experimentation, dedicated/controlled namespaces for critical pipelines/serving.

**Implications**

- **Single Shared:** Higher risk of resource contention (needs quotas, OCP-MGT-04). Complex internal RBAC/NetworkPolicy. Hard to track usage per initiative.
- **Project per Team:** Increases namespace count. Requires automation for project creation/config. Clearer resource/security boundaries per team.
- **Project per ML Project:** Largest number of namespaces, needs high automation. Granular control/chargeback.
- **Hybrid:** Balances flexibility/control but needs clear promotion processes between shared/dedicated namespaces.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-14: Notebook images for data scientists

**Architectural Question**
What notebook images (providing JupyterLab or other IDE environments) will be made available to data scientists?

**Issue or Problem**
Data scientists use notebook images within workbenches for their runtime environment (libs, tools). The choice and management strategy impacts available tools, consistency, security, maintenance, and user experience.

**Assumption**
Workbenches will be used (RHOAI-SM-16).

**Alternatives**

- Red Hat Provided Standard Images (CPU)
- Red Hat Provided CUDA Images (if NVIDIA GPUs enabled, RHOAI-SM-22)
- Red Hat Provided ROCm Images (if AMD GPUs enabled, RHOAI-SM-25)
- Red Hat Provided Intel Images (if Intel accelerators enabled, RHOAI-SM-24 / RHOAI-SM-26)
- Open Data Hub (ODH) Community Images
- Custom-Built Images (Derived from Red Hat/ODH)
- Combination of Above

**Decision**
#TODO#

**Justification**

- **Red Hat Provided Standard/CUDA/ROCm/Intel Images:** Use officially supported, certified images ensuring compatibility. Accelerator-specific images are necessary for GPU/HPU workloads.
- **ODH Community Images:** Leverage wider variety from upstream ODH (community support).
- **Custom-Built Images:** Create tailored environments with specific libraries/drivers/tools pre-installed for consistency/project needs.
- **Combination:** Offer a mix (supported base + custom) for flexibility.

**Implications**

- **Red Hat Provided:** Limited customization (users install packages at runtime). Updates managed via RHOAI upgrades. Consistent, supported baseline.
- **ODH Community:** More options but no official Red Hat support. Requires vetting. Community-dependent updates.
- **Custom-Built:** Max control/standardization. Requires build pipeline (Pipelines, Jenkins, etc.), dependency management, security scanning, updates. Increases maintenance. (See RHOAI-SM-15, RHOAI-SM-16).
- **Combination:** Flexibility but needs governance on support/management of custom images.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-15: Required Python packages (for Custom Notebook Images)

**Architectural Question**
If building custom notebook images, what additional Python packages (beyond the base image) are required by data scientists?

**Issue or Problem**
Custom notebook images need defined package sets. Identifying necessary packages upfront is crucial for image design, dependency management, and reproducibility.

**Assumption**
Custom notebook images will be built (Decision from RHOAI-SM-14).

**Alternatives**

- Minimal Common Set (e.g., visualization, data manipulation extensions)
- Domain-Specific Sets (e.g., NLP, CV, Time Series)
- Framework-Specific Sets (e.g., TensorFlow, PyTorch, XGBoost variants)
- Comprehensive Custom Set (Mixing multiple domains/frameworks)
- Allow Runtime Installation Only (No custom packages baked-in)

**Decision**
#TODO#

**Justification**

- **Minimal Common Set:** Provide generally useful tools with minimal bloat.
- **Domain/Framework-Specific Sets:** Create optimized, tailored images, reducing size/conflicts.
- **Comprehensive Custom Set:** Build 'kitchen-sink' image for convenience, potentially large/complex.
- **Runtime Installation Only:** Simplest custom image (base only), users install via pip/conda in workbench.

**Implications**

- **Baking Packages:** Ensures consistency/reproducibility. Reduces user startup time. Requires managing dependencies, rebuilding images for updates. Increases image size. Security scanning critical.
- **Domain/Framework-Specific:** Multiple images to manage, but tailored/smaller environments.
- **Runtime Installation Only:** Smallest images. Max user flexibility but risks inconsistencies. Users need internet/mirrors for install. Increases workbench setup time.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-16: Custom notebook images location

**Architectural Question**
Where will custom-built notebook server images be stored and accessed from?

**Issue or Problem**
Custom notebook images need hosting in a container registry accessible by the OpenShift cluster. The choice impacts accessibility, security, build pipeline integration, and operational management. (Aligns with OCP-MGT-03 for application images).

**Assumption**
Custom notebook images will be built (Decision from RHOAI-SM-14).

**Alternatives**

- Existing HA Corporate Registry (e.g., Quay, Artifactory, Nexus)
- OpenShift Internal Registry (Image Registry Operator)

**Decision**
#TODO#

**Justification**

- **Existing HA Corporate Registry:** Leverage existing enterprise registry for central storage, governance (scanning, signing), availability, scalability. Aligns with existing practices.
- **OpenShift Internal Registry:** Store images within the cluster. Simplifies network access (no external pulls), optimizes pull times, reduces external dependencies.

**Implications**

- **Existing HA Corporate Registry:** Requires network connectivity. Pull secrets needed in workbench namespaces. Build pipelines need push access. Integrates with existing security scanning/signing.
- **OpenShift Internal Registry:** Requires configuring internal registry with persistent storage (ODF RWO/RWX or other PVs, OCP-STOR-01). Lifecycle tied to cluster. Build pipelines within cluster can easily push. May need separate security scanning setup.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-17: Workbenches provisioning strategy

**Architectural Question**
How will workbenches (JupyterLab or other IDE environments) be provisioned and managed for data scientists?

**Issue or Problem**
Workbenches are the primary IDE. The provisioning strategy impacts resource allocation (CPU, memory, PVCs, GPUs), user experience, environment consistency, and cost.

**Assumption**
N/A

**Alternatives**

- Individual Workbench per User (Self-Service)
- Shared Team Workbenches
- Role/Task-Specific Workbench Configurations (e.g., GPU vs. CPU)

**Decision**
#TODO#

**Justification**

- **Individual Workbench per User:** Max isolation. Users self-select size/image within limits. Most common.
- **Shared Team Workbenches:** Potential resource savings by sharing larger instances. Requires user coordination.
- **Role/Task-Specific Configurations:** Pre-defined templates (sizes, images, accelerators) for roles/tasks. Simplifies user choice, enforces standards.

**Implications**

- **Individual:** Can lead to higher resource consumption if users provision large/GPU workbenches. Needs defined profiles/sizes and potentially quotas. Best user autonomy.
- **Shared:** Difficult to manage contention/interference. Impractical for sensitive data. Less common.
- **Role/Task-Specific:** Simplifies user choice with curated options. Requires admin definition/maintenance. Helps control resource usage.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-18: code-server workbenches enablement

**Architectural Question**
Will the `code-server` (VS Code in browser) workbench option be enabled alongside JupyterLab?

**Issue or Problem**
RHOAI allows enabling `code-server` as an alternative IDE, offering a VS Code experience. However, it's often Tech Preview, may lack full integration (e.g., Elyra, RHOAI-SM-34), and uses a different base image.

**Assumption**
Red Hat notebook server images (RHOAI-SM-14) are used. Workbenches are provisioned (RHOAI-SM-17).

**Alternatives**

- Enable Code-Server Workbench Option
- Disable Code-Server Workbench Option (JupyterLab Only)

**Decision**
#TODO#

**Justification**

- **Enable Code-Server:** Provide VS Code users an alternative IDE, potentially better for extensive scripting or specific extensions.
- **Disable Code-Server:** Standardize on JupyterLab, ensuring full feature compatibility (Elyra) and simplifying available image options.

**Implications**

- **Enable Code-Server:** Makes `code-server` image available. Users get VS Code but may lose Jupyter-specific integrations (Elyra). Often requires enabling Tech Preview features in `DataScienceCluster` CR.
- **Disable Code-Server:** Simplifies user choice, ensures all users get fully integrated JupyterLab. Reduces number of base images to manage/customize.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner

---

## RHOAI-SM-19: Cluster Storage (PVC) Sizing for Workbenches

**Architectural Question**
How will Persistent Volume Claim (PVC) sizing be managed for workbench local storage (/home/jovyan)?

**Issue or Problem**
Workbench PVC size impacts local data storage capacity and overall cluster storage consumption.

**Assumption**
Workbenches are configured (RHOAI-SM-17). Local PVC storage is used (RHOAI-SM-20).

**Alternatives**

- Fixed Default Size for All Workbenches
- User-Selectable Size (within pre-defined limits/tiers)
- Custom Size per Workbench (Admin controlled)

**Decision**
#TODO#

**Justification**

- **Fixed Default Size:** Simplest administration. Consistent starting point (e.g., 20Gi).
- **User-Selectable Size:** Flexibility for users to choose based on needs (e.g., Small-20Gi, Medium-50Gi, Large-100Gi).
- **Custom Size:** Most flexible but requires manual intervention/automation by admins.

**Implications**

- **Fixed Default:** May be insufficient for large local datasets/libraries. Users might hit limits. Easiest capacity planning.
- **User-Selectable:** Balances flexibility/control. Needs defined tiers and potentially project quotas (OCP-MGT-04). Users need guidance.
- **Custom:** High admin overhead unless automated. Precise allocation but complicates capacity management.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert

---

## RHOAI-SM-20: Notebook file storage location

**Architectural Question**
Where will data scientists primarily store their notebook files (`.ipynb`) and associated code/scripts developed within workbenches?

**Issue or Problem**
Notebook files are core work products. The storage strategy impacts version control, collaboration, reproducibility, backup/recovery, and MLOps practices.

**Assumption**
Workbenches are used (RHOAI-SM-17).

**Alternatives**

- Local Workbench Storage (PVC) Only
- Git Repository (Integrated with Workbench)

**Decision**
#TODO#

**Justification**

- **Local Workbench Storage (PVC):** Simplicity and immediate persistence within user's workbench environment (on attached PVC, RHOAI-SM-19).
- **Git Repository:** Enable version control, collaboration, code reviews, easier integration with CI/CD or MLOps pipelines. Workbenches can clone Git repos. Recommended best practice.

**Implications**

- **Local PVC Only:** Simplest setup. Persists across workbench restarts. Difficult version control/collaboration. Requires PVC backup strategy (RHOAI-SM-40) for resilience. Can lead to data silos.
- **Git Repository:** Promotes best practices. Requires users to commit/push regularly. Needs network connectivity to Git server. Git credentials management needed (secrets). Enables GitOps workflows. Data resilience relies on Git server backup strategy. Enables RHOAI-SM-21.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner

---

## RHOAI-SM-21: Notebook Git repository structure

**Architectural Question**
If using Git for notebook storage, how will repositories be structured and managed for data science collaboration?

**Issue or Problem**
Repository structure/access patterns impact collaboration efficiency, code sharing, version control clarity, MLOps integration.

**Assumption**
Notebook files/code primarily stored in Git (RHOAI-SM-20).

**Alternatives**

- Single Shared Mono-Repository (All projects/teams)
- Repository per Team/Group
- Repository per Project/Initiative
- Hybrid Approach (e.g., Shared libs repo + project repos)

**Decision**
#TODO#

**Justification**

- **Mono-Repo:** Simplify discovery/dependency management. Easier central standards enforcement.
- **Repo per Team:** Provide autonomy/clear ownership. Align access control with team structure.
- **Repo per Project:** Isolate work per ML model/business problem. Facilitate project-specific lifecycles.
- **Hybrid:** Balance central standards/shared code (common lib repo) with project flexibility (dedicated project repos).

**Implications**

- **Mono-Repo:** Can become large/complex. Needs robust branching strategies/CODEOWNERS. CI/CD triggers can be noisy.
- **Repo per Team:** Can lead to code duplication if sharing needed. Needs mechanisms for cross-team discovery/reuse. Simplifies team access control.
- **Repo per Project:** Creates many repos. Clear isolation but potentially hinders cross-project collaboration/standardization.
- **Hybrid:** Flexible but needs clear governance (what belongs where, dependency management).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner

---

**(Start of Data & Accelerators Section)**

## RHOAI-SM-22: Data sources accessibility

**Architectural Question**
Which types of data sources need to be accessible to data scientists within the OpenShift AI platform?

**Issue or Problem**
Data scientists require access to various data sources. Identifying these and planning connectivity impacts network configuration, security policies, authentication, and tools needed within workbenches.

**Assumption**
Data scientists will need to access data beyond local workbench storage. S3 Location decided (RHOAI-SM-09).

**Alternatives**

- S3-Compatible Object Storage (Configured in RHOAI-SM-09)
- Relational Databases (e.g., PostgreSQL, MySQL)
- Data Warehouses (e.g., Snowflake, Redshift, Teradata)
- Data Lakes (e.g., HDFS, Iceberg via Trino/Spark)
- Feature Stores
- Streaming Platforms (e.g., Kafka)
- Combination of Above
- Primarily Local/Uploaded Data Only

**Decision**
#TODO#

**Justification**

- **S3-Compatible:** Access large datasets in object storage.
- **Relational DBs:** Query structured data.
- **Data Warehouses:** Connect to enterprise DWs for analytics/BI data.
- **Data Lakes:** Access large volumes of raw/semi-structured data.
- **Feature Stores:** Access curated, reusable features.
- **Streaming Platforms:** Process real-time data streams.
- **Combination:** Provide maximum flexibility.
- **Local/Uploaded Only:** Simplify initial setup, relying on manual data transfer.

**Implications**

- **Connecting External Sources:** Requires network connectivity (firewalls, routing, DNS - OCP-NET decisions), credentials/authentication (secrets management, OCP-SEC-10), and necessary drivers/libraries within notebook images (RHOAI-SM-14). Security reviews needed.
- **S3:** Requires configuring access credentials and potentially S3 libraries (boto3).
- **DBs/DWs:** Requires installing drivers (psycopg2) and managing connection strings/credentials securely.
- **Lakes/Streaming:** May require specialized libraries (PySpark, Kafka clients) and complex network configs.
- **Feature Stores:** Requires deploying/integrating the feature store platform.
- **Local/Uploaded:** Simplest network/security setup but limits scalability/collaboration on large datasets.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert

---

## RHOAI-SM-23: NVIDIA GPU Support enablement

**Architectural Question**
Will NVIDIA GPUs be utilized by Red Hat OpenShift AI workloads?

**Issue or Problem**
OpenShift AI supports NVIDIA GPUs for compute-intensive tasks (training, inference). Enabling them impacts hardware requirements, cost, installation complexity (NVIDIA GPU Operator), versus potential performance gains.

**Assumption**
Workloads potentially require GPU acceleration. Sizing Strategy considered (OCP-BASE-10).

**Alternatives**

- Enable NVIDIA GPU Support
- Disable NVIDIA GPU Support

**Decision**
#TODO#

**Justification**

- **Enable NVIDIA GPU Support:** Accelerate demanding AI/ML workloads using NVIDIA GPU hardware. Essential for many deep learning tasks.
- **Disable NVIDIA GPU Support:** Simplify cost/setup if workloads don't require NVIDIA GPUs or if alternative accelerators (RHOAI-SM-24, RHOAI-SM-25) are sufficient.

**Implications**

- **Enable NVIDIA GPU Support:** Requires compatible NVIDIA GPU hardware. Necessitates installation/configuration of NVIDIA GPU Operator (see NVIDIA-GPU-01). Increases cost/complexity. Enables use of CUDA images (RHOAI-SM-14) and potentially NVIDIA AI Enterprise (RHOAI-SM-12), NIM (RHOAI-SM-30), NIM Metrics (RHOAI-SM-31), DCGM Monitoring (NVIDIA-GPU-04). Affects Sizing (OCP-BASE-10).
- **Disable NVIDIA GPU Support:** Simplifies setup/maintenance. Limits high-performance workloads suitable for NVIDIA GPUs.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## RHOAI-SM-24: Intel HPU Accelerator Usage

**Architectural Question**
Will Intel HPUs (e.g., Gaudi) be utilized by Red Hat OpenShift AI workloads?

**Issue or Problem**
OpenShift AI supports Intel HPUs for cost-effective deep learning performance. Enabling them impacts hardware needs, cost, and complexity versus potential gains.

**Assumption**
Workloads potentially require HPU acceleration. Sizing Strategy considered (OCP-BASE-10).

**Alternatives**

- Enable Intel HPU Usage (Gaudi)
- Do Not Enable Intel HPU Usage

**Decision**
#TODO#

**Justification**

- **Enable Intel HPU Usage (Gaudi):** Utilize supported Intel Gaudi devices for a cost-efficient, flexible, scalable solution optimized for deep learning.
- **Do Not Enable Intel HPU Usage:** Simplify hardware/procurement by relying on CPU, GPUs (RHOAI-SM-23, RHOAI-SM-25), or other accelerators.

**Implications**

- **Enable Intel HPU Usage (Gaudi):** Requires installation/configuration of device plugins/operators (Intel AI Tools or Habana Operator). Requires specific Intel hardware procurement. Needs container images compatible with Habana SynapseAI SDK (RHOAI-SM-14). Affects Sizing (OCP-BASE-10). Enables RHOAI-SM-26.
- **Do Not Enable Intel HPU Usage:** Limits acceleration options. Reduces operational overhead for Intel devices.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## RHOAI-SM-25: AMD GPU Accelerator Usage

**Architectural Question**
Will AMD GPUs (ROCm) be utilized by Red Hat OpenShift AI workloads?

**Issue or Problem**
Enabling AMD GPUs supports high-performance AI/ML using ROCm but impacts hardware, complexity, and has limitations (e.g., disconnected environments).

**Assumption**
Workloads potentially require GPU acceleration. Sizing Strategy considered (OCP-BASE-10).

**Alternatives**

- Enable AMD GPU Usage (ROCm)
- Do Not Enable AMD GPU Usage

**Decision**
#TODO#

**Justification**

- **Enable AMD GPU Usage (ROCm):** Support high-performance AI/ML leveraging AMD ROCm platform, providing an alternative accelerator option.
- **Do Not Enable AMD GPU Usage:** Simplify hardware/ecosystem dependency by relying on other supported accelerators (NVIDIA RHOAI-SM-23, Intel RHOAI-SM-24, CPU).

**Implications**

- **Enable AMD GPU Usage (ROCm):** Requires AMD GPU Operator installation. **Currently unsupported for disconnected installations (RHOAI-SM-03)**. Requires compatible AMD Instinct hardware and ROCm-compatible images (RHOAI-SM-14). Affects Sizing (OCP-BASE-10).
- **Do Not Enable AMD GPU Usage:** Limits hardware options. Avoids ROCm integration complexity and disconnected limitation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## RHOAI-SM-26: Workbenches on Intel hardware

**Architectural Question**
If using Intel accelerators (e.g., Intel Data Center GPUs, potentially HPUs), will Intel-optimized workbench images be used?

**Issue or Problem**
Leveraging Intel accelerators within workbenches requires specific Intel libraries/drivers. Standard images may not utilize hardware efficiently.

**Assumption**
Intel accelerators are available (RHOAI-SM-24). Intel partner component might be enabled (RHOAI-SM-12). Notebook images decided (RHOAI-SM-14).

**Alternatives**

- Use Intel-Optimized Workbench Images
- Use Standard Red Hat Workbench Images

**Decision**
#TODO#

**Justification**

- **Use Intel-Optimized Images:** Provide environments with necessary Intel libraries (oneAPI AI Toolkit, OpenVINO) for developing/testing workloads optimized for Intel hardware.
- **Use Standard Images:** Simplify if Intel optimization within workbench isn't primary, or if Intel hardware isn't present/used by workbenches.

**Implications**

- **Use Intel-Optimized Images:** Requires making these images available (Red Hat/Intel provided or custom, RHOAI-SM-14). May need Intel device plugin operator installed. Ensures workloads can leverage Intel features.
- **Use Standard Images:** Simplifies image management. Workloads needing Intel optimizations require runtime library installation or rely on CPU. Intel accelerators likely unused by these workbenches.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner

---

**(Start of Pipelines & Distributed Workloads Section)**

## RHOAI-SM-27: Data Science Pipelines enablement (KFP/Tekton)

**Architectural Question**
Will the Data Science Pipelines component (based on Kubeflow Pipelines with Tekton backend) be enabled within RHOAI?

**Issue or Problem**
Enabling Data Science Pipelines provides a framework for orchestrating multi-step ML workflows. It requires specific configuration (database, object storage) and impacts the tools available to MLOps engineers. (Related to PIPELINES-01 for broader CI/CD strategy).

**Assumption**
Orchestration of ML workflows is required.

**Alternatives**

- Enable Data Science Pipelines Component
- Disable Data Science Pipelines Component (Rely on OpenShift Pipelines/Tekton or external orchestrators)

**Decision**
#TODO#

**Justification**

- **Enable Data Science Pipelines:** To provide an integrated, UI-driven (via RHOAI dashboard and Elyra) and SDK-driven platform specifically designed for defining, running, and managing ML pipelines within OpenShift AI. Uses Kubeflow Pipelines API standard with Tekton execution.
- **Disable Data Science Pipelines:** To simplify the RHOAI deployment if ML pipeline orchestration is handled by other tools (e.g., standard OpenShift Pipelines/Tekton for simpler CI/CD-like tasks, external orchestrators like Airflow, or if not required initially).

**Implications**

- **Enable Data Science Pipelines:** Installs KFP/Tekton components. Requires configuring a database backend (RHOAI-SM-29) and S3 object storage (RHOAI-SM-09). Enables Elyra usage (RHOAI-SM-28). Consumes additional cluster resources. Provides ML-specific pipeline features (artifact tracking, metadata).
- **Disable Data Science Pipelines:** Reduces RHOAI footprint and dependencies. Users needing pipeline orchestration must use alternative tools. Elyra extension in JupyterLab will not function for pipeline submission.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-28: Pipelines in JupyterLab (Elyra) usage

**Architectural Question**
Will the Elyra extension for visual pipeline authoring within JupyterLab be enabled and utilized for Data Science Pipelines?

**Issue or Problem**
Elyra provides a UI within JupyterLab for building KFP/Tekton pipelines visually. Enabling it requires compatible notebook images and impacts user workflow.

**Assumption**
Data Science Pipelines component is enabled (RHOAI-SM-27). Users primarily use JupyterLab (RHOAI-SM-17/RHOAI-SM-18).

**Alternatives**

- Enable and Promote Elyra Usage
- Disable or Do Not Promote Elyra (Use KFP SDK Primarily)

**Decision**
#TODO#

**Justification**

- **Enable Elyra:** Provide intuitive visual tool for pipeline construction in Jupyter, lowering barrier to entry.
- **Disable Elyra:** Standardize on programmatic pipeline definition using KFP SDK directly in code. Offers more flexibility/control for complex pipelines but needs more coding expertise.

**Implications**

- **Enable Elyra:** Requires notebook images including Elyra (most standard RHOAI images do, RHOAI-SM-14). Simplifies pipeline creation. Generated pipeline is KFP/Tekton compatible. Some advanced KFP features might not be exposed via UI.
- **Disable Elyra:** Users define pipelines entirely via KFP SDK (Python). Requires SDK in notebook images. Provides full access to all KFP features but steeper learning curve.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner

---

## RHOAI-SM-29: Pipeline database backend (KFP)

**Architectural Question**
Which database backend will be used for storing Red Hat OpenShift AI Pipelines (Kubeflow Pipelines / KFP Tekton) metadata?

**Issue or Problem**
Data Science Pipelines require a database (SQL-based) for run history, metadata, artifacts. Choice impacts scalability, reliability, persistence, operational management.

**Assumption**
Data Science Pipelines component is enabled (RHOAI-SM-27).

**Alternatives**

- Internal MariaDB (Auto-deployed by RHOAI)
- External MySQL/MariaDB (User-managed)

**Decision**
#TODO#

**Justification**

- **Internal MariaDB:** Simplicity/ease of setup. RHOAI auto-deploys MariaDB within cluster. Suitable for non-prod or smaller scale.
- **External MySQL/MariaDB:** Production environments needing higher scalability, reliability, integration with existing DB backup/management. Leverages external, potentially HA database.

**Implications**

- **Internal MariaDB:** Simplest deployment. Runs as pods, consumes cluster resources. Data on PVC; persistence/backup depend on cluster storage/backup strategy (RHOAI-SM-40). May not scale for very high throughput.
- **External MySQL/MariaDB:** Requires provisioning/managing separate DB instance. RHOAI Pipelines need connection details config. Offloads DB management but adds external dependency. Allows leveraging enterprise DB features (HA, backup, monitoring).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert (if internal uses ODF)

---

## RHOAI-SM-30: Distributed workloads enablement (Ray/CodeFlare)

**Architectural Question**
Will the capability for distributed AI/ML workloads using Ray (via CodeFlare/KubeRay) be enabled?

**Issue or Problem**
RHOAI includes operators for temporary Ray clusters (distributed data processing/training). Enabling impacts cluster resources, dependencies, complexity.

**Assumption**
Workloads might benefit from distributed computation.

**Alternatives**

- Enable Distributed Workloads (CodeFlare/KubeRay)
- Disable Distributed Workloads

**Decision**
#TODO#

**Justification**

- **Enable Distributed Workloads:** Allow data scientists to scale computationally intensive tasks (large data preprocessing, distributed training) across multiple nodes using Ray framework.
- **Disable Distributed Workloads:** Simplicity/resource conservation if workloads don't require distributed compute beyond single-node (multi-core/GPU).

**Implications**

- **Enable Distributed Workloads:** Installs CodeFlare/KubeRay operators. Requires additional cluster resources (~1.6 vCPU, ~2 GiB RAM for operators minimum). Users define/launch Ray clusters (`AppWrapper` or `RayCluster` CRs). Requires configuring security (Ray dashboard certs). Adds complexity but enables performance gains for suitable workloads. Enables RHOAI-SM-31, RHOAI-SM-32, RHOAI-SM-33.
- **Disable Distributed Workloads:** Reduces operators/resources consumed by RHOAI. Simplifies platform but limits ability to scale certain tasks horizontally.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-31: Quota management for distributed workloads (Kueue)

**Architectural Question**
How will resource quotas and scheduling for distributed workloads (Ray clusters via CodeFlare) be managed?

**Issue or Problem**
Distributed workloads (Ray clusters) consume significant resources. RHOAI integrates Kueue for batch scheduling/resource quota management specifically for these, preventing cluster saturation. Configuration impacts resource sharing/prioritization.

**Assumption**
Distributed workloads (CodeFlare/KubeRay) are enabled (RHOAI-SM-30).

**Alternatives**

- Enable Kueue Integration (Recommended)
- Disable Kueue Integration (Rely on OpenShift Quotas only)

**Decision**
#TODO#

**Justification**

- **Enable Kueue:** Leverage Kueue's batch scheduling (fair sharing, prioritization) and resource quotas (`ClusterQueue`, `LocalQueue`) designed for managing ephemeral, high-resource jobs like Ray clusters. Finer control than standard OpenShift quotas.
- **Disable Kueue:** Rely solely on standard OpenShift ResourceQuotas at namespace level (OCP-MGT-04). Simpler setup but lacks advanced scheduling features.

**Implications**

- **Enable Kueue:** Installs Kueue operator. Requires configuring `ClusterQueue` (overall resources) and potentially `LocalQueue`s (user namespace subdivision). Adds scheduling overhead but better control over resource-intensive batch jobs.
- **Disable Kueue:** Simplifies installation. Ray cluster consumption limited only by standard OCP quotas, risking resource exhaustion/unfair distribution with concurrent large jobs. Lacks queuing/prioritization.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-32: Authentication Method for Ray Dashboard

**Architectural Question**
Which authentication method will be used to secure access to the Ray Dashboard associated with distributed Ray clusters?

**Issue or Problem**
The Ray Dashboard needs protection. RHOAI supports integrating it with OpenShift OAuth (SSO) or alternative methods.

**Assumption**
Distributed workloads (CodeFlare/KubeRay) are enabled (RHOAI-SM-30).

**Alternatives**

- OpenShift OAuth Integration (Default/Recommended)
- Custom/No Integrated Authentication

**Decision**
#TODO#

**Justification**

- **OpenShift OAuth:** Leverage cluster's existing authentication for seamless/secure access based on OpenShift user/RBAC. Simplifies user management.
- **Custom/No Auth:** Use alternative methods (Ray's own, or unprotected in trusted envs). Flexible but potentially less secure or more config effort.

**Implications**

- **OpenShift OAuth:** Requires configuring OCP OAuth details in Ray cluster definition (often handled by CodeFlare defaults). Access controlled via OCP login/roles. May need cert handling for custom cluster CAs.
- **Custom/No Auth:** Bypasses OCP login for dashboard. Requires manual Ray security config or accepts lower security. Simpler in isolated test envs, not recommended for prod.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-33: Distributed workloads monitoring (Ray)

**Architectural Question**
Will monitoring be enabled for distributed workloads (Ray clusters)?

**Issue or Problem**
Monitoring Ray clusters provides visibility (resource usage, job status) but requires enabling OpenShift User Workload Monitoring (UWM) and ensuring Ray metrics are scraped, impacting resources/configuration. (Aligns with OCP-MON-01).

**Assumption**
Distributed workloads (CodeFlare/KubeRay) are enabled (RHOAI-SM-30).

**Alternatives**

- Enable Ray Monitoring via UWM
- Disable Ray Monitoring

**Decision**
#TODO#

**Justification**

- **Enable Ray Monitoring:** Collect metrics from Ray clusters (resource utilization, task status), integrate into OpenShift Monitoring (Grafana) for observability. Essential for performance/troubleshooting.
- **Disable Ray Monitoring:** Simpler deployment, reduced resource use if detailed Ray metrics aren't needed (rely on basic pod metrics, logs, Ray Dashboard).

**Implications**

- **Enable Ray Monitoring:** Requires enabling User Workload Monitoring (UWM) in cluster (OCP-MON-01). Consumes Prometheus resources for scraping/storing Ray metrics. Ray cluster defs need annotations/labels for scraping. Provides valuable operational insights.
- **Disable Ray Monitoring:** Reduces monitoring overhead/resource use. Limits visibility into Ray cluster internal state/performance, making troubleshooting harder.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

**(Start of Model Serving Section)**

## RHOAI-SM-34: Model Serving Platform Selection

**Architectural Question**
Which model serving platform architecture will be used in Red Hat OpenShift AI?

**Issue or Problem**
A decision is needed on the technology for deploying models as scalable endpoints, affecting dependencies, resources, complexity, and features (e.g., scale-to-zero).

**Assumption**
Model deployment capabilities are required.

**Alternatives**

- KServe (Single Model Serving / RawDeployment Mode)
- Custom Application Deployment (OpenShift Deployments)

**Decision**
#TODO#

**Justification**

- **KServe (RawDeployment Mode):** Deploy each model as a separate, scalable endpoint optimized for AI/ML using integrated KServe. Leverages standardized inference protocols, model management, observability. RawDeployment avoids reliance on OpenShift Serverless.
- **Custom Application Deployment:** Use standard OpenShift methods (`Deployment`, `Service`) for model endpoints, wrapping model in custom container. Max control over Kubernetes primitives but requires building more infrastructure manually.

**Implications**

- **KServe (RawDeployment Mode):** Requires KServe components (Operator, Controller). Relies on Istio Service Mesh for advanced traffic management. Provides standardized MLOps workflow but abstracts some K8s details. RawDeployment ensures compatibility/avoids deprecated Serverless dependencies.
- **Custom Application Deployment:** Requires developers to build container images with serving logic (Flask/FastAPI) and manually create K8s resources (`Deployment`, `Service`, `Route`, `HPA`). Lacks specialized KServe features (standardized metrics, easy canary) unless implemented manually.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-35: Authorization provider for KServe Model Serving

**Architectural Question**
Will an authorization provider (Authorino) be used for KServe single-model serving endpoints?

**Issue or Problem**
KServe endpoints may need fine-grained authorization beyond basic OpenShift RBAC. Using Authorino (integrated with Istio) impacts security granularity and complexity. Skipping it relies on simpler OpenShift/Istio mechanisms.

**Assumption**
Single-model serving platform (KServe) is enabled (RHOAI-SM-34).

**Alternatives**

- Use Authorino for KServe Authorization
- Do Not Use Authorino (Rely on OpenShift RBAC/Istio Policy)

**Decision**
#TODO#

**Justification**

- **Use Authorino:** Enable dynamic, policy-based, fine-grained authorization (OIDC tokens, API keys, JWT claims) for accessing served models, enhancing endpoint security.
- **Do Not Use Authorino:** Simpler authorization management, relying on native OpenShift RBAC and standard Istio authorization policies for basic access control.

**Implications**

- **Use Authorino:** Requires Authorino Operator installation/configuration. Needs expertise in Authorino `AuthConfig` policies and Istio integration. Increases complexity but provides robust, flexible authorization.
- **Do Not Use Authorino:** Reduces admin overhead/dependencies. Authorization relies on standard K8s/Istio mechanisms, possibly offering less granularity.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-36: Model-serving runtime for KServe

**Architectural Question**
Which specific model serving runtime(s) will be primarily used within the KServe single-model serving platform?

**Issue or Problem**
KServe supports various runtimes for different model formats and optimizations (LLMs, ONNX, scikit-learn). Selecting runtimes determines which models can be served and how efficiently.

**Assumption**
Single-model serving platform (KServe) is enabled (RHOAI-SM-34).

**Alternatives**

- RHOAI Custom Runtimes (Caikit+TGIS based, default for LLMs)
- KServe Core Runtimes (e.g., SKLearnServer, XGBoostServer, PMMLServer)
- vLLM Runtime (via KServe Custom Runtime - for high-throughput LLM inference)
- OpenVINO Model Server (OVMS) Runtime (via KServe Custom Runtime - optimized for Intel)
- NVIDIA Triton Inference Server (via KServe Custom Runtime - GPU-focused, multi-format)
- Custom-Built Runtimes

**Decision**
#TODO#

**Justification**

- **RHOAI Custom (Caikit+TGIS):** Use default RHOAI runtime, optimized for LLMs with Caikit framework/TGIS.
- **KServe Core:** Leverage standard runtimes for common formats (scikit-learn, XGBoost, PMML).
- **vLLM:** Achieve high throughput/low latency LLM inference via specialized vLLM engine (custom runtime).
- **OVMS:** Optimize inference performance, particularly on Intel hardware (CPU, GPU, VPU) (custom runtime).
- **Triton:** Use NVIDIA's flexible inference server (multiple frameworks, NVIDIA GPU optimized) (custom runtime).
- **Custom-Built:** Support niche formats or bespoke logic by building custom KServe runtime container.

**Implications**

- **RHOAI/KServe Core:** Easier management (often included/documented). May not offer peak performance for all types/hardware.
- **vLLM/OVMS/Triton (Custom):** Higher performance for specialized domains (LLMs, Intel, NVIDIA GPUs). Requires deploying/managing custom `ServingRuntime`/`ClusterServingRuntime`. May need specific hardware (GPUs for vLLM/Triton). Compatibility must be maintained.
- **Custom-Built:** Max flexibility but requires significant development/maintenance for runtime container/KServe integration.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-37: NVIDIA NIM Serving Platform Integration

**Architectural Question**
Will NVIDIA NIM integration be enabled for the single-model serving platform in Red Hat OpenShift AI?

**Issue or Problem**
NVIDIA NIM provides optimized inference microservices for LLMs. Enabling it impacts integration complexity and hardware dependency.

**Assumption**
NVIDIA GPU acceleration is enabled (RHOAI-SM-23). Single-model serving (KServe) is enabled (RHOAI-SM-34).

**Alternatives**

- Enable NVIDIA NIM Integration
- Rely on Standard KServe Runtime Environment (e.g., vLLM, Triton, Caikit)

**Decision**
#TODO#

**Justification**

- **Enable NVIDIA NIM:** Leverage NVIDIA's optimized microservices for deploying high-performance LLMs, maximizing GPU utilization for inference.
- **Rely on Standard KServe:** Use generic KServe model servers without specialized NVIDIA inference components.

**Implications**

- **Enable NVIDIA NIM:** Requires specific hardware/software configs validated by NVIDIA/Red Hat. Requires access to NIM images (NGC). Increases complexity (integrating specialized proprietary software). Requires deploying NIM as custom KServe runtime. May involve NVIDIA AI Enterprise licensing (RHOAI-SM-12).
- **Rely on Standard KServe:** Less specialized integration. Performance optimization relies on chosen model server (vLLM, Triton, Caikit) and GPU Operator config (NVIDIA-GPU-XX ADs).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## RHOAI-SM-38: Distributed Inference with LLM-D [TECH-PREVIEW]

**Architectural Question**
Will the Distributed Inference with llm-d component [TECH-PREVIEW] be used for large language model serving?

**Issue or Problem**
Serving LLMs often requires significant resources and sharding workloads across multiple nodes/GPUs, which is complex for scaling/recovery. `llm-d` aims to simplify this.

**Assumption**
LLMs requiring distributed processing (multi-GPU/multi-node) are planned for deployment via KServe (RHOAI-SM-34).

**Alternatives**

- Enable Distributed Inference with llm-d [TECH-PREVIEW]
- Rely on Standard KServe (Single-Instance or basic scaling) Deployment

**Decision**
#TODO#

**Justification**

- **Enable llm-d:** Simplify complex LLM deployments by providing capabilities for sharding workloads across multiple nodes/GPUs using this specialized framework.
- **Rely on Standard KServe:** Use default serving mechanism where model runs within single KServe instance (can use multi-GPU on one node). Suitable for models not requiring multi-node sharding.

**Implications**

- **Enable llm-d:** **Technology Preview** feature, not supported under production SLAs. Requires specific configuration in KServe `InferenceService` to use `llm-d` runtime. Adds complexity specific to this preview feature.
- **Rely on Standard KServe:** Limits size/requirements of models efficiently served from single KServe endpoint (though KServe scales replicas horizontally). Doesn't natively handle model sharding across instances.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

**(Start of Monitoring & Lifecycle Section)**

## RHOAI-SM-39: Single-model serving platform (KServe) monitoring enablement

**Architectural Question**
Will monitoring be enabled for the KServe single-model serving platform?

**Issue or Problem**
Monitoring KServe `InferenceService` deployments provides visibility into request latency, throughput, success/error rates, and resource usage. Enabling it requires User Workload Monitoring (UWM). (Aligns with OCP-MON-01).

**Assumption**
Single-model serving platform (KServe) is enabled (RHOAI-SM-34).

**Alternatives**

- Enable KServe Monitoring via UWM
- Disable KServe Monitoring

**Decision**
#TODO#

**Justification**

- **Enable KServe Monitoring:** Collect metrics from served models, integrate into OpenShift Monitoring (Grafana). Crucial for understanding serving performance, identifying bottlenecks, setting alerts.
- **Disable KServe Monitoring:** Simpler deployment, reduced resource use if detailed serving metrics aren't required (rely on basic pod metrics/logs).

**Implications**

- **Enable KServe Monitoring:** Requires enabling User Workload Monitoring (UWM) in cluster (OCP-MON-01). Consumes Prometheus resources for scraping/storing KServe metrics. Provides essential MLOps observability. RHOAI typically configures KServe scraping automatically if UWM enabled.
- **Disable KServe Monitoring:** Reduces monitoring overhead. Limits visibility into model serving performance, making diagnosis/optimization harder.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-40: NVIDIA NIM Metrics collection

**Architectural Question**
If using NVIDIA NIM, will metrics collection be enabled for NIM-based KServe deployments?

**Issue or Problem**
Monitoring NIM-specific metrics (GPU utilization, inference latency) enhances visibility but requires ensuring NIM endpoints are scraped by OpenShift Monitoring (UWM).

**Assumption**
NVIDIA NIM integration is enabled (RHOAI-SM-37). User Workload Monitoring (UWM) is enabled (OCP-MON-01 / RHOAI-SM-39).

**Alternatives**

- Enable NIM Metrics Collection
- Disable NIM Metrics Collection

**Decision**
#TODO#

**Justification**

- **Enable NIM Metrics:** Detailed visibility into performance/resource consumption of NIM inference servers for troubleshooting/optimization.
- **Disable NIM Metrics:** Reduce monitoring overhead if standard KServe/pod metrics suffice.

**Implications**

- **Enable NIM Metrics:** Requires configuring `ServiceMonitor`/`PodMonitor` to target NIM metrics endpoint within KServe `InferenceService`. May need custom annotations. Consumes Prometheus resources.
- **Disable NIM Metrics:** Simplifies monitoring config but limits insight into NIM runtime behavior. Relies on higher-level KServe metrics.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-41: TrustyAI Monitoring for Data Science Models

**Architectural Question**
Will the TrustyAI component be enabled for monitoring model fairness and explainability?

**Issue or Problem**
TrustyAI provides advanced monitoring (fairness metrics, explainability) beyond basic serving metrics. Enabling it requires deploying the TrustyAI service and integrating it with model serving runtimes.

**Assumption**
Model serving (likely KServe, RHOAI-SM-34) is enabled.

**Alternatives**

- Enable TrustyAI Service
- Disable TrustyAI Service

**Decision**
#TODO#

**Justification**

- **Enable TrustyAI:** Gain insights into model fairness, identify bias, generate explanations for predictions, supporting responsible AI/compliance.
- **Disable TrustyAI:** Simpler deployment if advanced fairness/explainability monitoring aren't immediate needs (rely on standard performance metrics, RHOAI-SM-39).

**Implications**

- **Enable TrustyAI:** Requires enabling `trustyai` component in `DataScienceCluster` CR. Deploys TrustyAI operator/service pods (consumes resources). `InferenceService`s need configuration (annotations) to send prediction data to TrustyAI. Requires expertise in configuring fairness metrics/interpreting explanations.
- **Disable TrustyAI:** Reduces resource use/config complexity. Limits observability to standard operational metrics, lacking insights into bias/rationale.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-42: Persistent Volume Claim (PVC) Backup Strategy for RHOAI

**Architectural Question**
Will backup be implemented for Persistent Volume Claims (PVCs) used specifically by Red Hat OpenShift AI components (e.g., workbenches, pipeline metadata DB if internal)?

**Issue or Problem**
A defined backup strategy is needed for data recoverability/compliance for critical artifacts stored in RHOAI-related PVCs. (Aligns with OCP-MGT-05 for general platform backup).

**Assumption**
RHOAI components utilize PVCs (e.g., Workbenches RHOAI-SM-17/RHOAI-SM-19, Internal Pipeline DB RHOAI-SM-29). Data persistence/recovery is required.

**Alternatives**

- OADP Operator using CSI Snapshots/Kopia (Leveraging Platform Strategy)
- No Dedicated Backup Solution for RHOAI PVCs (Rely on user actions like Git or underlying storage snapshots only)

**Decision**
#TODO#

**Justification**

- **OADP Operator:** Leverage official OpenShift API for Data Protection (OADP) for application-consistent backup of RHOAI PVCs (using volume snapshots for CSI storage like ODF, or file backups via Kopia). Integrates with platform backup strategy (OCP-MGT-05). Recommended for comprehensive protection.
- **No Dedicated Backup:** Rely on underlying storage snapshots (application-unaware) or manual user actions (Git push, RHOAI-SM-20). Accepts risk of non-integrated backup/recovery.

**Implications**

- **OADP Operator:** Requires OADP configured (as per OCP-MGT-05) with backup storage location (S3). Ensures application-aware backup/restore integrated with K8s resources. Adds management overhead for schedules/restores.
- **No Dedicated Backup:** Recovery relies on external storage mechanisms or manual intervention. High risk of data loss/complex recovery for data solely on PVCs. Violates enterprise data protection best practices.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert

---
