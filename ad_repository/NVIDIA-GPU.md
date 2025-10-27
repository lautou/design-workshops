# NVIDIA GPU Operator

## NVIDIA-GPU-01: GPU Operator Deployment Method

**Architectural Question**
Which method will be used to deploy the NVIDIA GPU Operator onto the OpenShift cluster?

**Issue or Problem**
The GPU Operator manages device drivers, container toolkits, and device plugins, automating the configuration required to utilize NVIDIA GPUs. The deployment method impacts management complexity and flexibility.

**Assumption**
GPUs will be used for AI/ML or high-performance computing workloads.

**Alternatives**

- OperatorHub Deployment
- Manual/Helm Deployment

**Decision**
#TODO: Document the decision.#

**Justification**

- **OperatorHub Deployment:** To simplify management by leveraging the Operator Lifecycle Manager (OLM). The operator's components (drivers, device plugin, etc.) are managed automatically. This is the recommended approach for standard deployments.
- **Manual/Helm Deployment:** The platform team is fully responsible for managing the Helm release, including tracking new versions and performing upgrades manually. This can be more error-prone. This option offers greater customization but substantially increases operational overhead.

**Implications**

- **OperatorHub Deployment:** Relies on OperatorHub availability and may require configuration if the cluster is disconnected (OCP-BASE-5).
- **Manual/Helm Deployment:** Requires careful version tracking to ensure compatibility with the specific RHCOS kernel versions deployed on the cluster.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## NVIDIA-GPU-02: GPU Resource Configuration

**Architectural Question**
How will GPU resources be partitioned or shared among multiple workloads?

**Issue or Problem**
Efficient GPU utilization in multi-tenant environments requires choosing a method (such as MIG or Time Slicing) to safely share GPU resources without conflicts.

**Assumption**
Multiple applications or tenants will share physical GPU hardware.

**Alternatives**

- No Sharing (Exclusive Use)
- Multi-Instance GPU (MIG)
- Time Slicing

**Decision**
#TODO: Document the decision.#

**Justification**

- **No Sharing (Exclusive Use):** To dedicate entire physical GPUs to single workloads, ensuring maximum performance isolation but leading to lower utilization.
- **Multi-Instance GPU (MIG):** To securely partition NVIDIA GPUs into multiple smaller, isolated GPU instances. This is ideal for production workloads requiring guaranteed quality of service and memory isolation.
- **Time Slicing:** To allow multiple containers to share the physical GPU over time, suitable for development or testing workloads where strong isolation is not the primary requirement.

**Implications**

- **Multi-Instance GPU (MIG):** Requires specific GPU hardware (NVIDIA Ampere generation or newer) and specialized configuration via the NVIDIA GPU Operator.
- **Time Slicing:** Easier to configure than MIG but lacks strong hardware isolation, potentially exposing workloads to noisy neighbor issues.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## NVIDIA-GPU-03: GPUDirect Technology Enablement

**Architectural Question**
Which GPUDirect technologies will be enabled to accelerate data transfer?

**Issue or Problem**
For high-performance AI/ML workloads, data transfer between GPUs, network interfaces, and storage can become a bottleneck. GPUDirect technologies can bypass the CPU to accelerate these data paths.

**Assumption**
Extreme performance is required for specific workloads, and the hardware (NICs, Storage) supports GPUDirect.

**Alternatives**

- No GPUDirect
- Enable Specific GPUDirect Technologies

**Decision**
#TODO: Document the decision for each instance.#

**Justification**

- **No GPUDirect:** To maintain a standard network and storage configuration for workloads that do not have extreme performance requirements.
- **Enable Specific GPUDirect Technologies:** To enable one or more complementary technologies (RDMA, P2P, Storage) to meet the demands of high-performance workloads, reducing latency and freeing up CPU cycles.

**Implications**

- **No GPUDirect:** All data transfers will involve the CPU and system memory, which can limit the performance of data-intensive applications.
- **Enable Specific GPUDirect Technologies:** Requires specialized hardware and complex configuration of the GPU Operator, secondary networks (SR-IOV), and potentially storage drivers.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert
- Person: #TODO#, Role: Storage Expert
- Person: #TODO#, Role: AI/ML Platform Owner

---

## NVIDIA-GPU-04: Monitoring Strategy

**Architectural Question**
How will NVIDIA GPU metrics be monitored?

**Issue or Problem**
Standard OpenShift monitoring does not provide detailed, GPU-specific metrics (e.g., GPU utilization, memory temperature, power draw). A specialized solution is needed to collect this data.

**Assumption**
Worker nodes with NVIDIA GPUs will be part of the cluster.

**Alternatives**

- No GPU-specific Monitoring
- Enable DCGM Exporter and Dashboards

**Decision**
#TODO: Document the decision for each instance.#

**Justification**

- **No GPU-specific Monitoring:** To rely only on standard OpenShift monitoring for basic node-level metrics.
- **Enable DCGM Exporter and Dashboards:** To deploy the NVIDIA Data Center GPU Manager (DCGM) components via the GPU Operator. This exposes detailed GPU metrics to the OpenShift Prometheus instance and enables pre-built Grafana dashboards.

**Implications**

- **No GPU-specific Monitoring:** The platform team will have no visibility into the performance or health of the individual GPUs, making it difficult to manage the GPU-accelerated environment effectively.
- **Enable DCGM Exporter and Dashboards:** Requires configuring the GPU Operator to enable the DCGM exporter. OpenShift Monitoring (with User Workload Monitoring) must be configured to scrape these metrics. This provides invaluable insights.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner
