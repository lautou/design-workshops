# OpenShift Container Platform storage

## OCP-STOR-01: Storage

**Architectural Question**
Which storage provider will be deployed in each cluster for persistent application data?

**Issue or Problem**
A storage provider must be selected to meet the persistence, performance, and access mode requirements (e.g., ReadWriteMany, RWX) of stateful applications.

**Assumption**
#N/A

**Alternatives**

- Platform-Native Storage
- OpenShift Data Foundation (ODF)
- Third-Party CSI Storage

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Platform-Native Storage:** Leverages existing storage infrastructure and expertise (e.g., OSP Cinder/Manila, cloud provider CSI). For bare metal deployments, the recommended local storage solution is Logical Volume Management Storage (LVMS), replacing the older Local Volume Management Operator (LVMO).
- **OpenShift Data Foundation (ODF):** Provides a consistent, integrated software-defined storage platform (file, block, object) across any infrastructure. ODF supports crucial security requirements like FIPS-140-2 compliance.
- **Third-Party CSI Storage:** Allows integration of a pre-existing enterprise storage solution that the organization has standardized on.

**Implications**

- **Platform-Native Storage:** Storage features and access modes (especially ReadWriteMany [RWX]) are dependent on the capabilities of the underlying platform's storage.
- **OpenShift Data Foundation (ODF):** **Requires a separate subscription and dedicated resources**. It is the preferred option for HA scaled registries and provides maximum resilience via Multi-AZ deployment.
- **Third-Party CSI Storage:** The organization is dependent on the vendor for the quality and support of the Container Storage Interface (CSI) driver.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Platform administrator
- Person: #TODO#, Role: Storage expert
