# Red Hat OpenShift AI Self Managed

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
Red Hat OpenShift AI instances have been defined.

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

## RHOAI-SM-03: Red Hat OpenShift AI OpenShift solution

**Architectural Question**
Which OpenShift solutions will be used for OpenShift clusters hosting Red Hat OpenShift AI instances?

**Issue or Problem**
The choice of OpenShift hosting solution impacts deployment flexibility, management overhead, scalability, and cost. Different OpenShift flavors (self-managed vs. managed, on-premises vs. cloud) offer varying levels of control, support, and integration with Red Hat OpenShift AI.

**Assumption**
OpenShift host clusters have been defined.

**Alternatives**

- OpenShift Container Platform (OCP)
- ROSA Classic (Red Hat OpenShift Service on AWS)
- ROSA HCP (Red Hat OpenShift Service on AWS with Hosted Control Planes)
- Azure Red Hat OpenShift (ARO)
- Any Combination of Above

**Decision**
#TODO#

**Justification**

- **OpenShift Container Platform (OCP):** For full control over configuration, ideal for custom or on-premises setups.
- **ROSA Classic:** For managed simplicity and AWS integration, reducing admin burden.
- **ROSA HCP:** For hosted control planes, enhancing scalability with minimal management.
- **Azure Red Hat OpenShift (ARO):** For Azure integration and managed benefits, appealing to Azure-focused setups.
- **Any Combination of Above:** To leverage strengths of multiple solutions, matching specific needs.

**Implications**

- **OpenShift Container Platform (OCP):** Demands skilled admins; requires self-managed clusters, increasing setup and patching effort with higher maintenance costs.
- **ROSA Classic:** Reduces admin overhead; simplifies setup with managed AWS infrastructure, tying to AWS costs.
- **ROSA HCP:** Eases scaling; minimizes management with hosted control planes, binding to AWS.
- **Azure Red Hat OpenShift (ARO):** Reduces admin load; leverages Azure’s managed services, restricting to Azure environment.
- **Any Combination of Above:** Requires cross-platform monitoring; involves managing hybrid platforms, adding orchestration complexity.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-04: Environment connectivity

**Architectural Question**
Should Red Hat OpenShift AI Self-Managed be deployed in a connected or disconnected environment?

**Issue or Problem**
The environment’s internet connectivity impacts access to external resources (e.g., container images, updates) and security requirements. A connected environment requires internet access, while a disconnected environment must operate without it.

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
- **Disconnected Environment:** Demands manual update processes and skilled admins; requires mirroring resources (e.g., images to local registry), adding setup time.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-05: Internet firewall

**Architectural Question**
Will outbound traffic to the Internet be restricted by a firewall (in a connected environment or in an environment with Internet access to prepare a disconnected environment)?

**Issue or Problem**
Firewall restrictions on outbound traffic affect access to external resources needed for OpenShift AI deployment and operation. Unrestricted access simplifies setup but poses security risks, while restricted access enhances control but may complicate installation or updates.

**Assumption**
N/A

**Alternatives**

- Unrestricted Outbound Traffic
- Restricted Outbound Traffic

**Decision**
#TODO#

**Justification**

- **Unrestricted Outbound Traffic:** For ease of access to external resources, simplifying setup.
- **Restricted Outbound Traffic:** To enhance security by controlling connections, aligning with strict policies.

**Implications**

- **Unrestricted Outbound Traffic:** Requires additional monitoring to mitigate risks; speeds up resource access (e.g., registries), reducing setup effort.
- **Restricted Outbound Traffic:** Strengthens compliance with increased admin effort; limits connections to whitelisted domains (e.g., registry.redhat.io), adding setup time for whitelist management.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-06: Hosts having connection to OpenShift API server

**Architectural Question**
From which hosts will you connect to the OpenShift API server?

**Issue or Problem**
The method of connecting to the OpenShift API server impacts security and operational simplicity. Direct connections from workstations may streamline access but expose the API, while a bastion/jump server adds security but increases complexity.

**Assumption**
N/A

**Alternatives**

- Bastion/Jump Server Only
- Direct Workstation Access

**Decision**
#TODO#

**Justification**

- **Bastion/Jump Server Only:** To centralize and secure API access, reducing exposure risks.
- **Direct Workstation Access:** For simplicity and speed, easing admin tasks.

**Implications**

- **Bastion/Jump Server Only:** Centralizes access control with auditing capabilities; requires a bastion host setup, adding infrastructure effort with potential workflow delays.
- **Direct Workstation Access:** Risks broader exposure needing strict network policies; enables direct API connections, reducing setup needs with faster access.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-07: Mirror registry (disconnected environment)

**Architectural Question**
What mirror registry will be used?

**Issue or Problem**
In a disconnected environment, a mirror registry is essential for providing OpenShift AI with access to container images and operators. The choice of registry impacts availability, scalability, and integration.

**Assumption**
OpenShift cluster is in a disconnected environment.

**Alternatives**

- Mirror registry for Red Hat OpenShift
- Existing HA Corporate Registry
- Installing a new dedicated HA corporate images registry

**Decision**
#TODO#

**Justification**

- **Mirror registry for Red Hat OpenShift:** To use the simple, filesystem-based mirror registry included with OpenShift Container Platform subscriptions. This option meets the minimum requirement for mirroring installation artifacts.
- **Existing HA Corporate Registry:** To leverage existing scalable infrastructure (e.g., Quay, Nexus, Artifactory), reducing setup costs and leveraging existing enterprise management.
- **Installing a new dedicated HA corporate images registry:** To deploy a new, fully-featured registry (like Red Hat Quay) optimized to serve as the single source of truth for both required mirrored content and internal application images.

**Implications**

- **Mirror registry for Red Hat OpenShift:** Adds management overhead for a potential single point of failure if deployed non-HA; simplifies setup but risks downtime without redundancy. This solution is not a full-featured registry.
- **Existing HA Corporate Registry:** Requires integrating the existing platform (e.g., Nexus, Artifactory) to handle Red Hat content, potentially straining existing capacity. Relies on the registry team supporting the OCP mirroring process.
- **Installing a new dedicated HA corporate images registry:** Increases infrastructure footprint, resource costs, and administrative overhead associated with deploying and maintaining a new registry solution. Offers most features (security, team isolation).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-08: Internet connected host for preparing disconnected environment

**Architectural Question**
Will the internet connected host for preparing a disconnected environment be able to connect to the mirrored registry?

**Issue or Problem**
An internet-connected host is used to download images before transferring them to the mirrored registry in the disconnected environment. Whether this host can connect directly to the mirrored registry affects the workflow and security boundaries.

**Assumption**
OpenShift cluster is in a disconnected environment.

**Alternatives**

- Direct Access to Mirrored Registry
- No Direct Access to Mirrored Registry

**Decision**
#TODO#

**Justification**

- **Direct Access to Mirrored Registry:** To streamline mirroring by pushing directly to the registry, reducing steps.
- **No Direct Access to Mirrored Registry:** To enforce security isolation, aligning with air-gapped policies.

**Implications**

- **Direct Access to Mirrored Registry:** Requires network config (e.g., VPN) and security reviews; simplifies image mirroring (e.g., oc mirror push), reducing setup time but risking exposure.
- **No Direct Access to Mirrored Registry:** Enhances security with isolated processes; requires staging (e.g., USB transfer), adding manual steps with potential transfer errors.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-09: S3 Object Storage Location

**Architectural Question**
Will S3-compatible object storage be used for OpenShift AI, and if so, where will it be hosted?

**Issue or Problem**
OpenShift AI requires S3-compatible object storage for serving models and running Data Science Pipelines. Not using S3 prevents model serving and pipeline execution.

**Assumption**
S3-compatible object storage is required for RHOAI operations (model serving/pipelines).

**Alternatives**

- OpenShift Data Foundation (MCG)
- External Cloud Provider S3 Storage (e.g., AWS S3, Azure Blob, GCP)
- External Dedicated S3 Storage (e.g., MinIO, Ceph RGW)

**Decision**
#TODO#

**Justification**

- **OpenShift Data Foundation (MCG):** To utilize integrated, on-cluster object storage provided by ODF, optimizing data co-location and simplifying platform storage management. MCG is the standard component provided by ODF.
- **External Cloud Provider S3 Storage (e.g., AWS S3, Azure Blob, GCP):** To leverage native cloud services, benefiting from hyperscaler scalability, durability, and managed service features.
- **External Dedicated S3 Storage (e.g., MinIO, Ceph RGW):** To utilize an existing, dedicated, enterprise-grade S3 solution for centralized storage management outside of the OCP cluster lifecycle.

**Implications**

- **OpenShift Data Foundation (MCG):** Requires ODF installation and configuration; ensures low-latency access but requires proper sizing of ODF storage infrastructure within the OCP nodes. Adds resource overhead of MCG components.
- **External Cloud Provider S3 Storage (e.g., AWS S3, Azure Blob, GCP):** Requires external connectivity and secure credential management (e.g., Secrets) within OCP/RHOAI namespaces to access the bucket. Cannot leverage ODF's native object storage capabilities. Offloads S3 management.
- **External Dedicated S3 Storage (e.g., MinIO, Ceph RGW):** Requires configuration of external storage cluster connectivity and dependencies; potentially minimizes network latency by using high-speed internal network links. Offloads S3 management.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert

---

## RHOAI-SM-10: Default storage class for Red Hat OpenShift AI components

**Architectural Question**
Which default storage class (StorageClass) will be configured for use by Red Hat OpenShift AI components?

**Issue or Problem**
OpenShift AI components, particularly workbenches creating PVCs, require a default `StorageClass` to be defined in the cluster for dynamic volume provisioning. The selected default class affects performance, access modes (RWO/RWX), and storage capacity management for these components.

**Assumption**
A default StorageClass is required if dynamic provisioning is used (standard practice).

**Alternatives**

- Use Existing Cluster Default StorageClass
- Designate a Specific RHOAI Default StorageClass

**Decision**
#TODO#

**Justification**

- **Use Existing Cluster Default:** To leverage the pre-configured default `StorageClass` in the OpenShift cluster, minimizing RHOAI-specific storage configuration. Simple if the existing default meets RHOAI's needs (e.g., provides RWO block storage).
- **Designate a Specific RHOAI Default:** To explicitly choose or create a `StorageClass` (e.g., one provided by ODF with specific performance tiers or features) and mark it as the default for the cluster, ensuring RHOAI components use the desired storage backend. Requires cluster-admin privilege to change the default annotation.

**Implications**

- **Use Existing Cluster Default:** RHOAI component storage characteristics (performance, availability) are tied to whatever the cluster default happens to be. May not be optimal (e.g., if the default is slow or doesn't support required features). Easiest initial setup.
- **Designate Specific RHOAI Default:** Ensures RHOAI components (like workbench PVCs) use the intended storage backend (e.g., ODF `ocs-storagecluster-ceph-rbd`). Requires careful planning to choose the right `StorageClass` and administrative action to set it as default (patching the `storageclass.kubernetes.io/is-default-class` annotation). Changing the default affects _all_ workloads in the cluster that don't specify an explicit `storageClassName`.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert

---

## RHOAI-SM-11: Identity provider

**Architectural Question**
Which OpenShift identity provider (IdP) will be used to authenticate users accessing Red Hat OpenShift AI?

**Issue or Problem**
OpenShift AI relies entirely on the OpenShift platform's configured authentication mechanism. The choice of IdP affects user login experience, integration with enterprise directories, group management for RBAC, and overall security posture.

**Assumption**
An appropriate OpenShift IdP must be configured (see OCP-SEC-01).

**Alternatives**

- OpenShift Built-in (HTPasswd - typically non-production)
- Enterprise LDAP/Active Directory
- OpenID Connect (OIDC) / OAuth (e.g., Keycloak, Azure AD, Okta)

**Decision**
#TODO#

**Justification**

- **OpenShift Built-in (HTPasswd):** For simplicity during initial setup, testing, or small PoCs where integration with external systems is not required. Not suitable for enterprise use.
- **Enterprise LDAP/Active Directory:** To integrate directly with existing corporate user directories for authentication and potentially group synchronization (see OCP-SEC-02). Common in traditional enterprises.
- **OpenID Connect (OIDC) / OAuth:** To integrate with modern identity providers, offering features like Single Sign-On (SSO), Multi-Factor Authentication (MFA), and standardized token-based authentication. Recommended for flexibility and security.

**Implications**

- **HTPasswd:** User management is manual and cluster-specific. Does not scale and lacks enterprise features.
- **LDAP/AD:** Requires configuring connection details, schemas, and potentially group sync (OCP-SEC-02). Leverages existing user identities but might be less flexible than OIDC.
- **OIDC/OAuth:** Requires configuring an OAuth client within the IdP and corresponding provider details in OpenShift. Enables seamless SSO and modern authentication workflows. RHOAI dashboard and components integrate directly with this OpenShift authentication layer.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-12: OpenShift AI Namespace Strategy

**Architectural Question**
What namespace strategy will be used for deploying OpenShift AI components and managing data science workloads?

**Issue or Problem**
Red Hat OpenShift AI Self-Managed uses default projects (`redhat-ods-operator`, `redhat-ods-applications`, `rhods-notebooks`), but enterprise environments often require custom names for standardization, compliance, or multi-tenancy isolation.

**Assumption**
N/A

**Alternatives**

- Use Default RHOAI Namespaces
- Configure Custom Namespaces for RHOAI Core Components
- Use Dedicated Namespaces per Data Science Project/Team

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Use Default RHOAI Namespaces:** To simplify installation and maintenance by accepting the standard naming (`redhat-ods-*`, `rhods-notebooks`). Aligns directly with documentation and default operator behavior.
- **Configure Custom Namespaces for RHOAI Core:** To adhere to strict organizational naming conventions by specifying custom project names for the core RHOAI operator and application components during installation.
- **Use Dedicated Namespaces per Data Science Project/Team:** To isolate data science work (notebooks, pipelines, models) into separate OpenShift projects beyond the default `rhods-notebooks`, enabling finer-grained RBAC, quotas, and network policies per team or initiative (aligns with OCP-MGT-01).

**Implications**

- **Use Default Namespaces:** Easiest setup. The `rhods-notebooks` namespace serves as the default location for user workbenches unless specific data science projects are configured. May not meet strict naming policies.
- **Configure Custom Core Namespaces:** Requires defining custom names via `DataScienceCluster` CR _before_ initial installation. Ensures compliance with naming standards for platform components but adds configuration steps.
- **Dedicated Data Science Namespaces:** Provides strong isolation for user workloads (notebooks, models). Requires configuring RHOAI (`DataScienceCluster` CR) to recognize these projects for deploying workbenches and enabling RHOAI features within them. Requires robust project provisioning and RBAC automation (see OCP-MGT-01, OCP-MGT-02).

**Agreeing Parties**

- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-13: Model Serving Platform Selection

**Architectural Question**
Which model serving platform architecture will be used in Red Hat OpenShift AI?

**Issue or Problem**
A decision is required on the underlying technology for deploying models as scalable endpoints, affecting dependencies, resource usage, complexity, and supported features (like scale-to-zero).

**Assumption**
Model deployment capabilities are required.

**Alternatives**

- KServe (Single Model Serving / RawDeployment Mode)
- Custom Application Deployment (OpenShift Deployments)

**Decision**
#TODO#

**Justification**

- **KServe (Single Model Serving / RawDeployment Mode):** To deploy each model as a separate, highly scalable endpoint optimized for AI/ML workloads using the integrated KServe platform. Leverages features like standardized inference protocols, model management, and observability hooks. RawDeployment mode avoids reliance on OpenShift Serverless.
- **Custom Application Deployment (OpenShift Deployments):** To use standard OpenShift deployment methods (e.g., `Deployment`, `Service`) for model endpoints, wrapping the model in a custom container. Maximizes control over native Kubernetes primitives but requires building more infrastructure manually.

**Implications**

- **KServe (RawDeployment Mode):** Requires installation of KServe components (Operator, Controller). Relies on Istio Service Mesh for advanced traffic management. Provides a standardized MLOps workflow for serving but abstracts some Kubernetes details. RawDeployment mode ensures compatibility and avoids deprecated Serverless dependencies.
- **Custom Application Deployment:** Requires developers to build container images with model serving logic (e.g., using Flask/FastAPI) and manually create `Deployment`, `Service`, `Route`/`Ingress`, `HPA` resources. Lacks the specialized features of KServe (e.g., standardized metrics, easy canary rollouts) unless implemented manually.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-14: Authorization provider for KServe Model Serving

**Architectural Question**
Will an authorization provider (Authorino) be used for KServe single-model serving endpoints?

**Issue or Problem**
KServe single-model serving endpoints may require fine-grained authorization beyond basic OpenShift RBAC. Using Authorino—an external authorization service integrated with Istio—impacts security granularity and configuration complexity. Skipping it relies on simpler, built-in OpenShift/Istio mechanisms.

**Assumption**
Single-model serving platform (KServe) is enabled (RHOAI-SM-13).

**Alternatives**

- Use Authorino for KServe Authorization
- Do Not Use Authorino (Rely on OpenShift RBAC/Istio Policy)

**Decision**
#TODO#

**Justification**

- **Use Authorino for KServe Authorization:** To enable dynamic, policy-based, fine-grained authorization (e.g., based on OIDC tokens, API keys, JWT claims) for accessing served models, enhancing endpoint security.
- **Do Not Use Authorino:** For simpler authorization management, relying on native OpenShift RBAC and standard Istio authorization policies for basic access control to KServe endpoints.

**Implications**

- **Use Authorino for KServe Authorization:** Requires installing and configuring the Authorino Operator and Authorino instances. Demands expertise in defining Authorino `AuthConfig` policies and integrating them with Istio. Increases overall complexity but provides robust, flexible authorization.
- **Do Not Use Authorino:** Reduces administrative overhead and dependencies. Authorization relies on standard Kubernetes/Istio mechanisms, which might offer less granularity than required for complex security scenarios.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-15: NVIDIA GPU Support

**Architectural Question**
Will NVIDIA GPUs be used in Red Hat OpenShift AI?

**Issue or Problem**
OpenShift AI supports NVIDIA GPUs for compute-intensive tasks (training, inference). Deciding to use them impacts hardware requirements, cost, installation complexity (NVIDIA GPU Operator), versus potential performance gains.

**Assumption**
N/A

**Alternatives**

- Enable NVIDIA GPU Support
- Disable NVIDIA GPU Support

**Decision**
#TODO#

**Justification**

- **Enable NVIDIA GPU Support:** For accelerating demanding AI/ML workloads by leveraging NVIDIA GPU hardware. Essential for many deep learning training and inference tasks.
- **Disable NVIDIA GPU Support:** For simplicity and cost savings if workloads do not require GPU acceleration or if alternative accelerators (e.g., Intel HPUs) are used.

**Implications**

- **Enable NVIDIA GPU Support:** Requires purchasing and installing compatible NVIDIA GPU hardware in worker nodes. Necessitates installation and configuration of the NVIDIA GPU Operator to manage drivers and make GPUs available to containers. Increases setup cost and complexity.
- **Disable NVIDIA GPU Support:** Simplifies cluster setup and maintenance. Limits the types of high-performance workloads that can be efficiently run on the platform.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## RHOAI-SM-16: CA Certificate management

**Architectural Question**
Which CA certificate bundle will be used for Red Hat OpenShift AI components, and how will its lifecycle be managed?

**Issue or Problem**
OpenShift AI components require trusted CA certificates for secure TLS communication. Choosing the bundle and manager affects trust scope, integration effort, and operational consistency, especially with recent changes favouring external management.

**Assumption**
N/A

**Alternatives**

- Managed by RHOAI Operator (Legacy/Compatibility Mode)
- Externally Managed (`managementState: Removed`)

**Decision**
#TODO#

**Justification**

- **Managed by RHOAI Operator:** To have the OpenShift AI Operator automatically manage a `trusted-ca-bundle` ConfigMap containing necessary CAs for internal and potentially external communication trust. Simpler initial setup but less control.
- **Externally Managed (`managementState: Removed`):** To align with the recommended approach (RHOAI 2.25+), where the operator does not manage the CA bundle directly. Trust is managed externally (e.g., via cluster-wide proxy settings, injecting CAs via ConfigMaps referenced by workloads, or using service mesh trust). Offers better security separation and aligns with standard cluster practices.

**Implications**

- **Managed by RHOAI Operator:** The Operator actively manages the `trusted-ca-bundle` ConfigMap in relevant namespaces. Provides automatic trust injection for components managed by the operator but increases the operator's configuration scope and might conflict with external CA management strategies.
- **Externally Managed/Removed:** Requires administrators to ensure necessary CAs are trusted via other mechanisms (e.g., cluster proxy config, manual ConfigMap creation and volume mounts, service mesh CA integration). More administrative effort initially but provides clearer separation of concerns and reduces operator complexity/potential conflicts. This is the preferred long-term approach.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-17: Persistent Volume Claim (PVC) Backup Strategy

**Architectural Question**
Will you implement backup for Persistent Volume Claims (PVCs) used by Red Hat OpenShift AI components?

**Issue or Problem**
A defined backup strategy is required to ensure data recoverability and compliance for critical data scientist artifacts stored in PVCs (e.g., notebooks, datasets, workbench configurations).

**Assumption**
N/A

**Alternatives**

- OADP Operator using CSI Snapshots/Kopia
- No Dedicated Platform Backup Solution

**Decision**
#TODO#

**Justification**

- **OADP Operator using CSI Snapshots/Kopia:** To leverage the official OpenShift API for Data Protection (OADP) solution for backing up application data (PVCs) using volume snapshots (for CSI-compatible storage like ODF) or file system backups (Kopia, replacing deprecated Restic), enabling application-consistent backup capabilities.
- **No Dedicated Platform Backup Solution:** To rely entirely on underlying storage platform capabilities (e.g., ODF snapshot management or external storage provider snapshots) or manual user actions (e.g., Git push) for volume protection, accepting the risk associated with non-integrated backup.

**Implications**

- **OADP Operator using CSI Snapshots/Kopia:** Requires OADP Operator installation and configuration, plus a backup storage location (S3-compatible). Ensures application-aware backup/restore capabilities integrated with Kubernetes resources. Adds management overhead for backup schedules and restores. Recommended for comprehensive protection.
- **No Dedicated Platform Backup Solution:** Recovery procedures rely on external, non-Kubernetes-native storage mechanisms or manual user intervention. High risk of data loss or complex manual recovery for data solely on PVCs. Violates best practices for enterprise data protection.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert

---

## RHOAI-SM-18: Usage data collection

**Architectural Question**
Will you enable usage data collection (telemetry) for Red Hat OpenShift AI?

**Issue or Problem**
OpenShift AI Self-Managed can optionally send anonymized usage data to Red Hat via telemetry to help improve the product. Enabling this affects privacy considerations, connectivity requirements, and compliance policies.

**Assumption**
N/A

**Alternatives**

- Enable Sending Usage Data to Red Hat
- Disable Sending Usage Data to Red Hat

**Decision**
#TODO#

**Justification**

- **Enable Sending Usage Data to Red Hat:** To contribute usage statistics that help Red Hat understand product usage patterns and prioritize improvements. May facilitate proactive support in some cases.
- **Disable Sending Usage Data to Red Hat:** To maintain strict data isolation, comply with privacy regulations, or operate in environments without outbound internet connectivity.

**Implications**

- **Enable Sending Usage Data to Red Hat:** Requires outbound internet connectivity from the cluster to Red Hat's telemetry endpoints. Data sent is typically anonymized configuration and usage metrics. May require review by security/privacy teams.
- **Disable Sending Usage Data to Red Hat:** Ensures no data leaves the cluster for telemetry purposes. Requires explicitly setting `spec.telemetry.enabled: false` in the `DataScienceCluster` CR. Simplifies setup in disconnected environments.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-19: Red Hat partner solutions integration

**Architectural Question**
Which Red Hat partner software (ISV) components will be enabled or integrated with Red Hat OpenShift AI?

**Issue or Problem**
OpenShift AI supports enabling certified partner software components to enhance AI/ML capabilities (e.g., specialized libraries, alternative workbenches, data platforms). Choosing which components to enable impacts functionality, licensing, compatibility, resource usage, and complexity.

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

- **Anaconda Enterprise Notebooks:** To provide Anaconda's curated package distribution and management within RHOAI workbenches.
- **IBM Watson Studio:** To integrate IBM's suite of AI tools and MLOps capabilities.
- **Intel AI Tools (including OpenVINO):** For leveraging Intel-optimized libraries, frameworks (like OpenVINO for inference), and potentially Intel hardware acceleration.
- **NVIDIA AI Enterprise:** To utilize NVIDIA's optimized software suite for AI/ML, particularly on NVIDIA GPUs.
- **Pachyderm:** To integrate Pachyderm's data versioning and pipelining capabilities.
- **Starburst Galaxy:** For integrating Starburst's distributed SQL query engine for data access and federation.
- **None:** To rely solely on the components provided directly by Red Hat within OpenShift AI for simplicity and minimal dependencies.

**Implications**

- **Enabling ISV Components:**
  - Typically requires separate licenses from the ISV partner.
  - May consume additional cluster resources.
  - Requires managing the lifecycle (installation, upgrades) of the partner operator/components.
  - Adds specific functionalities tailored to the partner's offering.
  - Compatibility needs to be maintained between RHOAI and partner software versions.
- **None:**
  - Simplifies licensing and dependency management.
  - Relies entirely on RHOAI's built-in features and available community integrations.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-20: Data sources

**Architectural Question**
Which types of data sources need to be accessible to data scientists within the OpenShift AI platform?

**Issue or Problem**
Data scientists require access to various data sources for model training, analysis, and experimentation. Identifying these sources and planning for connectivity impacts network configuration, security policies, authentication, and the tools needed within workbenches.

**Assumption**
N/A

**Alternatives**

- S3-Compatible Object Storage
- Relational Databases (e.g., PostgreSQL, MySQL)
- Data Warehouses (e.g., Snowflake, Redshift)
- Data Lakes (e.g., HDFS, Iceberg)
- Feature Stores
- Streaming Platforms (e.g., Kafka)
- Combination of Above
- Primarily Local/Uploaded Data Only

**Decision**
#TODO#

**Justification**

- **S3-Compatible Object Storage:** For accessing large datasets stored in scalable object storage (on-cluster via ODF/MCG or external).
- **Relational Databases:** For querying structured data from traditional databases.
- **Data Warehouses:** For connecting to enterprise data warehouses for analytics and BI data.
- **Data Lakes:** For accessing large volumes of raw, semi-structured, or unstructured data.
- **Feature Stores:** For accessing curated, reusable features for model training.
- **Streaming Platforms:** For processing real-time data streams.
- **Combination of Above:** To provide maximum flexibility for diverse data science needs.
- **Primarily Local/Uploaded Data Only:** To simplify initial setup, relying on data manually uploaded to workbenches or PVCs.

**Implications**

- **Connecting to External Sources:** Requires network connectivity (firewall rules, routing, DNS), appropriate credentials/authentication mechanisms (potentially managed via secrets), and necessary drivers or libraries within notebook images. Security reviews are often necessary.
- **S3-Compatible Storage:** Requires configuring access credentials and potentially S3-specific libraries (like boto3). (See RHOAI-SM-09 for hosting decision).
- **Databases/Warehouses:** Requires installing relevant database drivers (e.g., psycopg2) and managing connection strings/credentials securely.
- **Data Lakes/Streaming:** May require specialized libraries (e.g., PySpark, Kafka clients) and potentially more complex network configurations.
- **Feature Stores:** Requires deploying and integrating the feature store platform itself.
- **Local/Uploaded Data Only:** Simplest network/security setup but limits scalability and collaboration on large datasets.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-21: Notebook images for data scientists

**Architectural Question**
What notebook images (providing JupyterLab environments) will be made available to data scientists?

**Issue or Problem**
Data scientists use notebook images within workbenches to get their runtime environment (Python/R, libraries, tools). The choice and management strategy impacts available tools, consistency, security, maintenance effort, and user experience.

**Assumption**
N/A

**Alternatives**

- Red Hat Provided Standard Images
- Red Hat Provided CUDA Images (if GPUs enabled)
- Open Data Hub (ODH) Community Images
- Custom-Built Images (Derived from Red Hat/ODH)
- Combination of Above

**Decision**
#TODO#

**Justification**

- **Red Hat Provided Standard/CUDA Images:** To use the officially supported, certified images included with RHOAI, ensuring compatibility and supportability. CUDA images are necessary for GPU workloads.
- **Open Data Hub (ODH) Community Images:** To leverage a wider variety of pre-built images from the upstream ODH community, potentially offering newer versions or different toolsets (support is community-based).
- **Custom-Built Images:** To create tailored environments with specific libraries, drivers, or internal tools pre-installed, ensuring consistency and meeting specific project needs.
- **Combination of Above:** To offer a mix, providing supported base images alongside custom ones for flexibility.

**Implications**

- **Red Hat Provided Images:** Limited customization out-of-the-box (users install packages at runtime). Updates are managed by Red Hat through RHOAI upgrades. Ensures a consistent, supported baseline.
- **ODH Community Images:** May offer more options but lack official Red Hat support. Requires vetting for security and compatibility. Update lifecycle is community-dependent.
- **Custom-Built Images:** Provides maximum control and standardization but requires establishing a build pipeline (e.g., using OpenShift Builds/Pipelines, Jenkins, GitLab CI), managing dependencies, and handling security scanning and updates. Increases maintenance overhead. (See RHOAI-SM-22, RHOAI-SM-23).
- **Combination:** Offers flexibility but requires clear governance on which images are supported and how custom images are managed.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-22: Required Python packages (for Custom Images)

**Architectural Question**
If building custom notebook images, what additional Python packages (beyond those in the base image) are required by data scientists?

**Issue or Problem**
Custom notebook images are built to provide specific environments. Identifying the necessary Python packages upfront is crucial for image design, dependency management, and ensuring reproducibility.

**Assumption**
Custom notebook images will be built (Decision from RHOAI-SM-21).

**Alternatives**

- Minimal Common Set (e.g., visualization, data manipulation extensions)
- Domain-Specific Sets (e.g., NLP, Computer Vision, Time Series)
- Framework-Specific Sets (e.g., TensorFlow, PyTorch, XGBoost variants)
- Comprehensive Custom Set (Mixing multiple domains/frameworks)
- Allow Runtime Installation Only (No custom packages baked-in)

**Decision**
#TODO#

**Justification**

- **Minimal Common Set:** For providing generally useful tools not in the base image with minimal bloat.
- **Domain/Framework-Specific Sets:** To create optimized images tailored to specific types of data science work, reducing image size and potential conflicts.
- **Comprehensive Custom Set:** To build a 'kitchen-sink' image with many tools pre-installed for maximum convenience, potentially at the cost of image size and complexity.
- **Allow Runtime Installation Only:** Simplest custom image (just the base), forcing users to install packages via pip/conda within their running workbench.

**Implications**

- **Baking Packages into Images:** Ensures consistency and reproducibility. Reduces startup time for users. Requires managing dependencies and rebuilding images when updates are needed. Increases image size. Security scanning of added packages is critical.
- **Domain/Framework-Specific Images:** Leads to multiple custom images to manage but provides more tailored and potentially smaller environments.
- **Allow Runtime Installation Only:** Smallest custom images. Gives users maximum flexibility but can lead to environment inconsistencies ("works on my machine"). Users need internet access (or internal mirrors) for installation. Can increase workbench startup/setup time.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-23: Custom notebook images location

**Architectural Question**
Where will custom-built notebook server images be stored and accessed from?

**Issue or Problem**
Custom notebook images need to be hosted in a container registry accessible by the OpenShift cluster. The choice of registry impacts accessibility, security, build pipeline integration, and operational management.

**Assumption**
Custom notebook images will be built (Decision from RHOAI-SM-21).

**Alternatives**

- Existing HA Corporate Registry (e.g., Quay, Artifactory, Nexus)
- OpenShift Internal Registry (Image Registry Operator)

**Decision**
#TODO#

**Justification**

- **Existing HA Corporate Registry:** To leverage existing, enterprise-managed registry infrastructure for centralized image storage, governance (scanning, signing), and potentially better availability and scalability. Aligns with existing artifact management practices.
- **OpenShift Internal Registry:** To store images locally within the cluster, simplifying network access (no external connectivity needed for pulls), optimizing pull times, and potentially reducing reliance on external systems.

**Implications**

- **Existing HA Corporate Registry:** Requires network connectivity from the cluster to the registry. Image pull secrets must be configured in the namespaces where workbenches run (e.g., `rhods-notebooks` or data science project namespaces). Build pipelines need push access. Integrates with existing security scanning/signing infrastructure.
- **OpenShift Internal Registry:** Requires configuring the internal registry with adequate persistent storage (e.g., ODF RWO/RWX or other PVs - see OCP-STOR-01). Lifecycle and availability of the internal registry must be managed. Build pipelines run within the cluster can easily push to it. May require separate setup for security scanning if not integrated.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-24: Notebook file location

**Architectural Question**
Where will data scientists primarily store their notebook files (`.ipynb`) and associated code/scripts?

**Issue or Problem**
Notebook files represent the core work product of data scientists. The storage strategy impacts version control, collaboration, reproducibility, backup/recovery, and data management practices.

**Assumption**
N/A

**Alternatives**

- Local Workbench Storage (PVC)
- Git Repository (Integrated with Workbench)

**Decision**
#TODO#

**Justification**

- **Local Workbench Storage (PVC):** For simplicity and immediate persistence within the user's workbench environment. Files are stored on the PVC attached to the workbench pod.
- **Git Repository (Integrated with Workbench):** For enabling version control, collaboration, code reviews, and easier integration with CI/CD or MLOps pipelines. Workbenches can clone Git repos on startup.

**Implications**

- **Local Workbench Storage (PVC):** Simplest setup. Data persists across workbench restarts. Difficult to version control or collaborate effectively. Requires a PVC backup strategy (RHOAI-SM-17) for resilience. Can lead to data silos.
- **Git Repository:** Promotes best practices (version control, collaboration). Requires users to commit/push changes regularly. Needs network connectivity to the Git server. Git credentials must be managed (e.g., via secrets). Enables GitOps workflows for notebooks and code. Data resilience relies on the Git server's backup strategy.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-25: Notebook repositories (if Git used)

**Architectural Question**
If using Git, how will repositories be structured and managed for data science collaboration?

**Issue or Problem**
Defining repository structures and access patterns impacts collaboration efficiency, code sharing, version control clarity, and integration with MLOps workflows.

**Assumption**
Notebook files and code will be stored primarily in Git repositories (Decision from RHOAI-SM-24).

**Alternatives**

- Single Shared Mono-Repository (All projects/teams)
- Repository per Team/Group
- Repository per Project/Initiative
- Hybrid Approach (e.g., Shared libs repo + project repos)

**Decision**
#TODO#

**Justification**

- **Single Shared Mono-Repository:** To simplify discovery and dependency management across all data science work. Easier to enforce standards centrally.
- **Repository per Team/Group:** To provide autonomy and clear ownership boundaries for different data science teams. Aligns access control with team structure.
- **Repository per Project/Initiative:** To isolate work related to specific ML models or business problems, facilitating project-specific lifecycles.
- **Hybrid Approach:** To balance central standards/shared code (e.g., in a common library repo) with project-specific flexibility (in dedicated project repos).

**Implications**

- **Mono-Repository:** Can become large and complex to navigate. Requires robust branching strategies and potentially CODEOWNERS configuration to manage contributions. CI/CD triggers can become noisy.
- **Repository per Team/Group:** Can lead to code duplication if sharing between teams is needed. Requires mechanisms for discovering and reusing work across team boundaries. Simplifies team-level access control.
- **Repository per Project/Initiative:** Creates many repositories to manage. Clear isolation but potentially hinders cross-project collaboration or standardization.
- **Hybrid Approach:** Offers flexibility but requires clear governance on what belongs where and how dependencies between repos are managed.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-26: Data science projects

**Architectural Question**
How will OpenShift Projects (Kubernetes Namespaces) be allocated and used for data science activities within Red Hat OpenShift AI?

**Issue or Problem**
OpenShift Projects provide isolation boundaries for resources, RBAC, network policies, and quotas. The strategy for allocating projects impacts multi-tenancy, resource management, security, and collaboration among data scientists.

**Assumption**
N/A

**Alternatives**

- Single Shared Data Science Project (e.g., `rhods-notebooks`)
- Project per Team/Group
- Project per ML Project/Initiative
- Hybrid (e.g., Shared for experimentation, dedicated for production pipelines/serving)

**Decision**
#TODO#

**Justification**

- **Single Shared Data Science Project:** Simplest approach, often using the default `rhods-notebooks` project. All users share resources and potentially RBAC within this single namespace. Suitable for small teams or initial pilots.
- **Project per Team/Group:** Provides isolation between different data science teams. Allows team-specific RBAC, quotas, and network policies. Promotes team autonomy.
- **Project per ML Project/Initiative:** Offers the highest level of isolation, dedicating a namespace to a specific model or business problem. Facilitates project-specific resource tracking and security boundaries.
- **Hybrid:** Allows experimentation in a shared space while promoting critical pipelines or served models to dedicated, more controlled namespaces.

**Implications**

- **Single Shared Project:** Higher risk of resource contention (quotas needed - OCP-MGT-04). RBAC and network policy management become complex within the shared namespace. Difficult to track resource usage per initiative.
- **Project per Team/Group:** Increases the number of namespaces to manage. Requires automation for project creation and configuration. Clearer resource allocation and security boundaries per team.
- **Project per ML Project/Initiative:** Results in the largest number of namespaces, significantly increasing management overhead if not highly automated. Provides granular control and chargeback capabilities.
- **Hybrid:** Balances flexibility with control but requires clear processes for promoting work between shared and dedicated namespaces.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-27: Workbenches

**Architectural Question**
How will workbenches (JupyterLab environments) be provisioned and managed for data scientists?

**Issue or Problem**
Workbenches are the primary interactive development environment. The provisioning strategy impacts resource allocation (CPU, memory, PVCs, GPUs), user experience, environment consistency, and cost.

**Assumption**
N/A

**Alternatives**

- Individual Workbench per User (Self-Service)
- Shared Team Workbenches
- Role/Task-Specific Workbench Configurations (e.g., GPU vs. CPU)

**Decision**
#TODO#

**Justification**

- **Individual Workbench per User:** Provides maximum isolation and allows users to self-select workbench size and image based on their needs (within defined limits/profiles). Most common approach.
- **Shared Team Workbenches:** To potentially save resources by having team members share a single, larger workbench instance. Requires careful coordination among users.
- **Role/Task-Specific Workbench Configurations:** To pre-define specific workbench templates (sizes, images, accelerator profiles) tailored for common roles (e.g., data analyst, ML engineer) or tasks (e.g., exploration, training).

**Implications**

- **Individual Workbench per User:** Can lead to higher overall resource consumption if many users provision large or GPU-enabled workbenches. Requires clear definitions of available workbench sizes/profiles and potentially quotas. Offers best user autonomy.
- **Shared Team Workbenches:** Difficult to manage resource contention and user interference within the shared environment. May not be practical for sensitive data. Less common.
- **Role/Task-Specific Configurations:** Simplifies the choices for users by providing curated options. Requires administrators to define and maintain these configurations. Can help enforce standards and control resource usage.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-28: Intel HPU Accelerator Usage

**Architectural Question**
Will Intel HPUs be used in Red Hat OpenShift AI?

**Issue or Problem**
OpenShift AI supports Intel HPUs (e.g., Gaudi) for cost-effective performance. Deciding to use them impacts hardware needs, cost, and complexity versus potential gains.

**Assumption**
N/A

**Alternatives**

- Enable Intel HPU Usage (Gaudi)
- Do Not Enable Intel HPU Usage

**Decision**
#TODO#

**Justification**

- **Enable Intel HPU Usage (Gaudi):** To utilize supported Intel Gaudi 2 and Intel Gaudi 3 devices, providing a cost-efficient, flexible, and scalable solution optimized for deep learning workloads.
- **Do Not Enable Intel HPU Usage:** To simplify hardware requirements and procurement by relying only on CPU, standard GPUs, or alternative accelerators.

**Implications**

- **Enable Intel HPU Usage (Gaudi):** Requires installation and configuration of the necessary device plugins and operators (e.g., Intel AI Tools Operator or Habana Operator) to expose Gaudi resources to the cluster; requires procurement of specific Intel hardware. Requires using container images compatible with Habana SynapseAI SDK.
- **Do Not Enable Intel HPU Usage:** Limits AI/ML acceleration options to available alternative hardware; reduces the operational overhead associated with managing Intel-specific devices.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## RHOAI-SM-29: code-server workbenches

**Architectural Question**
Will the `code-server` (VS Code in browser) workbench option be enabled alongside JupyterLab?

**Issue or Problem**
RHOAI allows enabling `code-server` as an alternative IDE within workbenches, offering a VS Code experience. However, it's often a Tech Preview feature, may lack full integration (like Elyra pipeline support), and uses a different base image.

**Assumption**
Red Hat notebook server images are used.

**Alternatives**

- Enable Code-Server Workbench Option
- Disable Code-Server Workbench Option (JupyterLab Only)

**Decision**
#TODO#

**Justification**

- **Enable Code-Server Workbench Option:** To provide users familiar with VS Code an alternative IDE choice, potentially beneficial for tasks involving more extensive scripting or specific VS Code extensions.
- **Disable Code-Server Workbench Option:** To standardize on JupyterLab as the primary IDE, ensuring full feature compatibility (like Elyra) and simplifying the available image options.

**Implications**

- **Enable Code-Server:** Makes the `code-server` image available for selection when creating workbenches. Users choosing it get a VS Code interface but may lose access to Jupyter-specific integrations provided in RHOAI (e.g., Elyra visual pipeline editor). Often requires enabling Tech Preview features in the `DataScienceCluster` CR.
- **Disable Code-Server:** Simplifies the user choice and ensures all users have access to the fully integrated JupyterLab environment. Reduces the number of base images potentially needing customization or management.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-30: Cluster Storage (PVC) for Workbenches

**Architectural Question**
How will Persistent Volume Claim (PVC) sizing be managed for workbench local storage?

**Issue or Problem**
Each workbench requires a PVC for its local filesystem (/home/jovyan). The size of this PVC impacts the amount of local data a user can store and the overall storage consumption on the cluster.

**Assumption**
Workbenches are configured (RHOAI-SM-27). Local storage (PVC) is used, at least partially (RHOAI-SM-24).

**Alternatives**

- Fixed Default Size for All Workbenches
- User-Selectable Size (within pre-defined limits/tiers)
- Custom Size per Workbench (Admin controlled)

**Decision**
#TODO#

**Justification**

- **Fixed Default Size:** Simplest approach for administrators. Provides a consistent starting point for all users (e.g., 20Gi).
- **User-Selectable Size:** Offers flexibility by allowing users to choose a PVC size (e.g., Small-20Gi, Medium-50Gi, Large-100Gi) when creating their workbench, based on anticipated needs.
- **Custom Size per Workbench:** Most flexible but requires manual intervention or automation by administrators to set specific sizes, potentially based on requests.

**Implications**

- **Fixed Default Size:** May be insufficient for users working with large local datasets or numerous libraries. Can lead to users hitting storage limits. Easiest to manage capacity planning for.
- **User-Selectable Size:** Balances flexibility and control. Requires defining appropriate size tiers and potentially setting quotas (OCP-MGT-04) at the project level to prevent excessive consumption. Users need guidance on selecting appropriate sizes.
- **Custom Size per Workbench:** High administrative overhead unless heavily automated. Offers most precise allocation but can complicate capacity management.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Storage Expert

---

## RHOAI-SM-31: Pipeline database

**Architectural Question**
Which database backend will be used for storing Red Hat OpenShift AI Pipelines (Kubeflow Pipelines / KFP Tekton) metadata?

**Issue or Problem**
Data Science Pipelines require a database (typically SQL-based) to store pipeline run history, metadata, and potentially artifacts. The choice impacts scalability, reliability, data persistence, and operational management.

**Assumption**
Data Science Pipelines component will be enabled within RHOAI.

**Alternatives**

- Internal MariaDB (Auto-deployed by RHOAI)
- External MySQL/MariaDB (User-managed)

**Decision**
#TODO#

**Justification**

- **Internal MariaDB:** For simplicity and ease of setup. RHOAI automatically deploys a MariaDB instance within the cluster specifically for pipelines when the component is enabled. Suitable for non-production or smaller-scale deployments.
- **External MySQL/MariaDB:** For production environments requiring higher scalability, reliability, and integration with existing database backup/management strategies. Leverages an external, potentially HA database instance managed by the organization.

**Implications**

- **Internal MariaDB:** Simplest deployment. Database runs as pods within the cluster, consuming cluster resources. Data is typically stored on a PVC; persistence and backup depend on the cluster's storage and backup strategy (RHOAI-SM-17). May not scale sufficiently for very high pipeline throughput.
- **External MySQL/MariaDB:** Requires provisioning and managing a separate MySQL/MariaDB instance outside the RHOAI deployment. RHOAI Pipelines must be configured with connection details (hostname, credentials). Offloads database management from the cluster but adds an external dependency. Allows leveraging robust, enterprise-grade database features (HA, backup, monitoring).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-32: Pipelines in JupyterLab (Elyra)

**Architectural Question**
Will the Elyra extension for visual pipeline authoring within JupyterLab be enabled and utilized?

**Issue or Problem**
Elyra provides a UI within JupyterLab for building Data Science Pipelines by connecting notebook or script components visually. Enabling it requires using compatible notebook images and impacts the user workflow for pipeline creation.

**Assumption**
Data Science Pipelines component will be enabled. Users will primarily use JupyterLab workbenches.

**Alternatives**

- Enable and Promote Elyra Usage
- Disable or Do Not Promote Elyra (Use KFP SDK Primarily)

**Decision**
#TODO#

**Justification**

- **Enable and Promote Elyra Usage:** To provide data scientists with an intuitive visual tool for pipeline construction directly within their familiar Jupyter environment, lowering the barrier to entry for creating pipelines.
- **Disable or Do Not Promote Elyra:** To standardize on programmatic pipeline definition using the Kubeflow Pipelines (KFP) SDK directly in code. This offers more flexibility and control for complex pipelines but requires more coding expertise.

**Implications**

- **Enable Elyra:** Requires using notebook images that include Elyra and its dependencies (most standard RHOAI images do). Simplifies pipeline creation for many users. The generated pipeline is still ultimately KFP/Tekton compatible. Some advanced KFP features might not be exposed through the UI.
- **Disable Elyra:** Users define pipelines entirely via the KFP SDK (Python). Requires ensuring SDK is available in notebook images. Provides full access to all KFP features but has a steeper learning curve for users unfamiliar with the SDK.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-33: Distributed workloads (Ray)

**Architectural Question**
Will the capability for distributed AI/ML workloads using Ray be enabled?

**Issue or Problem**
RHOAI includes CodeFlare and KubeRay operators to enable the creation and management of temporary Ray clusters for distributed data processing and model training. Enabling this feature impacts cluster resources, dependencies, and configuration complexity.

**Assumption**
N/A

**Alternatives**

- Enable Distributed Workloads (CodeFlare/KubeRay)
- Disable Distributed Workloads

**Decision**
#TODO#

**Justification**

- **Enable Distributed Workloads:** To allow data scientists to scale computationally intensive tasks (e.g., large-scale data preprocessing, distributed training) across multiple nodes using the Ray framework.
- **Disable Distributed Workloads:** For simplicity and resource conservation if workloads do not require distributed computing capabilities beyond single-node execution (potentially with multiple cores/GPUs).

**Implications**

- **Enable Distributed Workloads:** Installs the CodeFlare and KubeRay operators. Requires additional cluster resources (minimum ~1.6 vCPU, ~2 GiB RAM just for operators). Users can then define and launch Ray clusters via `AppWrapper` CRs (managed by CodeFlare) or `RayCluster` CRs. Requires configuring security aspects (certificates for Ray dashboard). Adds complexity but enables significant performance gains for suitable workloads.
- **Disable Distributed Workloads:** Reduces the number of operators and resources consumed by RHOAI. Simplifies the platform but limits the ability to scale certain types of data science tasks horizontally across the cluster.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-34: Quota management for distributed workloads (Kueue)

**Architectural Question**
How will resource quotas and scheduling for distributed workloads (Ray clusters) be managed?

**Issue or Problem**
Distributed workloads launched via CodeFlare can consume significant cluster resources. RHOAI integrates Kueue for batch scheduling and resource quota management specifically for these workloads, preventing cluster saturation. Configuration impacts how resources are shared and prioritized.

**Assumption**
Distributed workloads (CodeFlare/KubeRay) are enabled (RHOAI-SM-33).

**Alternatives**

- Enable Kueue Integration (Recommended)
- Disable Kueue Integration (Rely on OpenShift Quotas only)

**Decision**
#TODO#

**Justification**

- **Enable Kueue Integration:** To leverage Kueue's batch scheduling capabilities (fair sharing, prioritization) and resource quotas (`ClusterQueue`, `LocalQueue`) specifically designed for managing ephemeral, high-resource distributed jobs like Ray clusters. Provides finer-grained control than standard OpenShift quotas.
- **Disable Kueue Integration:** To rely solely on standard OpenShift ResourceQuotas applied at the namespace level (OCP-MGT-04). Simpler setup but lacks the advanced scheduling features of Kueue.

**Implications**

- **Enable Kueue Integration:** Installs the Kueue operator. Requires configuration of at least one `ClusterQueue` defining the overall cluster resources available for distributed workloads, and potentially `LocalQueue`s within user namespaces to further subdivide quotas. Adds scheduling overhead but provides better control over resource-intensive batch jobs.
- **Disable Kueue Integration:** Simplifies installation. Resource consumption by Ray clusters is only limited by standard OpenShift quotas, potentially leading to resource exhaustion or unfair resource distribution if many large jobs are submitted concurrently. Lacks queuing and prioritization features.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-35: Authentication Method for Ray Dashboard

**Architectural Question**
Which authentication method will be used to secure access to the Ray Dashboard associated with distributed Ray clusters?

**Issue or Problem**
The Ray Dashboard provides visibility into Ray clusters but needs protection. RHOAI supports integrating it with OpenShift OAuth for single sign-on or allowing configuration of alternative methods.

**Assumption**
Distributed workloads (CodeFlare/KubeRay) are enabled (RHOAI-SM-33).

**Alternatives**

- OpenShift OAuth Integration (Default/Recommended)
- Custom/No Integrated Authentication

**Decision**
#TODO#

**Justification**

- **OpenShift OAuth Integration:** To leverage the cluster's existing authentication mechanism for seamless and secure access to the Ray Dashboard based on OpenShift user credentials and RBAC. Simplifies user management.
- **Custom/No Integrated Authentication:** To use alternative methods (e.g., Ray's own mechanisms if configured, or leaving it unprotected in trusted environments). Offers flexibility but potentially reduces security or increases configuration effort.

**Implications**

- **OpenShift OAuth Integration:** Requires configuring OpenShift OAuth details within the Ray cluster definition (often handled by CodeFlare defaults). Ray dashboard access is then controlled via OpenShift login and potentially specific roles. May require handling certificates if using custom cluster CAs.
- **Custom/No Integrated Authentication:** Bypasses OpenShift login for the dashboard. Requires configuring Ray's security settings manually or accepting lower security. May be simpler in isolated test environments but not recommended for production.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-36: Distributed workloads monitoring

**Architectural Question**
Will monitoring be enabled for distributed workloads (Ray clusters)?

**Issue or Problem**
Monitoring Ray clusters provides visibility into resource usage and job status but requires enabling OpenShift User Workload Monitoring (UWM) and ensuring Ray metrics are scraped, impacting cluster resources and configuration.

**Assumption**
Distributed workloads (CodeFlare/KubeRay) are enabled (RHOAI-SM-33).

**Alternatives**

- Enable Ray Monitoring via UWM
- Disable Ray Monitoring

**Decision**
#TODO#

**Justification**

- **Enable Ray Monitoring via UWM:** To collect metrics from Ray clusters (e.g., resource utilization, task status) and integrate them into the OpenShift Monitoring dashboard (Grafana) for observability. Essential for understanding performance and troubleshooting issues.
- **Disable Ray Monitoring:** For simpler deployment and reduced resource consumption if detailed Ray metrics are not required, relying instead on basic pod metrics, logs, or the Ray Dashboard.

**Implications**

- **Enable Ray Monitoring:** Requires enabling User Workload Monitoring (UWM) in the cluster's monitoring configuration (see OCP-MON-01). Consumes additional Prometheus resources for scraping and storing Ray metrics. Ray cluster definitions need appropriate annotations/labels for scraping. Provides valuable operational insights.
- **Disable Ray Monitoring:** Reduces monitoring overhead and resource usage. Limits visibility into the internal state and performance of Ray clusters, potentially making troubleshooting more difficult.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-37: Model-serving runtime for the single-model serving platform (KServe)

**Architectural Question**
Which specific model serving runtime(s) will be primarily used within the KServe single-model serving platform?

**Issue or Problem**
KServe supports various runtimes for serving different model formats and optimizing performance (e.g., for LLMs, ONNX, scikit-learn). Selecting and configuring appropriate runtimes determines which models can be served and how efficiently they run.

**Assumption**
Single-model serving platform (KServe) is enabled (RHOAI-SM-13).

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

- **RHOAI Custom Runtimes (Caikit+TGIS):** To use the default, supported runtime provided by RHOAI, optimized for Large Language Models (LLMs) using the Caikit framework and Text Generation Inference Server (TGIS).
- **KServe Core Runtimes:** To leverage standard runtimes included with KServe for common formats like scikit-learn, XGBoost, PMML, etc.
- **vLLM Runtime:** To achieve high throughput and low latency for LLM inference using the specialized vLLM engine, deployed as a custom KServe runtime.
- **OpenVINO Model Server (OVMS):** To optimize inference performance, particularly on Intel hardware (CPU, GPU, VPU), deployed as a custom KServe runtime.
- **NVIDIA Triton Inference Server:** To use NVIDIA's flexible inference server supporting multiple frameworks and optimized for NVIDIA GPUs, deployed as a custom KServe runtime.
- **Custom-Built Runtimes:** To support niche model formats or implement bespoke serving logic by building and configuring a custom KServe runtime container.

**Implications**

- **RHOAI/KServe Core Runtimes:** Generally easier to manage as they are often included or well-documented within the respective platforms. May not offer the absolute peak performance for all model types/hardware.
- **vLLM/OVMS/Triton (as Custom Runtimes):** Typically offer higher performance for their specialized domains (LLMs, Intel hardware, NVIDIA GPUs respectively). Require deploying and managing custom `ServingRuntime` or `ClusterServingRuntime` resources. May need specific hardware (e.g., GPUs for vLLM/Triton). Compatibility with RHOAI/KServe versions must be maintained.
- **Custom-Built Runtimes:** Provides maximum flexibility but requires significant development and maintenance effort for the runtime container image and KServe integration.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-38: Single-model serving platform (KServe) monitoring

**Architectural Question**
Will monitoring be enabled for the KServe single-model serving platform?

**Issue or Problem**
Monitoring KServe `InferenceService` deployments provides visibility into request latency, throughput, success/error rates, and resource usage. Enabling it requires User Workload Monitoring (UWM).

**Assumption**
Single-model serving platform (KServe) is enabled (RHOAI-SM-13).

**Alternatives**

- Enable KServe Monitoring via UWM
- Disable KServe Monitoring

**Decision**
#TODO#

**Justification**

- **Enable KServe Monitoring via UWM:** To collect metrics from served models and integrate them into the OpenShift Monitoring dashboard (Grafana). Crucial for understanding serving performance, identifying bottlenecks, and setting up alerts.
- **Disable KServe Monitoring:** For simpler deployment and reduced resource consumption if detailed serving metrics are not required, relying only on basic pod/deployment metrics or logs.

**Implications**

- **Enable KServe Monitoring:** Requires enabling User Workload Monitoring (UWM) in the cluster (OCP-MON-01). Consumes additional Prometheus resources for scraping and storing KServe metrics. Provides essential observability for MLOps. RHOAI typically configures KServe for scraping automatically when UWM is enabled.
- **Disable KServe Monitoring:** Reduces monitoring overhead. Limits visibility into model serving performance, making it harder to diagnose issues or optimize resource allocation for served models.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-39: NVIDIA NIM Serving Platform Integration

**Architectural Question**
Will NVIDIA NIM integration be enabled for the single-model serving platform in Red Hat OpenShift AI?

**Issue or Problem**
NVIDIA NIM provides optimized inference microservices for large language models. Enabling it impacts integration complexity and hardware dependency.

**Assumption**
NVIDIA GPU acceleration is leveraged (see RHOAI-SM-15). Single-model serving platform (KServe) is enabled (RHOAI-SM-13).

**Alternatives**

- Enable NVIDIA NIM Integration
- Rely on Standard KServe Runtime Environment

**Decision**
#TODO#

**Justification**

- **Enable NVIDIA NIM Integration:** To leverage NVIDIA's optimized microservices for deploying high-performance, large language models, maximizing GPU utilization for inference workloads.
- **Rely on Standard KServe Runtime Environment:** To use generic KServe model servers (e.g., VLLM, Triton, Caikit+TGIS) without relying on specialized NVIDIA inference components.

**Implications**

- **Enable NVIDIA NIM Integration:** Requires adherence to specific hardware and software configurations validated by NVIDIA and Red Hat. Requires access to NIM container images (NGC). Increases complexity due to integrating specialized proprietary software. Requires deploying NIM as a custom KServe runtime. May involve NVIDIA AI Enterprise licensing.
- **Rely on Standard KServe Runtime Environment:** Deployment requires less specialized integration effort; performance optimization relies solely on the chosen model server (like vLLM, Triton, Caikit) and underlying GPU Operator configuration.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-40: NVIDIA NIM Metrics

**Architectural Question**
If using NVIDIA NIM, will metrics collection be enabled for NIM-based KServe deployments?

**Issue or Problem**
Monitoring NIM-specific metrics (e.g., GPU utilization within the NIM container, inference latency) enhances visibility but requires ensuring NIM endpoints are scraped by OpenShift Monitoring (UWM).

**Assumption**
NVIDIA NIM integration is enabled (RHOAI-SM-39). User Workload Monitoring (UWM) is enabled (OCP-MON-01/RHOAI-SM-38).

**Alternatives**

- Enable NIM Metrics Collection
- Disable NIM Metrics Collection

**Decision**
#TODO#

**Justification**

- **Enable NIM Metrics Collection:** For detailed visibility into the performance and resource consumption of NIM inference servers, aiding troubleshooting and optimization.
- **Disable NIM Metrics Collection:** To reduce monitoring overhead if standard KServe/pod-level metrics are considered sufficient.

**Implications**

- **Enable NIM Metrics Collection:** Requires configuring `ServiceMonitor` or `PodMonitor` resources to target the metrics endpoint exposed by the NIM containers within the KServe `InferenceService`. May require custom annotations on KServe resources if not automatically configured. Consumes additional Prometheus resources.
- **Disable NIM Metrics Collection:** Simplifies monitoring configuration but limits insight into the internal behavior of the NIM runtime itself. Relies on higher-level KServe metrics.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-41: AMD GPU Accelerator Usage

**Architectural Question**
Will AMD GPUs be used in Red Hat OpenShift AI?

**Issue or Problem**
Enabling AMD GPUs supports high-performance AI/ML workloads using the ROCm platform but impacts hardware requirements and complexity, including limitations in disconnected environments.

**Assumption**
N/A

**Alternatives**

- Enable AMD GPU Usage (ROCm)
- Do Not Enable AMD GPU Usage

**Decision**
#TODO#

**Justification**

- **Enable AMD GPU Usage (ROCm):** To support high-performance AI/ML workloads by leveraging the AMD ROCm platform, providing an alternative accelerator option to NVIDIA or Intel.
- **Do Not Enable AMD GPU Usage:** To simplify hardware procurement and ecosystem dependency management by relying on other supported accelerators (e.g., NVIDIA, Intel, CPU).

**Implications**

- **Enable AMD GPU Usage (ROCm):** Requires installation of the AMD GPU Operator. Currently (as of RHOAI 2.x), installing the AMD GPU Operator is _not supported_ for installations in a disconnected environment due to required external dependencies. Requires compatible AMD Instinct hardware and ROCm-compatible container images/frameworks.
- **Do Not Enable AMD GPU Usage:** Limits hardware utilization to non-AMD accelerators; avoids the complexity associated with integrating the ROCm platform and the current disconnected installation limitation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## RHOAI-SM-42: Workbenches on Intel hardware

**Architectural Question**
If using Intel accelerators (e.g., Intel Data Center GPUs), will Intel-optimized workbench images be used?

**Issue or Problem**
To fully leverage Intel accelerators within workbenches, specific Intel-optimized libraries and potentially drivers (managed via an operator) are needed. Using standard images may not utilize the hardware efficiently.

**Assumption**
Intel accelerators (GPUs like Max Series, potentially others) are planned or available in some worker nodes. The Intel partner solution component might be enabled (RHOAI-SM-19).

**Alternatives**

- Use Intel-Optimized Workbench Images
- Use Standard Red Hat Workbench Images (CPU or other accelerator focus)

**Decision**
#TODO#

**Justification**

- **Use Intel-Optimized Workbench Images:** To provide data scientists with environments containing the necessary Intel libraries (e.g., oneAPI AI Analytics Toolkit, OpenVINO) for developing and testing workloads optimized for Intel hardware.
- **Use Standard Red Hat Workbench Images:** For simplicity if Intel optimization within the workbench is not a primary requirement, or if Intel hardware is not present.

**Implications**

- **Use Intel-Optimized Images:** Requires making these specific images available (either provided by Red Hat/Intel or custom-built). May necessitate installing an Intel device plugin operator (e.g., Intel Device Plugins for Kubernetes Operator) on the cluster to manage accelerator drivers and expose them to pods. Ensures workloads can leverage Intel hardware features.
- **Use Standard Images:** Simplifies image management. Workloads requiring Intel optimizations would need libraries installed at runtime or rely on CPU execution. Intel accelerators in the nodes would likely remain unused by these workbenches.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## RHOAI-SM-43: TrustyAI Monitoring for Data Science Models

**Architectural Question**
Will the TrustyAI component be enabled for monitoring model fairness and explainability?

**Issue or Problem**
TrustyAI provides advanced model monitoring capabilities beyond basic serving metrics (latency, throughput). It focuses on operationalizing AI ethics by tracking fairness metrics (e.g., disparate impact) and providing explanations for model predictions. Enabling it requires deploying the TrustyAI service and integrating it with model serving runtimes.

**Assumption**
Model serving (likely KServe, RHOAI-SM-13) is enabled.

**Alternatives**

- Enable TrustyAI Service
- Disable TrustyAI Service

**Decision**
#TODO#

**Justification**

- **Enable TrustyAI Service:** To gain insights into model fairness, identify potential biases, and generate explanations for model predictions, supporting responsible AI practices and regulatory compliance.
- **Disable TrustyAI Service:** For simpler deployment if advanced fairness and explainability monitoring are not immediate requirements, relying only on standard performance metrics (RHOAI-SM-38).

**Implications**

- **Enable TrustyAI Service:** Requires enabling the `trustyai` component in the `DataScienceCluster` CR. Deploys the TrustyAI operator and service pods, consuming additional cluster resources. Model serving runtimes (`InferenceService`s) need to be configured (often via annotations) to send prediction data to TrustyAI for analysis. Requires expertise in configuring fairness metrics and interpreting explanations.
- **Disable TrustyAI Service:** Reduces resource consumption and configuration complexity. Limits observability to standard operational metrics, lacking insights into model bias or prediction rationale.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---

## RHOAI-SM-44: Distributed Inference with LLM-D [TECH-PREVIEW]

**Architectural Question**
Will the Distributed Inference with llm-d component be used for large language model serving?

**Issue or Problem**
Using LLMs for AI/ML inference often requires significant compute resources and sharding workloads across multiple nodes, which is complex regarding scaling and recovery. `llm-d` aims to simplify this.

**Assumption**
Large language models requiring distributed processing (multi-GPU or multi-node) are planned for deployment via KServe (RHOAI-SM-13).

**Alternatives**

- Enable Distributed Inference with llm-d [TECH-PREVIEW]
- Rely on Standard KServe (Single-Instance) Deployment

**Decision**
#TODO#

**Justification**

- **Enable Distributed Inference with llm-d:** To simplify complex deployments of large language models (LLMs) by providing capabilities for sharding workloads across multiple nodes/GPUs, addressing challenges in scaling and fault recovery using this specialized framework.
- **Rely on Standard KServe (Single-Instance) Deployment:** To use the default, less complex serving mechanism where a model runs within a single KServe `InferenceService` instance (which might still use multiple GPUs on one node if configured). Suitable for models that do not require multi-node sharding.

**Implications**

- **Enable Distributed Inference with llm-d:** This is currently available as a **Technology Preview** feature and is not supported with Red Hat production SLAs. It requires specific configuration within KServe `InferenceService` definitions to utilize the `llm-d` runtime and framework. Adds complexity specific to this preview feature.
- **Rely on Standard KServe:** Limits the size and computational requirements of models that can be efficiently served from a single KServe endpoint, although KServe itself can scale replicas horizontally. Does not natively handle model sharding across multiple instances.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## RHOAI-SM-45: User/Group Dashboard Access Configuration

**Architectural Question**
How will access to the OpenShift AI dashboard be controlled based on user groups?

**Issue or Problem**
By default, any authenticated OpenShift user can access the RHOAI dashboard. A mechanism is needed to restrict access to specific administrator and standard user groups defined in OpenShift, aligning with RBAC best practices.

**Assumption**
Access to the OpenShift AI dashboard must be restricted based on OpenShift user groups. OpenShift groups are synchronized or defined (OCP-SEC-02).

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
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: MLOps Engineer
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Security Expert

---
