## *⭐ Platform Genesis ⭐*

![PNG](./assets/png/roadmap_01.png)


<br>


```mermaid
gantt
    title Platform Genesis Evolution

    dateFormat YYYY-MM

    section Phase 1
    OLTP-OLAP Consolidation Strategy            :done, a1, 2026-03, 1M

    section Phase 2
    Technology Exploration                      :done, a2, 2026-03, 2M

    section Phase 3
    Construction Logic & Standardization        :done, a3, 2026-03, 2M

    section Phase 4
    Kubernetes & GitOps                         :done, a4, 2026-05, 2M

    section Phase 5
    HA & DR & Validation                        :active, a5, 2026-06, 1M

    section Phase 6
    Lessons Learned & Scope Control             :active, a6, 2026-06, 1M

    section Phase 7
    Resume & Job Search                         :milestone, a7, 2026-07, 1d

    section Future
    Lakehouse                                   :crit, a8, 2026-07, 1M
```

> ##### *Platform Engineering Learning Sprint ( Mar 2026 – Present )*
>
> ##### *A self-built platform engineering environment focused on infrastructure automation, Kubernetes operations, GitOps delivery, observability, and quantitative validation. The project evolved from an OLTP/OLAP data platform initiative into a broader platform engineering practice emphasizing reliability, governance, recovery, and operational standardization.*

<br>

## *🚀　Key Achievements*

- ### *Infrastructure Automation*
  * #### *Built repeatable infrastructure provisioning using Terraform and Ansible*
  * #### *Automated Kubernetes cluster bootstrap and node lifecycle management*
  * #### *Implemented multi-master K3s architecture with HA control plane*

- ### *GitOps Delivery*
  * #### *Implemented GitLab CI + ArgoCD deployment workflow*
  * #### *Adopted Layered GitOps and App-of-Apps architecture*
  * #### *Established deployment governance and drift control validation*

- ### *Observability*
  * #### *Metrics: Prometheus*
  * #### *Logging: Loki + ELK*
  * #### *Tracing: Tempo*
  * #### *Visualization: Grafana*

- ### *Reliability Engineering*
  * #### *Node failure recovery validation*
  * #### *Workload recovery validation*
  * #### *Control plane resiliency validation*
  * #### *GitOps recovery validation*
  * #### *Deployment governance validation*

<br>

## *📊　Platform Engineering Deliverables ( PED )*

| ID | Deliverable | Status |
|:--|:-- |:--:|
| [PED-1](./docs/DB-RBAC.md) | *Database RBAC* | ✅ |
| [PED-2](./docs/Database-Environment-Benchmark.md) | *Database Environment Benchmark* | ✅ |
| [PED-3](./docs/OLTP-OLAP-Consolidation-Strategy.md) | *OLTP-OLAP Consolidation Strategy* | 🚧 |
| [PED-4](./docs/Database-Query-Performance-Optimization.md) | *Database Query Performance Optimization* | 🚧 |
| [PED-5](./docs/Evolution-of-Core-Data-Architecture.md) | *Core Data Architecture Evolution* | 🚧 |
| [PED-6](./docs/Application-Workload-Performance-Analysis.md) | *Application Workload Analysis* | 🚧 |
| [PED-7](./docs/Deployment-Delivery-Baseline.md) | *Deployment Delivery Baseline* | ✅ |
| [PED-8](./docs/K8s-Resiliency-Availability-Validation.md) | *Kubernetes Resiliency & Availability Validation* | ✅ |
| [PED-9](./docs/Observability-Platform-Validation.md) | *Observability Platform Validation* | 🚧 |
| [PED-10](./docs/Vault.md) | *Vault Secret Management & Distribution* | 🚧 |
| [PED-11](./docs/End-to-End-DevOps-Operating-Model.md) | *End-to-End DevOps Operating Model* | ✅ |
| [PED-12](./docs/GitOps-Deployment-Governance-Validation.md) | *GitOps Deployment Governance Validation* | ✅ |

<br>

## *🏗　Architecture Domains*

[//]: # (| Domain | Technologies |)

[//]: # (| :-- | -- |)

[//]: # (| Infrastructure | `Terraform` `Ansible` `VMware` `Libvirt` |)

[//]: # (| Container Platform | `Docker` `Kubernetes` `K3s` |)

[//]: # (| GitOps | `GitLab CI` `ArgoCD` |)

[//]: # (| Observability | `Prometheus` Grafana` `Loki` `Tempo` |)

[//]: # (| Data Platform | `PostgreSQL` `Airflow` |)

[//]: # (| Event Streaming | `Kafka` `MQTT` |)

[//]: # (| Security | `Vault` |)

[//]: # (| Future Expansion | `Debezium` `Iceberg` `Flink` `MinIO` |)

<div align="left">

|*Category*| *Service & Tech Stack*|
|--:|:--|
|*Data Core*| ![OLTP](https://img.shields.io/badge/Architecture-OLTP-red?style=flat-square) ![OLAP](https://img.shields.io/badge/Architecture-OLAP-red?style=flat-square) ![HTAP](https://img.shields.io/badge/Architecture-HTAP-red?style=flat-square)<br>![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) |
|*Orchestration* | ![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?style=flat-square&logo=apache-airflow&logoColor=white) ![Apache Superset](https://img.shields.io/badge/Apache_Superset-00A699?style=flat-square&logo=apache-superset&logoColor=white) |
|*Event Streaming* | ![Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=flat-square&logo=apache-kafka&logoColor=white) ![MQTT](https://img.shields.io/badge/MQTT-660066?style=flat-square&logo=mqtt&logoColor=white) ![Schema Registry](https://img.shields.io/badge/Schema_Registry-blue?style=flat-square&logo=apache-kafka&logoColor=white) |
|*Lakehouse* | ![Debezium](https://img.shields.io/badge/Debezium-9400D3?style=flat-square&logo=red-hat&logoColor=white) ![Apache Iceberg](https://img.shields.io/badge/Apache_Iceberg-000080?style=flat-square&logo=apache&logoColor=white) ![Apache Flink](https://img.shields.io/badge/Apache_Flink-E6522C?style=flat-square&logo=apache-flink&logoColor=white) ![MinIO](https://img.shields.io/badge/MinIO-C72E2E?style=flat-square&logo=MinIO&logoColor=white) |
|*Monitoring* | ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white) ![Loki](https://img.shields.io/badge/Loki-F46800?style=flat-square&logo=grafana&logoColor=white) ![Tempo](https://img.shields.io/badge/Tempo-F46800?style=flat-square&logo=grafana&logoColor=white) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white) |
|*Log Management*| ![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=flat-square&logo=elasticsearch&logoColor=white) ![Logstash](https://img.shields.io/badge/Logstash-005571?style=flat-square&logo=logstash&logoColor=white) ![Kibana](https://img.shields.io/badge/Kibana-005571?style=flat-square&logo=kibana&logoColor=white) |
|*Cloud & Infra*| ![GKE](https://img.shields.io/badge/GKE-4285F4?style=flat-square&logo=google-cloud&logoColor=white) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white) ![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white) ![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat-square&logo=ansible&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) |
|*DevOps & Security* | ![Gitlab](https://img.shields.io/badge/Gitlab-FC6D26?style=flat-square&logo=gitlab&logoColor=white) ![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=flat-square&logo=Argo&logoColor=white) ![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white) ![Docker Registry](https://img.shields.io/badge/Docker_Registry-2496ED?style=flat-square&logo=docker&logoColor=white) ![Vault](https://img.shields.io/badge/HashiCorp_Vault-6070E1?style=flat-square&logo=hashicorp&logoColor=white) ![Portainer](https://img.shields.io/badge/Portainer-13BEFF?style=flat-square&logo=portainer&logoColor=white) |
|*Other*| <a href='https://github.com/Junwu0615/Platform Genesis'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/Platform Genesis.svg'> ![Debian](https://img.shields.io/badge/Debian-gray?style=flat-square&logo=debian&logoColor=white) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E9433F?style=flat-square&logo=ubuntu&logoColor=white) ![WSL2](https://img.shields.io/badge/WSL2-0078D4?style=flat-square&logo=windows&logoColor=white) ![Windows 11](https://img.shields.io/badge/Windows_11-0078D4?style=flat-square&logo=windows-11&logoColor=white) |

</div>

<br>

## *📁　Repository Structure*

| Repository | Purpose |
| :-- | :-- |
| [*PG-Infrastructure*](https://github.com/Junwu0615/PG-Infrastructure) |  *Infrastructure as Code & Automation* |
| [*PG-APP-Core*](https://github.com/Junwu0615/PG-APP-Core) |  *Business Logic & Simulation Engine*  |
| [*PG-Shared-Lib*](https://github.com/Junwu0615/PG-Shared-Lib) |  *Shared Framework Components* |
| [*PG-Edge-Container*](https://github.com/Junwu0615/PG-Edge-Container) |  *Edge Runtime Deployment* |
| [*PG-Airflow-DAGs*](https://github.com/Junwu0615/PG-Airflow-DAGs) |  *Data Orchestration* |

<br>

## *🔍　Engineering Highlights*

- ### *Kubernetes*
  * #### *Multi-master control plane*
  * #### *Lease re-election validation*
  * #### *Affinity / Anti-affinity scheduling*
  * #### *HPA scaling validation*
  * #### *NFS-backed persistent workloads*

- ### *GitOps*
  * #### *App-of-Apps architecture*
  * #### *ApplicationSet automation*
  * #### *Environment-based deployment model*
  * #### *Drift detection and reconciliation*

- ### *Infrastructure*
  * #### *Terraform modularization*
  * #### *Ansible role-based architecture*
  * #### *Automated VM provisioning*
  * #### *HA cluster bootstrap*

<br>

## *⚖️　Lessons Learned & Evolution*
> *Platform Genesis began as an attempt to address a practical data*
> *infrastructure challenge: consolidating OLTP and OLAP workloads*
> *into a unified architecture.*
>
> *As the project evolved, the scope naturally expanded beyond data*
> *engineering into infrastructure automation, Kubernetes operations,*
> *GitOps workflows, observability, secret management, and reliability*
> *validation.*
>
> *Through continuous implementation and validation, the project*
> *gradually shifted from technology exploration toward architecture*
> *convergence and operational standardization.*
>
> *The most important lesson learned was that building individual*
> *components is relatively straightforward; integrating them into a*
> *maintainable, highly available, and operationally sustainable*
> *platform is significantly more challenging.*
>
> *As a result, the current focus has shifted from expanding the*
> *technology stack to improving reliability, reducing operational*
> *complexity, and establishing production-oriented engineering*
> *practices.*

<br>

> *⛏　Platform Genesis v1.0　|　Platform Foundation Release　|　Status: In Progress*
>
> *🚀　Platform Genesis v2.0　|　Data Platform & Lakehouse Expansion　|　Status: Future Work*
> 
> *📚　Further Reading　|　[Platform Evolution & Full Project History](./docs/Platform-Evolution.md)*

[//]: # (> *⛏　Platform Genesis v1.0　|　Platform Foundation Release　|　Status: Feature Complete &#40; 2026-07 &#41;*)


<br><br><br>