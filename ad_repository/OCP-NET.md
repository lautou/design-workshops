# OpenShift Container Platform networking

## OCP-NET-01: Outbound Firewall Policy

**Architectural Question**
How will egress traffic from the cluster be managed by external firewalls?

**Issue or Problem**
Corporate security policies often require outbound connections to be restricted. This impacts cluster functionality, updates, and access to external services.

**Assumption**
N/A

**Alternatives**

- Firewall with Required Rules
- No Firewall

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Firewall with Required Rules:** To meet strict corporate security requirements by ensuring only necessary ports and protocols are open to approved external destinations (e.g., Red Hat registries).
- **No Firewall:** To simplify setup and provide unrestricted outbound access to all external resources.

**Implications**

- **Firewall with Required Rules:** Requires close collaboration with the network security team to implement and maintain the necessary rules. The list of required sites must be kept up-to-date.
- **No Firewall:** Provides unrestricted outbound access, which simplifies setup but may violate corporate security policies.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-02: Firewall configuration

**Architectural Question**
How will the firewall be configured for the cluster's outbound internet access?

**Issue or Problem**
In a connected environment, the cluster requires access to specific external sites for installation, subscription management, and telemetry. The firewall must be configured to allow this traffic without exposing the cluster to unnecessary security risks.

**Assumption**
N/A

**Alternatives**

- Open Firewall Policy
- Restricted Firewall Policy (Whitelisting required sites)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Open Firewall Policy:** To simplify operations, allowing the cluster broad access to external resources. This is suitable if network security is managed primarily at the proxy level or higher layer firewalls.
- **Restricted Firewall Policy (Whitelisting required sites):** To enforce the principle of least privilege, allowing communication only with documented Red Hat endpoints and required third-party services. This is essential for highly secured or regulated environments.

**Implications**

- **Open Firewall Policy:** Increases the security surface area of the cluster.
- **Restricted Firewall Policy (Whitelisting required sites):** Requires rigorous maintenance to track and update the necessary list of external FQDNs and IP ranges for OpenShift updates and telemetry endpoints. Changes in cloud provider IPs or Red Hat services require immediate firewall rule updates.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-03: Pod Network CIDR Selection

**Architectural Question**
Will the default internal Pod network addressing be used, or will a custom range be specified?

**Issue or Problem**
The Pod network CIDR must not overlap with any existing network reachable from the cluster, otherwise Pod-to-external communication will fail.

**Assumption**
N/A

**Alternatives**

- Default Pod Network CIDR
- Custom Pod Network CIDR

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Pod Network CIDR:** Use the out-of-the-box 10.128.0.0/14 range for simplicity when it is confirmed not to overlap with any existing networks.
- **Custom Pod Network CIDR:** Specify a custom range when the default range is already in use within the network. This ensures that Pod traffic can be correctly routed to and from external services.

**Implications**

- **Default Pod Network CIDR:** Simplifies installation but may require confirmation across the entire enterprise network structure to prevent routing conflicts.
- **Custom Pod Network CIDR:** Requires careful pre-planning and communication with network administrators to select an appropriate, unused IP range.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-04: Node IP Address Management

**Architectural Question**
How will the cluster nodes (Control Plane and Compute) obtain their IP addresses?

**Issue or Problem**
IP Address Management (IPAM) affects the predictability of node addresses, which is critical for infrastructure setup, security policy adherence, and installation method compatibility.

**Assumption**
N/A

**Alternatives**

- DHCP
- Static IP Configuration

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **DHCP:** To simplify node provisioning by automatically assigning IP addresses, which reduces manual configuration effort across all installation methods.
- **Static IP Configuration:** To ensure that nodes have persistent, predictable IP addresses, which is a common requirement for enterprise network and security policies, especially in production environments.

**Implications**

- **DHCP:** Requires a highly available DHCP server with properly configured reservations to ensure nodes retain their IPs. It simplifies adding or replacing nodes.
- **Static IP Configuration:** Increases the manual configuration effort during and after installation (e.g., when scaling the cluster). It requires a robust IP Address Management (IPAM) process to avoid conflicts.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-05: Service SDN IP Range

**Architectural Question**
Which IP address range will be used for the Service network?

**Issue or Problem**
A dedicated, non-overlapping IP range must be allocated for the Service network. If this range conflicts with any existing network CIDRs, cluster services will be unreachable.

**Assumption**
N/A

**Alternatives**

- Default Service Network CIDR
- Custom Service Network CIDR

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Service Network CIDR:** Use the out-of-the-box `172.30.0.0/16` range for simplicity when it is confirmed not to overlap with any existing networks.
- **Custom Service Network CIDR:** Specify a custom range when the default range is already in use. This prevents routing conflicts and ensures services within the cluster can communicate with external networks.

**Implications**

- **Default Service Network CIDR:** Simplifies installation. A failure to verify that this range is free will lead to network connectivity issues for services.
- **Custom Service Network CIDR:** Requires coordination with the network team to select and reserve a suitable IP range. This range must be provided during the installation configuration.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-06: Machine IP Range

**Architectural Question**
Which IP address range will be used for the cluster nodes (machines)?

**Issue or Problem**
The machine network CIDR defines the IP range from which cluster nodes are allocated their addresses. This range must be routable within the organization's network to allow administrative access and communication with infrastructure services (DNS, NTP, etc.).

**Assumption**
N/A

**Alternatives**

- Default Machine Network CIDR
- Custom Machine Network CIDR

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Machine Network CIDR:** Use the out-of-the-box `10.0.0.0/16` range (for IPI on some platforms) when it is available and suitable for the network topology.
- **Custom Machine Network CIDR:** Specify a custom range to align with the existing network segmentation and IP addressing plan. This is required for UPI installations and most enterprise environments.

**Implications**

- **Default Machine Network CIDR:** Only applicable for certain IPI installations. Using this without validation can lead to IP conflicts and prevent nodes from joining the cluster.
- **Custom Machine Network CIDR:** Requires a pre-allocated, routable subnet from the network team. The network must be configured to allow access to and from this range for all necessary infrastructure services.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-07: Load Balancer

**Architectural Question**
Which load balancer solution will be used for exposing cluster services and ingress traffic?

**Issue or Problem**
A choice must be made between using the default, platform-provided load balancer or integrating an existing, user-managed load balancer. This choice affects cost, performance, feature set, and operational responsibility.

**Assumption**
N/A

**Alternatives**

- Default Platform Load Balancer
- User-Managed Load Balancer

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Platform Load Balancer:** To leverage the tightly integrated, automatically configured load balancer. For cloud platforms, this is the provider's native service. For on-premises, this is often a software-based solution (HAProxy/Keepalived).
- **User-Managed Load Balancer:** To utilize an existing enterprise-standard load balancer (e.g., F5, NetScaler) that offers advanced features, meets specific security requirements, and aligns with current operational workflows.

**Implications**

- **Default Platform Load Balancer:** Functionality is limited to what the platform's default load balancer offers. Configuration is managed automatically by OpenShift, which can be simpler but less flexible.
- **User-Managed Load Balancer:** Requires manual configuration and integration. The operations team retains full control and responsibility for the load balancer's lifecycle, but it adds operational overhead.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-08: Default Network Policy

**Architectural Question**
What will be the default cross-namespace network policy implementation strategy?

**Issue or Problem**
The default network policy configuration establishes the security posture regarding inter-project communication and blast radius containment.

**Assumption**
N/A

**Alternatives**

- Default Open (No Policies)
- Allow Same-Namespace by Default
- Default Deny (Zero Trust)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default Open (No Policies):** To maximize ease of deployment and debugging by allowing all pods to communicate across namespaces freely by default.
- **Allow Same-Namespace by Default:** To improve security by isolating projects from each other, requiring developers to explicitly define policies for cross-project traffic.
- **Default Deny (Zero Trust):** To provide the strongest security posture by mandating that developers define explicit allow policies for all required internal and external traffic.

**Implications**

- **Default Open (No Policies):** Offers no network segmentation between projects, increasing the security risk and blast radius of a compromised pod.
- **Allow Same-Namespace by Default:** Improves security by isolating projects from each other. Requires developers to create network policies for any required cross-project communication.
- **Default Deny (Zero Trust):** Provides the strongest security posture but requires significant effort from development teams to define and maintain detailed network policies for their applications to function correctly.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-09: Ingress Controller

**Architectural Question**
Which ingress controller solution will be used for application workload ingress traffic?

**Issue or Problem**
An ingress controller strategy is needed to route external traffic to applications inside the cluster. This decision impacts multi-tenancy, performance isolation, security, and the ability to use custom domain names.

**Assumption**
N/A

**Alternatives**

- Default OpenShift Ingress Controller
- Dedicated OpenShift Ingress Controller
- Third-Party Ingress Controller

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default OpenShift Ingress Controller:** To use the out-of-the-box controller for simplicity. It handles all routes using the default wildcard domain (`*.apps.clustername.domain`).
- **Dedicated OpenShift Ingress Controller:** To create separate ingress controllers for different applications or tenants. This allows the use of custom domains and provides performance and security isolation.
- **Third-Party Ingress Controller:** To integrate a vendor-specific ingress controller (e.g., NGINX) to leverage advanced features or existing expertise.

**Implications**

- **Default OpenShift Ingress Controller:** All application routes share the same ingress controller. This can lead to "noisy neighbor" performance issues and limits domain name flexibility.
- **Dedicated OpenShift Ingress Controller:** Increases cluster resource consumption. It requires additional configuration to create a new controller and to scope routes to it using a custom domain.
- **Third-Party Ingress Controller:** The organization is responsible for the full lifecycle management of the third-party controller. It provides domain flexibility but requires manual integration.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-NET-10: Number of ingress controller replicas

**Architectural Question**
How many replicas of each ingress controller will be deployed?

**Issue or Problem**
The number of ingress controller replicas determines its high availability and capacity to handle traffic. An insufficient number of replicas can lead to performance bottlenecks or outages.

**Assumption**
N/A

**Alternatives**

- Default Replica Count (2)
- Custom Replica Count

**Decision**
#TODO: Document the decision for each cluster and each ingress controller pool.#

**Justification**

- **Default Replica Count (2):** To use the out-of-the-box configuration, which provides a baseline level of high availability suitable for non-production or low-traffic environments.
- **Custom Replica Count:** To scale the number of replicas up (or down) to match the expected traffic load and meet specific high-availability requirements for production workloads.

**Implications**

- **Default Replica Count (2):** Provides basic redundancy. May not be sufficient to handle high traffic volumes or to survive a multi-node failure without performance degradation.
- **Custom Replica Count:** Allows the ingress tier to be scaled to handle production traffic loads, including bursty traffic from model inference requests. Each replica consumes additional CPU and memory resources.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-NET-11: SSL/TLS Termination

**Architectural Question**
Where will SSL/TLS termination for application traffic occur?

**Issue or Problem**
A decision must be made where to terminate encrypted traffic. This choice impacts security posture, certificate management complexity, and the ability to enforce end-to-end encryption.

**Assumption**
N/A

**Alternatives**

- Edge Termination
- Passthrough Termination
- Re-encryption Termination

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Edge Termination:** To simplify certificate management by centralizing it at the ingress controller. This offloads TLS processing from application pods.
- **Passthrough Termination:** To achieve true end-to-end encryption from the client to the application pod, which is often a requirement for high-security workloads.
- **Re-encryption Termination:** To ensure traffic is encrypted both externally and internally within the cluster. The ingress controller terminates the external TLS session and establishes a new one to the application pod.

**Implications**

- **Edge Termination:** Traffic between the ingress controller and the application pod is unencrypted. This may not be acceptable for all security policies.
- **Passthrough Termination:** The ingress controller cannot inspect L7 traffic, so features like path-based routing or header manipulation are not possible. Certificate management is decentralized to application teams.
- **Re-encryption Termination:** Adds a minor performance overhead due to double encryption. It requires certificate management for both the ingress controller and the application pods.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: AI/ML Platform Owner

---

## OCP-NET-12: DNS Forwarding

**Architectural Question**
How will the cluster's internal DNS resolve external hostnames?

**Issue or Problem**
By default, the in-cluster DNS resolver forwards requests it cannot resolve locally to the upstream DNS servers configured on the nodes. This behavior may need to be overridden to integrate with specific enterprise DNS servers.

**Assumption**
N/A

**Alternatives**

- Default DNS Forwarding
- Override DNS Forwarding

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Default DNS Forwarding:** To use the standard behavior, which is sufficient for environments where the node-level DNS resolvers are correctly configured to reach all necessary internal and external domains.
- **Override DNS Forwarding:** To explicitly direct the cluster's DNS queries to specific corporate DNS servers. This is necessary when the node-level resolvers are not suitable or when fine-grained control over name resolution is required.

**Implications**

- **Default DNS Forwarding:** Relies on the correctness of the underlying infrastructure's network configuration (e.g., DHCP options).
- **Override DNS Forwarding:** The cluster's ability to resolve external names becomes dependent on the availability and correctness of the specified upstream DNS servers. This configuration is managed via the `dns.operator.openshift.io` custom resource.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Network Expert

---

## OCP-NET-13: Egress IP addresses

**Architectural Question**
How will outbound traffic from pods be routed to external services that require a fixed source IP?

**Issue or Problem**
Some external services (e.g., databases, legacy APIs) use firewall rules that allow access only from specific, whitelisted source IP addresses. By default, outbound traffic from a pod can originate from any node in the cluster.

**Assumption**
External services require source IP whitelisting for access.

**Alternatives**

- No Egress IP
- Egress IP per Project
- Egress IP for Specific Pods

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Egress IP:** For environments where fixed source IPs are not required for outbound connections.
- **Egress IP per Project:** To assign a predictable, static source IP address for all outbound traffic originating from a specific project/namespace. This simplifies firewall management for external services.
- **Egress IP for Specific Pods:** To provide a dedicated egress IP for a subset of pods within a project, allowing for fine-grained control over traffic routing.

**Implications**

- **No Egress IP:** Pods will egress using the IP of the node they are running on, which is unpredictable.
- **Egress IP per Project:** Requires reserving a pool of available IP addresses on the node network. The Egress IP must be hosted on a node within the same subnet.
- **Egress IP for Specific Pods:** Offers more granular control but increases configuration complexity, as pods must be labeled to select the correct egress IP object.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Security Expert

---

## OCP-NET-14: Secondary networks

**Architectural Question**
How will pods connect to additional, specialized networks beyond the primary cluster network?

**Issue or Problem**
Certain applications, particularly in Telco, high-performance computing, or those interfacing with legacy systems, require direct access to specific physical or VLAN-based networks.

**Assumption**
Specific workloads require direct access to specialized (e.g., L2 VLAN) or high-performance (e.g., SR-IOV) networks.

**Alternatives**

- No Secondary Networks
- Layer 2 CNI Plugin (Macvlan/Ipvlan)
- SR-IOV Network Device Plugin

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **No Secondary Networks:** To maintain the simplest network configuration for standard enterprise applications that do not have specialized connectivity requirements.
- **Layer 2 CNI Plugin (Macvlan/Ipvlan):** To integrate pods directly into existing physical or VLAN networks, allowing them to function as first-class citizens on those networks.
- **SR-IOV Network Device Plugin:** To provide applications with direct, high-performance access to a physical network interface by bypassing the host's network stack. This is critical for workloads that demand the lowest possible latency and highest throughput.

**Implications**

- **No Secondary Networks:** The platform will not be able to host applications with specialized networking requirements.
- **Layer 2 CNI Plugin (Macvlan/Ipvlan):** Requires careful IP Address Management (IPAM) for the secondary network. The Multus CNI plugin must be used to manage the multiple network attachments for pods.
- **SR-IOV Network Device Plugin:** This is critical for high-performance data ingest for AI/ML or low-latency inference. It requires worker nodes with specific, SR-IOV capable NICs. Configuration is complex, involving BIOS settings, kernel modules, and the SR-IOV Network Operator.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: OCP Platform Owner

---

## OCP-NET-15: Administrative Network Policy Strategy

**Architectural Question**
Will cluster-scoped administrative network policies (AdminNetworkPolicy/BaselineAdminNetworkPolicy) be used to enforce baseline security rules above tenant controls?

**Issue or Problem**
Standard Kubernetes `NetworkPolicy` objects are namespace-scoped, meaning project owners can inadvertently or intentionally bypass critical platform network security requirements. A cluster-scoped mechanism is needed for centralized policy enforcement.

**Assumption**
The cluster uses the OVN-Kubernetes CNI plugin.

**Alternatives**

- Implement AdminNetworkPolicy (ANP)
- Implement BaselineAdminNetworkPolicy (BANP)
- Rely solely on standard NetworkPolicy (OCP-NET-08)

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **Implement AdminNetworkPolicy (ANP):** To enforce mandatory, non-overridable rules (Allow, Deny, Pass actions) for high-priority traffic like control plane communication or security boundaries.
- **Implement BaselineAdminNetworkPolicy (BANP):** To set optional baseline rules (Allow or Deny actions) that can be overridden by users employing standard `NetworkPolicy` objects if customization is required.
- **Rely solely on standard NetworkPolicy (OCP-NET-08):** To minimize complexity, accepting that all network rules are managed at the namespace level by project owners.

**Implications**

- **Implement ANP/BANP:** Requires rigorous testing to ensure policies do not disrupt core platform functionality (e.g., monitoring scraping or operator communication).
- **Rely solely on standard NetworkPolicy (OCP-NET-08):** Compliance or Zero Trust architectures may be difficult to enforce consistently across all projects.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Security Expert
- Person: #TODO#, Role: Network Expert
