# ODC Noord - Workshops Roadmap

## Week 1: OCP Core Platform

### **Tuesday (Day 1)**

#### **AM Session: Platform Vision & Strategy**

- **Workshop Topic:** Day 1: Platform Vision & Strategy
- **Sub-Topics:**
  - `OCP-BASE-01`: Cluster Isolation Strategy
  - `OCP-BASE-02`: Cloud model
  - `OCP-BASE-03`: Platform infrastructure (Confirming OSP & BM)
  - `OCP-BASE-04`: Cluster Topology (Standard/Compact/SNO)
  - `OCP-BASE-05`: Multi-Site Deployment Strategy (On-Premises)
  - `OCP-BASE-06`: Intra-Site Availability Zone / Failure Domain Strategy
  - `OCP-BASE-07`: Network Connectivity Model (Connected vs. Disconnected)
  - `OCP-BASE-08`: Mirrored images registry (Disconnected Environments)
  - `OCP-BASE-09`: Platform Installation and Upgrade Automation Strategy
  - `GITOPS-01`: Argo CD Instance Model (High Level)
- **Customer Attendees:**
  - Enterprise Architect
  - Infra Leader
  - Security Expert
  - AI/ML Platform Owner
  - Network Expert
  - Storage Expert
- **Red Hat Attendees:**
  - Senior Architect
  - Storage Architect
  - Senior Consultant

#### **PM Session: Installation & Initial Sizing**

- **Workshop Topic:** Day 1: Installation & Initial Sizing
- **Sub-Topics:**
  - `OCP-SEC-01`: FIPS Compliance Requirement # <-- Moved FIPS earlier as it impacts install
  - `OCP-OSP-01`: OCP installation method on OSP infrastructure
  - `OCP-BM-01`: OCP installation method on baremetal infrastructure
  - `OCP-OSP-02`: OpenStack Project Tenancy
  - `OCP-BM-02`: Bare Metal Node Remediation
  - `OCP-BASE-10`: Cluster Sizing Strategy (Nodes, CPU, RAM, GPU)
- **Customer Attendees:**
  - Enterprise Architect
  - Infra Leader
  - AI/ML Platform Owner (for GPU input)
  - Operations Expert
  - Security Expert
- **Red Hat Attendees:**
  - Senior Architect
  - Storage Architect
  - Senior Consultant

### **Wednesday (Day 2)**

#### **AM Session: Networking Deep Dive**

- **Workshop Topic:** Day 2: Networking Deep Dive
- **Sub-Topics:**
  - `OCP-NET-01`: Machine IP Range
  - `OCP-NET-02`: Node IP Address Management (DHCP/Static)
  - `OCP-NET-03`: Pod Network CIDR Selection
  - `OCP-NET-04`: Service Network CIDR Selection
  - `OCP-NET-05`: CNI Plugin Selection (OVN vs Kuryr for OSP)
  - `OCP-NET-06`: Outbound Connectivity (External Firewall/Proxy)
  - `OCP-NET-07`: External Firewall Rule Granularity
  - `OCP-NET-08`: DNS Forwarding Configuration
  - `OCP-NET-09`: Load Balancer Strategy (API & Ingress)
  - `OCP-NET-10`: Ingress Controller Strategy (Default/Dedicated)
  - `OCP-NET-11`: Ingress Controller Replica Count
  - `OCP-NET-12`: SSL/TLS Termination Strategy
  - `OCP-NET-13`: Default Network Policy (Pod Isolation)
  - `OCP-NET-14`: Administrative Network Policy Strategy (Cluster-wide)
  - `OCP-NET-15`: Egress IP Address Strategy
  - `OCP-NET-16`: Secondary Network Strategy (Multus / SR-IOV)
- **Customer Attendees:**
  - Enterprise Architect
  - Network Expert
  - Security Expert
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

#### **PM Session: Storage Deep Dive (ODF)**

- **Workshop Topic:** Day 2: Storage Deep Dive (ODF)
- **Sub-Topics:**
  - `OCP-STOR-01`: Storage Provider Decision (ODF vs. Native vs. Other)
  - `OCP-OSP-04`: OpenStack Storage Integration (Cinder/Manila CSI - Non-ODF PVs)
  - `ODF-BASE-01`: ODF Deployment Approach (Internal vs External)
  - `ODF-OSP-01`: ODF Deployment on OpenStack (Cinder Volume Types)
  - `ODF-OSP-02`: OpenStack Failure Domain and AZ Awareness (for ODF)
  - `ODF-BM-01`: ODF Deployment on Bare Metal (LSO vs LVMS)
  - `ODF-BM-02`: Bare Metal Node and Device Failure Domain Awareness (for ODF)
  - `ODF-BASE-02`: ODF Storage Class Design
  - `ODF-BASE-03`: On-Cluster Object Storage (MCG/NooBaa)
- **Customer Attendees:**
  - Enterprise Architect
  - Storage Expert
  - Infra Leader
- **Red Hat Attendees:**
  - Storage Architect
  - Storage Senior Consultant
  - Senior Consultant

### **Thursday (Day 3)**

#### **AM Session: Security & Governance**

- **Workshop Topic:** Day 3: Security & Governance
- **Sub-Topics:**
  - `OCP-SEC-02`: Compliance Automation Strategy (Compliance Operator) # <-- Compliance after FIPS
  - `OCP-SEC-03`: Identity Provider Selection
  - `OCP-SEC-04`: Identity Provider Group Synchronization
  - `OCP-SEC-05`: Multi-Tenant Identity Provider Integration
  - `OCP-SEC-06`: Security Context Constraint (SCC) / Pod Security Admission (PSA) Policy
  - `OCP-SEC-07`: Admission Control Strategy (Custom Policies)
  - `OCP-SEC-08`: Container Image Trust and Signature Verification
  - `OCP-SEC-09`: Data Protection (etcd) Encryption
  - `OCP-SEC-10`: Centralized Secret Management Integration (GitOps context)
- **Customer Attendees:**
  - Enterprise Architect
  - Security Expert
  - OCP Platform Owner
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

#### **PM Session: Day-2 Operations & Observability**

- **Workshop Topic:** Day 3: Day-2 Operations & Observability
- **Sub-Topics:**
  - `OCP-MGT-01`: Namespace/Project Allocation Strategy
  - `OCP-MGT-02`: RBAC Model (Delegation Strategy) # <-- Moved RBAC here, follows Project Allocation
  - `OCP-MGT-03`: Image Registry Strategy (Application Images)
  - `OCP-MGT-04`: Project Resource Quotas Strategy
  - `OCP-MGT-05`: Platform Backup and Restore Strategy (OADP)
  - `OCP-MON-01`: Monitoring Strategy (Platform vs. UWM)
  - `OCP-MON-02`: Custom Monitoring Stack (Cluster Observability Operator)
  - `LOG-01`: Logging Platform Solution (LokiStack vs. External)
  - `LOG-02`: Log Forwarding
  - `LOG-03`: On-Cluster Log Storage Sizing (LokiStack)
  - `NETOBSERV-01`: Network Observability (Flow Data)
  - `TRACING-01`: Trace Collection and Instrumentation Strategy (OTel)
  - `TRACING-02`: Trace Storage and Aggregation Solution (Tempo)
- **Customer Attendees:**
  - Enterprise Architect
  - Operations Expert
  - OCP Platform Owner
  - Security Expert (for RBAC)
- **Red Hat Attendees:**
  - Senior Architect
  - Storage Architect
  - Senior Consultant

---

## Week 2: OpenShift AI - Data Science

### **Tuesday (Day 4)**

#### **AM Session: AI Platform Intro & Arch**

- **Workshop Topic:** Day 4: AI Platform Intro & Arch
- **Sub-Topics:**
  - `RHOAI-SM-01`: Red Hat OpenShift AI instances and purposes
  - `RHOAI-SM-02`: Red Hat OpenShift AI host OpenShift clusters
  - `RHOAI-SM-03`: Environment connectivity (Aligns with OCP-BASE-07)
  - `RHOAI-SM-04`: Mirror registry (If disconnected - Aligns with OCP-BASE-08)
  - `RHOAI-SM-05`: Identity provider Integration (Aligns with OCP-SEC-03)
  - `RHOAI-SM-06`: User/Group Dashboard Access Configuration
  - `RHOAI-SM-07`: OpenShift AI Namespace Strategy (Core Components)
  - `RHOAI-SM-08`: CA Certificate management
  - `RHOAI-SM-09`: S3 Object Storage Location (Requirement)
  - `RHOAI-SM-10`: Default storage class for RHOAI components (Requirement)
  - `RHOAI-SM-11`: Usage data collection (Telemetry)
  - `RHOAI-SM-12`: Red Hat partner solutions integration
- **Customer Attendees:**
  - Enterprise Architect
  - AI/ML Platform Owner
  - Lead Data Scientist
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

#### **PM Session: Data Science User Environment**

- **Workshop Topic:** Day 4: Data Science User Environment
- **Sub-Topics:**
  - `RHOAI-SM-13`: Data science project allocation strategy (User Namespaces)
  - `RHOAI-SM-14`: Notebook images for data scientists
  - `RHOAI-SM-15`: Required Python packages (for Custom Notebook Images)
  - `RHOAI-SM-16`: Custom notebook images location (Registry)
  - `RHOAI-SM-17`: Workbenches provisioning strategy
  - `RHOAI-SM-18`: code-server workbenches enablement
  - `RHOAI-SM-19`: Cluster Storage (PVC) Sizing for Workbenches
  - `RHOAI-SM-20`: Notebook file storage location (Git vs PVC)
  - `RHOAI-SM-21`: Notebook Git repository structure (if Git used)
- **Customer Attendees:**
  - Enterprise Architect
  - AI/ML Platform Owner
  - Lead Data Scientist
  - ML Engineer
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

### **Wednesday (Day 5)**

#### **AM Session: Data & Accelerator Integration**

- **Workshop Topic:** Day 5: Data & Accelerator Integration
- **Sub-Topics:**
  - `RHOAI-SM-22`: Data sources accessibility (DBs, Lakes, etc.)
  - `RHOAI-SM-23`: NVIDIA GPU Support enablement
  - `NVIDIA-GPU-01`: GPU Operator Deployment Method
  - `NVIDIA-GPU-02`: GPU Resource Configuration (MIG/TimeSlicing)
  - `RHOAI-SM-24`: Intel HPU Accelerator Usage (e.g., Gaudi)
  - `RHOAI-SM-25`: AMD GPU Accelerator Usage (ROCm)
  - `RHOAI-SM-26`: Workbenches on Intel hardware (Optimized Images)
- **Customer Attendees:**
  - Enterprise Architect
  - AI/ML Platform Owner
  - Lead Data Scientist
  - Infra Leader (for accelerators)
  - Network Expert (for data source connectivity)
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

#### **PM Session: Pipelines & Distributed Workloads**

- **Workshop Topic:** Day 5: Pipelines & Distributed Workloads
- **Sub-Topics:**
  - `PIPELINES-01`: Pipeline Strategy and Scope (Tekton vs KFP/RHOAI focus)
  - `RHOAI-SM-27`: Data Science Pipelines enablement (KFP/Tekton)
  - `RHOAI-SM-28`: Pipelines in JupyterLab (Elyra) usage
  - `RHOAI-SM-29`: Pipeline database backend (KFP)
  - `RHOAI-SM-30`: Distributed workloads enablement (Ray/CodeFlare)
  - `RHOAI-SM-31`: Quota management for distributed workloads (Kueue)
  - `RHOAI-SM-32`: Authentication Method for Ray Dashboard
  - `RHOAI-SM-33`: Distributed workloads monitoring (Ray metrics)
- **Customer Attendees:**
  - Enterprise Architect
  - AI/ML Platform Owner
  - ML Engineer
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

### **Thursday (Day 6 - Week 2)**

#### **AM Session: Review & Catch-up**

- **Workshop Topic:** Review & Catch-up
- **Sub-Topics:** (Review ADs from Days 4 & 5, address open questions)
- **Customer Attendees:**
  - Enterprise Architect
  - AI/ML Platform Owner
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

---

## Week 3: OpenShift AI - MLOps

### **Tuesday (Day 7 - Week 3)**

#### **AM Session: Model Serving (KServe)**

- **Workshop Topic:** Day 7: Model Serving (KServe)
- **Sub-Topics:**
  - `RHOAI-SM-34`: Model Serving Platform Selection (KServe vs. Custom)
  - `RHOAI-SM-35`: Authorization provider for KServe Model Serving (Authorino)
  - `RHOAI-SM-36`: Model-serving runtime for KServe (Caikit/TGIS, OVMS, Triton, vLLM)
  - `RHOAI-SM-37`: NVIDIA NIM Serving Platform Integration
  - `RHOAI-SM-38`: Distributed Inference with LLM-D [TECH-PREVIEW]
- **Customer Attendees:**
  - Enterprise Architect
  - AI/ML Platform Owner
  - ML Engineer
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

#### **PM Session: Serving Architecture & Performance**

- **Workshop Topic:** Day 7: Serving Architecture & Performance
- **Sub-Topics:**
  - `NVIDIA-GPU-03`: GPUDirect Technology Enablement (RDMA/P2P/Storage)
  - Review `OCP-NET-15` (Egress IP) in context of serving
  - Review `OCP-NET-16` (Secondary Networks/SR-IOV) in context of serving
  - Discuss KServe scaling (Autoscaling, Resource requests/limits)
- **Customer Attendees:**
  - Enterprise Architect
  - ML Engineer
  - Operations Expert
  - Network Expert
  - Infra Leader
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

### **Wednesday (Day 8)**

#### **AM Session: Model Monitoring**

- **Workshop Topic:** Day 8: Model Monitoring
- **Sub-Topics:**
  - `RHOAI-SM-39`: Single-model serving platform (KServe) monitoring enablement
  - `RHOAI-SM-40`: NVIDIA NIM Metrics collection
  - `RHOAI-SM-41`: TrustyAI Monitoring for Data Science Models (Fairness/Explainability)
  - `NVIDIA-GPU-04`: NVIDIA DCGM Monitoring Strategy (GPU Metrics)
- **Customer Attendees:**
  - Enterprise Architect
  - ML Engineer
  - Operations Expert
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

#### **PM Session: Model & Platform Lifecycle Management**

- **Workshop Topic:** Day 8: Model & Platform Lifecycle Management
- **Sub-Topics:**
  - `GITOPS-02`: Platform GitOps Deployment Scope (Multi-cluster GitOps)
  - `GITOPS-03`: Repository Structure (Focus on MLOps artifacts)
  - `GITOPS-04`: Secret Management Strategy (Focus on MLOps secrets)
  - Review `PIPELINES-02`/`03`/`04` (Tekton concepts applied to MLOps CI/CD if used)
  - `RHOAI-SM-42`: Persistent Volume Claim (PVC) Backup Strategy for RHOAI (Revisit)
  - Discuss RHOAI Upgrade Strategy (Operator lifecycle)
  - Discuss Model Registry integration/strategy (if enabled)
- **Customer Attendees:**
  - Enterprise Architect
  - AI/ML Platform Owner
  - Lead Data Scientist
  - ML Engineer
  - Operations Expert
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant

### **Thursday (Day 9)**

#### **AM Session: Final Review & Sign-off**

- **Workshop Topic:** Final Review & Sign-off
- **Sub-Topics:**
  - Review all `#TODO#` ADs
  - Discuss next steps, potential PoCs
  - Address outstanding questions
- **Customer Attendees:**
  - Enterprise Architect
  - AI/ML Platform Owner
- **Red Hat Attendees:**
  - Senior Architect
  - Senior Consultant
