# OpenShift Container Platform Networking

## OCP-NET-01: Machine IP Range

**Architectural Question**
Which IP address range will be used for the cluster nodes (control plane, compute machines)?

**Issue or Problem**
The machine network CIDR defines the node IP range. This range must be routable within the organization's network for administrative access and communication with infrastructure services (DNS, NTP).

**Assumption**
N/A

**Alternatives**

- Default Machine Network CIDR (Platform Specific, e.g., 10.0.0.0/16 for IPI)
- Custom Machine Network CIDR

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Machine Network CIDR:** Use platform defaults (e.g., `10.0.0.0/16` for IPI on some platforms) when available and suitable.
- **Custom Machine Network CIDR:** Specify a custom range to align with existing network segmentation and IP plans. Required for UPI and most enterprise environments.

**Implications**

- **Default:** Only applicable for certain IPI installs. Using without validation risks IP conflicts.
- **Custom:** Requires a pre-allocated, routable subnet from the network team. Network must allow access to/from this range for necessary infrastructure services.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-02: Node IP Address Management

**Architectural Question**
How will the cluster nodes (Control Plane and Compute) obtain their IP addresses from the Machine IP Range?

**Issue or Problem**
IP Address Management (IPAM) affects node address predictability, critical for setup, security policies, and installation method compatibility.

**Assumption**
Machine IP Range (OCP-NET-01) is defined.

**Alternatives**

- DHCP
- Static IP Configuration

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **DHCP:** Simplifies node provisioning by automatically assigning IPs. Reduces manual configuration.
- **Static IP Configuration:** Ensures persistent, predictable node IPs, often required by enterprise network/security policies, especially in production.

**Implications**

- **DHCP:** Requires a highly available DHCP server, ideally with reservations. Simplifies node scaling/replacement.
- **Static IP Configuration:** Increases manual configuration effort during install and scaling. Requires a robust external IPAM process to avoid conflicts.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-03: Pod Network CIDR Selection

**Architectural Question**
Which internal IP address range will be used for Pod networking?

**Issue or Problem**
The Pod network CIDR provides IPs for pods within the cluster's SDN. It must not overlap with any existing network reachable from the cluster (including Machine and Service networks) to avoid routing failures.

**Assumption**
N/A

**Alternatives**

- Default Pod Network CIDR (e.g., 10.128.0.0/14)
- Custom Pod Network CIDR

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Pod Network CIDR:** Use defaults for simplicity when confirmed not to overlap.
- **Custom Pod Network CIDR:** Specify a custom range when the default overlaps with existing networks, ensuring correct pod routing to/from external services.

**Implications**

- **Default:** Simplifies installation but requires enterprise-wide network validation to prevent conflicts.
- **Custom:** Requires pre-planning and coordination with network admins to select an appropriate unused IP range.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-04: Service Network CIDR Selection

**Architectural Question**
Which IP address range will be used for the Cluster Service network?

**Issue or Problem**
A dedicated, non-overlapping IP range is needed for ClusterIP Services. Conflicts with existing networks will make cluster services unreachable.

**Assumption**
N/A

**Alternatives**

- Default Service Network CIDR (e.g., 172.30.0.0/16)
- Custom Service Network CIDR

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Service Network CIDR:** Use defaults for simplicity when confirmed not to overlap.
- **Custom Service Network CIDR:** Specify a custom range when the default overlaps, preventing routing conflicts and ensuring service reachability.

**Implications**

- **Default:** Simplifies installation. Failure to verify non-overlap leads to service connectivity issues.
- **Custom:** Requires coordination with the network team to select and reserve a suitable IP range provided during installation.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-05: CNI Plugin Selection (Platform Specific)

**Architectural Question**
Which Container Network Interface (CNI) plugin will manage Pod networking?

**Issue or Problem**
The CNI plugin choice impacts network features, performance, and integration with the underlying infrastructure (especially relevant for OpenStack).

**Assumption**
Cluster platform (OCP-BASE-03) is known. For OpenStack, Neutron and Octavia are available.

**Alternatives**

- **Default:** OVN-Kubernetes CNI (Platform Agnostic)
- **OpenStack Specific:** Kuryr-Kubernetes CNI

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **OVN-Kubernetes CNI:** Standard, platform-agnostic OCP networking stack. Creates a virtual overlay network independent of underlying infrastructure. Generally recommended for simplicity and consistency.
- **Kuryr-Kubernetes CNI (OpenStack Only):** Achieves higher network performance on OpenStack by eliminating "double overlay". Creates Neutron ports for pods and uses Octavia LBs for services. Makes pods first-class OpenStack network citizens.

**Implications**

- **OVN-Kubernetes:** Simplest, standard, universally supported. Performance usually sufficient. Traffic traverses OCP SDN overlay.
- **Kuryr (OpenStack Only):** Significant performance benefits, simplified network tracing (pod IPs visible on OSP network). Consumes Neutron ports rapidly, risking quota exhaustion. More complex configuration, specialized CNI.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader (Especially for OpenStack decision)

---

## OCP-NET-06: Outbound Connectivity (External Firewall/Proxy)

**Architectural Question**
How will cluster egress traffic destined for external networks (e.g., Internet, other corporate networks) be managed by external firewalls and/or proxies?

**Issue or Problem**
Corporate security requires controlling outbound connections. This impacts cluster installation, updates, OperatorHub access, workload external service access, and requires coordination with network security teams.

**Assumption**
Cluster Network Connectivity Model (OCP-BASE-07) is decided (Connected/Disconnected).

**Alternatives**

- Direct Outbound (Potentially behind Firewall Rules)
- Via HTTP/S Proxy Server

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Direct Outbound:** Simplifies cluster configuration if external firewalls allow required traffic (potentially restricted by rules per OCP-NET-07).
- **Via HTTP/S Proxy:** Necessary when direct outbound access is blocked. Centralizes egress control and filtering at the proxy server, aligning with common enterprise security patterns.

**Implications**

- **Direct Outbound:** Requires firewall rules allowing access to Red Hat registries, telemetry, cloud APIs (if applicable), and any external services needed by workloads. Firewall rule management (OCP-NET-07) is critical.
- **Via Proxy:** Requires configuring OpenShift cluster-wide proxy settings during installation (for core components) and potentially per-workload proxy settings. Cluster functionality depends on proxy availability and correct configuration (including trusting proxy CA).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-07: External Firewall Rule Granularity (Connected Environments)

**Architectural Question**
If using direct outbound connectivity (behind firewalls) in a connected environment, how granular will the firewall rules be?

**Issue or Problem**
Firewall rules for direct outbound access must balance security (least privilege) with operational feasibility (allowing necessary Red Hat and workload traffic).

**Assumption**
Cluster is Connected (OCP-BASE-07) and uses Direct Outbound (OCP-NET-06).

**Alternatives**

- Open/Broad Firewall Policy
- Restricted Firewall Policy (Whitelisting specific FQDNs/IPs)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Open/Broad Policy:** Simplifies operations, allowing broad cluster access to external resources (e.g., allow all HTTPS outbound). Assumes security is managed elsewhere (e.g., higher-level firewalls).
- **Restricted Policy:** Enforces least privilege, allowing communication only with documented Red Hat endpoints and required third-party services. Essential for high-security environments.

**Implications**

- **Open Policy:** Increases cluster security surface area. Simpler firewall management.
- **Restricted Policy:** Requires rigorous maintenance to track/update necessary external FQDNs/IPs for OCP updates, telemetry, OperatorHub, cloud APIs, etc. Changes by Red Hat or providers require immediate firewall updates.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-08: DNS Forwarding Configuration

**Architectural Question**
How will the cluster's internal DNS resolve external hostnames?

**Issue or Problem**
Cluster-internal DNS (CoreDNS) forwards requests for external domains to upstream resolvers. This behavior might need overriding to use specific enterprise DNS servers.

**Assumption**
N/A

**Alternatives**

- Default DNS Forwarding (Use Node's Upstream Resolvers)
- Override DNS Forwarding (Specify Upstream Corporate DNS Servers)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Forwarding:** Standard behavior, sufficient if node-level DNS resolvers (from DHCP or static config) correctly reach all required internal/external domains.
- **Override Forwarding:** Explicitly directs cluster DNS queries to specific corporate DNS servers. Necessary when node resolvers are unsuitable or fine-grained control is required (e.g., split DNS).

**Implications**

- **Default:** Relies on correct underlying infrastructure network config (DHCP options, node setup).
- **Override:** Cluster external name resolution depends on availability/correctness of specified upstream DNS servers. Managed via `dns.operator.openshift.io` CR.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-09: Load Balancer Strategy (API & Ingress)

**Architectural Question**
Which load balancer solution will expose the OpenShift API and application ingress traffic?

**Issue or Problem**
A load balancer is needed for external access to the cluster API and applications. Choice impacts cost, performance, features, automation, and operational responsibility.

**Assumption**
External access to API and applications is required.

**Alternatives**

- Default Platform Load Balancer (Cloud Provider LBaaS / On-Prem Keepalived/HAProxy)
- User-Managed Load Balancer (e.g., F5, NetScaler, external HAProxy)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Platform Load Balancer:** Leverages tightly integrated, automatically configured LB (cloud native service or built-in on-prem solution). Simplest approach, especially with IPI.
- **User-Managed Load Balancer:** Utilizes existing enterprise-standard LB offering advanced features, specific security compliance, and aligning with current operational workflows. Required for UPI.

**Implications**

- **Default:** Functionality limited by the platform's default LB. Configuration managed automatically by OCP (simpler but less flexible). Cost typically included or based on cloud usage.
- **User-Managed:** Requires manual configuration and integration for API and Ingress Operator Services. Operations team retains full control and responsibility (lifecycle, HA, features). Adds operational overhead but allows advanced customization.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Infra Leader

---

## OCP-NET-10: Ingress Controller Strategy

**Architectural Question**
How will ingress controllers be deployed and managed for routing external traffic to applications?

**Issue or Problem**
Strategy impacts multi-tenancy, performance isolation, security, custom domain usage, and resource consumption.

**Assumption**
Applications need to be exposed externally.

**Alternatives**

- Default OpenShift Ingress Controller (Shared)
- Dedicated OpenShift Ingress Controllers (Per Tenant/App Group)
- Third-Party Ingress Controller (e.g., Nginx Ingress Operator)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default:** Simplest, uses out-of-the-box controller for all routes under the default apps domain (`*.apps.cluster.domain`).
- **Dedicated:** Creates separate controllers for different apps/tenants using `IngressController` CR. Allows custom domains, performance/security isolation.
- **Third-Party:** Integrates vendor-specific controller for advanced features or existing expertise.

**Implications**

- **Default:** All routes share one controller. Risk of "noisy neighbor" performance issues. Limits domain flexibility. Least resource usage.
- **Dedicated:** Increases cluster resource consumption (CPU, RAM per controller replica). Requires config for new controller and route scoping (custom domains, route labels/selectors). Provides isolation.
- **Third-Party:** Org responsible for full lifecycle management. Domain flexibility but requires manual integration and potentially different operational model.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-NET-11: Ingress Controller Replica Count

**Architectural Question**
How many replicas will be deployed for each ingress controller instance (default and dedicated)?

**Issue or Problem**
Replica count determines HA and traffic handling capacity. Insufficient replicas cause bottlenecks or outages.

**Assumption**
Ingress Controller strategy (OCP-NET-10) is decided.

**Alternatives**

- Default Replica Count (Typically 2)
- Custom Replica Count (Scaled based on load/HA needs)

**Decision**
#TODO: Document the decision for each cluster and each ingress controller pool.#

**Justification**

- **Default (2):** Baseline HA, suitable for non-prod or low traffic.
- **Custom:** Scale replicas up (or down) to match expected load and meet specific HA requirements (e.g., survive node/AZ failure) for production.

**Implications**

- **Default (2):** Basic redundancy. May not handle high volume or survive multi-node/AZ failure without degradation.
- **Custom:** Allows scaling for production loads (including bursty AI inference traffic). Each replica consumes additional CPU/memory. Requires monitoring to determine appropriate count.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: Operations Expert

---

## OCP-NET-12: SSL/TLS Termination Strategy

**Architectural Question**
Where will SSL/TLS encryption for application ingress traffic be terminated?

**Issue or Problem**
Decision impacts security posture, certificate management complexity, and ability to enforce end-to-end encryption.

**Assumption**
Application traffic requires HTTPS.

**Alternatives**

- **Edge Termination:** TLS terminates at Ingress Controller; traffic to Pod is HTTP.
- **Passthrough Termination:** TLS terminates at the Pod; Ingress Controller routes encrypted TCP.
- **Re-encryption Termination:** TLS terminates at Ingress Controller, which then initiates a new TLS connection to the Pod.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Edge:** Simplifies certificate management (centralized at Ingress). Offloads TLS processing from pods.
- **Passthrough:** Achieves true end-to-end encryption (client to pod). Often required for high security/compliance.
- **Re-encryption:** Ensures traffic is encrypted both externally and internally within the cluster. Balances security and L7 routing capability.

**Implications**

- **Edge:** Traffic between Ingress and Pod is unencrypted. May violate security policies. Allows L7 inspection/routing at Ingress.
- **Passthrough:** Ingress cannot inspect L7 traffic (no path-based routing, header manipulation). Certificate management decentralized to app teams.
- **Re-encryption:** Minor performance overhead (double encryption). Requires certificate management at both Ingress and Pods. Allows L7 inspection/routing.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-13: Default Network Policy (Pod Isolation)

**Architectural Question**
What default network policy will govern pod communication _within_ and _between_ namespaces?

**Issue or Problem**
Default policy sets the baseline security posture for pod network isolation, impacting security risk and developer workflow (need to create explicit allow rules).

**Assumption**
Network segmentation between projects/pods is desired or required.

**Alternatives**

- **Default Open:** All pods can communicate freely across all namespaces.
- **Allow Same-Namespace:** Pods within a namespace can communicate freely; cross-namespace traffic is denied by default.
- **Default Deny (Zero Trust):** All traffic (within and between namespaces) is denied by default.

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Open:** Maximizes ease of deployment/debugging initially. Lowest security.
- **Allow Same-Namespace:** Improves security by isolating projects. Requires explicit `NetworkPolicy` for cross-namespace communication. Good balance for many orgs.
- **Default Deny:** Strongest security (Zero Trust). Requires developers to define explicit allow policies for _all_ required traffic (in-namespace and cross-namespace).

**Implications**

- **Default Open:** No network segmentation. Increases blast radius of compromised pod.
- **Allow Same-Namespace:** Isolates projects. Developers must create policies for intended cross-project traffic.
- **Default Deny:** Strongest security. Significant effort for developers to define/maintain detailed `NetworkPolicy` objects for applications to function.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert

---

## OCP-NET-14: Administrative Network Policy Strategy (Cluster-wide)

**Architectural Question**
Will cluster-scoped administrative network policies (`AdminNetworkPolicy`/`BaselineAdminNetworkPolicy`) enforce baseline security rules above tenant-controlled `NetworkPolicy`?

**Issue or Problem**
Standard `NetworkPolicy` is namespace-scoped, allowing project owners to potentially bypass critical platform security requirements. A cluster-scoped mechanism enables centralized enforcement.

**Assumption**
Cluster uses OVN-Kubernetes CNI (OCP-NET-05). Centralized network policy enforcement is desired.

**Alternatives**

- Implement AdminNetworkPolicy (ANP) - Mandatory Rules
- Implement BaselineAdminNetworkPolicy (BANP) - Default Rules (Overridable)
- Rely Solely on Standard NetworkPolicy (OCP-NET-13)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **ANP:** Enforces mandatory, non-overridable rules (Allow, Deny, Pass actions) for high-priority traffic (control plane, security boundaries). Highest precedence.
- **BANP:** Sets default baseline rules (Allow or Deny) that _can_ be overridden by standard `NetworkPolicy`. Provides a starting point for tenants.
- **Standard Only:** Minimizes complexity, accepting all network rules are managed at namespace level by project owners.

**Implications**

- **ANP/BANP:** Requires rigorous testing to avoid disrupting core platform functions (monitoring, operators). ANP ensures critical rules cannot be bypassed. BANP provides guidance but allows tenant flexibility. Requires OVN-Kubernetes CNI.
- **Standard Only:** Compliance or Zero Trust architectures harder to enforce consistently across all projects. Simpler operationally.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-15: Egress IP Address Strategy

**Architectural Question**
How will outbound traffic from specific pods/projects ensure a predictable source IP address when connecting to external services requiring IP whitelisting?

**Issue or Problem**
External services (databases, legacy APIs) often use firewalls allowing access only from specific source IPs. Default pod egress uses the node IP, which is unpredictable.

**Assumption**
External services require source IP whitelisting.

**Alternatives**

- No Egress IP Configuration
- Egress IP per Project/Namespace
- Egress IP for Specific Pods (via selectors)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Egress IP:** For environments where fixed source IPs aren't needed.
- **Egress IP per Project:** Assigns a static source IP for all outbound traffic from a project. Simplifies external firewall management.
- **Egress IP for Specific Pods:** Provides dedicated egress IP for a pod subset (via labels), allowing fine-grained control.

**Implications**

- **No Egress IP:** Pods egress via unpredictable node IPs.
- **Egress IP per Project:** Requires reserving IPs on the node network. Egress IP must be hosted on a node in the same subnet. Simple for project-wide rules.
- **Egress IP for Specific Pods:** More granular but increases config complexity (labeling pods, managing multiple EgressIP objects).

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-16: Secondary Network Strategy (Multus / SR-IOV)

**Architectural Question**
How will pods connect to additional, specialized networks (e.g., VLANs, high-performance NICs) beyond the primary cluster network?

**Issue or Problem**
Certain apps (Telco, HPC, AI/ML data ingest, legacy systems) require direct access to specific physical, VLAN-based, or high-performance networks.

**Assumption**
Specific workloads require specialized network access.

**Alternatives**

- No Secondary Networks
- Layer 2 CNI Plugin (Macvlan/Ipvlan via Multus)
- SR-IOV Network Device Plugin (via Multus)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Secondary Networks:** Simplest config for standard enterprise apps without specialized connectivity needs.
- **Layer 2 CNI (Macvlan/Ipvlan):** Integrates pods directly into existing physical/VLAN networks, making them L2 citizens on those networks. Uses Multus CNI meta-plugin.
- **SR-IOV Plugin:** Provides pods direct, high-performance access to physical NIC VFs (Virtual Functions), bypassing host network stack. Critical for lowest latency/highest throughput (AI/ML ingest, inference, Telco NFV). Uses Multus.

**Implications**

- **No Secondary Networks:** Cannot host apps with specialized network requirements.
- **Layer 2 CNI:** Requires careful IPAM for the secondary network. Multus manages multiple network attachments (`NetworkAttachmentDefinition` CRs).
- **SR-IOV:** Critical for high-performance AI/ML/Telco. Requires SR-IOV capable NICs on workers. Complex config (BIOS, kernel, SR-IOV Network Operator). Provides near bare-metal network performance to pods.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Infra Leader (for SR-IOV hardware)
- Person: #TODO#, Role: AI/ML Platform Owner (for SR-IOV use case)
