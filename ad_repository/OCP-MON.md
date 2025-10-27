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
- Third-Party Monitoring Solution

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Platform Monitoring:** To use the out-of-the-box monitoring stack, which provides comprehensive metrics for the core OpenShift platform and its components.
- **Enable User Workload Monitoring:** To extend the built-in monitoring stack to allow development teams to scrape custom metrics from their own applications and services within their projects.
- **Third-Party Monitoring Solution:** To integrate with an existing, enterprise-standard monitoring tool by deploying a vendor-specific agent to scrape and forward metrics.

**Implications**

- **Default Platform Monitoring:** Provides excellent visibility into the platform's health but does not collect metrics from user-deployed applications.
- **Enable User Workload Monitoring:** Empowers developers with self-service monitoring. This is critical for high-performance workloads, as it allows collection of custom application metrics and specialized hardware metrics (e.g., from GPU exporters).
- **Third-Party Monitoring Solution:** Leverages existing tools and expertise but adds another agent to be managed on the cluster. It may lead to two separate monitoring systems if the default stack is not disabled.

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
