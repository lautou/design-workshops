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

- **User-Provisioned Infrastructure (UPI):** To manually provision the operating system (RHEL CoreOS) on each physical node. This offers maximum control and is used when automation is not feasible or desired.
- **Installer-Provisioned Infrastructure (IPI):** To use the fully automated, IPI-based workflow. This requires a dedicated "provisioning" host, a flat "provisioning" network (for PXE), and BMC (e.g., Redfish/IPMI) integration.
- **Agent-based Installer (ABI):** To use a pre-built agent image (ISO) to boot the nodes. This is ideal for disconnected environments or when PXE is not feasible. It simplifies the provisioning network requirements.
- **Assisted Installer:** To use a web-based, wizard-like experience that simplifies the installation process and reduces manual configuration errors. It can be used via the Red Hat Hybrid Cloud Console or deployed on-premises.

**Implications**

- **User-Provisioned Infrastructure (UPI):** Places the full burden of hardware lifecycle management, OS installation, and node recovery on the operations team. The Machine API is not available.
- **Installer-Provisioned Infrastructure (IPI):** This is the most integrated approach. It enables the Machine API and automated node remediation. It requires detailed information for each node's BMC.
- **Agent-based Installer (ABI):** Offers a good balance, simplifying provisioning while still enabling cluster-driven installation. Well-suited for GitOps and large-scale deployments.
- **Assisted Installer:** Greatly simplifies the data-gathering and validation process for on-premises installs. It guides the user through generating a discovery ISO for booting nodes.

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
