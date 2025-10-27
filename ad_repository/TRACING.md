# OpenShift Distributed Tracing

## TRACING-01: Trace Collection and Instrumentation Strategy

**Architectural Question**
What strategy will be used to deploy the Red Hat build of OpenTelemetry Collector (OTC) and instrument applications to send traces?

**Issue or Problem**
A method is needed to automatically or manually inject instrumentation into applications and route the collected telemetry data to the central tracing backend (TRACING-02).

**Assumption**
N/A

**Alternatives**

- Sidecar Injection (OTEL Collector Sidecar Mode)
- Centralized Collector (OTEL Collector Deployment/DaemonSet Mode)

**Decision**
#TODO: Document the decision for application instrumentation and collection deployment.#

**Justification**

- **Sidecar Injection:** To simplify the developer experience by having the OpenTelemetry Collector run as a sidecar in the application pod, automatically receiving data via localhost. This removes the need for application teams to manually configure network endpoints.
- **Centralized Collector (Deployment/DaemonSet Mode):** To consolidate telemetry collection outside of application pods, minimizing resource consumption in the application runtime environment. This requires applications to be configured manually with the correct OTLP endpoint (e.g., `OTEL_EXPORTER_OTLP_ENDPOINT`).

**Implications**

- **Sidecar Injection:** Requires the OpenTelemetry Operator to be configured for sidecar mode and the use of the `sidecar.opentelemetry.io/inject` annotation on application deployments. Increases resource usage slightly within each application pod.
- **Centralized Collector:** Requires configuration of network policies and routing to ensure that application pods can reach the central Collector deployment (Deployment or DaemonSet mode). Requires applications to be instrumented to send data directly to the collector service endpoint.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: AI/ML Platform Owner

---

## TRACING-02: Trace Storage and Aggregation Solution

**Architectural Question**
Which Red Hat Distributed Tracing Platform architecture will be used for trace storage, aggregation, and query?

**Issue or Problem**
A robust and scalable backend system is required to persist trace data collected by the OpenTelemetry Collector (TRACING-01) and enable efficient querying and visualization.

**Assumption**
N/A

**Alternatives**

- TempoStack (Microservices Mode)
- TempoMonolithic (Monolithic Mode) [TECH-PREVIEW]

**Decision**
#TODO: Document the decision for the trace backend architecture.#

**Justification**

- **TempoStack (Microservices Mode):** To deploy a highly available and horizontally scalable tracing backend based on Grafana Tempo, suitable for production workloads and large data volumes. This architecture separates components like the Distributor, Ingester, and Query Frontend for high scalability.
- **TempoMonolithic (Monolithic Mode) [TECH-PREVIEW]:** To deploy a single-container instance containing all Tempo components (Compactor, Distributor, Ingester, Query Frontend). This mode is preferred for small deployments, demonstrations, testing, or as a migration path from the deprecated Jaeger all-in-one deployment.

**Implications**

- **TempoStack (Microservices Mode):** Requires external object storage (e.g., ODF, S3, GCS, Azure Blob Storage) for persistence. Provides separation of resource utilization across multiple components and supports horizontal scaling.
- **TempoMonolithic [TECH-PREVIEW]:** Is a **Technology Preview** feature, meaning it is not supported under production SLAs and does not scale horizontally.
- **General:** Requires the installation of the Tempo Operator. Visualization is achieved through the Jaeger UI exposed via the Query Frontend or the Distributed Tracing UI plugin of the Cluster Observability Operator.

**Agreeing Parties**

- Person: #TODO#, Role: Enterprise Architect
- Person: #TODO#, Role: OCP Platform Owner
- Person: #TODO#, Role: Operations Expert
