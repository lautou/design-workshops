# OpenShift GitOps

## GITOPS-01: Argo CD Instance Model

**Architectural Question**
What is the deployment topology for Argo CD instances that manage applications?

**Issue or Problem**
Choosing the right model dictates the operational complexity, resource utilization, and tenant isolation level across the fleet of clusters.

**Assumption**
N/A

**Alternatives**

- Single, Shared Argo CD Instance
- Dual-Instance Model (Platform & Apps)
- Multi-Instance Model (Per-Team/Business Unit)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Single, Shared Argo CD Instance:** To minimize the resource footprint and simplify the management of the GitOps tooling itself. Tenancy is enforced logically using AppProject.
- **Dual-Instance Model (Platform & Apps):** To create a strong physical and logical separation of concerns between infrastructure configuration and application delivery. This aligns with security best practices.
- **Multi-Instance Model (Per-Team/Business Unit):** To provide maximum autonomy and physical isolation to different teams (e.g., AppDev, MLOps), allowing each to manage their own dedicated Argo CD instance.

**Implications**

- **Single, Shared Argo CD Instance:** Requires complex RBAC and disciplined use of AppProject to enforce tenancy. A misconfiguration could have a wide blast radius.
- **Dual-Instance Model (Platform & Apps):** Establishes a clear security boundary. The platform instance runs with high privileges, while the shared application instance is more restricted. This increases the resource footprint but improves security.
- **Multi-Instance Model (Per-Team/Business Unit):** Results in the highest resource consumption and operational overhead. However, it offers the greatest flexibility and fault isolation between teams.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## GITOPS-02: Platform GitOps Deployment Scope

**Architectural Question**
How will the Argo CD instance for platform management be deployed across multiple clusters?

**Issue or Problem**
The deployment model for the platform-focused Argo CD instance determines whether infrastructure configuration is managed by an instance inside each cluster or from a central control plane.

**Assumption**
Multiple OpenShift clusters will be managed.

**Alternatives**

- Cluster-Scoped (Decentralized)
- Centralized Hub (Standalone Argo CD)
- Managed by RHACM

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Cluster-Scoped (Decentralized):** To ensure that each cluster manages its own configuration independently. This model is simple and fault-tolerant.
- **Centralized Hub (Standalone Argo CD):** To manage the configuration of multiple clusters from a single, central Argo CD instance. This simplifies observability and policy enforcement.
- **Managed by RHACM:** To leverage Red Hat Advanced Cluster Management for a fully integrated multi-cluster solution. RHACM's built-in GitOps capabilities can deploy and enforce configurations across the entire fleet.

**Implications**

- **Cluster-Scoped (Decentralized):** Increases operational overhead for applying consistent policies across the fleet. Policy drift is harder to detect centrally.
- **Centralized Hub (Standalone Argo CD):** Creates a single point of management failure. Requires robust network connectivity and security between the hub and managed clusters.
- **Managed by RHACM:** Requires licensing and deployment of RHACM. Highly recommended when using GitOps Zero Touch Provisioning (ZTP) for lifecycle management. Complexity is shifted to RHACM policy management.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner

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
