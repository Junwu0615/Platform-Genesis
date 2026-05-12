<div align="left">

|*Category*| *Service & Tech Stack*|
|--:|:--|
|*Data Core*| ![OLTP](https://img.shields.io/badge/Architecture-OLTP-red?style=flat-square) ![OLAP](https://img.shields.io/badge/Architecture-OLAP-red?style=flat-square) ![HTAP](https://img.shields.io/badge/Architecture-HTAP-red?style=flat-square)<br>![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![PgAdmin](https://img.shields.io/badge/PgAdmin-336791?style=flat-square&logo=postgresql&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) |
|*Orchestration* | ![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?style=flat-square&logo=apache-airflow&logoColor=white) ![Apache Superset](https://img.shields.io/badge/Apache_Superset-00A699?style=flat-square&logo=apache-superset&logoColor=white) |
|*Event Streaming* | ![Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=flat-square&logo=apache-kafka&logoColor=white) ![MQTT](https://img.shields.io/badge/MQTT-660066?style=flat-square&logo=mqtt&logoColor=white) ![Schema Registry](https://img.shields.io/badge/Schema_Registry-blue?style=flat-square&logo=apache-kafka&logoColor=white) |
|*Lakehouse* | ![Debezium](https://img.shields.io/badge/Debezium-9400D3?style=flat-square&logo=red-hat&logoColor=white) ![Apache Iceberg](https://img.shields.io/badge/Apache_Iceberg-000080?style=flat-square&logo=apache&logoColor=white) ![Apache Flink](https://img.shields.io/badge/Apache_Flink-E6522C?style=flat-square&logo=apache-flink&logoColor=white) |
|*Monitoring* | ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white) ![Loki](https://img.shields.io/badge/Loki-F46800?style=flat-square&logo=grafana&logoColor=white) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white) ![Exporter](https://img.shields.io/badge/Node_Exporter-607D8B?style=flat-square&logo=prometheus&logoColor=white) ![Exporter](https://img.shields.io/badge/Postgres_Exporter-607D8B?style=flat-square&logo=prometheus&logoColor=white) ![PoWA](https://img.shields.io/badge/Tool-PoWA-blueviolet?style=flat-square) |
|*Log Management*| ![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=flat-square&logo=elasticsearch&logoColor=white) ![Logstash](https://img.shields.io/badge/Logstash-005571?style=flat-square&logo=logstash&logoColor=white) ![Kibana](https://img.shields.io/badge/Kibana-005571?style=flat-square&logo=kibana&logoColor=white) |
|*Cloud & Infra*| ![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=google-cloud&logoColor=white) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white) ![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white) ![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat-square&logo=ansible&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) |
|*DevOps & Security* | ![Gitlab](https://img.shields.io/badge/Gitlab-FC6D26?style=flat-square&logo=gitlab&logoColor=white) ![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white) ![Docker Registry](https://img.shields.io/badge/Docker_Registry-2496ED?style=flat-square&logo=docker&logoColor=white) ![Vault](https://img.shields.io/badge/HashiCorp_Vault-6070E1?style=flat-square&logo=hashicorp&logoColor=white) ![Portainer](https://img.shields.io/badge/Portainer-13BEFF?style=flat-square&logo=portainer&logoColor=white) |
|*Other*| <a href='https://github.com/Junwu0615/Platform Genesis'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/Platform Genesis.svg'> ![Debian](https://img.shields.io/badge/Debian-gray?style=flat-square&logo=debian&logoColor=white) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E9433F?style=flat-square&logo=ubuntu&logoColor=white) ![WSL2](https://img.shields.io/badge/WSL2-0078D4?style=flat-square&logo=windows&logoColor=white) ![Windows 11](https://img.shields.io/badge/Windows_11-0078D4?style=flat-square&logo=windows-11&logoColor=white) |

</div>

<br>

## *⭐ Platform Genesis ⭐*

```
* A Cloud-Native Infrastructure Project Focused on Automated Data Platform Engineering. 
* IaC ( Terraform / Ansible ) to Orchestrate a Full-Stack Ecosystem.
* From IoT Ingestion ( Kafka / MQTT ) to Database ( HTAP / [OLTP / OLAP] ) Optimization.
* Full-Stack ( ELK / Grafana / Loki / Prometheus / Superset ) Observability.
```

<br>

### *A.　Project Structure*
|*Project Name*|*Responsibilities*|*Tech Stack*|
|--:|:--|:--|
| [Platform Genesis](https://github.com/Junwu0615/Platform-Genesis) | **Homepage :**<br>Construction Records & Quantitative Testing | - |
| [PG-Infrastructure](https://github.com/Junwu0615/PG-Infrastructure) | **IaC & Automation :**<br>Orchestrates environment lifecycles via<br>Terraform, Ansible, and Makefiles. | `GCP` `K8s` `Terraform` `Ansible`<br>`Docker` `Makefile` |
| [PG-APP-Core](https://github.com/Junwu0615/PG-APP-Core) | **Business & Stream Logic :**<br>Core engine for multi-version factory simulations,<br>stream processing, and data infrastructure optimization. | `Python` |
| [PG-Shared-Lib](https://github.com/Junwu0615/PG-Shared-Lib) | **Core Library :**<br>Provides standardized,<br>high-reusability modules across the ecosystem. | `EntryPoint` `Logger` `MqttServer`<br>`KafkaConsumerManager`<br>`KafkaProducerManager` |
| [PG-Edge-Container](https://github.com/Junwu0615/PG-Edge-Container) | **Edge Deployment :**<br>Lightweight IoT units for data acquisition<br>and real-time MQTT/SQLite HA processing. | `MQTT` `SQLite` |
| [PG-Airflow-DAGs](https://github.com/Junwu0615/PG-Airflow-DAGs) | **Data Orchestration :**<br>Manages ETL pipelines, data lineage,<br>and OLTP-to-OLAP transformations. | `Airflow` `DAGs` |

<br>

### *B.　Current Progress*

<details>
<summary><b><i>　b.1.　Simple </i></b></summary>
<ul>

|**Item**|**Description**|**Time**|
|--:|:--|:--:|
| Create Project | - | 2026-03-20 |
| Add `PostgreSQL` | - | 2026-03-20 |
| Add `Airflow` | for `OLAP` | 2026-03-21 |
| Add `PoWA` | for `Monitoring` | 2026-03-23 |
| Quantitation 1 | Docker Desktop vs. WSL2 | 2026-04-04 |
| Add `Monitoring` | - | 2026-04-04 |
| Add `Portainer` | for `Manage Containers` | 2026-04-11 |
| Terraform | Modularization | 2026-04-20 |
| Ansible | Modularization | 2026-04-20 |
| Add `IoT Platform` | `MQTT Broker` + `Apache Kafka` | 2026-04-25 |
| Add `ELK` | for `Manage Log` | 2026-05-05 |
| K8s | Beginner : `Minikube` | 2026-05-09 |
| K8s | Advanced : `K3d` | 2026-05-10 |
| K8s | Advanced : `K3s` + `VMware` | 2026-05-10 |
| K8s | Bottom Layer : `Kubeadm` + `VMware` | - |
| Quantitation 6 |  `infra` High Availability Comparison Test | - |
| Add `Gitlab` | for `CI` & `Manage Projects` | - |
| Add `Jenkins` | for `CD` | - |
| Add `Docker Registry` | for `CI / CD` & `Manage Images` | - |
| Quantitation 4 | Automated Deployment of the Edge :<br>`Manual` vs. `CD -> Helm` | - |
| Add `Loki` | for `Manage Log` | - |
| Add `Debezium` | Change Data Capture | - |
| Add `Apache Iceberg` | Data Lake | - |
| Add `Apache Flink` | consumer of `CDC` | - |
| Build `Lakehouse` | - | - |
| Quantitation 5 | `OLTP vs OLAP` Core Business<br>Recovery and Evolution :<br>`Direct Read` vs. `MV` vs. `CDC` | - |
| Add `HashiCorp Vault` | Enterprise Key Management System | - |
| Add `Superset` | for `OLAP` | - |
| Quantitation 2 | Workload Benchmark | - |
| Quantitation 3 | OLTP Query Efficiency<br>Optimization ( Index / Partition )<br>`Before` vs. `After` | - |
| K8s | Public Cloud : `GKE` | - |
| Summary | - | - |

</ul>
</details>

<details>
<summary><b><i>　b.2.　Details </i></b></summary>
<ul>

<br>

<details>
<summary><b><i>　b.2.1　Project Journey </i></b></summary>
<ul>

|**Item**|**Description**|**Time**|
|--:|:--|:--:|
| Create Project | - | 2026-03-20 |
| Define Process | - | 2026-03-20 |
| Define Event Story | - | 2026-03-21 |
| Define Project Directory | - | 2026-03-21 |
| Define Table DDL | - | 2026-03-21 |
| Create OLTP DDL ( 6 ) | 3NF | 2026-03-21 |
| Create OLAP DDL ( 5 ) | Star Schema | 2026-04-06 |
| Redefine Project Name | `OLTP-OLAP-Unified-DB`<br>to `Platform Genesis` | 2026-05-08 |
| Project Breakdown | `5` Major Categories | 2026-05-08 |
| Summary | - | - |

</ul>
</details>


<details>
<summary><b><i>　b.2.2　Code </i></b></summary>
<ul>

|**Item**|**Description**|**Time**|
|--:|:--|:--:|
| Script | delete_data.py | 2026-03-24 |
| Script | drop_table.py | 2026-03-24 |
| Script | factory_config.yaml | 2026-03-24 |
| Script | init_factory_data.py | 2026-03-24 |
| Script | simulate_factory_stream.py | 2026-03-24 |
| Single to Batch Insert | batch sending | 2026-03-26 |
| Generate Rigorous<br>Static Data | - | 2026-03-26 |
| Rigorous Calibration<br>of Dynamic Data | 單一機台同時間只允許做一件事 /<br>排隊消化訂單 / 訂單生產週期戳記 | 2026-03-27 |
| Adjusting Contextual | ~~insert machine event :<br>machine_events~~ | 2026-03-28 |
| execute -> execute_batch | batch sending + batch submission :<br>不適用於目前模擬方式 | X |
| Adjusting Contextual | insert machine status :<br>machine_status_logs | 2026-03-30 |
| Increase Data Volume | - | 2026-03-30 |
| Auto Partition | `dags/sql/auto_partition/*` | 2026-04-06 |
| OLTP to OLAP | `dags/sql/*` | 2026-04-06 |
| DAG | Build Coding Style | 2026-04-06 |
| DAG ETL Script | Fan-out Queue Pattern | 2026-04-06 |
| DAG | Try `Param` | 2026-04-07 |
| DAG | Try `Dataset` | 2026-04-08 |
| Docker Compose | Compose Modularization | 2026-04-11 |
| Add Makefile | for `docker-compose` | 2026-04-11 |
| Add Airflow Config UI | `Trigger w/ Config` | 2026-04-18 |
| DAG | update Coding Style | 2026-04-18 |
| Add Makefile | for `terraform + ansible` | 2026-04-19 |
| Terraform | Modularization | 2026-04-20 |
| Ansible | Modularization | 2026-04-20 |
| Simple Simulation | organizing old versions : `v1` | 2026-04-28 |
| Multi-Instance | like real-edge : `v2` | 2026-04-28 |
| MQTT logic | for `cp` | 2026-04-28 |
| Kafka Connect | `source` : producer  | 2026-04-30 |
| Kafka logic | for `inst` | 2026-05-03 |
| Kafka Connect | `sink` : consumers | 2026-05-04 |
| Define the Version Number<br>of each service  | settings to `.env` | 2026-05-05 |
| logging logic | mixed ( `ELK` + `logging` ) | 2026-05-06 |
| Encapsulation Entry | app.py | 2026-05-06 |
| logging logic | Logs Correct Paths<br>Based on Module Calls | 2026-05-07 |
| update `v2` logic | Apply the<br>New Underlying Module | 2026-05-07 |
| Import Shared Lib | - | - |
| DAG | init.py + create_topic.py | - |
| Add `SQLite`<br>to Edge scripts  | Improve the HA<br>of Consumer Transactions | - |
| loki logic | - | - |
| make `v2` Dockerfile | - | - |
| upload images | - | - |
| Add CI script | - | - |
| Add CD script | - | - |
| Grafana Dashboard | `htap_grafana.json` | - |
| Create MV | Materialized View | - |
| Analytical Queries | - | - |
| Security Message :<br>`Message Queue Layer` | Encryption ( `kafka` + `mqtt` ) | - |
| Security Message :<br>`Software Layer` | 非對稱加密 | X |
| `IS_KUBERNETS` | 布林注入強制轉換配置 | X |
| API Service logic | - | X |

</ul>
</details>


<details>
<summary><b><i>　b.2.3　Infra </i></b></summary>
<ul>

|**Item**|**Description**|**Time**|
|--:|:--|:--:|
| Add `PostgreSQL` | - | 2026-03-20 |
| Add `Airflow` | for `OLAP` | 2026-03-21 |
| Add `PoWA` | for `Monitoring` | 2026-03-23 |
| Docker Engine | for `WSL2` | 2026-04-03 |
| Add `Monitoring` | `Postgres Exporter` + `Prometheus` + `Grafana` | 2026-04-04 |
| Add `Monitoring` | `Node Exporter` | 2026-04-05 |
| Add `Portainer` | for `Manage Containers` | 2026-04-11 |
| Add `IoT Platform` | `MQTT Broker` + `Apache Kafka` | 2026-04-25 |
| Add `ELK` | for `Manage Log` | 2026-05-05 |
| K8s | Beginner : `Minikube` | 2026-05-09 |
| K8s | Advanced : `K3d` | 2026-05-10 |
| K8s | Advanced : `K3s` + `VMware` | 2026-05-10 |
| Add `Loki` | for `Manage Log` | - |
| Add `Gitlab` | for `CI` & `Manage Projects` | - |
| Add `Jenkins` | for `CD` | - |
| Add `Docker Registry` | for `CI / CD` & `Manage Images` | - |
| Build `Hierarchical`<br>`Log Management` | `Loki` + `ELK` | - |
| Add `Debezium` | Change Data Capture | - |
| Add `Apache Iceberg` | Data Lake | - |
| Add `Apache Flink` | consumer of CDC | - |
| Build `Lakehouse` | - | - |
| Add `HashiCorp Vault` | Enterprise Key Management System | - |
| Add `Superset` | for `OLAP` | - |
| K8s | Bottom Layer : `Kubeadm` + `VMware` | - |
| K8s | Public Cloud : `GKE` | - |

</ul>
</details>


<details>
<summary><b><i>　b.2.4　Experience </i></b></summary>
<ul>

|**Item**|**Description**|**Time**|
|--:|:--|:--:|
| PoWA Web Login Failed | ⚠️no reason found yet | 2026-03-23 |
| DB Settings | Permission Settings | 2026-03-23 |
| New Role | Migration User | 2026-03-24 |
| PoWA( Running Normally ) | - | 2026-03-30 |
| Try Again PoWA Web | ⚠️very difficult to deal with | 2026-03-30 |
| Fine-tuning<br>PostgreSQL Settings | `shm-size` | 2026-04-01 |
| Grafana Dashboard | Organize Observation Indicators | 2026-04-05 |
| WSL2 Settings | `.wslconfig` | 2026-04-06 |
| Partition Settings | `default_partition` | 2026-04-06 |
| Terraform | Declaration Config : `Docker Provider` | 2026-04-19 |
| Terraform | Config Transfer : `docker-compose` | 2026-04-19 |
| Ansible | node `init` & `config` | 2026-04-19 |
| Terraform vs. Compose | Experience :<br>`狀態管理差異性 ; 復原配置崩潰 ; 提高 HA` | 2026-04-19 |
| Terraform & Ansible | Experience :<br>`Ansible 如何補足 Terraform 的不足` | 2026-04-19 |
| ELK | Experience : `ELK` | 2026-05-05 |
| K8s | Experience :<br>`Pod` `Node` `Helm` `Kubectl`<br>`Deployment` `Service` `Ingress`<br>`Secret` `ConfigMap` `PVC` | 2026-05-09 |
| K8s | Experience : MiniKube | 2026-05-09 |
| K8s | Experience : Ansible 初始化節點 | 2026-05-10 |
| K8s | Experience : K3d | 2026-05-10 |
| K8s | Experience : K3s + VM | 2026-05-10 |
| K8s | Experience : 以 Ping 自動喚醒 VM 防止深度睡眠 | - |
| K8s | Experience : Terraform 安裝基礎設施 ( VM ) | 2026-05-11 |
| K8s | Experience : 簡化 kubectl 指令 | 2026-05-12 |
| K8s | Experience : 非負載平衡服務之後補單元測試 | - |
| K8s | Experience : 橫向擴展 Node | 2026-05-12 |
| K8s | Experience :<br>Filebeat / Fluent Bit ( DaemonSet ) | - |
| K8s | Experience : NFS 儲存機制 ( SQLite ) | - |
| K8s | Experience : Edge & Service 分離標籤 | - |
| K8s | Experience : CI / CD 管道 | - |
| K8s | Experience :<br>`Lens` / `k9s` / `Kubernetes Dashboard` | - |

</ul>
</details>


<details>
<summary><b><i>　b.2.5　Quantitation </i></b></summary>
<ul>

|**Item**|**Description**|**Time**|
|--:|:--|:--:|
| Design Benchmark 1 | Generic DB Benchmark | 2026-03-31 |
| Quantitation 1.1 | 64MB | 2026-03-31 |
| Design Benchmark 2 | Generic DB Benchmark | 2026-04-03 |
| Quantitation 1.2 | Docker Desktop ( 64MB )<br>vs. WSL2 ( 16GB ) | 2026-04-04 |
| Design Benchmark-3 | Workload Benchmark | 2026-04-04 |
| Quantitation 2 | Workload Benchmark | - |
| Quantitation 3 | OLTP Query Efficiency<br>Optimization ( Index / Partition )<br>`Before` vs. `After` | - |
| Quantitation 4 | Automated Deployment of the Edge :<br>`Manual` vs. `CD -> Helm` | - |
| Quantitation 5 | `OLTP vs OLAP` Core Business<br>Recovery and Evolution :<br>`Direct Read` vs. `MV` vs. `CDC` | - |
| Quantitation 6 |  `infra` High Availability Comparison Test | - |


</ul>
</details>


</ul>
</details>


<br>


### *C.　Roadmap*

[//]: # (- ![PNG]&#40;./assets/roadmap.PNG&#41;)

<details>
<summary><b><i>　Project Tree </i></b></summary>
<ul>

```bash
tree -I 'venv|.git|__pycache__|docs|logs|assets|kafka_data'
tree -d -I 'venv|.git|__pycache__|docs|logs|assets|kafka_data'

.
├── PG-APP-Core
│   ├── README.md
│   └── src
│       ├── __init__.py
│       ├── core
│       │   ├── __init__.py
│       │   ├── models
│       │   │   ├── __init__.py
│       │   │   ├── simulator.py
│       │   │   └── sink_format.py
│       │   ├── v1
│       │   │   ├── __init__.py
│       │   │   ├── factory_config.yaml
│       │   │   ├── init_factory_data.py
│       │   │   └── simulate_factory_stream.py
│       │   └── v2
│       │       ├── __init__.py
│       │       ├── api
│       │       │   └── __init__.py
│       │       ├── cp
│       │       │   ├── __init__.py
│       │       │   └── main.py
│       │       ├── factory_config.yaml
│       │       ├── inst
│       │       │   ├── __init__.py
│       │       │   └── main.py
│       │       └── scripts
│       │           ├── __init__.py
│       │           ├── create_topic.py
│       │           ├── init.py
│       │           └── topics_config.json
│       └── scripts
│           ├── __init__.py
│           ├── generic_benchmark
│           │   ├── dashboard_benchmark.sql
│           │   └── olap_benchmark.sql
│           └── sql
│               ├── auto_partition.py
│               ├── delete_data.py
│               └── drop_table.py
├── PG-Airflow-DAGs
│   ├── README.md
│   └── dags
│       ├── OP_SQL.py
│       ├── WF_AUTO_PARTITION.py
│       ├── WF_A_DATASET.py
│       ├── WF_B_DATASET.py
│       ├── WF_CREATE_TABLE.py
│       ├── WF_C_DATASET.py
│       ├── __init__.py
│       ├── configs
│       │   ├── __init__.py
│       │   ├── constants.py
│       │   └── dag_config.py
│       ├── sql
│       │   ├── __init__.py
│       │   ├── auto_partition
│       │   │   ├── fact_production.sql
│       │   │   ├── machine_status_logs.sql
│       │   │   └── production_records.sql
│       │   ├── dim_date.sql
│       │   ├── dim_machine.sql
│       │   ├── dim_product.sql
│       │   ├── fact_machine_status.sql
│       │   ├── fact_production.sql
│       │   └── models
│       │       ├── olap
│       │       │   ├── dim_date.sql
│       │       │   ├── dim_machine.sql
│       │       │   ├── dim_product.sql
│       │       │   ├── fact_machine_status.sql
│       │       │   └── fact_production.sql
│       │       └── oltp
│       │           ├── machine.sql
│       │           ├── machine_events.sql
│       │           ├── machine_status_logs.sql
│       │           ├── product.sql
│       │           ├── production_orders.sql
│       │           └── production_records.sql
│       └── utils
│           ├── __init__.py
│           └── dag_tool.py
├── PG-Edge-Container
│   └── README.md
├── PG-Infrastructure
│   ├── README.md
│   └── infra
│       ├── docker-compose
│       │   ├── Makefile
│       │   ├── ansible
│       │   │   ├── inventory.ini
│       │   │   ├── playbook.yml
│       │   │   └── roles
│       │   │       └── monitoring
│       │   │           ├── handlers
│       │   │           │   └── main.yml
│       │   │           ├── tasks
│       │   │           │   └── main.yml
│       │   │           ├── templates
│       │   │           │   └── prometheus.yml.j2
│       │   │           └── vars
│       │   │               └── main.yml
│       │   ├── docker
│       │   │   ├── airflow
│       │   │   │   ├── deploy_dags.sh
│       │   │   │   └── docker-compose.yaml
│       │   │   ├── elk
│       │   │   │   ├── docker-compose.yaml
│       │   │   │   ├── elasticsearch.yaml
│       │   │   │   └── logstash
│       │   │   │       ├── logstash.yaml
│       │   │   │       └── pipeline
│       │   │   │           └── logstash.conf
│       │   │   ├── iot-platform
│       │   │   │   ├── config
│       │   │   │   │   ├── connectors
│       │   │   │   │   │   ├── sink
│       │   │   │   │   │   │   ├── sink-inst-prod-orders.json
│       │   │   │   │   │   │   ├── sink-inst-prod-records.json
│       │   │   │   │   │   │   └── sink-inst-status-logs.json
│       │   │   │   │   │   └── source
│       │   │   │   │   │       └── source-cp-mach-order.json
│       │   │   │   │   └── mosquitto.conf
│       │   │   │   ├── dockerfile
│       │   │   │   │   └── Dockerfile.kafka
│       │   │   │   ├── kafka-compose.yaml
│       │   │   │   └── mqtt-compose.yaml
│       │   │   ├── monitoring
│       │   │   │   ├── docker-compose.yaml
│       │   │   │   ├── htap_grafana.json
│       │   │   │   └── prometheus.yaml
│       │   │   ├── portainer
│       │   │   │   └── docker-compose.yaml
│       │   │   ├── postgresql
│       │   │   │   ├── Dockerfile
│       │   │   │   ├── docker-compose.yaml
│       │   │   │   └── init
│       │   │   │       └── init.sql
│       │   │   └── powa
│       │   │       ├── Dockerfile
│       │   │       ├── docker-compose.yaml
│       │   │       └── init
│       │   │           └── powa.sql
│       │   ├── docker-compose.yaml
│       │   ├── terraform
│       │   │   ├── main.tf
│       │   │   ├── modules
│       │   │   │   ├── docker_container
│       │   │   │   │   ├── main.tf
│       │   │   │   │   ├── outputs.tf
│       │   │   │   │   └── variables.tf
│       │   │   │   ├── monitoring
│       │   │   │   │   ├── main.tf
│       │   │   │   │   ├── outputs.tf
│       │   │   │   │   └── variables.tf
│       │   │   │   └── portainer
│       │   │   │       ├── main.tf
│       │   │   │       ├── outputs.tf
│       │   │   │       └── variables.tf
│       │   │   ├── outputs.tf
│       │   │   ├── terraform.tfvars
│       │   │   └── variables.tf
│       │   └── wsl2
│       ├── gcp
│       ├── k3d
│       │   ├── Makefile
│       │   ├── app
│       │   │   ├── app.py
│       │   │   └── dockerfile
│       │   │       └── Dockerfile.app
│       │   └── helm
│       │       └── app-stack
│       │           ├── Chart.yaml
│       │           ├── templates
│       │           │   ├── app
│       │           │   │   └── app-deploy.yaml
│       │           │   ├── configmap.yaml
│       │           │   ├── db-pvc.yaml
│       │           │   ├── ingress.yaml
│       │           │   ├── portainer
│       │           │   │   ├── portainer-deploy.yaml
│       │           │   │   └── portainer-service.yaml
│       │           │   ├── postgres
│       │           │   │   ├── db-deploy.yaml
│       │           │   │   └── db-service.yaml
│       │           │   └── secret.yaml
│       │           ├── values-dev.yaml
│       │           ├── values-prod.yaml
│       │           └── values.yaml
│       ├── k3s
│       │   ├── Makefile
│       │   ├── ansible
│       │   │   ├── ansible.cfg
│       │   │   ├── hosts.ini
│       │   │   └── scripts
│       │   │       ├── deploy_k3s.yml
│       │   │       ├── init_nodes.yml
│       │   │       └── power_manage.yml
│       │   ├── app
│       │   │   ├── app.py
│       │   │   └── dockerfile
│       │   │       └── Dockerfile.app
│       │   ├── helm
│       │   │   └── app-stack
│       │   │       ├── Chart.yaml
│       │   │       ├── templates
│       │   │       │   ├── app
│       │   │       │   │   └── app-deploy.yaml
│       │   │       │   ├── configmap.yaml
│       │   │       │   ├── db-pvc.yaml
│       │   │       │   ├── ingress.yaml
│       │   │       │   ├── portainer
│       │   │       │   │   ├── portainer-deploy.yaml
│       │   │       │   │   └── portainer-service.yaml
│       │   │       │   ├── postgres
│       │   │       │   │   ├── db-deploy.yaml
│       │   │       │   │   └── db-service.yaml
│       │   │       │   └── secret.yaml
│       │   │       ├── values-dev.yaml
│       │   │       ├── values-prod.yaml
│       │   │       └── values.yaml
│       │   └── terraform
│       ├── kubeadm
│       └── minikube
│           ├── Makefile
│           ├── app
│           │   ├── app.py
│           │   └── dockerfile
│           │       └── Dockerfile.app
│           ├── helm
│           │   └── app-stack
│           │       ├── Chart.yaml
│           │       ├── templates
│           │       │   ├── app
│           │       │   │   └── app-deploy.yaml
│           │       │   ├── configmap.yaml
│           │       │   ├── db-pvc.yaml
│           │       │   ├── ingress.yaml
│           │       │   ├── portainer
│           │       │   │   ├── portainer-deploy.yaml
│           │       │   │   └── portainer-service.yaml
│           │       │   ├── postgres
│           │       │   │   ├── db-deploy.yaml
│           │       │   │   └── db-service.yaml
│           │       │   └── secret.yaml
│           │       ├── values-dev.yaml
│           │       ├── values-prod.yaml
│           │       └── values.yaml
│           └── k8s-manifests
├── PG-Shared-Lib
│   ├── README.md
│   ├── requirements.txt
│   └── shared
│       ├── __init__.py
│       ├── configs
│       │   ├── __init__.py
│       │   ├── constant.py
│       │   └── settings.py
│       ├── modules
│       │   ├── __init__.py
│       │   ├── entry.py
│       │   ├── kafka_consumer.py
│       │   ├── kafka_producer.py
│       │   ├── log.py
│       │   └── mqtt.py
│       └── utils
│           ├── __init__.py
│           ├── env_config.py
│           ├── postgres_tools.py
│           └── tools.py
└── Platform-Genesis
    ├── LICENSE
    ├── Makefile
    └── README.md
```

</ul>
</details>

<br>



### *D.　Quantitation*
- #### *d.1.　[透過通用工具進行資料庫極限測試](./docs/generic_benchmark.md)*
- #### *d.2.　[透過監控系統觀察業務系統瓶頸](./docs/workload_benchmark.md)*
- #### *d.3.　優化查詢 [ 前 / 後 ] 比較測試 ( Index / Partition )*
- #### *d.4.　邊緣裝置部署效率測試 ( `Manual` vs. `CD -> Helm` )*
- #### *d.5.　資料庫核心業務解套演進 ( `Direct Read` vs. `MV` vs. `CDC` )*
- #### *d.6.　基礎設施高可用性測試*


<br>

### *E.　Summary*

<br>



### *F.　Notice*
- #### *f.1.　[OLTP-OLAP-Unified-DB](./docs/oltp-olap-unified-db.md)*
- #### *f.2.　[SQL Implement](./docs/sql_implement.md)*


<br><br><br>