# OpenShift GitOps

## GITOPS-01: Argo CD Instance Model

**Architectural Question**
Which Argo CD instance deployment model (Namespace-scoped vs. Cluster-scoped) will be used to isolate cluster management configuration from application delivery pipelines?

**Issue or Problem**
Adopting a consistent, automated method is essential for scaling configuration management across a fleet of clusters, minimizing configuration drift, and standardizing security policies. The chosen model dictates the boundary between platform control and application tenancy isolation.

**Assumption**
OpenShift GitOps (Argo CD) is the chosen engine for declarative configuration management.

**Alternatives**

- Single Cluster-Scoped Instance (Shared)
- Dual Instance (Dedicated Platform Instance + Application Instance(s))
- Namespace-Scoped Instances (Application Delivery Only).

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Single Cluster-Scoped Instance (Shared):** Provides the simplest operational profile with the lowest overhead. Suitable when administrative separation between platform configuration and applications is not a primary concern. The default instance is cluster-scoped.
- **Dual Instance (Dedicated Platform Instance + Application Instance(s)):** Provides strict separation of concerns, ensuring platform administration tasks are isolated from application rollouts. The platform team manages the Cluster-scoped instance, while application teams utilize dedicated instances or segregated resources.
- **Namespace-Scoped Instances (Application Delivery Only):** Maximizes security and blast radius reduction by limiting each Argo CD instance to a single namespace (project).

**Implications**

- **Single Cluster-Scoped Instance (Shared):** Any configuration error in one domain (e.g., application) could potentially impact cluster-wide stability. Higher privileges are required for the single Argo CD instance.
- **Dual Instance (Dedicated Platform Instance + Application Instance(s)):** Increases management complexity due to multiple Argo CD installations and potentially overlapping configuration files.
- **Namespace-Scoped Instances (Application Delivery Only):** Requires higher operational overhead for deploying and maintaining potentially dozens or hundreds of individual Argo CD instances.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## GITOPS-02: Platform GitOps Deployment Scope

**Architectural Question**
Will platform configuration (NodeConfigs, Networking, Operator subscriptions) be managed locally within each cluster or centrally from a dedicated hub/management cluster?

**Issue or Problem**
Platform management for multiple clusters (fleet management) requires standardization and governance. Choosing the right scope impacts consistency, scalability, and recovery posture.

**Assumption**
Multiple managed OpenShift clusters exist, necessitating a multi-cluster management strategy.

**Alternatives**

- Local/Decentralized Scope
- Centralized Hub Scope (Managed by RHACM)
- Managed by RHACM

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Local/Decentralized Scope:** Each managed cluster hosts its own configuration Argo CD instance responsible only for local platform settings. This ensures the cluster remains operational and manageable even if network connectivity to a central hub is temporarily lost.
- **Centralized Hub Scope (Managed by RHACM):** Leverages a central OpenShift cluster (the Hub) running Red Hat Advanced Cluster Management (RHACM) and Argo CD ApplicationSets. This approach uses RHACM PolicyGenerator CRs to enforce compliance and roll out consistent configurations (e.g., policy updates, MachineConfigs) across the entire fleet declaratively, which is fundamental to GitOps ZTP deployments.

**Implications**

- **Local/Decentralized Scope:** Requires custom tooling outside of the cluster itself to orchestrate configuration updates consistently across the entire fleet, leading to potential configuration drift.
- **Centralized Hub Scope (Managed by RHACM):** Provides centralized visibility and control (Single Pane of Glass). It requires the Hub cluster and the RHACM infrastructure to be highly available. This model is commonly used for large-scale management, particularly in edge computing scenarios.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## GITOPS-03: Repository Structure

**Architectural Question**
What is the strategy for structuring the Git repositories that store configuration manifests?

**Issue or Problem**
The organization of Git repositories is the foundation of a GitOps practice. The choice between a monorepo versus multirepo impacts access control, CI/CD pipeline complexity, and change promotion.

**Assumption**
A GitOps operational model will be used.

**Alternatives**

- Monorepo
- Multirepo (Repo per Component)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Monorepo:** To simplify dependency management and atomic changes across multiple components by keeping all platform and application manifests in a single repository.
- **Multirepo (Repo per Component):** To provide strong ownership and access control by giving each team or application its own repository. This aligns well with a microservices architecture.

**Implications**

- **Monorepo:** Requires powerful tooling (e.g., Argo CD App of Apps or Kustomize structuring) to enforce logical separation and prevent large-scale lock contention. Pull requests can become complex due to high volume of changes.
- **Multirepo (Repo per Component):** Increases the number of repositories, secrets, and webhooks to manage. Requires cross-repository tooling if dependencies exist between components.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## GITOPS-04: Secret Management Strategy

**Architectural Question**
How will secrets be securely managed and exposed to applications deployed via GitOps?

**Issue or Problem**
Storing unencrypted secrets in Git is a major security risk. A secure solution is required to manage secrets (e.g., API keys, passwords) and make them available to applications at runtime.

**Assumption**
Applications require secrets, and a GitOps operational model will be used.

**Alternatives**

- Sealed Secrets
- External Secrets Operator (with Vault/Other)
- Argo CD Vault Plugin

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Sealed Secrets:** To adopt a simple, Kubernetes-native approach. Secrets are encrypted locally before being committed to Git and can only be decrypted by a controller running in the target cluster.
- **External Secrets Operator (with Vault/Other):** To integrate with an existing, enterprise-grade external secret store like HashiCorp Vault. This leverages a central, audited system for secret management.
- **Argo CD Vault Plugin:** To enable Argo CD to dynamically fetch secrets from Vault and inject them into manifests during the sync process, avoiding the creation of persistent Kubernetes `Secret` objects.

**Implications**

- **Sealed Secrets:** The encryption key is managed within the cluster, creating a dependency on the controller's availability. Sharing secrets across clusters requires sharing the private key.
- **External Secrets Operator (with Vault/Other):** The cluster's ability to deploy applications becomes dependent on the availability of the external secret store. It creates native Kubernetes `Secret` objects, which are stored in etcd.
- **Argo CD Vault Plugin:** Avoids storing secrets in etcd, which can be a security benefit. However, it tightly couples the deployment process to Argo CD and Vault.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner
