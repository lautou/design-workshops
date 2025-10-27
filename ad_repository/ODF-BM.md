# OpenShift Data Foundation - Bare Metal

## ODF-BM-01: ODF Deployment on Bare Metal

**Architectural Question**
What is the deployment strategy for OpenShift Data Foundation on the Bare Metal cluster?

**Issue or Problem**
On Bare Metal, ODF requires direct access to physical storage devices. A strategy is needed for device discovery, selection, and configuration (e.g., using LVM or directly consuming devices).

**Assumption**
ODF will be deployed on the Bare Metal cluster (see OCP-STOR-01).

**Alternatives**

- ODF using Local Storage Operator (LSO)
- ODF using Logical Volume Manager Storage (LVMS)

**Decision**
#TODO: Document the decision for the Bare Metal cluster.#

**Justification**

- **ODF using Local Storage Operator (LSO):** To leverage the older, established method where LSO discovers and prepares local devices for ODF OSDs.
- **ODF using Logical Volume Manager Storage (LVMS):** To utilize the newer, recommended operator (introduced in OCP 4.12+) which uses LVM thin provisioning on top of local devices. This approach is more flexible and aligns with future storage management directions.

**Implications**

- **ODF using Local Storage Operator (LSO):** Simpler to set up initially but less flexible regarding device management post-deployment.
- **ODF using Logical Volume Manager Storage (LVMS):** Requires the LVMS operator to be deployed and configured. Offers better flexibility for managing underlying devices and aligns with modern OCP storage practices.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader

---

## ODF-BM-02: Bare Metal Node and Device Failure Domain Awareness

**Architectural Question**
How will the ODF cluster be configured for high availability across physical failure domains (e.g., nodes, racks, chassis) on Bare Metal?

**Issue or Problem**
To ensure ODF can survive physical hardware failures (node failure, rack power loss), its components (OSDs) must be distributed across different physical failure domains. ODF needs to be made aware of the underlying physical topology.

**Assumption**
ODF will be deployed on the Bare Metal cluster.

**Alternatives**

- No Failure Domain Awareness (Best Effort)
- Rack-Aware Deployment (using Node Labels)

**Decision**
#TODO: Document the decision for the Bare Metal cluster.#

**Justification**

- **No Failure Domain Awareness (Best Effort):** To allow ODF to distribute replicas based solely on node availability. This provides node-level resilience but does not protect against failures impacting multiple nodes simultaneously (e.g., rack failure).
- **Rack-Aware Deployment (using Node Labels):** To explicitly inform ODF about the physical rack location of each node using Kubernetes node labels (e.g., `topology.kubernetes.io/zone=rack1`). ODF will then ensure data replicas are placed across different racks.

**Implications**

- **No Failure Domain Awareness (Best Effort):** A failure impacting multiple nodes in the same physical location (rack) could lead to data loss or cluster unavailability.
- **Rack-Aware Deployment (using Node Labels):** This is the recommended production architecture for Bare Metal. It requires administrators to accurately label each ODF worker node with its physical rack location during or after cluster installation. Requires at least 3 racks for full resilience.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Infra Leader
