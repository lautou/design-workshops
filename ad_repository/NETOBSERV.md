# Network Observability

## NETOBSERV-01: Network Observability

**Architectural Question**
Will network flow data be collected for visibility and troubleshooting?

**Issue or Problem**
To understand and troubleshoot complex network interactions between services within the cluster, a tool is needed to capture and visualize network flow data.

**Assumption**
Deep visibility into pod-to-pod network traffic is required for troubleshooting.

**Alternatives**

- Network Observability Disabled
- Network Observability Enabled

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Network Observability Disabled:** To conserve resources if detailed network flow analysis is not a requirement.
- **Network Observability Enabled:** To provide deep visibility into network traffic, allowing operators to analyze flows, identify bottlenecks, and troubleshoot connectivity issues between pods and services.

**Implications**

- **Network Observability Disabled:** Troubleshooting network issues will rely on traditional tools like `ping`, `traceroute`, and manual log inspection.
- **Network Observability Enabled:** Requires the installation of the Network Observability Operator. The operator collects network flow data using eBPF and provides a topology view and filtering capabilities. This consumes additional CPU, memory, and storage resources.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner
