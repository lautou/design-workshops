# OpenShift Container Platform High-Level Strategy

## OCP-BASE-01: Cluster Isolation Strategy

**Architectural Question**
How will workloads for different lifecycle stages (e.g., Dev, Test, Prod) be separated and hosted across OpenShift clusters?

**Issue or Problem**
Isolation is required for security, stability, and adherence to change control policies, balanced against the management overhead of multiple clusters

**Assumption**
N/A

**Alternatives**

- Consolidated Cluster Model
- Prod/Non-Prod Split Model
- Per-Environment Model

**Decision**
#TODO#

**Justification**

- **Consolidated Cluster Model:** Minimizes the infrastructure footprint and simplifies cluster management by consolidating all environments (Dev, Test, Prod) into a single operational cluster. This minimizes cost but requires reliance on OpenShift Namespaces/Projects, ResourceQuotas, NetworkPolicy, and RBAC for isolation.
- **Prod/Non-Prod Split Model:** Provides strong isolation between production and non-production workloads, preventing development or testing activities from impacting the production environment. This is often a minimum compliance requirement.
- **Per-Environment Model:** Offers maximum isolation between all environments (e.g., dev, test, UAT, prod), which is ideal for organizations with strict compliance, security, or change-control requirements for each stage, incurring maximum management overhead.

**Implications**

- **Consolidated Cluster Model:** Increased risk of resource contention ("noisy neighbors") and Single Point of Failure (SPoF) impacting all environments if a critical component or underlying infrastructure service fails.
- **Prod/Non-Prod Split Model:** Requires managing at least two separate clusters, increasing infrastructure and operational costs.
- **Per-Environment Model:** Highest operational overhead due to managing multiple, smaller clusters, but offers the clearest path to strict regulatory compliance and failure domain separation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-BASE-02: Cloud model

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

## OCP-BASE-03: Platform infrastructure

**Architectural Question**
On which specific infrastructure platform(s) will OpenShift Container Platform be installed?

**Issue or Problem**
The choice of underlying infrastructure platform directly impacts the available installation methods, supported features, operational complexity, performance characteristics, and required team skill sets. More than one platform can be selected.

**Assumption**
N/A

**Alternatives**

- Public Cloud Managed (ROSA/ARO/OSD)
- Self-Managed Public Cloud (AWS, Azure, GCP, OCI)
- Bare Metal / On-Premise Virtualized (vSphere, OpenStack, Bare Metal)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Public Cloud Managed (ROSA/ARO/OSD):** Leverages fully automated installation and relies on Red Hat and/or the cloud vendor for control plane management. Simplifies Day 2 operations but limits customization.
- **Self-Managed Public Cloud (AWS, Azure, GCP, OCI):** Allows for Installer-Provisioned Infrastructure (IPI) for maximum integration with cloud services (Load Balancers, Storage) or User-Provisioned Infrastructure (UPI) for flexibility.
- **Bare Metal / On-Premise Virtualized (vSphere, OpenStack, Bare Metal):** Provides full hardware control and optimization potential. Requires use of UPI, Assisted Installer, or Agent-based Installer (ABI), relying on internal virtualization or hardware expertise.

**Implications**

- **Public Cloud Managed (ROSA/ARO/OSD):** Reduces administrative overhead for underlying infrastructure components. Installation methods are limited to the managed service offering.
- **Self-Managed Public Cloud (AWS, Azure, GCP, OCI):** IPI mode abstracts infrastructure management via the Machine API, simplifying cluster scaling and node lifecycle. Requires cloud credentials and IAM setup.
- **Bare Metal / On-Premise Virtualized (vSphere, OpenStack, Bare Metal):** Requires cluster administrators to manually manage or pre-provision all underlying infrastructure components (networking, storage, VMs/hosts).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-04: Cluster Topology

**Architectural Question**
What OpenShift topology should be deployed based on resource availability, HA requirements, and scale for each cluster?

**Issue or Problem**
Selecting the cluster topology determines the minimum node count, control plane resilience, resource usage efficiency, and suitability for specific use cases (e.g., edge). This choice impacts HA capabilities within a site and influences multi-site strategies.

**Assumption**
N/A

**Alternatives**

- Standard Topology (3+ Control Plane, 3+ Workers)
- Compact Topology (3 Control Plane/Workers)
- Single Node OpenShift (SNO)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Standard HA (3+ Control Plane, N Workers):** Provides maximum resilience, scalability, and performance isolation by separating control plane functions from application workloads onto dedicated worker nodes. Recommended for large or general-purpose production clusters.
- **Compact HA (3 Combined Control/Worker):** Reduces the hardware footprint and minimizes network latency between control and worker planes by running all roles on three nodes. Suitable for smaller production environments that require high availability but have resource constraints.
- **Single Node OpenShift (SNO):** Ideal for edge computing workloads, portable clouds, and environments with intermittent connectivity or severe resource constraints, such as 5G radio access networks (RAN).

**Implications**

- **Standard HA (3+ Control Plane, N Workers):** Requires a minimum of 6 nodes (3 control plane, 3 worker) for production environments, increasing infrastructure costs.
- **Compact HA (3 Combined Control/Worker):** Infrastructure components (monitoring, registry, ingress) often share resources with the control plane, requiring careful sizing and potentially dedicated infrastructure nodes (infra nodes) for production scale workloads.
- **Single Node OpenShift (SNO):** The major tradeoff is the **lack of high availability**, as failure of the single node stops the cluster.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-05: Disaster recovery site strategy

**Architectural Question**
What strategy will be adopted to ensure platform and application availability in the event of a complete site failure, considering the chosen cluster topology?

**Issue or Problem**
A strategy is needed to ensure platform and application availability in the event of a complete site failure, considering the chosen cluster topology.

**Assumption**
An on-premises deployment across multiple physical sites is planned or considered. Disaster recovery across sites is a requirement. The Cluster Topology (OCP-BASE-04) has been considered.

**Alternatives**

- Stretched Cluster Across Sites (Topology Permitting)
- Multi-Cluster (Independent Cluster per Site)

**Decision**
#TODO: Document the decision.#

**Justification**

- **Stretched Cluster Across Sites (Topology Permitting):** Provides low Recovery Point Objective (RPO)/Recovery Time Objective (RTO) by running a single control plane spanning two sites. Requires very low latency and high bandwidth between sites to maintain etcd quorum.
- **Multi-Cluster (Independent Cluster per Site):** Uses independent clusters in geographically separated sites, leveraging asynchronous replication (e.g., ODF Regional-DR [25]) or application-level deployment tools to manage failover. Recommended when site latency is high [4].

**Implications**

- **Stretched Cluster Across Sites (Topology Permitting):** High dependence on ultra-low latency networking. Failures often require coordinated remediation across both sites. Not suitable for environments subject to high latency or jitter.
- **Multi-Cluster (Independent Cluster per Site):** Higher RPO/RTO than a stretched cluster, but offers greater isolation between failures. Requires managing two distinct cluster control planes.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-06: Intra-Site Availability Zone / Failure Domain Strategy

**Architectural Question**
Within a single site or region, how will OpenShift cluster nodes (Control Plane, Compute) be distributed across available Availability Zones (AZs) or Failure Domains (FDs) for high availability?

**Issue or Problem**
Lack of distribution across failure domains can lead to a Single Point of Failure (SPoF) if a physical location, rack, or infrastructure zone experiences an outage, impacting the control plane (etcd) quorum and worker node availability.

**Assumption**
N/A

**Alternatives**

- Single AZ/FD Deployment (No HA)
- Two AZ/FD Deployment (Limited HA, Not Recommended for Control Plane)
- Three or More AZ/FD Deployment (Recommended HA for Standard/Compact)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Single Failure Domain (No AZ/FD separation):** Simplifies network planning and latency management since all nodes reside in one logical or physical area. However, this subjects the entire cluster to a site-wide or rack-level outage event.
- **Multi-Availability Zone / Failure Domain (Cluster-spanning HA):** Provides maximum resilience by ensuring the control plane's etcd quorum members and worker nodes are distributed across physically isolated domains. This is the preferred approach for production clusters.

**Implications**

- **Single Failure Domain (No AZ/FD separation):** Significantly increases the risk of a Single Point of Failure (SPoF) for OpenShift infrastructure services and the cluster state (etcd).
- **Multi-Availability Zone / Failure Domain (Cluster-spanning HA):** Requires careful network design to manage inter-AZ latency, especially for the control plane (etcd). Requires that the underlying platform supports multiple availability zones/failure domains.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Storage Expert

---

## OCP-BASE-07: Network Connectivity Model

**Architectural Question**
Will the OpenShift cluster be deployed in an environment with direct internet access or a highly restricted (air-gapped) network?

**Issue or Problem**
The connectivity model dictates how installation files, container images, and cluster updates are sourced, impacting initial complexity and ongoing operational tooling.

**Assumption**
N/A

**Alternatives**

- Connected (Direct Internet Access)
- Disconnected (Restricted/Air-Gapped Network)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Connected (Direct Internet Access):** Enables simplified installation and uses the OpenShift Update Service (OSUS) to provide over-the-air updates and update recommendations directly from Red Hat.
- **Disconnected (Restricted/Air-Gapped Network):** Required for environments with high security constraints or lack of external network access. Requires establishing a mirroring process to synchronize content from the public Red Hat repositories to a local registry.

**Implications**

- **Connected (Direct Internet Access):** Requires stable internet access for all nodes and adherence to firewall egress rules for Red Hat endpoints.
- **Disconnected (Restricted/Air-Gapped Network):** Significantly increases installation complexity and requires dedicated mirroring infrastructure. For hosted control planes, the ImageContentSourcePolicy (ICSP) for the data plane is managed via the ImageContentSources API.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BASE-08: Mirrored images registry (Disconnected Environments)

**Architectural Question**
In a disconnected environment, which mirrored images registry solution will be used to provide required container images to the cluster?

**Issue or Problem**
In a disconnected environment, the cluster needs access to Red Hat software (release images, operators) via a local mirror registry for installation and updates.

**Assumption**
Environment is disconnected (as decided in OCP-BASE-07).

**Alternatives**

- Filesystem-based Mirror (using `oc mirror` or `oc adm release mirror`)
- Dedicated Mirror Registry Server (e.g., Quay, Nexus, Artifactory)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Filesystem-based Mirror:** Uses oc mirror (preferred) to create a simple mirror (filesystem or basic registry push). Minimum requirement for mirroring essential OCP software.
- **Dedicated Mirror Registry Server:** Leverages a full-featured registry (existing or new) as the single source for both mirrored Red Hat content and internal application images. This is the preferred enterprise approach.

**Implications**

- **Filesystem-based Mirror:** Primarily for Red Hat content, not a full registry (no UI, advanced RBAC, scanning unless paired). Simpler setup for core content, less suitable for applications. Requires manual sync.
- **Dedicated Mirror Registry Server:** Preferred enterprise approach. Requires ensuring the registry supports OCP content formats (Operator catalogs) and the mirroring process. Leverages existing HA, security, and management features.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Operations Expert

---

## OCP-BASE-09: Platform Installation and Upgrade Automation Strategy

**Architectural Question**
What strategy or tooling will be used for automating the installation and ongoing upgrades of OpenShift Container Platform clusters?

**Issue or Problem**
Manual installation and upgrade processes are prone to human error, lead to configuration drift, and do not scale effectively for a fleet of clusters.

**Assumption**
N/A

**Alternatives**

- Manual Execution (CLI/Web Console)
- Automated Provisioning (IPI/Agent/Assisted)
- Centralized GitOps Orchestration [TECH-PREVIEW]

**Decision**
#TODO: Document the decision.#

**Justification**

- **Manual Execution (CLI/Web Console):** Suitable for highly customized, one-off deployments (UPI) or initial test environments, giving granular control over every step. Does not scale well.
- **Automated Provisioning (IPI/Agent/Assisted):** Leverages the `openshift-install` program or Assisted Installer to deploy the cluster and utilize the Cluster Version Operator (CVO) and Machine Config Operator (MCO) for post-install Day 2 management and rolling upgrades.
- **Centralized GitOps Orchestration:** Leverages Red Hat Advanced Cluster Management (RHACM) and GitOps Zero Touch Provisioning (ZTP) to manage the entire lifecycle of a fleet of clusters declaratively from a single source of truth (Git).

**Implications**

- **Manual Execution (CLI/Web Console):** High reliance on human expertise; difficult to repeat reliably.
- **Automated Provisioning (IPI/Agent/Assisted):** Requires robust platform credentials for IPI, or careful network/ignition setup for UPI/Agent-based. Post-install upgrades are automated via CVO/MCO.
- **Centralized GitOps Orchestration:** Requires a separate hub cluster running RHACM. Configuration is complex initially but provides scalable, declarative management for hundreds of clusters.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-10: Cluster Sizing Strategy

**Architectural Question**
What is the methodology for determining the required size (node count, CPU, RAM, GPU types/counts, storage capacity) for control plane, infrastructure, and worker nodes for each OpenShift cluster?

**Issue or Problem**
Under-sizing leads to stability problems, resource exhaustion, and application degradation. Over-sizing leads to unnecessary infrastructure costs and poor utilization.

**Assumption**
N/A

**Alternatives**

- Rule-of-Thumb / Default Minimum
- Application Load-Based Capacity Planning
- Dynamic Scaling with MachineSets

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Rule-of-Thumb / Default Minimum:** Uses standard Red Hat recommendations (e.g., 3 control plane nodes, specific RAM/CPU minimums). This minimizes planning time and ensures the cluster meets basic stability criteria.
- **Application Load-Based Capacity Planning:** Methodology based on modeling peak resource demand and application performance requirements (e.g., latency, throughput, anticipated number of pods). The OpenShift Cluster Capacity Tool can assist in estimating pod density limits.
- **Dynamic Scaling with MachineSets:** Defines minimum and maximum boundaries and relies on the Cluster Autoscaler (based on Machine API/MachineSets) to automatically adjust the number of worker nodes based on real-time application demand.

**Implications**

- **Rule-of-Thumb / Default Minimum:** May result in significant over- or under-provisioning if application requirements deviate greatly from average assumptions.
- **Application Load-Based Capacity Planning:** High upfront effort in modeling and prediction, but results in optimized resource utilization and capacity guarantees.
- **Dynamic Scaling with MachineSets:** Only applicable on platforms supporting the Machine API (e.g., cloud platforms, bare metal IPI). Requires defining cloud provider credentials and managing MachineSet resource definitions.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert
