# OpenShift Container Platform High-Level Strategy

## OCP-BASE-01: Cluster Isolation Strategy

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

## OCP-BASE-04: Cluster Topology

**Architectural Question**
What OpenShift topology should be deployed based on resource availability, HA requirements, and scale for each cluster?

**Issue or Problem**
Selecting the cluster topology determines the minimum node count, control plane resilience, resource usage efficiency, and suitability for specific use cases (e.g., edge). This choice impacts HA capabilities within a site and influences multi-site strategies.

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

- **Standard Topology:** **Highest minimum resource requirement** (typically 3 control plane + >=2 compute nodes = 5+ nodes). Provides **full high availability and isolation for the control plane**. Best performance and scalability characteristics. Supports robust multi-site and intra-site HA strategies.
- **Compact Topology:** Reduced footprint (minimum 3 nodes total). The **control plane is co-located with workloads**, increasing the risk of resource contention impacting control plane stability. Supports intra-site HA but stretching across sites is complex/risky.
- **Single Node OpenShift (SNO):** Minimal footprint (1 node). Provides **no cluster-level high availability**. Cannot be stretched. Multi-site strategy relies purely on deploying independent SNO nodes.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-05: Multi-Site Deployment Strategy (On-Premises)

**Architectural Question**
For on-premises deployments spanning multiple physical sites (datacenters, regions), what high-level cluster distribution strategy will be used for disaster recovery?

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

- **Stretched Cluster Across Sites:** Attempts to provide automated high availability within a single logical cluster spanning sites. **Only feasible with Standard or potentially Compact topologies** and requires specialized infrastructure, very low latency (< 5-10ms RTT), and carries significant complexity/risk. Not possible with SNO.
- **Multi-Cluster (Independent Cluster per Site):** Deploys separate, independent OpenShift clusters in each site, regardless of topology (Standard, Compact, or SNO). Each cluster is a distinct failure domain. Simplifies cluster operations, reduces blast radius, aligns with standard Kubernetes practices. Generally recommended for resilience.

**Implications**

- **Stretched Cluster:** **Strict latency/bandwidth requirements**. Complex design, operation, and potential failure modes (split-brain). May require specialized storage replication. Not applicable if SNO topology is used.
- **Multi-Cluster:** Requires a strategy for deploying applications to multiple clusters (GitOps, RHACM). DR and failover become application-level concerns (DNS GSLB, app replication, ODF Regional-DR). Increases management overhead compared to a single cluster but offers superior site-level fault isolation and works with any topology.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-06: Intra-Site Availability Zone / Failure Domain Strategy

**Architectural Question**
Within a single site or region, how will OpenShift cluster nodes (Control Plane, Compute) be distributed across available Availability Zones (AZs) or Failure Domains (FDs) for high availability?

**Issue or Problem**
To maintain cluster availability during infrastructure failures _within_ a site (e.g., rack failure, PDU failure, network switch failure), critical components (especially control plane nodes for Standard/Compact topologies) must be spread across distinct failure domains.

**Assumption**
The deployment site/region provides multiple Availability Zones or Failure Domains (e.g., >=3 distinct physical racks, server groups, vSphere clusters, or cloud AZs). High availability _within_ the site/region is required (unless SNO topology was chosen).

**Alternatives**

- Single AZ/FD Deployment (No HA)
- Two AZ/FD Deployment (Limited HA, Not Recommended for Control Plane)
- Three or More AZ/FD Deployment (Recommended HA for Standard/Compact)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Single AZ/FD Deployment:** Simplest deployment but offers no protection against AZ/FD-level failures. Only suitable for non-critical environments or SNO topology.
- **Two AZ/FD Deployment:** Offers limited HA. Control plane quorum is challenging for Standard/Compact. Recovery may require manual intervention. Not recommended for production control planes.
- **Three or More AZ/FD Deployment:** **Required for robust HA with Standard or Compact topologies.** Distributes Control Plane nodes across three distinct failure domains for etcd quorum and automated recovery. Compute nodes are also spread across these zones. Provides the standard level of high availability against infrastructure failures within a site.

**Implications**

- **Single AZ/FD:** A failure impacting that zone results in a complete cluster outage (unless SNO).
- **Two AZ/FD:** Control plane may not survive a full AZ/FD failure gracefully (Standard/Compact). Compute availability reduced by 50%.
- **Three or More AZ/FD:** Control plane (Standard/Compact) can automatically survive a single AZ/FD failure. Compute capacity loss is limited (e.g., 33% for 3 AZs). Requires infrastructure to provide >=3 independent zones. Negligible inter-AZ network latency is assumed.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Network Expert (re: inter-AZ latency/connectivity)
- Person: #TODO#, Role: Storage Expert (re: storage availability across zones)

---

## OCP-BASE-07: Network Connectivity Model

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

- **Connected Environment:** Simplest method. Allows direct access to Red Hat's registries/services, streamlining installation, upgrades, and OperatorHub access.
- **Disconnected (Air-Gapped) Environment:** Necessary for environments with strict security policies forbidding public internet connections (gov, finance, critical infra).

**Implications**

- **Connected Environment:** Requires careful firewall and proxy configuration for secure outbound traffic.
- **Disconnected (Air-Gapped) Environment:** Requires setup, maintenance, and synchronization of a mirror registry. Installation, upgrades, and software import are significantly more complex.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert

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

- **Filesystem-based Mirror:** Uses `oc mirror` (preferred) or legacy tools to create a simple mirror (filesystem or basic registry push). Minimum requirement for mirroring essential OCP software.
- **Dedicated Mirror Registry Server:** Leverages a full-featured registry (existing or new) as the single source for both mirrored Red Hat content and internal application images (see OCP-MGT-03).

**Implications**

- **Filesystem-based Mirror:** Primarily for Red Hat content, not a full registry (no UI, advanced RBAC, scanning unless paired). Simpler setup for core content, less suitable for apps. Requires manual sync.
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
Manual cluster installation/upgrades are error-prone, slow, and don't scale, especially for multi-cluster or production environments. Automation is crucial for consistency, speed, reliability, and reducing operational burden.

**Assumption**
Clusters need consistent, reliable installation and upgrades. Multi-cluster management may be required.

**Alternatives**

- Manual Installation / Upgrades (`openshift-install`, Console/CLI)
- In-house Automation Solution (e.g., Ansible, Terraform wrappers)
- Red Hat Advanced Cluster Management (ACM)

**Decision**
#TODO: Document the decision.#

**Justification**

- **Manual Installation / Upgrades:** Baseline approach using standard tools. Suitable for initial single clusters, PoCs, or learning. No extra tool dependencies.
- **In-house Automation Solution:** Leverages existing automation expertise (Ansible, Terraform) to script installation/upgrades. Allows deep customization and integration with existing workflows.
- **Red Hat Advanced Cluster Management (ACM):** Red Hat's strategic multi-cluster platform. Provides comprehensive lifecycle management (automated provisioning via Hive, upgrades), policy enforcement, observability, and application deployment across the fleet. Recommended for managing clusters at scale.

**Implications**

- **Manual:** High operational overhead, risk of human error, inconsistent configurations, slow velocity. Not suitable for production fleets.
- **In-house Automation:** Requires significant development, testing, and maintenance of custom automation. Reliability depends on internal expertise. Needs adaptation for different infrastructures/OCP versions.
- **Red Hat Advanced Cluster Management (ACM):** Requires ACM Hub cluster infrastructure and ACM subscription. Provides powerful unified control but introduces dependency on ACM and its concepts (Policies, Hive, Placements). Streamlines fleet management significantly.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-BASE-10: Cluster Sizing Strategy (New AD)

**Architectural Question**
What is the methodology for determining the required size (node count, CPU, RAM, GPU types/counts, storage capacity) for control plane, infrastructure, and worker nodes for each OpenShift cluster?

**Issue or Problem**
Accurate sizing is critical for performance, stability, cost-effectiveness, and meeting workload requirements (like RHOAI). Under-sizing leads to performance issues, while over-sizing wastes resources. A consistent strategy is needed, considering different node roles and specialized hardware (GPUs).

**Assumption**
Cluster topology (OCP-BASE-04) and primary workloads (e.g., RHOAI) are known. Initial estimates for workload resource needs are available or need to be gathered.

**Alternatives**

- T-Shirt Sizing (Small, Medium, Large presets based on rough estimates)
- Workload-Driven Sizing (Detailed analysis of application/platform resource needs)
- Iterative Sizing (Start with estimate, monitor, and adjust based on actual usage)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **T-Shirt Sizing:** Provides a quick, simplified approach for initial estimates or standardized environments. Easier to manage but less precise.
- **Workload-Driven Sizing:** Most accurate approach, involving detailed analysis of expected resource consumption (CPU, RAM, GPU VRAM, network IO, storage IOPS/throughput) for platform components (monitoring, logging, registry, ODF, RHOAI control plane) and key applications/workloads (RHOAI workbenches, training jobs, model serving). Requires significant upfront effort.
- **Iterative Sizing:** Practical approach combining initial estimates (T-Shirt or basic Workload-Driven) with robust monitoring (OCP-MON-01) post-deployment to identify bottlenecks and adjust node counts/sizes based on real-world usage patterns. Allows starting smaller and scaling as needed.

**Implications**

- **T-Shirt Sizing:** High risk of under or over-provisioning if estimates are inaccurate. May require significant adjustments later.
- **Workload-Driven Sizing:** Requires deep understanding of application performance characteristics and platform overhead. Effort-intensive analysis phase. Provides the most accurate initial deployment size.
- **Iterative Sizing:** Requires strong monitoring capabilities and operational processes for scaling nodes/resources. Allows optimizing resource usage over time but might involve periods of sub-optimal performance before adjustments are made. This is often the most realistic approach for complex platforms like RHOAI. Sizing needs to account for Control Plane (3 nodes for Standard/Compact), Infrastructure Nodes (optional, for routers, registry etc.), general Compute Nodes, and specialized Compute Nodes (e.g., GPU-enabled).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: Operations Expert
