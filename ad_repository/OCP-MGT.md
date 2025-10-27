# OpenShift cluster management

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

- **Shared Project per Environment:** To minimize the number of projects for operational simplicity. Suitable for small teams or a single business unit where applications can coexist.
- **Project per Team per Environment:** To provide teams with autonomy and a clear boundary for resource and security management. This is a common and balanced approach.
- **Project per Application per Environment:** To achieve the highest level of isolation between applications, often used when a single team manages many distinct applications.
- **Project per Team per Application per Environment:** To provide the most granular level of organization, creating a unique project for each application owned by a specific team.

**Implications**

- **Shared Project per Environment:** Increases the risk of "noisy neighbor" issues and configuration conflicts. RBAC and resource quota management become more complex within the shared project.
- **Project per Team per Environment:** Strikes a good balance between isolation and operational overhead. Teams can manage their own resources and permissions within their projects.
- **Project per Application per Environment:** Creates a large number of projects, which can increase management complexity, but offers strong application-level isolation.
- **Project per Team per Application per Environment:** Results in the highest number of projects, requiring robust automation for project creation and configuration to be manageable.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-MGT-02: RBAC Model

**Architectural Question**
What is the strategy for delegating project-level administration and resource management permissions?

**Issue or Problem**
Defining the proper RBAC strategy is critical for balancing centralized platform governance (security) with development team autonomy and velocity.

**Assumption**
N/A

**Alternatives**

- Centralized Platform Team Control
- Delegated Project Administration
- Custom Role-Based Access Control (RBAC)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Centralized Platform Team Control:** To maintain strict, centralized control, a platform team is given the cluster-admin role and development teams are given the edit role in their projects. This minimizes the security attack surface area.
- **Delegated Project Administration:** To empower project team leaders with administrative control (admin role) over their own projects, fostering autonomy and reducing the burden on the central platform team.
- **Custom Role-Based Access Control (RBAC):** To implement a tailored permissions model that meets specific and complex organizational requirements not covered by the standard roles.

**Implications**

- **Centralized Platform Team Control:** Creates a bottleneck, as developers must rely on the platform team for many administrative tasks (e.g., managing project-level roles or quotas).
- **Delegated Project Administration:** Increases the surface area for potential misconfigurations, but drastically reduces the operational load on the central platform team, improving developer velocity.
- **Custom Role-Based Access Control (RBAC):** Requires significant effort for development, testing, and maintenance of custom roles and cluster role bindings.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Security Expert

---

## OCP-MGT-03: Images registry

**Architectural Question**
Which image registry will be used for application images?

**Issue or Problem**
An image registry strategy is needed to store, scan, and distribute container images for CI/CD pipelines and application deployments. This is separate from the disconnected mirror registry.

**Assumption**
N/A

**Alternatives**

- OpenShift Internal Registry (Image Registry Operator)
- Using an existing HA corporate images registry
- Installing a new dedicated HA corporate images registry

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **OpenShift Internal Registry (Image Registry Operator):** To use the built-in registry. This is the simplest option but may lack advanced enterprise features like robust scanning or integration into existing authentication systems. The registry is managed by the Cluster Image Registry Operator.
- **Using an existing HA corporate images registry:** To leverage existing, hardened, and managed registry infrastructure (e.g., Artifactory, Nexus). This maintains a single source of truth for all artifacts.
- **Installing a new dedicated HA corporate images registry:** To deploy a new, fully-featured registry (like Red Hat Quay) optimized to serve as the highly available source of truth for internally-built application images.

**Implications**

- **OpenShift Internal Registry (Image Registry Operator):** The lifecycle and availability of the internal registry must be managed, and its storage must be sized appropriately for custom images. Requires configuration of persistent storage (e.g., ODF RWO/RWX or other PVs - see OCP-STOR-01). Lifecycle is tied to the cluster. May require additional security hardening if exposed externally.
- **Using an existing HA corporate images registry:** Requires establishing and maintaining network connectivity and secure pull secrets in application namespaces to access the external registry. Build pipelines need push credentials. May require `ImageContentSourcePolicy` configuration. This relies on the registry team supporting the OCP mirroring process and hosting Red Hat content. Relies on external system availability and management.
- **Installing a new dedicated HA corporate images registry:** Provides the most features (security, team isolation) but adds another critical, highly-available component to be deployed and managed. Requires dedicated infrastructure or significant OpenShift cluster resources if run internally. Requires a separate Quay subscription or license.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-MGT-04: Project Resource Quotas

**Architectural Question**
What strategy will be used to enforce resource consumption limits at the project (tenant) level?

**Issue or Problem**
Without resource quotas, a single project could monopolize cluster resources (CPU, memory, storage, GPUs), impacting the stability and availability of all other tenants.

**Assumption**
N/A

**Alternatives**

- No Quotas
- Standardized Tier-Based Quotas
- Custom Per-Project Quotas

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Quotas:** To simplify administration in non-production or trusted environments where the risk of resource contention is low.
- **Standardized Tier-Based Quotas:** To provide a scalable and manageable approach by defining standard project sizes (e.g., Small, Medium, Large) with pre-set resource budgets.
- **Custom Per-Project Quotas:** To offer maximum flexibility by tailoring resource budgets to the specific, measured needs of each project or application team.

**Implications**

- **No Quotas:** Carries a high risk of resource starvation and "noisy neighbor" problems, where one project's high consumption can destabilize the entire cluster.
- **Standardized Tier-Based Quotas:** Simplifies project onboarding and capacity planning. This can also include quotas for specialized resources like `requests.nvidia.com/gpu`.
- **Custom Per-Project Quotas:** Provides the most accurate resource allocation but requires significant administrative overhead to define, approve, and manage each custom quota.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-MGT-05: Platform Backup and Restore Strategy

**Architectural Question**
What is the strategy for backing up and restoring the OpenShift Container Platform clusters and application data?

**Issue or Problem**
A comprehensive and tested backup and restore strategy is critical to protect against data loss, corruption, and disaster scenarios. This strategy must cover the control plane (etcd), persistent application data (PVs), and stateless application resources.

**Assumption**
A strategy for disaster recovery and data protection is required.

**Alternatives**

- **OCP Cluster-Level Backup (etcd):** Relying solely on the built-in control plane snapshots for cluster-level recovery.
- **Storage-Level Snapshots/Replication:** Using the underlying storage provider's capabilities to protect application persistent volumes.
- **Integrated Container Backup Solution (OADP):** Deploying a dedicated, Kubernetes-native backup solution like the OpenShift API for Data Protection (OADP) operator.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **OCP Cluster-Level Backup (etcd):** Provides a fast and effective way to recover the state of the control plane. It is essential for disaster recovery of the cluster's configuration but does not protect application persistent data.
- **Storage-Level Snapshots/Replication:** Leverages existing, potentially high-performance storage features. It is excellent for protecting the data within PVs but is "application-unaware," meaning it does not back up the associated Kubernetes resources.
- **Integrated Container Backup Solution (OADP):** Provides the most comprehensive, application-centric protection. It backs up Kubernetes objects and integrates with the storage provider (via CSI snapshots) to back up the associated persistent data together.

**Implications**

- **OCP Cluster-Level Backup (etcd):** Restoring from an etcd snapshot is a destructive operation and should only be used for full cluster disaster recovery. It does not help with individual application data corruption.
- **Storage-Level Snapshots/Replication:** The restore process is manual, requiring operators to restore the PV and then manually re-apply the Kubernetes object manifests.
- **Integrated Container Backup Solution (OADP):** Requires the installation of the OADP operator and a compatible object storage backend to store the backups. It adds a component to be managed but significantly simplifies and automates recovery.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert
