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

- **FIPS Mode Enabled:** To meet stringent security and compliance requirements (e.g., federal or highly regulated industries). This enforces the use of FIPS-validated cryptographic libraries across the entire platform.
- **FIPS Mode Disabled:** To avoid potential performance overhead or limitations imposed by FIPS-validated libraries, suitable for environments without strict FIPS requirements.

**Implications**

- **FIPS Mode Enabled:** Must be configured during the operating system installation phase and is **irreversible**. Requires validation throughout the cluster lifecycle. Certain components, extensions, or third-party software may not support FIPS mode.
- **FIPS Mode Disabled:** The cluster may not be suitable for deploying highly regulated workloads requiring FIPS validation.

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
Regulatory compliance beyond FIPS needs to be managed. FIPS decision (OCP-SEC-01) is made.

**Alternatives**

- Full Compliance Automation (Compliance Operator with Remediation)
- Auditing Only (Compliance Operator without Remediation)
- Manual Auditing/Remediation

**Decision**
#TODO#

**Justification**

- **Full Compliance Automation:** Uses the **Compliance Operator** to automate auditing and remediation against predefined profiles (e.g., PCI-DSS, FedRAMP). Provides proactive enforcement.
- **Auditing Only:** Uses the Compliance Operator to generate scan reports (`ComplianceCheckResult`) identifying non-compliance, avoiding risks of automatic remediation disabling critical services (like `sshd` with STIG).
- **Manual Auditing/Remediation:** Relies on manual checks and fixes, suitable only for very small or non-critical environments.

**Implications**

- **Full Compliance Automation:** Applying automated remediations requires high operator privileges and may need manual exceptions (e.g., disabling `sshd`). Ensures continuous compliance posture.
- **Auditing Only:** Increases manual effort for security teams to apply fixes but provides more control over remediation actions.
- **Manual Auditing/Remediation:** High operational burden, inconsistent results, not scalable or suitable for regulated environments.

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

- **Baseline Enforcement** (Default: `restricted-v2` SCC / PSA `restricted` profile)
- **Permissive Exceptions** (Assigning `privileged` SCC or less restrictive PSA profile)

**Decision**
#TODO#

**Justification**

- **Baseline Enforcement:** Provides the strongest default security posture by aligning with the PSA `restricted` profile, dropping capabilities, preventing root execution and privilege escalation. Recommended default for user workloads.
- **Permissive Exceptions:** Only justified for trusted platform components or specific legacy/system applications that demonstrably cannot run restricted. Avoid for general workloads due to high security risks.

**Implications**

- **Baseline Enforcement:** Applications needing higher privileges (host access, root, specific capabilities) require manual Pod Security Context adjustments or assignment of custom SCCs / less restrictive PSA namespace labels.
- **Permissive Exceptions:** Significantly increases risk if a container is compromised (gains high host access). Requires strict auditing, control, and justification.

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
- OpenShift Policy Enforcement (`ImagePolicy`, `ClusterImagePolicy` with Sigstore)
- External Admission Policy (via Webhooks, OCP-SEC-07)

**Decision**
#TODO#

**Justification**

- **No Verification:** Simplest operationally, but highest risk of running compromised software.
- **OpenShift Policy Enforcement:** Recommended. Uses built-in CRs (`ClusterImagePolicy`, `ImagePolicy`) for Sigstore verification. Defines root of trust (public key, PKI cert, Fulcio/Rekor). CVO automatically verifies release images.
- **External Admission Policy:** Uses third-party policy engines (Gatekeeper, Kyverno) via webhooks to enforce image verification.

**Implications**

- **No Verification:** High vulnerability to supply chain attacks.
- **OpenShift Policy Enforcement:** Requires managing keys/certificates for trust root. Failure to mirror signatures in disconnected environments can block updates if enforced for release images.
- **External Admission Policy:** Adds external components and management overhead.

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
