# OpenShift Container Platform high level overview

## OCP-BASE-1: Cluster Isolation Strategy

**Architectural Question**
How will workloads for different lifecycle stages (e.g., Dev, Test, Prod) be separated and hosted across OpenShift clusters?

**Issue or Problem**
Isolation is required for security, stability, and adherence to change control policies, balanced against the management overhead of multiple clusters.

**Assumption**
N/A

**Alternatives**

- Consolidated Cluster Model
- Prod/Non-Prod Split Model
- Per-Environment Model

**Decision**
#TODO#

**Justification**

- **Consolidated Cluster Model:** Minimizes the infrastructure footprint and simplifies cluster management by consolidating all environments into a single operational cluster.
- **Prod/Non-Prod Split Model:** Provides strong isolation between production and non-production workloads, preventing development or testing activities from impacting the production environment.
- **Per-Environment Model:** Offers maximum isolation between all environments (e.g., dev, test, UAT, prod), which is ideal for organizations with strict compliance, security, or change-control requirements for each stage.

**Implications**

- **Consolidated Cluster Model:** Requires strict enforcement of RBAC, resource quotas, and network policies to prevent interference between environments. There is a higher risk of non-production issues affecting production stability.
- **Prod/Non-Prod Split Model:** Increases infrastructure costs and management overhead compared to a single cluster. It requires a process for promoting applications and configurations between the non-production and production clusters.
- **Per-Environment Model:** Results in the highest infrastructure cost and operational complexity. Advanced multi-cluster management solutions (e.g., Red Hat Advanced Cluster Management) are strongly recommended for efficient operations.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-BASE-2: Cloud model

**Architectural Question**
Which cloud operating model will be adopted for the OpenShift platform?

**Issue or Problem**
A cloud model must be selected that aligns with the organization's strategy for infrastructure ownership, operational expenditure (OpEx) versus capital expenditure (CapEx), scalability, and data governance.

**Assumption**
N/A

**Alternatives**

- Private Cloud Model
- Public Cloud Model
- Hybrid Cloud Model

**Decision**
#TODO#

**Justification**

- **Private Cloud Model:** Leverages existing data center investments, provides maximum control over the hardware and network stack, and can help meet strict data sovereignty or residency requirements.
- **Public Cloud Model:** Offers rapid provisioning, on-demand scalability, a pay-as-you-go pricing model (OpEx), and offloads the management of physical infrastructure.
- **Hybrid Cloud Model:** Provides the flexibility to run workloads in the most suitable environment, balancing cost, performance, security, and features between private and public clouds.

**Implications**

- **Private Cloud Model:** The organization is fully responsible for infrastructure capacity planning, maintenance, power, cooling, and networking. Lead times for new hardware can be long. This is a CapEx-intensive model.
- **Public Cloud Model:** Incurs ongoing operational expenses tied to usage. It requires expertise in the specific cloud provider's services, security models, and cost management.
- **Hybrid Cloud Model:** Introduces complexity in network connectivity (e.g., VPN, Direct Connect) and management across different environments. Multi-cluster management tools are essential for a unified operational view.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-BASE-3: Platform infrastructure

**Architectural Question**
On which specific infrastructure platform(s) will OpenShift Container Platform be installed?

**Issue or Problem**
The choice of underlying infrastructure platform directly impacts the available installation methods, supported features, operational complexity, performance characteristics, and required team skill sets. More than one platform can be selected.

**Assumption**
N/A

**Alternatives**

- AWS
- Azure
- Google Cloud Platform (GCP)
- IBM Cloud
- VMware vSphere
- Red Hat OpenStack Platform
- Nutanix
- Bare Metal (x86, IBM Power, IBM Z)
- AWS Outposts
- Azure Stack Hub
- Any non-tested by Red Hat platforms

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**
The choice of platform is driven by factors such as existing enterprise agreements, strategic partnerships, or specific technical capabilities. Officially supported platforms are recommended for stability and access to support. Non-tested platforms may be considered to leverage unique or legacy hardware but carry inherent risks. A multi-platform approach is used to place workloads on the most suitable infrastructure based on business or technical needs.

**Implications**
Each platform has unique integration points, operational requirements, and cost structures. The chosen platform(s) will determine the available installation methods and the necessary skill sets. Using a non-tested platform means the organization assumes all risks related to support, compatibility, and upgrades, as Red Hat support will be on a best-effort basis. Selecting multiple platforms increases management complexity and necessitates robust multi-cluster management tools.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-4: Multi-Site Deployment Strategy (On-Premises)

**Architectural Question**
For on-premises deployments spanning multiple physical sites (datacenters, regions), what high-level cluster distribution strategy will be used for disaster recovery?

**Issue or Problem**
A strategy is needed to ensure platform and application availability in the event of a complete site failure. This involves deciding between stretching a single cluster across sites or deploying independent clusters per site.

**Assumption**
An on-premises deployment across multiple physical sites is planned. Disaster recovery across sites is a requirement.

**Alternatives**

- Stretched Cluster Across Sites
- Multi-Cluster (Independent Cluster per Site)

**Decision**
#TODO: Document the decision.#

**Justification**

- **Stretched Cluster Across Sites:** Attempts to provide automated high availability for applications within a single logical cluster construct spanning multiple sites, managed from one control plane. **Note:** This often requires specialized infrastructure, very low latency, and carries significant complexity and risk.
- **Multi-Cluster (Independent Cluster per Site):** Deploys separate, independent OpenShift clusters in each site. Each cluster is a distinct failure domain at the site level. This simplifies cluster operations, reduces the blast radius of a site failure, and aligns with standard Kubernetes practices. This is the generally recommended approach for resilience.

**Implications**

- **Stretched Cluster:** **Strictly requires extremely low latency (typically < 5-10ms round-trip, depending on components like etcd and storage)** and high-bandwidth, reliable network connectivity between sites. Complex to design, implement, and operate. Failure in the interconnecting network or one site can severely impact the _entire_ stretched cluster (split-brain scenarios). May require specialized storage replication if stretching stateful workloads.
- **Multi-Cluster:** Requires a strategy for deploying applications to multiple clusters (e.g., using GitOps with tools like Argo CD or Red Hat Advanced Cluster Management - RHACM). Disaster recovery and failover become application-level concerns (e.g., using DNS load balancing like Global Load Balancing, application-level replication, or DR orchestration tools like ODF Regional-DR). Increases management overhead compared to a single cluster construct but provides superior site-level fault isolation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-5: Intra-Site Availability Zone / Failure Domain Strategy

**Architectural Question**
Within a single site or region, how will OpenShift cluster nodes (Control Plane, Compute) be distributed across available Availability Zones (AZs) or Failure Domains (FDs) for high availability?

**Issue or Problem**
To maintain cluster availability during infrastructure failures _within_ a site (e.g., rack failure, server group outage, cloud provider AZ issue), critical cluster components, especially control plane nodes, must be spread across distinct failure domains.

**Assumption**
The deployment site/region provides multiple Availability Zones or Failure Domains (e.g., at least 3 distinct physical racks, server groups, vSphere clusters, or cloud AZs). High availability _within_ the site/region is required.

**Alternatives**

- Single AZ/FD Deployment (No HA)
- Two AZ/FD Deployment (Asymmetric, Limited HA)
- Three or More AZ/FD Deployment (Recommended HA)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Single AZ/FD Deployment:** To deploy all cluster nodes within a single failure domain. Simplest deployment but offers no protection against AZ/FD-level failures. Suitable only for non-critical environments (e.g., temporary dev/test).
- **Two AZ/FD Deployment:** To spread nodes across two failure domains. While better than one, this offers limited and often asymmetric HA. Control plane quorum can be challenging, and recovery from a full AZ/FD failure might be impaired or require manual intervention. Not typically recommended for production control planes. Compute nodes can sometimes be split this way if application HA allows.
- **Three or More AZ/FD Deployment:** To distribute Control Plane nodes across three distinct failure domains (the minimum required for robust etcd quorum and automated control plane recovery). Compute nodes can also be spread across these three (or more) zones. This provides the standard and recommended level of high availability against infrastructure failures within a site/region.

**Implications**

- **Single AZ/FD:** A failure impacting that zone (power, network, cooling, cloud AZ issue) results in a complete cluster outage.
- **Two AZ/FD:** Control plane may not survive a full AZ/FD failure gracefully due to etcd quorum requirements (2 out of 3 needed). Recovery might be complex. Compute node availability is reduced by 50% during an AZ failure.
- **Three or More AZ/FD:** Control plane can automatically survive the failure of a single AZ/FD. Compute capacity loss is limited to the proportion of nodes in the failed zone (e.g., 33% loss for a 3-AZ deployment). Requires the underlying infrastructure to provide at least three independent zones with sufficient resources in each. May introduce negligible inter-AZ network latency.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert (re: inter-AZ latency/connectivity)
- Person: #TODO#, Role: Storage Expert (re: storage availability across zones)

---

## OCP-BASE-6: Network Connectivity Model

**Architectural Question**
Will the OpenShift cluster be deployed in an environment with direct internet access or a highly restricted (air-gapped) network?

**Issue or Problem**
The connectivity model dictates how the cluster performs installation, access updates (Over-The-Air or mirrored), and consumes Operators from Red Hat registries.

**Assumption**
N/A

**Alternatives**

- Connected Environment
- Disconnected (Air-Gapped) Environment

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Connected Environment:** This is the simplest and recommended method. It allows direct access to Red Hat's registries and services, which streamlines installation, upgrades, and access to the OperatorHub catalog.
- **Disconnected (Air-Gapped) Environment:** This model is necessary for environments with strict security policies that forbid any connection to the public internet, common in government, finance, or critical infrastructure sectors.

**Implications**

- **Connected Environment:** Requires careful configuration of firewalls and HTTP/S proxies to ensure that outbound traffic is secure and compliant with corporate policy.
- **Disconnected (Air-Gapped) Environment:** Requires the setup, maintenance, and regular synchronization of a mirror registry. The process for performing cluster upgrades and importing new software is significantly more complex and manual.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-BASE-7: Cluster Topology/Sizing

**Architectural Question**
What OpenShift topology should be deployed based on resource availability, HA requirements, and scale?

**Issue or Problem**
Selecting the cluster topology determines the minimum node count, control plane resilience, resource usage efficiency, and suitability for specific use cases (e.g., edge).

**Assumption**
N/A

**Alternatives**

- Standard Topology (Dedicated Control Plane Nodes)
- Compact Topology (Combined Control Plane/Worker Nodes)
- Single Node OpenShift (SNO)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Standard Topology:** Recommended for production-grade, highly available clusters handling significant workloads. Provides clear separation between control plane and compute resources, enhancing stability and simplifying resource management. Requires dedicated control plane nodes (typically 3).
- **Compact Topology:** Used for resource-constrained environments (e.g., smaller edge sites, labs) that still require Control Plane HA but aim for a smaller node footprint. Control plane components run on worker nodes (minimum 3 nodes total).
- **Single Node OpenShift (SNO):** Chosen for far edge, disconnected, or minimal footprint deployments where high availability is explicitly _not_ a requirement for the cluster itself. Runs all control plane and worker components on a single node.

**Implications**

- **Standard Topology:** **Highest minimum resource requirement** (typically 3 control plane + >=2 compute nodes = 5+ nodes). Provides **full high availability and isolation for the control plane**. Best performance and scalability characteristics.
- **Compact Topology:** Reduced footprint (minimum 3 nodes total). The **control plane is co-located with workloads**, increasing the risk of resource contention impacting control plane stability. Suitable where node count is a primary constraint.
- **Single Node OpenShift (SNO):** Minimal footprint (1 node). Provides **no cluster-level high availability**; a failure of the single node results in a complete cluster outage. Suitable only for specific edge use cases or scenarios where workloads handle their own HA externally.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-8: Mirrored images registry (Disconnected Environments)

**Architectural Question**
In a disconnected environment, which mirrored images registry solution will be used to provide required container images to the cluster?

**Issue or Problem**
In a disconnected or restricted network environment, the cluster cannot access external Red Hat registries. A local mirror registry is required to store all necessary Red Hat software (release images, operator catalogs, related images) for installation and updates.

**Assumption**
Environment is disconnected or restricted network (air gap) (as decided in OCP-BASE-6).

**Alternatives**

- Filesystem-based Mirror (using `oc mirror` or `oc adm release mirror`)
- Dedicated Mirror Registry Server (e.g., Quay, Nexus, Artifactory)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Filesystem-based Mirror:** To use the `oc mirror` (preferred) or legacy `oc adm release mirror` tooling to create a simple, filesystem-based mirror or push directly to a basic registry. Suitable for mirroring just the essential OpenShift software and is the minimum requirement. Can be hosted on a web server or simple registry.
- **Dedicated Mirror Registry Server:** To leverage a full-featured, potentially HA registry (e.g., Quay, Nexus, Artifactory) already part of the enterprise infrastructure or deployed specifically for this purpose. This registry serves as the single source of truth for both mirrored Red Hat software and internally-built application images (see OCP-MGT-03).

**Implications**

- **Filesystem-based Mirror:** Primarily designed for Red Hat content. Not a full-featured registry (lacks UI, advanced RBAC, scanning unless paired with one). Simpler initial setup for mirroring core content but less suitable for hosting application images. Requires manual synchronization process.
- **Dedicated Mirror Registry Server:** Often the preferred enterprise approach. Requires ensuring the chosen registry can host the required Red Hat content format (e.g., Operator catalogs) and handle the mirroring synchronization process. Leverages existing HA, security, and management features of the enterprise registry.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

## OCP-BASE-9: Platform Installation and Upgrade Automation Strategy

**Architectural Question**
What strategy or tooling will be used for automating the installation and ongoing upgrades of OpenShift Container Platform clusters?

**Issue or Problem**
Manual processes for cluster installation and upgrades are error-prone, time-consuming, and do not scale effectively, particularly in multi-cluster or production environments. An automation strategy is crucial for ensuring consistency, speed, reliability, and reducing operational burden throughout the cluster lifecycle.

**Assumption**
Clusters need to be installed and upgraded consistently and reliably. Multi-cluster deployments might be planned or exist, requiring scalable management.

**Alternatives**

- Manual Installation / Upgrades
- In-house Automation Solution (e.g., Ansible, Terraform)
- Red Hat Advanced Cluster Management (ACM)

**Decision**
#TODO: Document the decision.#

**Justification**

- **Manual Installation / Upgrades:** To use the standard `openshift-install` CLI and manual upgrade procedures via the console or CLI. This is the baseline approach, often used for initial single-cluster deployments, proofs-of-concept, or learning. No additional tooling dependencies.
- **In-house Automation Solution (e.g., Ansible, Terraform):** To leverage existing organizational expertise and investments in automation tools like Ansible or Terraform to script and manage the installation (often wrapping `openshift-install` or interacting with provider APIs) and potentially parts of the upgrade process. Allows for deep customization and integration with existing CI/CD or GitOps workflows.
- **Red Hat Advanced Cluster Management (ACM):** To adopt Red Hat's strategic multi-cluster management platform. ACM provides comprehensive lifecycle management features, including automated cluster provisioning (using Hive API) across various infrastructures (cloud, on-prem), centralized policy enforcement, observability, and application deployment across the entire fleet. It also facilitates coordinated cluster upgrades. Recommended for managing clusters at scale.

**Implications**

- **Manual Installation / Upgrades:** High operational overhead, especially for multiple clusters. Increased risk of human error leading to inconsistent configurations or failed upgrades. Difficult to scale operations. Slow rollout and upgrade velocity. Not suitable for managing production fleets.
- **In-house Automation Solution:** Requires significant effort to develop, test, and maintain the custom automation code/playbooks/modules. The reliability and effectiveness depend heavily on the quality of the automation and the internal team's expertise. Needs adaptation and maintenance for different infrastructure targets and OCP versions.
- **Red Hat Advanced Cluster Management (ACM):** Requires installing, configuring, and managing the ACM Hub cluster infrastructure. Incurs ACM subscription costs. Provides a powerful, unified control plane for fleet management but introduces a dependency on ACM and requires learning its specific concepts (Policies, Managed Clusters, Hive, Placement Rules, etc.). Significantly streamlines installation, upgrades, and governance across multiple clusters and diverse infrastructures.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader
