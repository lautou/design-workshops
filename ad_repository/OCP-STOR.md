# OpenShift Container Platform storage

## OCP-STOR-01: Storage

**Architectural Question**
Which storage provider will be deployed in each cluster for persistent application data?

**Issue or Problem**
A storage provider must be selected to meet the persistence, performance, and access mode requirements (e.g., ReadWriteMany, RWX) of stateful applications.

**Assumption**
N/A

**Alternatives**

- Platform-Native Storage
- OpenShift Data Foundation (ODF)
- Third-Party CSI Storage

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Platform-Native Storage:** Leverages integrated cloud storage (e.g., AWS EBS, Azure Disk, GCP PD) or basic on-premise PV types (e.g., Local Volume, HostPath). Reduces complexity but relies solely on the underlying platform's features.
- **OpenShift Data Foundation (ODF):** Provides a unified, software-defined storage layer backed by Red Hat Ceph Storage (Block/File) and NooBaa (Object). Provides advanced features like ReadWriteMany (RWX) access, replication, encryption, and multi-AZ resilience.
- **Third-Party CSI Storage:** Allows integration with existing enterprise storage solutions via a vendor-provided Container Storage Interface (CSI) driver. This utilizes existing hardware investments.

**Implications**

- **Platform-Native Storage:** Storage features and access modes (especially ReadWriteMany [RWX]) are dependent on the capabilities of the underlying platform's storage. Many native options only support ReadWriteOnce (RWO).
- **OpenShift Data Foundation (ODF):** **Requires a separate subscription and dedicated resources**. It is the preferred option for HA scaled registries and provides maximum resilience via Multi-AZ deployment. ODF is necessary when File (CephFS) or Object (MCG) storage capabilities are required.
- **Third-Party CSI Storage:** The organization is dependent on the vendor for the quality and support of the Container Storage Interface (CSI) driver.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Platform administrator
- Person: #TODO#, Role: Storage expert
