# OpenShift Container platform security and compliance

## OCP-SEC-01: Identity Provider Selection

**Architectural Question**
Which authentication identity provider (IdP) will OpenShift use for user login?

**Issue or Problem**
Choosing the right identity provider is foundational to user access and authorization, requiring alignment with existing enterprise directories or modern security standards.

**Assumption**
N/A

**Alternatives**

- HTPasswd
- LDAP
- OpenID Connect (OIDC)
- Other Providers

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **HTPasswd:** For simple, self-contained authentication without dependency on an external IdP. Suitable for proof-of-concept or small, isolated clusters.
- **LDAP:** To integrate with an existing enterprise directory (e.g., Active Directory, OpenLDAP) for user and group management. This is a common choice in established enterprises.
- **OpenID Connect (OIDC):** To integrate with modern, OIDC-compliant identity providers (e.g., Keycloak, Okta, Azure AD). This is the recommended approach for flexible, secure, and feature-rich authentication.
- **Other Providers:** To leverage existing authentication systems like Keystone for OpenStack integration or social providers like GitHub for development-focused clusters.

**Implications**

- **HTPasswd:** Requires cluster administrators to manage all users and passwords directly within OpenShift. Does not scale for large organizations.
- **LDAP:** Requires secure network connectivity (typically LDAPS) and detailed configuration of LDAP queries. LDAP group synchronization may require additional tooling (OCP-SEC-02).
- **OpenID Connect (OIDC):** Highly recommended for security and feature set. Requires managing client IDs, client secrets, and typically relies on external identity infrastructure (e.g., Keycloak).
- **Other Providers:** Integration complexity varies widely depending on the provider (e.g., GitLab, Google, Microsoft Entra ID are supported).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-02: Identity Provider Group Synchronization

**Architectural Question**
How will user groups from the external identity provider be synchronized with OpenShift?

**Issue or Problem**
To effectively manage permissions using Role-Based Access Control (RBAC), OpenShift needs to be aware of the user groups defined in the central IdP. A strategy is needed to synchronize this group membership.

**Assumption**
An external LDAP-compatible identity provider is used (see OCP-SEC-01).

**Alternatives**

- No Group Synchronization
- LDAP Group Sync Operator
- On-demand Group Sync (Legacy)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Group Synchronization:** To simplify the configuration by managing all groups and role bindings manually within OpenShift. This avoids a dependency on the IdP for authorization.
- **LDAP Group Sync Operator:** To implement a robust, scalable, and officially recommended method for synchronizing IdP groups. The operator periodically queries the IdP and creates/updates native OpenShift `Group` resources.
- **On-demand Group Sync (Legacy):** To use the older, built-in mechanism where group membership is fetched from the IdP only when a user logs in.

**Implications**

- **No Group Synchronization:** Places a high operational burden on cluster administrators, as all role bindings must be managed on a per-user basis. This does not scale for large organizations.
- **LDAP Group Sync Operator:** Provides a reliable, near-real-time reflection of IdP group memberships within the cluster. This is the most efficient and manageable approach for enterprise RBAC.
- **On-demand Group Sync (Legacy):** Can lead to performance issues and stale group information, as memberships are not updated until users log in again. This method is generally not recommended for new deployments.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-03: Multi-Tenant Identity Provider Integration

**Architectural Question**
How will the platform support multiple identity providers for different tenants?

**Issue or Problem**
When different teams (tenants) need to authenticate using their own distinct identity providers (IdPs), a strategy is needed to integrate them without creating a confusing user experience.

**Assumption**
Multiple, distinct identity providers are required for different sets of users (e.g., internal teams, external partners).

**Alternatives**

- Native OpenShift IdP Configuration
- Brokered IdP Configuration with Keycloak

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Native OpenShift IdP Configuration:** To use the built-in functionality for configuring multiple identity providers directly in OpenShift. This is the simplest approach from an infrastructure perspective.
- **Brokered IdP Configuration with Keycloak:** To use a central identity broker (the Red Hat build of Keycloak) as the single point of entry for OpenShift. Keycloak then manages the connections to all the upstream IdPs for each tenant.

**Implications**

- **Native OpenShift IdP Configuration:** All configured identity providers are displayed as options on the main OpenShift login page for all users, which cannot be customized or restricted. This can be confusing.
- **Brokered IdP Configuration with Keycloak:** Introduces an additional critical component (Keycloak) that must be deployed and managed. However, it provides a single, unified login entry point and allows for advanced features like custom branding per tenant.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-04: Security Context Constraint (SCC) Policy

**Architectural Question**
What default level of security enforcement will be applied to user application workloads?

**Issue or Problem**
The security context policy (SCC, or the newer PSA) defines the privileges containers can access. This decision balances necessary flexibility for applications against the need for cluster security.

**Assumption**
N/A

**Alternatives**

- Baseline Enforcement (SCC/PSA restricted-v2)
- Permissive Exceptions (privileged SCC)

**Decision**
#TODO#

**Justification**

- **Baseline Enforcement (SCC/PSA restricted-v2):** This is the most restrictive SCC provided by a new installation and is used by default for authenticated users. It provides the strongest security posture by aligning with the PSA restricted profile, dropping all capabilities, and preventing privilege escalation.
- **Permissive Exceptions (privileged SCC):** This is only justified for trusted platform components or critical system applications that cannot run restricted. This policy should be avoided for general application workloads, as it allows access to all host features.

**Implications**

- **Baseline Enforcement (SCC/PSA restricted-v2):** Applications requiring high privileges (e.g., host access, root UID, specific capabilities) will require manual adjustment of their Pod Security Context or assignment of a custom SCC/PSA exception.
- **Permissive Exceptions (privileged SCC):** Bypassing standard security controls significantly increases the risk if a container is compromised, as it gains high levels of host access. Requires strict auditing and control.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-SEC-05: Compliance Automation and FIPS Strategy

**Architectural Question**
How will regulatory compliance (e.g., FIPS, STIG, PCI-DSS) be enforced, tracked, and remediated across the cluster lifecycle?

**Issue or Problem**
FIPS compliance requires configuration prior to OS boot, and continuous auditing against configuration standards (e.S., DISA-STIG, FedRAMP, PCI-DSS) is necessary to maintain security posture and readiness.

**Assumption**
#N/A

**Alternatives**

- Full Compliance Automation
- Auditing Only

**Decision**
#TODO#

**Justification**

- **Full Compliance Automation:** **FIPS mode must be enabled during cluster installation** (see OCP-SEC-10) to ensure core components use FIPS-validated RHEL cryptographic libraries on supported architectures (x86_64, ppc64le, s390x). The **Compliance Operator** is the supported tool for automating auditing and remediation against predefined profiles (e.g., PCI-DSS, FedRAMP). For many benchmarks (like PCI-DSS), both Platform and Node profiles must be run.
- **Auditing Only:** Allows the platform team to identify non-compliance using the Compliance Operator to generate scan reports (`ComplianceCheckResult` objects). This avoids the risk of automatic remediation disabling critical services (like `sshd` when applying STIG profiles).

**Implications**

- **Full Compliance Automation:** Enabling **FIPS mode is irreversible** after installation. Applying automated remediations requires the operator to have high privileges to modify cluster objects, and may require manual exceptions for certain rules (e.g., disabling `sshd`).
- **Auditing Only:** Increases the manual effort required by the security team to apply fixes and ensure ongoing compliance.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-06: Data Protection (etcd) Encryption

**Architectural Question**
Should sensitive data stored by the control plane in etcd be encrypted at rest, and if so, what encryption mechanism will be used?

**Issue or Problem**
Etcd stores sensitive API server resources (Secrets, Config Maps, Routes, OAuth tokens). Application-layer encryption is necessary to protect this data if the underlying physical storage encryption is compromised, such as when an etcd backup is exposed.

**Assumption**
#N/A

**Alternatives**

- No Application-Layer Encryption
- Platform-Managed Encryption (AES-CBC/GCM)

**Decision**
#TODO#

**Justification**

- **No Application-Layer Encryption:** Relies solely on lower-level infrastructure security (e.g., RHCOS disk encryption or TPM/Tang encryption for boot volumes). This may be chosen to avoid the risk of performance degradation or potential complexity during the encryption process rollout.
- **Platform-Managed Encryption (AES-CBC/GCM):** Provides an **additional layer of data security** for sensitive resources like Secrets and OAuth tokens. The supported encryption types are AES-CBC and AES-GCM. If FIPS mode is enabled (OCP-SEC-10), the cluster can use the FIPS-approved `aes cbc` algorithm.

**Implications**

- **No Application-Layer Encryption:** Exposes Secrets, ConfigMaps, and tokens if the etcd data or static backups are accessed without underlying disk encryption.
- **Platform-Managed Encryption (AES-CBC/GCM):** **Etcd encryption only encrypts values, not keys**, meaning resource types, namespaces, and object names remain unencrypted. The encryption keys (`static_kuberesources_<datetimestamp>.tar.gz` file) must be stored securely and separately from the etcd snapshot for disaster recovery.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-07: Admission Control Strategy

**Architectural Question**
How will cluster administrators enforce custom policies regarding resource definitions and configurations beyond basic SCC/PSA constraints?

**Issue or Problem**
Custom, granular policy enforcement is required to ensure organizational compliance, prevent the use of unsupported API versions, and manage resource configurations that fall outside the scope of default admission plugins.

**Assumption**
#N/A

**Alternatives**

- Default Admission Control
- Dynamic Admission Webhooks
- Declarative Admission Policies

**Decision**
#TODO#

**Justification**

- **Default Admission Control:** Relies exclusively on the built-in admission controllers (Mutating and Validating). This is the simplest configuration, providing essential policies like `LimitRanger` and `SecurityContextConstraint` required for fundamental cluster operation.
- **Dynamic Admission Webhooks:** Dynamically extends the admission chain by calling out to custom webhook servers. This is necessary for implementing advanced policies (validating) or automatically injecting required fields (mutating), such as adding a common set of labels. Mutating plugins run before validating plugins.
- **Declarative Admission Policies:** Leverages the modern Kubernetes API (`ValidatingAdmissionPolicy`) to define policies using Common Expression Language (CEL) expressions. This avoids the operational overhead of running external webhook servers.

**Implications**

- **Default Admission Control:** Provides limited flexibility for custom organizational policy enforcement.
- **Dynamic Admission Webhooks:** Introduces external components (webhook servers) that must be secured, managed, and maintained. Setting the failure policy to `Fail` means errors during webhook calls will deny requests, while `Ignore` accepts requests unconditionally, leading to potential unpredictable behavior.
- **Declarative Admission Policies:** Policy definition requires careful testing, as CEL expressions must have a computed cost below the maximum budget.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-08: Container Image Trust and Signature Verification

**Architectural Question**
What solution will be used to enforce image authenticity by verifying signatures for container images consumed by the cluster?

**Issue or Problem**
Supply chain integrity requires assurance that container images running on the cluster originate from trusted sources and have not been tampered with. The platform must enforce verification before images are allowed to run.

**Assumption**
#N/A

**Alternatives**

- No Verification
- OpenShift Policy Enforcement
- External Admission Policy

**Decision**
#TODO#

**Justification**

- **No Verification:** Simplifies operations by eliminating the need for key management and signing artifacts, but introduces the highest risk of running compromised software.
- **OpenShift Policy Enforcement:** Recommended approach. Uses built-in `ClusterImagePolicy` (cluster-scoped) and `ImagePolicy` (namespace-scoped) CRs to configure Sigstore signature verification. The policy defines the root of trust, which can be a public key, BYOPKI certificate, or Fulcio/Rekor certificate. The Cluster Version Operator (CVO) automatically performs this verification for release images during updates.
- **External Admission Policy:** Allows the organization to enforce image verification using third-party policy engines (via Dynamic Admission Webhooks, see OCP-SEC-07).

**Implications**

- **No Verification:** High vulnerability to supply chain attacks.
- **OpenShift Policy Enforcement:** Requires managing the keys or certificates that define the root of trust. Failure to mirror signatures in disconnected environments may prevent updates if the policy enforces verification for release images.
- **External Admission Policy:** Adds external components and management overhead (see OCP-SEC-07).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-09: Centralized Secret Management

**Architectural Question**
What method will be used to safely externalize and inject sensitive configuration data (secrets) into application workloads managed by GitOps?

**Issue or Problem**
Sensitive information must not be stored unencrypted in Git. A mechanism is required to securely retrieve credentials from dedicated enterprise secrets stores and make them available to pods at runtime.

**Assumption**
#N/A

**Alternatives**

- Kubernetes Native Secrets
- External Secrets Operator / SSCSI Driver
- Sealed Secrets

**Decision**
#TODO#

**Justification**

- **Kubernetes Native Secrets:** Simplest solution, relying on the platform to store secrets as native objects. Data at rest is protected by **etcd encryption** (OCP-SEC-06). Secrets are provided to pods via volume mounts or environment variables.
- **External Secrets Operator / SSCSI Driver:** Recommended enterprise approach. This method decouples application deployment from the secret lifecycle, centralizes secret storage for compliance, and utilizes enterprise stores (e.g., Vault, Azure Key Vault, AWS Secrets Manager). The Secrets Store CSI Driver (SSCSI) ensures secrets are mounted as a pod volume and do not persist on the system after the pod is destroyed. This operator supports FIPS compliance (OCP-SEC-10).
- **Sealed Secrets:** Provides a simple, Kubernetes-native solution for encrypting secrets that must be committed to Git. The secret is decrypted only by the in-cluster controller.

**Implications**

- **Kubernetes Native Secrets:** Secrets remain vulnerable if users with appropriate RBAC or API access retrieve them while decrypted.
- **External Secrets Operator / SSCSI Driver:** Application deployment becomes **dependent on the availability of the external secret store**. When the SSCSI Driver is used, the pod service account must be granted access to the `privileged` SCC.
- **Sealed Secrets:** Requires that the private key used for decryption is securely managed within the cluster. Sharing secrets across clusters requires sharing the private key.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-10: FIPS Compliance Requirement

**Architectural Question**
Will OpenShift Container Platform be configured to operate in FIPS mode to meet regulatory requirements?

**Issue or Problem**
FIPS (Federal Information Processing Standards) 140-2 compliance requires the system to use validated cryptographic modules, which necessitates specific operating system and cluster configuration choices prior to installation.

**Assumption**
N/A

**Alternatives**

- FIPS Mode Enabled
- FIPS Mode Disabled

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **FIPS Mode Enabled:** To meet stringent security and compliance requirements (e.g., federal or highly regulated industries). This enforces the use of FIPS-validated cryptographic libraries across the entire platform.
- **FIPS Mode Disabled:** To avoid potential performance overhead or limitations imposed by FIPS-validated libraries, suitable for environments without strict FIPS requirements.

**Implications**

- **FIPS Mode Enabled:** Must be configured during the operating system installation phase and must be validated throughout the cluster lifecycle. Certain components, extensions, or third-party software may not support FIPS mode.
- **FIPS Mode Disabled:** The cluster may not be suitable for deploying highly regulated workloads requiring FIPS validation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner
