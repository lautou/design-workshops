# OpenShift Container Platform Security and Compliance

## OCP-SEC-01: FIPS Compliance Requirement

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

- **FIPS Mode Enabled:** Required for clusters operating in highly regulated environments (e.g., US government, financial sector). When FIPS mode is enabled, core components use RHEL cryptographic libraries validated for FIPS 140-2/140-3 on **x86_64, ppc64le, and s390x** architectures.
- **FIPS Mode Disabled:** Standard mode. Provides maximum compatibility and performance, as not all Kubernetes components or workload dependencies may be FIPS validated.

**Implications**

- **FIPS Mode Enabled:** Requires that the underlying RHCOS/RHEL operating system is booted in FIPS mode. Cluster features or operators relying on non-FIPS compliant cryptography may not function or may require specific configuration changes.
- **FIPS Mode Disabled:** May not meet mandated security requirements for certain regulatory environments.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-02: Compliance Automation Strategy

**Architectural Question**
How will regulatory compliance (e.g., STIG, PCI-DSS) be enforced, tracked, and remediated across the cluster lifecycle, considering the FIPS decision?

**Issue or Problem**
Continuous auditing against configuration standards (e.g., DISA-STIG, FedRAMP, PCI-DSS) is necessary to maintain security posture and readiness, complementing the foundational FIPS setting if enabled.

**Assumption**
N/A

**Alternatives**

- Manual Policy Enforcement (External Audits)
- Compliance Operator (Automated Scanning/Remediation)
- Policy Automation via RHACM/ZTP

**Decision**
#TODO#

**Justification**

- **Manual Policy Enforcement (External Audits):** Relies on external tools and manual processes to check cluster configurations against standards. High effort and reactive remediation.
- **Compliance Operator (Automated Scanning/Remediation):** Recommended automated solution. The Compliance Operator uses OpenSCAP profiles (Platform/Node) to automatically run scans and generate machine configuration remediations for standards like STIG, PCI-DSS (v4), and FedRAMP.
- **Policy Automation via RHACM/ZTP:** For fleet management, leverages RHACM PolicyGenerator resources to distribute and enforce security and compliance policies across multiple clusters declaratively.

**Implications**

- **Manual Policy Enforcement (External Audits):** High potential for configuration drift and difficulty in maintaining continuous compliance.
- **Compliance Operator (Automated Scanning/Remediation):** Requires installing and maintaining the Compliance Operator. Automated remediations (e.g., those affecting SSHD or KubeletConfig) must be carefully reviewed before application.
- **Policy Automation via RHACM/ZTP:** Enables centralized compliance enforcement across a multi-cluster fleet but introduces dependency on RHACM infrastructure.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-03: Identity Provider Selection

**Architectural Question**
Which authentication identity provider (IdP) will OpenShift use for user login?

**Issue or Problem**
Choosing the right IdP is foundational to user access and authorization, requiring alignment with existing enterprise directories or modern security standards.

**Assumption**
N/A

**Alternatives**

- HTPasswd
- LDAP
- OpenID Connect (OIDC)
- Other Providers (e.g., Keystone)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **HTPasswd:** Simple, self-contained authentication. Suitable only for PoCs or small, isolated clusters.
- **LDAP:** Integrates with existing enterprise directories (AD, OpenLDAP). Common in established enterprises.
- **OpenID Connect (OIDC):** Integrates with modern IdPs (Keycloak, Okta, Azure AD). Recommended for flexibility, security (MFA, SSO), and feature richness.
- **Other Providers:** Leverages specific existing systems (Keystone for OpenStack) or social providers (GitHub).

**Implications**

- **HTPasswd:** Manual user management, does not scale.
- **LDAP:** Requires secure connectivity (LDAPS) and query configuration. Group sync needs OCP-SEC-04.
- **OpenID Connect (OIDC):** Recommended. Requires managing client IDs/secrets, relies on external IdP infrastructure.
- **Other Providers:** Integration complexity varies.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-04: Identity Provider Group Synchronization

**Architectural Question**
How will user groups from the external identity provider be synchronized with OpenShift for RBAC?

**Issue or Problem**
OpenShift needs awareness of external IdP groups to manage permissions effectively via RBAC. A synchronization strategy is needed.

**Assumption**
An external LDAP-compatible or OIDC IdP providing group claims is used (OCP-SEC-03).

**Alternatives**

- No Group Synchronization (Manual RBAC)
- LDAP Group Sync Operator (for LDAP)
- Claim-based Group Sync (for OIDC)
- On-demand Group Sync (Legacy LDAP)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Group Synchronization:** Simplifies IdP config by managing all groups/bindings manually in OpenShift. Avoids IdP dependency for authorization.
- **LDAP Group Sync Operator:** Robust, scalable, recommended method for LDAP. Periodically syncs IdP groups to OpenShift `Group` resources.
- **Claim-based Group Sync (OIDC):** Standard for OIDC. Group memberships are included in the user's token/claims during login and mapped dynamically.
- **On-demand Group Sync (Legacy LDAP):** Older LDAP mechanism, fetches groups only on login. Not recommended for new deployments.

**Implications**

- **No Group Synchronization:** High operational burden, managing RBAC per-user. Does not scale.
- **LDAP Group Sync Operator:** Reliable, near-real-time group reflection for LDAP. Most manageable for enterprise RBAC with LDAP.
- **Claim-based Group Sync (OIDC):** Efficient for OIDC. Relies on IdP correctly issuing group claims in tokens.
- **On-demand Group Sync (Legacy LDAP):** Can cause performance issues and stale group info.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-05: Multi-Tenant Identity Provider Integration

**Architectural Question**
How will the platform support multiple distinct identity providers, potentially for different tenants?

**Issue or Problem**
Integrating multiple IdPs for different user groups (e.g., internal vs. external partners) requires a strategy to manage the login experience and authentication flows.

**Assumption**
Multiple, distinct IdPs are required.

**Alternatives**

- Native OpenShift Multi-IdP Configuration
- Brokered IdP Configuration with Keycloak

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Native OpenShift Multi-IdP Configuration:** Uses built-in functionality to configure multiple IdPs directly in OpenShift. Simplest infrastructure approach.
- **Brokered IdP Configuration with Keycloak:** Uses a central identity broker (Red Hat build of Keycloak) as the single OCP entry point. Keycloak then connects to all upstream tenant IdPs.

**Implications**

- **Native OpenShift:** All configured IdPs appear as login options for _all_ users, which cannot be customized/restricted and can be confusing.
- **Brokered IdP (Keycloak):** Adds Keycloak as a critical component to manage. Provides a unified login entry point and allows advanced features (custom branding per tenant, attribute mapping).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-06: Security Context Constraint (SCC) / Pod Security Admission (PSA) Policy

**Architectural Question**
What default level of security enforcement (privileges) will be applied to user application workloads (pods)?

**Issue or Problem**
The security context policy (SCC/PSA) defines container privileges. This balances application flexibility against cluster security needs (Principle of Least Privilege).

**Assumption**
N/A

**Alternatives**

- Restricted Profile (Recommended Baseline)
- Baseline Profile (Mid-level Access)
- Permissive Exceptions (Privileged or Custom SCCs)

**Decision**
#TODO#

**Justification**

- **Restricted Profile (Recommended Baseline):** Applies the most secure standard (e.g., restricted-v2 SCC / Kubernetes PSA restricted profile) to pods, enforcing constraints like forbidding host networking, volume mounts, and the use of the root user.
- **Baseline Profile (Mid-level Access):** A more relaxed standard (e.g., PSA baseline profile) that allows default pod operation while preventing known privilege escalations. Suitable for compatibility requirements.
- **Permissive Exceptions (Privileged or Custom SCCs):** Assigns highly privileged access (e.g., `privileged` SCC or disabling enforcement) necessary for specific infrastructure components, storage operators (e.g., ODF), or legacy applications requiring host access.

**Implications**

- **Restricted Profile (Recommended Baseline):** May require modification or adaptation of application images and manifests that assume high privileges (e.g., running as root, using host paths).
- **Baseline Profile (Mid-level Access):** Provides greater compatibility than Restricted but introduces minor security flexibility tradeoffs.
- **Permissive Exceptions (Privileged or Custom SCCs):** Compromises the Principle of Least Privilege and significantly increases the attack surface of the workload and the host node.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-SEC-07: Admission Control Strategy (Custom Policies)

**Architectural Question**
How will custom organizational policies (beyond basic SCC/PSA) regarding resource definitions and configurations be enforced?

**Issue or Problem**
Custom, granular policy enforcement (e.g., requiring specific labels, preventing use of deprecated APIs, enforcing resource limits) is needed for compliance and governance beyond default admission plugins.

**Assumption**
Need for custom policy enforcement exists.

**Alternatives**

- Rely on Default Admission Control Only
- Implement Custom Policies via Dynamic Admission Webhooks (e.g., OPA Gatekeeper, Kyverno)
- Implement Custom Policies via Declarative Admission Policies (Kubernetes ValidatingAdmissionPolicy - CEL)

**Decision**
#TODO#

**Justification**

- **Default Admission Control Only:** Relies only on built-in controllers (`LimitRanger`, `ResourceQuota`, SCC/PSA). Simple but offers limited custom policy flexibility.
- **Dynamic Admission Webhooks:** Extends admission via external webhook servers (Gatekeeper, Kyverno). Powerful for complex validating/mutating policies but adds components to manage.
- **Declarative Admission Policies (CEL):** Uses modern Kubernetes API (`ValidatingAdmissionPolicy`) with Common Expression Language (CEL). Avoids external webhook servers but limited to validation policies and CEL expressiveness.

**Implications**

- **Default Only:** Limited custom policy enforcement.
- **Webhooks:** Adds external components requiring security, HA, maintenance. Failure policy (`Fail` vs `Ignore`) impacts behavior on webhook errors.
- **Declarative (CEL):** Simpler infrastructure. Policy complexity limited by CEL budget/features. Requires careful testing of CEL expressions.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-08: Container Image Trust and Signature Verification

**Architectural Question**
What solution will enforce image authenticity by verifying signatures for container images consumed by the cluster?

**Issue or Problem**
Supply chain integrity requires ensuring images originate from trusted sources and haven't been tampered with. Verification must be enforced before images run.

**Assumption**
Supply chain security is a requirement.

**Alternatives**

- No Verification
- OpenShift Policy Enforcement (ImagePolicy/Sigstore)
- External Verification Tools (Admission Webhooks)

**Decision**
#TODO#

**Justification**

- **No Verification:** Simplest approach, relying solely on access control (RBAC) to the registry, not validating image content origin or integrity.
- **OpenShift Policy Enforcement (ImagePolicy/Sigstore):** Recommended solution. Uses `ImagePolicy` or `ClusterImagePolicy` resources to define policies that enforce signature verification (e.g., Sigstore) for specific image registries/scopes before the image can be pulled and run.
- **External Verification Tools (Admission Webhooks):** Leverages a third-party policy engine (e.g., Gatekeeper, Kyverno) integrated via admission webhooks to validate image metadata or signatures against external sources.

**Implications**

- **No Verification:** Leaves the cluster vulnerable to supply chain attacks or unauthorized image modifications.
- **OpenShift Policy Enforcement (ImagePolicy/Sigstore):** Requires configuring trusted signing authorities and ensures that unauthorized or untrusted images are blocked at the cluster API level. MCO automatically verifies release image signatures.
- **External Verification Tools (Admission Webhooks):** Requires deployment and maintenance of additional policy enforcement infrastructure, which must integrate reliably with the OpenShift image registry workflow.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-09: Data Protection (etcd) Encryption

**Architectural Question**
Should sensitive API resources stored in etcd (Secrets, ConfigMaps, Routes, OAuth tokens) be encrypted at the application layer?

**Issue or Problem**
Etcd stores sensitive data. Application-layer encryption adds protection if underlying storage encryption is compromised (e.g., exposed etcd backup).

**Assumption**
Protection of sensitive configuration data at rest is required.

**Alternatives**

- No Application-Layer Encryption (Rely on Storage Encryption Only)
- Platform-Managed Encryption (AES-CBC / AES-GCM)

**Decision**
#TODO#

**Justification**

- **No Application-Layer Encryption:** Relies solely on lower-level security (RHCOS disk encryption, TPM/Tang). Simpler, avoids potential performance impact or complexity during rollout.
- **Platform-Managed Encryption:** Provides an **additional security layer** for sensitive resources (Secrets, OAuth tokens). Supports AES-CBC and AES-GCM. If FIPS mode (OCP-SEC-01) is enabled, uses FIPS-approved `aes cbc`.

**Implications**

- **No Application-Layer Encryption:** Exposes Secrets, ConfigMaps, tokens if etcd data/backups are accessed without underlying disk encryption.
- **Platform-Managed Encryption:** **Only encrypts values, not keys** (resource types, namespaces, object names remain clear). Encryption keys file (`static_kuberesources_<...>.tar.gz`) MUST be stored securely and separately from etcd snapshots for DR. Adds minor encryption/decryption overhead.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-SEC-10: Centralized Secret Management Integration

**Architectural Question**
What method will safely externalize and inject sensitive configuration data (secrets) into application workloads, especially those managed by GitOps?

**Issue or Problem**
Secrets must not be stored unencrypted in Git. A mechanism is needed to securely retrieve credentials from dedicated enterprise secret stores and make them available to pods at runtime.

**Assumption**
Applications require secrets; GitOps might be used (GITOPS-01); storing secrets directly in Git is forbidden.

**Alternatives**

- Rely Solely on Kubernetes Native Secrets (Potentially with GitOps encryption like Sealed Secrets)
- Integrate External Secret Store via External Secrets Operator (ESO) / Secrets Store CSI Driver (SSCSI)

**Decision**
#TODO#

**Justification**

- **Kubernetes Native Secrets:** Simplest K8s approach. Secrets stored as native objects, protected at rest by etcd encryption (OCP-SEC-09). Can be combined with GitOps tools like Sealed Secrets (GITOPS-04 option) to encrypt secrets _before_ committing to Git.
- **External Secret Store Integration (ESO/SSCSI):** Recommended enterprise approach. Decouples app deployment from secret lifecycle, centralizes secret storage (Vault, Cloud KMS), enhances compliance/auditing. Secrets Store CSI Driver (SSCSI) mounts secrets as volumes, avoiding persistence on node after pod deletion. ESO can sync external secrets into K8s native secrets.

**Implications**

- **Native Secrets / Sealed Secrets:** Secrets (decrypted) exist within the cluster's etcd (Native) or as K8s Secret objects (Sealed Secrets decryption target). Vulnerable if RBAC/API access allows retrieval. Sealed Secrets requires managing the decryption key securely in-cluster.
- **External Store (ESO/SSCSI):** App deployment **depends on external secret store availability**. SSCSI Driver requires `privileged` SCC for pod service account. Provides better lifecycle management and auditing via the central store. ESO creates native K8s secrets, sharing similar risks as Native Secrets once synced.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner
