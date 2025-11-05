# OpenShift Container Platform on Bare Metal

## OCP-BM-01: OCP installation method on baremetal infrastructure

**Architectural Question**
Which OCP installation method will be used to deploy a cluster on baremetal infrastructure?

**Issue or Problem**
The choice of installation method for Bare Metal impacts the level of automation, network prerequisites (like PXE), and how the cluster interacts with the physical hardware.

**Assumption**
N/A

**Alternatives**

- User-Provisioned Infrastructure (UPI)
- Installer-Provisioned Infrastructure (IPI)
- Agent-based Installer (ABI)
- Assisted Installer

**Decision**
#TODO: Document the decision for the Bare Metal cluster.#

**Justification**

- **User-Provisioned Infrastructure (UPI):** Requires the user to manually configure and manage networking, DNS, load balancers, and provisioning of RHCOS onto bare metal hosts prior to installation.
- **Installer-Provisioned Infrastructure (IPI):** Automates host provisioning and networking by leveraging Bare Metal Operator (BMO) features, suitable if metal resources are fully automated via BMO.
- **Agent-based Installer (ABI):** Uses discovery ISOs and a lightweight agent to gather hardware information, simplifying installation for both connected and disconnected bare metal environments.
- **Assisted Installer:** A web-based SaaS service designed to generate installation artifacts and manage the installation process, offering a simplified user experience for bare metal deployments.

**Implications**

- **User-Provisioned Infrastructure (UPI):** Highest operational overhead and responsibility for day 1/2 operations.
- **Installer-Provisioned Infrastructure (IPI):** Requires integration with BMO and related provisioning infrastructure. Allows use of Machine API for lifecycle management.
- **Agent-based Installer (ABI):** Highly flexible for restricted networks and provides integrated tools for configuring nodes (e.g., LVM storage configuration).
- **Assisted Installer:** Requires a working internet connection during the preparation phase (unless run disconnected). Simplifies deployment by handling Ignition configuration generation.

  **Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader

---

## OCP-BM-02: Bare Metal Node Remediation

**Architectural Question**
What is the strategy for automatically remediating unhealthy Bare Metal nodes?

**Issue or Problem**
A strategy is needed to automatically detect and recover failed physical nodes. This is critical for maintaining cluster health and HA for workloads, especially for stateful services that run directly on the nodes.

**Assumption**
N/A.

**Alternatives**

- No Automated Remediation
- Node Health Check (NHC) with Self Node Remediation
- Node Health Check (NHC) with BareMetal Operator (BMO) Remediation

**Decision**
#TODO: Document the decision for the Bare Metal cluster.#

**Justification**

- **No Automated Remediation:** To rely on manual detection (via monitoring) and manual intervention by an operator to troubleshoot and reboot physical nodes.
- **Node Health Check (NHC) with Self Node Remediation:** To deploy the Node Health Check operator, which monitors node health. When a node fails, the `SelfNodeRemediation` agent on other nodes will fence the unhealthy node and restart its workloads elsewhere.
- **Node Health Check (NHC) with BareMetal Operator (BMO) Remediation:** To use the NHC in combination with the BareMetal Operator (enabled by an IPI install). When NHC detects a failure, it triggers the BMO to power-cycle the node via its BMC, attempting a full hardware reboot.

**Implications**

- **No Automated Remediation:** High operational burden and slow recovery times. Not recommended for a production cluster.
- **Node Health Check (NHC) with Self Node Remediation:** Provides software-level remediation. It ensures workloads are moved but does not fix the underlying node, which will remain unavailable until manually repaired.
- **Node Health Check (NHC) with BareMetal Operator (BMO) Remediation:** This is the most robust, fully automated solution. It attempts to recover the node by "turning it off and on again" via its BMC. This requires a reliable IPI installation and stable Redfish/IPMI connectivity.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader
