# OpenShift Data Foundation - Base

## ODF-BASE-01: Storage Class Design

**Architectural Question**
What specific `StorageClasses` will be created to expose ODF's capabilities (File, Block, Object) to different types of workloads?

**Issue or Problem**
A clear strategy for defining `StorageClasses` is needed to provide users with self-service access to the correct type of storage. Without this, users might use inappropriate storage for their applications, leading to poor performance or functionality issues.

**Assumption**
OpenShift Data Foundation (ODF) will be deployed as the primary storage solution.

**Alternatives**

- **Default Classes Only:** Rely solely on the default `StorageClasses` created by the ODF installation.
- **Role-Based Storage Classes:** Create specific `StorageClasses` for different workload profiles (e.g., `odf-rwx-files-gold`, `odf-rwo-block-bronze`, `odf-s3-standard`).

**Decision**
#TODO: Document the decision.#

**Justification**

- **Default Classes Only:** Simplifies administration but offers no granularity or control over performance tiers. Users get a "one-size-fits-all" storage experience.
- **Role-Based Storage Classes:** The recommended approach. It allows the platform team to abstract the underlying storage complexity and offer a simple, tiered catalog of storage services to users. This is ideal for guiding data scientists to the correct storage for their specific needs (e.g., a "fast-rwx" class for training jobs).

**Implications**

- Choosing **Role-Based Storage Classes** requires the platform team to define, document, and manage these classes. It provides the best user experience and ensures workloads (e.g., data ingestion pipelines, model training jobs, or databases) are matched with the appropriate storage backend.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Lead Data Scientist

---

## ODF-BASE-02: On-Cluster Object Storage

**Architectural Question**
Will Red Hat OpenShift Data Foundation's Object Storage service be utilized?

**Issue or Problem**
A decision must be made whether the platform will deploy and use the Multicloud Object Gateway (MCG), powered by NooBaa, or rely entirely on external object storage solutions.

**Assumption**
N/A

**Alternatives**

- No On-Cluster Object Storage
- Deploy ODF with Multicloud Object Gateway (MCG)

**Decision**
#TODO: Document the decision.#

**Justification**

- **No On-Cluster Object Storage:** Can be a valid option if the organization has already invested heavily in an enterprise-wide object storage solution and prefers to centralize all object data there.
- **Deploy ODF with Multicloud Object Gateway (MCG):** The recommended approach for a self-contained platform. It co-locates the object storage with the compute, which can reduce latency for data-intensive operations. It provides file, block, and object storage from a single, integrated solution.

**Implications**

- **No On-Cluster Object Storage:** Requires configuring and maintaining external object storage connectivity; object storage consumption relies entirely on external systems.
- **Deploy ODF with Multicloud Object Gateway (MCG):** Adds the resource overhead of MCG components (NooBaa core/db, endpoint) and underlying Ceph RGW instances managed by the ODF Operator to the cluster; object storage availability and lifecycle are dependent on the ODF cluster status.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: Lead Data Scientist
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## ODF-BASE-03: ODF Deployment Approach (Internal vs External)

**Architectural Question**
Will OpenShift Data Foundation (ODF) be deployed internally on existing OpenShift worker nodes, or externally/in a separate cluster?

**Issue or Problem**
The deployment approach dictates resource sharing, scalability, and operational management boundaries for the storage platform.

**Assumption**
OpenShift Data Foundation (ODF) will be deployed as the storage solution (see OCP-STOR-01).

**Alternatives**

- Internal Storage Cluster
- External Storage Cluster

**Decision**
#TODO: Document the decision for ODF deployment.#

**Justification**

- **Internal Storage Cluster:** To deploy ODF co-located on the same worker nodes as application workloads. This is efficient for smaller clusters and simplifies setup by utilizing OCP resources directly.
- **External Storage Cluster:** To deploy ODF on dedicated nodes (potentially managed by a separate team or SRE) or leverage a pre-existing external Ceph cluster. This approach is favored when storage requirements are significant (e.g., 600+ storage devices) or when multiple OCP clusters need to consume storage services from a common external cluster.

**Implications**

- **Internal Storage Cluster:** Requires careful node sizing to prevent storage components (Ceph OSDs, Monitors) from impacting application performance (resource contention).
- **External Storage Cluster:** Provides clearer separation of concerns and resources, but increases network dependencies and requires configuration to integrate OCP storage endpoints with the external cluster.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: OCP Platform Owner
