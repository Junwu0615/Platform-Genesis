# ⭐ Platform Genesis

![PNG](./assets/png/roadmap_01.png)

> **Platform Engineering Learning Sprint (2026-03 ~ Present)**
>
> A self-built platform engineering environment focused on infrastructure automation, Kubernetes operations, GitOps delivery, observability, and quantitative validation.
>
> The project evolved from an OLTP/OLAP data platform initiative into a broader platform engineering practice emphasizing reliability, governance, recovery, and operational standardization.

---

# 🚀 Key Achievements

### Infrastructure Automation

* Built repeatable infrastructure provisioning using Terraform and Ansible
* Automated Kubernetes cluster bootstrap and node lifecycle management
* Implemented multi-master K3s architecture with HA control plane

### GitOps Delivery

* Implemented GitLab CI + ArgoCD deployment workflow
* Adopted Layered GitOps and App-of-Apps architecture
* Established deployment governance and drift control validation

### Observability

* Metrics: Prometheus
* Logging: Loki + ELK
* Tracing: Tempo
* Visualization: Grafana

### Reliability Engineering

* Node failure recovery validation
* Workload recovery validation
* Control plane resiliency validation
* GitOps recovery validation
* Deployment governance validation

---

# 📊 Platform Engineering Deliverables (PED)

| ID     | Deliverable                                     | Status |
| ------ | ----------------------------------------------- | ------ |
| PED-1  | Database RBAC Validation                        | ✅      |
| PED-2  | Environment Benchmark                           | ✅      |
| PED-3  | OLTP-OLAP Consolidation Strategy                | 🚧     |
| PED-4  | Query Performance Optimization                  | 🚧     |
| PED-5  | Core Data Architecture Evolution                | 🚧     |
| PED-6  | Application Workload Analysis                   | 🚧     |
| PED-7  | Deployment Delivery Baseline                    | ✅      |
| PED-8  | Kubernetes Resiliency & Availability Validation | ✅      |
| PED-9  | Observability Platform Validation               | 🚧     |
| PED-10 | Vault Secret Management & Distribution          | 🚧     |
| PED-11 | End-to-End DevOps Operating Model               | ✅      |
| PED-12 | GitOps Deployment Governance Validation         | ✅      |

---

# 🏗 Architecture Domains

| Domain             | Technologies                        |
| ------------------ | ----------------------------------- |
| Infrastructure     | Terraform, Ansible, VMware, Libvirt |
| Container Platform | Docker, Kubernetes, K3s             |
| GitOps             | GitLab CI, ArgoCD                   |
| Observability      | Prometheus, Grafana, Loki, Tempo    |
| Data Platform      | PostgreSQL, Airflow                 |
| Event Streaming    | Kafka, MQTT                         |
| Security           | Vault                               |
| Future Expansion   | Debezium, Iceberg, Flink, MinIO     |

---

# 📁 Repository Structure

| Repository        | Purpose                             |
| ----------------- | ----------------------------------- |
| PG-Infrastructure | Infrastructure as Code & Automation |
| PG-APP-Core       | Business Logic & Simulation Engine  |
| PG-Shared-Lib     | Shared Framework Components         |
| PG-Edge-Container | Edge Runtime Deployment             |
| PG-Airflow-DAGs   | Data Orchestration                  |

---

# 🔍 Engineering Highlights

### Kubernetes

* Multi-master control plane
* Lease re-election validation
* Affinity / Anti-affinity scheduling
* HPA scaling validation
* NFS-backed persistent workloads

### GitOps

* App-of-Apps architecture
* ApplicationSet automation
* Environment-based deployment model
* Drift detection and reconciliation

### Infrastructure

* Terraform modularization
* Ansible role-based architecture
* Automated VM provisioning
* HA cluster bootstrap

---

# 📚 Further Reading

### Platform Evolution

Detailed implementation records, architecture evolution, infrastructure journey, engineering challenges, and construction history:

👉 **[Platform Evolution & Full Project History](./docs/platform-evolution.md)**

### Validation Reports

All Platform Engineering Deliverables (PED):

👉 **[docs/](./docs/)**

---

# Lessons Learned

Building individual technologies is relatively straightforward.

Building a maintainable platform that integrates infrastructure automation, Kubernetes operations, GitOps workflows, observability, security, and recovery validation is significantly more challenging.

The project gradually shifted from technology exploration toward operational standardization, reliability engineering, and platform governance.

As a result, the current focus is no longer adding technologies, but improving resiliency, reducing operational complexity, and establishing production-oriented engineering practices.

---

> ⛏ Platform Genesis v1.0 — Platform Foundation Release
>
> 🚀 Platform Genesis v2.0 — Lakehouse & Platform Expansion
