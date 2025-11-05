# OpenShift Container Platform monitoring

## OCP-MON-01: Monitoring

**Architectural Question**
What is the strategy for monitoring cluster and application metrics?

**Issue or Problem**
A monitoring solution is required to collect and store metrics for observing cluster health, managing capacity, and troubleshooting performance issues. Decisions are needed on the scope of monitoring and long-term data retention.

**Assumption**
N/A

**Alternatives**

- Default Platform Monitoring
- Enable User Workload Monitoring
- Customized Monitoring Stack via COO

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Platform Monitoring:** Provides built-in, preconfigured monitoring for all core OpenShift components (e.g., etcd, Kubernetes API server, nodes, Operators) using Prometheus, Alertmanager, and Thanos Query. This is enabled by default.
- **Enable User Workload Monitoring:** Extends the Prometheus stack to collect metrics and expose alerts specifically for workloads running in user-defined projects (namespaces). This is optional.
- **Customized Monitoring Stack via COO:** Leverages the Cluster Observability Operator (COO) to create and manage highly customizable monitoring stacks, offering a more tailored and detailed view of specific namespaces or components beyond the default configuration.

**Implications**

- **Default Platform Monitoring:** Configuration is locked down and supported only via the Cluster Monitoring Operator (CMO) ConfigMap. Data storage capacity for Thanos is pre-allocated.
- **Enable User Workload Monitoring:** Increases resource consumption (CPU/RAM/storage) due to additional Prometheus and Thanos Ruler instances running in the `openshift-user-workload-monitoring` project.
- **Customized Monitoring Stack via COO:** Provides maximum flexibility for metric collection and routing, but introduces management overhead for the custom stacks and requires advanced knowledge of monitoring configuration.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Platform administrator
- Person: #TODO#, Role: Application team leadership

---

## OCP-MON-02: Custom Monitoring Stack (Cluster Observability Operator)

**Architectural Question**
Will the Cluster Observability Operator (COO) be deployed to enable highly customized, cluster-scoped monitoring configurations?

**Issue or Problem**
The default monitoring stack is comprehensive for platform components but customizing user workload monitoring extensively requires tailoring components traditionally outside the standard configuration.

**Assumption**
N/A

**Alternatives**

- Deploy Cluster Observability Operator (COO)
- Rely solely on Default/User Workload Monitoring (OCP-MON-01)

**Decision**
#TODO: Document the decision.#

**Justification**

- **Deploy Cluster Observability Operator (COO):** To automate configuration and management of monitoring components, offering a more tailored and detailed view of each namespace compared to the default OpenShift Container Platform monitoring system.
- **Rely solely on Default/User Workload Monitoring (OCP-MON-01):** To keep the monitoring footprint minimal, relying on the out-of-the-box features managed by the Cluster Monitoring Operator (CMO).

**Implications**

- **Deploy Cluster Observability Operator (COO):** Adds another Operator (and potentially complexity) to manage within the cluster lifecycle.
- **Rely solely on Default/User Workload Monitoring (OCP-MON-01):** Limits the ability to create highly custom metrics scraping or retention policies outside the standard configuration boundary.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Platform administrator
- Person: #TODO#, Role: Application team leadership
