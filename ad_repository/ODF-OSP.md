# OpenShift Data Foundation - OpenStack

## ODF-OSP-01: ODF Deployment on OpenStack

**Architectural Question**
What is the deployment strategy for OpenShift Data Foundation on the OpenStack cluster?

**Issue or Problem**
On OpenStack, ODF is deployed on top of virtual block devices (Cinder volumes) attached to the ODF worker nodes. A strategy is needed to select the correct Cinder backend and volume type to meet ODF's performance and HA requirements.

**Assumption**
ODF will be deployed on the OpenStack cluster (see OCP-STOR-01).

**Alternatives**

- ODF on Standard Cinder Volumes
- ODF on High-Performance Cinder Volumes

**Decision**
#TODO: Document the decision for the OpenStack cluster.#

**Justification**

- **ODF on Standard Cinder Volumes:** To use the default, general-purpose Cinder volume type. This is suitable for non-production, development, or workloads without high I/O requirements.
- **ODF on High-Performance Cinder Volumes:** To explicitly use a high-performance Cinder volume type (e.g., one backed by all-flash storage) for the ODF worker nodes. This is the recommended approach for production or I/O-intensive workloads.

**Implications**

- **ODF on Standard Cinder Volumes:** Performance will be entirely dependent on the underlying OpenStack Cinder backend. A slow backend will result in a slow ODF cluster, impacting all data-heavy applications.
- **ODF on High-Performance Cinder Volumes:** Requires coordination with the OpenStack team to ensure such a volume type is available and has sufficient quota. This will likely incur higher costs on the OpenStack platform but is necessary for performance.

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
