# OpenShift Container Platform on OpenStack

## OCP-OSP-01: OCP installation method on OSP infrastructure

**Architectural Question**
Which OCP installation method will be used to deploy a cluster on OpenStack infrastructure?

**Issue or Problem**
The choice of installation method for OpenStack impacts the level of automation and integration with OpenStack services like Neutron, Cinder, and Nova.

**Assumption**
N/A

**Alternatives**

- User-Provisioned Infrastructure (UPI)
- Installer-Provisioned Infrastructure (IPI)

**Decision**
#TODO: Document the decision for the OpenStack cluster.#

**Justification**

- **User-Provisioned Infrastructure (UPI):** To manually provision all OpenStack resources (VMs, networks, load balancers, security groups) before running the OpenShift installation. This provides maximum control and allows integration into existing, complex network topologies.
- **Installer-Provisioned Infrastructure (IPI):** To use the fully automated, IPI-based workflow. The installer will use the OpenStack APIs to create and manage all necessary resources, including VMs, networks, and load balancers (Octavia).

**Implications**

- **User-Provisioned Infrastructure (UPI):** Places the full burden of infrastructure lifecycle management on the operations team. The Machine API is not available, so node scaling and remediation are manual processes.
- **Installer-Provisioned Infrastructure (IPI):** This is the most integrated approach, enabling the Machine API for automated node scaling and remediation. It requires an OpenStack user with sufficient permissions to create and manage all cluster resources.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-OSP-02: OpenStack Project Tenancy

**Architectural Question**
How will the OpenShift cluster resources be isolated within the OpenStack platform?

**Issue or Problem**
The OpenShift cluster (control plane, compute nodes) will consume OpenStack resources (VMs, volumes, networks, ports). A decision must be made on how to isolate these resources from other tenants and projects within OpenStack.

**Assumption**
N/A

**Alternatives**

- Single OpenStack Project
- Dedicated OpenStack Project per Cluster

**Decision**
#TODO: Document the decision for the OpenStack cluster.#

**Justification**

- **Single OpenStack Project:** To co-locate the OpenShift cluster resources within an existing, shared OpenStack project. This may be done to share quotas or network resources with other (non-OCP) applications.
- **Dedicated OpenStack Project per Cluster:** To create a new, dedicated OpenStack project for each OpenShift cluster (e.g., `ocp-prod-project`, `ocp-nonprod-project`). This is the recommended approach for isolation.

**Implications**

- **Single OpenStack Project:** Requires careful management of OpenStack quotas (vCPU, RAM, Cinder volumes) to prevent the OCP cluster from consuming all resources or being starved by "noisy neighbors" in the same project.
- **Dedicated OpenStack Project per Cluster:** Provides a clear boundary for security, quota management, and chargeback. It ensures the OpenShift cluster's resources are managed independently, which is critical for production stability.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-OSP-03: OpenStack CNI Integration (Kuryr)

**Architectural Question**
Which CNI plugin will be used for pod networking on OpenStack?

**Issue or Problem**
When running on OpenStack, there is an option to use the default OVN-Kubernetes CNI (which creates a virtual overlay network) or the Kuryr CNI, which integrates directly with OpenStack Neutron.

**Assumption**
The OpenStack environment has Neutron and Octavia services available.

**Alternatives**

- Default OVN-Kubernetes CNI
- Kuryr-Kubernetes CNI

**Decision**
#TODO: Document the decision for the OpenStack cluster.#

**Justification**

- **Default OVN-Kubernetes CNI:** To use the standard, platform-agnostic OCP networking stack. This creates a pod network that is an overlay, independent of the underlying OpenStack network.
- **Kuryr-Kubernetes CNI:** To achieve higher network performance by eliminating the "double overlay" (OCP overlay on top of OSP overlay). Kuryr creates OpenStack Neutron ports for pods and uses Octavia LBs for services, making pods first-class citizens on the OpenStack network.

**Implications**

- **Default OVN-Kubernetes CNI:** This is the simplest, most standard, and universally supported option. Performance is generally sufficient, but traffic must traverse the OCP SDN before reaching the OSP network.
- **Kuryr-Kubernetes CNI:** Can provide significant performance benefits and simplifies network tracing, as pod IPs are visible on the OpenStack network. However, it consumes Neutron ports at a high rate, which can exhaust OpenStack quotas. It also has a more complex configuration and is a specialized CNI.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-OSP-04: OpenStack Storage Integration

**Architectural Question**
How will OpenShift integrate with OpenStack's storage services (Cinder and Manila) for application persistent volumes?

**Issue or Problem**
The cluster needs to integrate with the OpenStack cloud provider to provision persistent storage for applications. This requires configuring OCP to communicate with the correct Cinder (block) and/or Manila (file) backends using their respective CSI drivers. This decision is separate from any ODF deployment.

**Assumption**
Applications requiring persistent storage will be deployed. The OpenStack environment has Cinder and potentially Manila services available.

**Alternatives**

- Cinder CSI Driver (Block Storage)
- Manila CSI Driver (File Storage)
- Both Cinder and Manila CSI Drivers

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Cinder CSI Driver (Block Storage):** To provide persistent block storage (RWO - ReadWriteOnce access mode) suitable for databases and single-pod consumer workloads. This is the most common integration.
- **Manila CSI Driver (File Storage):** To provide shared, distributed file storage (RWX - ReadWriteMany access mode) suitable for multi-pod consumer workloads requiring shared filesystem access (e.g., collaborative tools, web content).
- **Both Cinder and Manila CSI Drivers:** To offer a comprehensive range of native OpenStack storage solutions, supporting applications requiring both dedicated block storage and shared file capabilities.

**Implications**

- **Cinder CSI Driver:** Provisioning is restricted to ReadWriteOnce access mode. Requires careful selection and configuration of Cinder volume types within OpenStack to meet desired performance characteristics (e.g., SSD vs. HDD backing).
- **Manila CSI Driver:** Requires a fully configured, available, and performant Manila service backend within the OpenStack environment. Performance and reliability depend entirely on the Manila share provider configuration.
- **Both Cinder and Manila CSI Drivers:** Increases the number of storage options available but also requires managing the installation and lifecycle of two distinct CSI driver operators within OpenShift.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader
- Person: #TODO#, Role: OCP Platform Owner
