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

- **Shared Project per Environment:** Minimizes overhead (fewest total projects). Requires strict enforcement of ResourceQuota and NetworkPolicy to isolate workloads within the shared project boundary.
- **Project per Team per Environment:** Balances overhead and isolation. Projects naturally delineate resource boundaries (quotas) and RBAC delegation based on team ownership (tenant).
- **Project per Application per Environment:** Provides the highest logical isolation, allowing granular resource allocation and specific security controls (e.g., SCC/PSA policies) for each application instance.
- **Project per Team per Application per Environment:** Granular control combining team ownership and per-application isolation.

**Implications**

- **Shared Project per Environment:** High risk of resource contention and "noisy neighbor" problems if quotas are not managed precisely.
- **Project per Team per Environment:** Limits the blast radius of a single misconfigured application to the owning team's project, preventing cluster-wide impact.
- **Project per Application per Environment:** Management overhead scales linearly with the number of deployed applications.
- **Project per Team per Application per Environment:** Highest complexity and management overhead.

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

- **Etcd Snapshot Only:** Backs up the critical control plane state (Kubernetes resources, cluster configuration) via etcd snapshots, which is sufficient for cluster recovery if underlying application data (PVs) is handled separately or is ephemeral.
- **OpenShift Data Protection (OADP/Velero) for PVs and Resources:** Uses the OADP Operator (based on Velero) to back up cluster resources and application persistent data volumes (PVs/PVCs). OADP supports incremental backups of block and Filesystem volumes.
- **Comprehensive Layered Backup:** Combines Etcd snapshots for cluster state with OADP for application data and additional measures for immutable objects (e.g., MachineConfigs, custom resources).

**Implications**

- **Etcd Snapshot Only:** Does not protect application data (PVs), leading to data loss unless application storage is managed by an external highly available/DR solution.
- **OpenShift Data Protection (OADP/Velero) for PVs and Resources:** Requires deploying the OADP Operator and defining backup storage locations (e.g., S3, ODF Object Storage). Requires enabling OpenShift User Workload Monitoring to observe OADP metrics.
- **Comprehensive Layered Backup:** Highest complexity and resource usage. Requires meticulous planning to ensure consistency between etcd snapshots and volume backups during restore operations.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner
