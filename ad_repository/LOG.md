# OpenShift Logging

## LOG-01: Logging Platform Solution

**Architectural Question**
Which solution will be used for collecting and analyzing container and platform logs?

**Issue or Problem**
A dedicated logging solution is required to gather, process, and make logs queryable for troubleshooting, capacity planning, and compliance auditing.

**Assumption**
N/A

**Alternatives**

- OpenShift Logging (LokiStack)
- External Log Collector (Forwarding Only)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **OpenShift Logging (LokiStack):** To deploy the integrated logging stack which collects logs from platform and user workloads, providing visualization and storage within the cluster. This is the standard, supported approach for on-cluster visibility.
- **External Log Collector (Forwarding Only):** To rely exclusively on an external log aggregation tool, configuring the cluster only to forward logs (LOG-02) without storing or querying them internally. This minimizes resource consumption on the cluster but eliminates immediate in-cluster visibility.

**Implications**

- **OpenShift Logging (LokiStack):** Requires sizing the local log store appropriately (LOG-03) and consumes worker node resources for storage and indexing.
- **External Log Collector (Forwarding Only):** Requires network configuration to reach the external collector. Cluster health monitoring relies heavily on the external system.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## LOG-02: Log Forwarding

**Architectural Question**
Will logs be forwarded to an external, long-term storage or analysis system?

**Issue or Problem**
On-cluster log storage is typically for short-term retention. For long-term archival, compliance, and advanced analytics, logs must be forwarded to a centralized, external system.

**Assumption**
N/A

**Alternatives**

- External Log Forwarding Enabled
- External Log Forwarding Disabled

**Decision**
#TODO: Document the decision.#

**Justification**

- **External Log Forwarding Enabled:** To satisfy compliance requirements for long-term data retention and to enable correlation with logs from outside the OpenShift clusters (e.g., infrastructure logs).
- **External Log Forwarding Disabled:** To minimize complexity and eliminate reliance on external logging infrastructure, suitable when short-term, on-cluster logs are sufficient.

**Implications**

- **External Log Forwarding Enabled:** Requires provisioning and configuring an external logging platform (e.g., Splunk, Elasticsearch, or cloud native services). Requires cluster resources for the forwarding components (e.g., Fluentd/Vector).
- **External Log Forwarding Disabled:** Limits auditability and long-term troubleshooting capability. All log data relies entirely on the sizing and retention policy of the internal log store (LOG-03).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## LOG-03: On-Cluster Log Storage Sizing (LokiStack)

**Architectural Question**
What will be the size of the on-cluster log store?

**Issue or Problem**
The LokiStack component, which provides the on-cluster log store, must be sized appropriately to handle the log volume and retention requirements without consuming excessive cluster resources.

**Assumption**
The OpenShift Logging Operator is deployed with the LokiStack storage solution (chosen in LOG-01).

**Alternatives**

- 1x.extra-small
- 1x.small
- 1x.medium

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **1x.extra-small:** For minimal resource consumption, suitable for development clusters or environments with very low log volume.
- **1x.small:** To provide a balanced, default starting size for most production or pre-production clusters with moderate log volume.
- **1x.medium:** For clusters with high log volume or longer on-cluster retention requirements.

**Implications**

- **1x.extra-small:** Has the lowest resource footprint but also the lowest capacity for ingestion, storage, and querying.
- **1x.small:** Provides a good baseline for performance and capacity. The size can be scaled up in the future if requirements change.
- **1x.medium:** Consumes more significant CPU, memory, and storage resources. This size should be chosen based on a clear understanding of the expected log volume.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
