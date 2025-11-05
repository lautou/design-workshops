# OpenShift Data Foundation - OpenStack

## ODF-OSP-01: ODF Deployment on OpenStack

**Architectural Question**
What is the deployment strategy for OpenShift Data Foundation on the OpenStack cluster?

**Issue or Problem**
On OpenStack, ODF is deployed on top of virtual block devices (Cinder volumes) attached to the ODF worker nodes. A strategy is needed to select the correct Cinder backend and volume type to meet ODF's performance and HA requirements.

**Assumption**
ODF will be deployed on the OpenStack cluster (see OCP-STOR-01).

**Alternatives**

- Default Cinder Provisioning
- Performance-Optimized Cinder Volume Types
- Dedicated Storage Nodes/Block Devices

**Decision**
#TODO: Document the decision for the OpenStack cluster.#

**Justification**

- **Default Cinder Provisioning:** Uses the standard OpenStack Cinder backend and volume types available to the OCP project. Simplifies deployment but risks variable performance based on OpenStack utilization.
- **Performance-Optimized Cinder Volume Types:** Explicitly defines and uses Cinder volume types backed by high-speed storage (e.g., SSDs or dedicated backends) to ensure ODF meets the necessary performance profile for production workloads.
- **Dedicated Storage Nodes/Block Devices:** Utilizes dedicated Bare Metal nodes or specially provisioned virtual machines/block devices within OpenStack solely for ODF, bypassing shared resource risks for maximal performance isolation.

**Implications**

- **Default Cinder Provisioning:** May be suitable for non-production or lightly utilized ODF clusters. Performance is subject to the OpenStack platform storage configuration.
- **Performance-Optimized Cinder Volume Types:** Requires coordination with the OpenStack administration team to provision and map specific volume types to the OCP tenant project.
- **Dedicated Storage Nodes/Block Devices:** Highest initial overhead and infrastructure cost, but guarantees quality of service (QoS) for storage I/O.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OpenStack administrator

---

## ODF-OSP-02: OpenStack Failure Domain and Availability Zone (AZ) Awareness

**Architectural Question**
How will the ODF cluster be configured for high availability across OpenStack Availability Zones?

**Issue or Problem**
To ensure ODF can survive an OpenStack compute or storage failure, its components (OSDs) must be distributed across different failure domains. This must be mapped to the underlying OpenStack AZ topology.

**Assumption**
ODF will be deployed on the OpenStack cluster, and the OpenStack environment has Availability Zones defined.

**Alternatives**

- No AZ Awareness (Single AZ)
- Multi-AZ Deployment

**Decision**
#TODO: Document the decision for the OpenStack cluster.#

**Justification**

- **No AZ Awareness (Single AZ):** To deploy all ODF worker nodes within a single OpenStack Availability Zone. This is a simpler deployment model but provides no protection against an AZ-level failure.
- **Multi-AZ Deployment:** To deploy ODF worker nodes across three different OpenStack Availability Zones. ODF will automatically distribute its data replicas across these zones, providing maximum resilience against infrastructure failures.

**Implications**

- **No AZ Awareness (Single AZ):** A failure of the underlying OpenStack infrastructure in that AZ will cause a complete ODF cluster outage. Not recommended for production.
- **Multi-AZ Deployment:** This is the recommended production architecture. It requires that the OpenStack platform has at least three distinct AZs available. It also introduces minimal network latency for cross-AZ data replication.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OpenStack administrator
