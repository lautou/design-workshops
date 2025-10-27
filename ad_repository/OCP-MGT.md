# OpenShift Cluster Management

## OCP-MGT-01: Namespace/Project Allocation Strategy

**Architectural Question**
What is the strategy for grouping and allocating namespaces (projects) to users, teams, and applications?

**Issue or Problem**
The project allocation model determines the level of isolation, complexity of resource quota management, and delegation of administrative tasks.

**Assumption**
N/A

**Alternatives**

- Shared Project per Environment
- Project per Team per Environment
- Project per Application per Environment
- Project per Team per Application per Environment

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Shared Project per Environment:** Minimizes project count for operational simplicity. Suitable for small teams where applications can coexist.
- **Project per Team per Environment:** Provides teams autonomy and clear boundaries for resource/security management. Common balanced approach.
- **Project per Application per Environment:** Highest application isolation, often used when one team manages many distinct apps.
- **Project per Team per Application per Environment:** Most granular organization, unique project per app per team.

**Implications**

- **Shared Project:** Increases risk of "noisy neighbors" / config conflicts. Complex RBAC/quota management within the project.
- **Project per Team:** Good balance between isolation/overhead. Teams manage resources/permissions within their projects.
- **Project per Application:** Large number of projects, increases management complexity but offers strong app-level isolation.
- **Project per Team per Application:** Highest project count, requires robust automation for creation/configuration.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-MGT-02: RBAC Model (Delegation Strategy)

**Architectural Question**
What is the strategy for delegating project-level administration and resource management permissions?

**Issue or Problem**
Defining the RBAC strategy balances centralized platform governance (security) with development team autonomy and velocity.

**Assumption**
Project Allocation Strategy (OCP-MGT-01) is defined. Identity Provider and Groups (OCP-SEC-03, OCP-SEC-04) are configured.

**Alternatives**

- Centralized Platform Team Control (e.g., `cluster-admin` for platform, `edit` for devs)
- Delegated Project Administration (e.g., `admin` role for team leads in their projects)
- Custom Role-Based Access Control (RBAC) (Tailored roles/bindings)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Centralized Control:** Maintains strict central control, platform team manages most project-level admin tasks. Minimizes security surface area delegated to tenants.
- **Delegated Admin:** Empowers project team leads (`admin` role) over their own projects, fostering autonomy and reducing burden on central platform team.
- **Custom RBAC:** Implements tailored permissions for specific complex organizational needs not met by standard roles.

**Implications**

- **Centralized:** Creates bottleneck, developers rely on platform team for admin tasks (project roles, quotas). Slower velocity for tenants.
- **Delegated:** Increases surface area for potential misconfigurations by tenants but reduces central operational load, improves developer velocity.
- **Custom:** Requires significant effort to develop, test, maintain custom roles/bindings. Increases complexity.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Security Expert

---

## OCP-MGT-03: Image Registry Strategy (Application Images)

**Architectural Question**
Which image registry will be used for storing internally built application images (including custom RHOAI notebook images)?

**Issue or Problem**
An image registry is needed to store, scan, and distribute container images for CI/CD and deployments. This is separate from the disconnected mirror registry (OCP-BASE-08) which primarily holds Red Hat content.

**Assumption**
Internal applications/images will be built and deployed. Custom RHOAI images might be needed (RHOAI-SM-14).

**Alternatives**

- OpenShift Internal Registry (Image Registry Operator)
- Existing HA Corporate Image Registry (e.g., Quay, Artifactory, Nexus)
- New Dedicated HA Corporate Image Registry (e.g., Deploying Quay)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **OpenShift Internal Registry:** Uses the built-in registry. Simplest option integrated with OCP. Managed by Cluster Image Registry Operator.
- **Existing Corporate Registry:** Leverages existing, hardened, managed registry infrastructure. Maintains single source of truth for all artifacts.
- **New Dedicated Registry (Quay):** Deploys a new, fully-featured registry optimized as HA source for internal images. Offers advanced features (security, team isolation).

**Implications**

- **Internal Registry:** Lifecycle tied to cluster. Requires persistent storage config (ODF RWO/RWX or other PVs, OCP-STOR-01). Storage must be sized appropriately. May need extra security hardening if exposed externally. Lacks advanced features of dedicated registries.
- **Existing Registry:** Requires network connectivity and pull secrets in app namespaces. Build pipelines need push credentials. May need `ImageContentSourcePolicy`. Relies on external system availability/management and registry team support.
- **New Dedicated Registry:** Provides most features but adds another critical HA component to deploy/manage. Requires dedicated infrastructure or significant OCP resources if run internally. May require separate subscription/license (e.g., Quay).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-MGT-04: Project Resource Quotas Strategy

**Architectural Question**
What strategy will enforce resource consumption limits (CPU, memory, storage, GPUs) at the project (tenant) level?

**Issue or Problem**
Without quotas, a single project could monopolize cluster resources, impacting stability and availability for all tenants.

**Assumption**
Multi-tenancy or resource contention is expected. Project Allocation (OCP-MGT-01) is defined.

**Alternatives**

- No Quotas
- Standardized Tier-Based Quotas (e.g., Small, Medium, Large)
- Custom Per-Project Quotas

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Quotas:** Simplifies administration in non-prod or trusted environments with low contention risk. Not recommended for production/multi-tenant.
- **Standardized Tiers:** Scalable, manageable approach. Defines standard project sizes with preset resource budgets (including specialized resources like `requests.nvidia.com/gpu`). Simplifies onboarding.
- **Custom Per-Project:** Maximum flexibility, tailoring budgets to specific project needs.

**Implications**

- **No Quotas:** High risk of resource starvation, "noisy neighbors" destabilizing the cluster.
- **Standardized Tiers:** Simplifies onboarding/capacity planning. May not perfectly fit every project's needs but provides reasonable bounds. Easier to automate.
- **Custom Per-Project:** Most accurate allocation but significant administrative overhead to define, approve, manage each custom quota. Harder to automate.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-MGT-05: Platform Backup and Restore Strategy

**Architectural Question**
What is the strategy for backing up and restoring OpenShift cluster state (etcd) and application persistent data (PVs)?

**Issue or Problem**
A comprehensive, tested backup/restore strategy is critical for disaster recovery and protecting against data loss/corruption. Must cover control plane (etcd), stateful app data (PVs), and potentially stateless app resources.

**Assumption**
Disaster recovery and data protection are required.

**Alternatives**

- **OCP Cluster-Level Backup Only (etcd):** Rely solely on built-in control plane snapshots.
- **Storage-Level Operations Only (Snapshots/Replication):** Use underlying storage provider's capabilities only.
- **Integrated Container Backup Solution (OADP):** Deploy Kubernetes-native backup solution (OADP operator). Recommended.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **etcd Only:** Essential for DR of cluster config but **does not protect application PV data**. Fast control plane recovery.
- **Storage Only:** Protects PV data using storage features but is **application-unaware** (doesn't back up associated K8s resources like PVCs, Deployments). Restore is manual (restore PV, reapply manifests).
- **OADP:** Most comprehensive, **application-centric** protection. Backs up K8s objects (Deployments, PVCs, etc.) and integrates with storage (CSI snapshots) to back up associated PV data together. Supports backup to S3-compatible storage.

**Implications**

- **etcd Only:** Restoring is destructive (full cluster DR only). Doesn't help with app data corruption. Insufficient on its own for stateful apps.
- **Storage Only:** Manual, complex restore process. Risk of inconsistency between restored PV data and K8s object state.
- **OADP:** Requires OADP operator installation and backup storage (S3). Adds a component to manage but significantly simplifies/automates application-aware recovery. Recommended approach.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner
