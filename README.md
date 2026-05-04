<a href='https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/OLTP-OLAP-UNIFIED-DB.svg'>
[![](https://img.shields.io/badge/Operating_System-Windows_11-blue.svg?style=plastic)](https://www.microsoft.com/zh-tw/software-download/windows10) <br> 
[![](https://img.shields.io/badge/Technology-Python-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-PostgreSQL-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-GCP-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) 
[![](https://img.shields.io/badge/Technology-Kubernetes-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) 
[![](https://img.shields.io/badge/Technology-Docker-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>
[![](https://img.shields.io/badge/Technology-OLTP-critical.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-OLAP-critical.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-HTAP-critical.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-Terraform-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-Ansible-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>
[![](https://img.shields.io/badge/Technology-Grafana-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) 
[![](https://img.shields.io/badge/Technology-Prometheus-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) 
[![](https://img.shields.io/badge/Technology-PoWA-inactive.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>
[![](https://img.shields.io/badge/Technology-Apache_Kafka-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-MQTT-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-Apache_Airflow-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>

<br>

## *⭐ OLTP-OLAP-Unified-DB ⭐*

Simulating HTAP workload using a single PostgreSQL instance with schema isolation, analyzing contention between transactional and analytical queries.
```
* Database architecture should be driven by workload.
 ↪︎ * Workload defines query patterns.
 ↪︎ * Query patterns define schema design.
 ↪︎ * Schema design defines indexing and storage strategy.


OLTP 與 OLAP 的本質差異不在【 資料結構 】，而在【 工作負載 】； Schema 設計只是為了【 服務該負載 】的結果。
```

<br>

### *A.　Current Progress*

<details open>
<summary><b><i>　Simple </i></b></summary>
<ul>

|**Item**|**Description**|**Time**|
|--:|:--|:--:|
| Create Project | - | 2026-03-20 |
| Add `PostgreSQL` | By Docker | 2026-03-20 |
| Create OLTP DDL ( 6 ) | 3NF | 2026-03-21 |
| Add `Airflow` | By Docker | 2026-03-21 |
| Add `PoWA` | By Docker | 2026-03-23 |
| Generic DB Benchmark | Docker Desktop vs WSL2 | 2026-04-04 |
| Workload Benchmark | Design Benchmark | 2026-04-04 |
| Add `Monitoring` | Postgres Exporter + Prometheus + Grafana | 2026-04-04 |
| Add `Monitoring` | Node Exporter | 2026-04-05 |
| Create OLAP DDL ( 5 ) | Star Schema | 2026-04-06 |
| Add `Portainer` | By Docker | 2026-04-11 |
| Add Makefile | for `docker-compose` | 2026-04-11 |
| Terraform | Declaration Configuration : `Docker Provider` | 2026-04-19 |
| Terraform | Configuration Transfer : `docker-compose` | 2026-04-19 |
| Ansible | node `initialization` & `configuration` | 2026-04-19 |
| Add Makefile | for `terraform + ansible` | 2026-04-19 |
| Terraform Modularization | - | 2026-04-20 |
| Ansible Modularization | - | 2026-04-20 |
| Add `iot-platform` | MQTT Broker + Apache Kafka | 2026-04-25 |
| Multi-Instance Simulation | like real-edge : `v2` | 2026-04-28 |
| MQTT Logic | for `command_platform` | 2026-04-28 |
| Kafka Connect | `source` : producer  | 2026-04-30 |
| Kafka Logic | for `instance` | 2026-05-03 |
| Kafka Connect | `sink` : consumers | 2026-05-04 |
| API Service Logic | - | - |
| `v2` make Dockerfile | - | - |
| Create Materialized View ( MV ) | - | - |
| Analytical Queries | - | - |
| Kubernetes | Beginner : `Minikube` | - |
| Kubernetes | Advanced : `K3s` + `VMware` | - |
| Kubernetes | Bottom Layer : `Kubeadm` + `VMware` | - |
| Kubernetes | Public Cloud : Google Kubernetes Engine ( `GKE` ) | - |

</ul>
</details>

<details>
<summary><b><i>　Details </i></b></summary>
<ul>

|**Item**|**Description**|**Time**|
|--:|:--|:--:|
| Create Project | - | 2026-03-20 |
| Add `PostgreSQL` | By Docker | 2026-03-20 |
| Define Process | - | 2026-03-20 |
| Define Event Story | - | 2026-03-21 |
| Define Project Directory | - | 2026-03-21 |
| Define Table DDL | - | 2026-03-21 |
| Create OLTP DDL ( 6 ) | 3NF | 2026-03-21 |
| Add `Airflow` | By Docker | 2026-03-21 |
| DB Settings | Permission Settings | 2026-03-23 |
| Add `PoWA` | By Docker | 2026-03-23 |
| PoWA Web Login Failed | ⚠️no reason found yet | 2026-03-23 |
| New Role | Migration User | 2026-03-24 |
| Script | delete_data.py | 2026-03-24 |
| Script | drop_table.py | 2026-03-24 |
| Script | factory_config.yaml | 2026-03-24 |
| Script | init_factory_data.py | 2026-03-24 |
| Script | simulate_factory_stream.py | 2026-03-24 |
| Single to Batch Insert | 批次發送 | 2026-03-26 |
| Generate Rigorous Static Data | - | 2026-03-26 |
| Rigorous Calibration of Dynamic Data | 單一機台同時間只允許做一件事 /<br>排隊消化訂單 / 訂單生產週期戳記 | 2026-03-27 |
| Adjusting Contextual Logic | ~~插入機台事件 : machine_events~~ | 2026-03-28 |
| execute -> execute_batch | 批次發送 + 批次提交 : 不適用於目前模擬方式 | X |
| Adjusting Contextual Logic | 插入機台狀態 : machine_status_logs | 2026-03-30 |
| Increase Data Volume Logic | - | 2026-03-30 |
| PoWA ( Running Normally ) | - | 2026-03-30 |
| Try Again PoWA Web | ⚠️very difficult to deal with | 2026-03-30 |
| Generic DB Benchmark | Design Benchmark-1 | 2026-03-31 |
| Generic DB Benchmark | 64MB | 2026-03-31 |
| Fine-tuning<br>PostgreSQL Docker Settings | `shm-size` | 2026-04-01 |
| WSL2 Startup Docker Engine | - | 2026-04-03 |
| Generic DB Benchmark | Design Benchmark-2 | 2026-04-03 |
| Generic DB Benchmark | Docker Desktop ( 64MB )<br>vs<br>WSL2 ( 16GB ) | 2026-04-04 |
| Workload Benchmark | Design Benchmark | 2026-04-04 |
| Add `Monitoring` | Postgres Exporter + Prometheus + Grafana | 2026-04-04 |
| Add `Monitoring` | Node Exporter | 2026-04-05 |
| Grafana Dashboard | Organize Observation Indicators | 2026-04-05 |
| WSL2 Settings | `.wslconfig` | 2026-04-06 |
| Create OLAP DDL ( 5 ) | Star Schema | 2026-04-06 |
| Partition Settings | `default_partition` | 2026-04-06 |
| Auto Partition | `dags/sql/auto_partition/*` | 2026-04-06 |
| OLTP to OLAP | `dags/sql/*` | 2026-04-06 |
| Build DAGs Coding Style | - | 2026-04-06 |
| DAG ETL Script | Fan-out Queue Pattern | 2026-04-06 |
| DAG | Try `Param` | 2026-04-07 |
| DAG | Try `Dataset` | 2026-04-08 |
| Add `Portainer` | By Docker | 2026-04-11 |
| Docker Compose Profiles | Compose Modularization | 2026-04-11 |
| Add Makefile | for `docker-compose` | 2026-04-11 |
| Add Airflow Config UI | `Trigger w/ Config` | 2026-04-18 |
| Update DAGs Coding Style | - | 2026-04-18 |
| Terraform | Declaration Configuration : `Docker Provider` | 2026-04-19 |
| Terraform | Configuration Transfer : `docker-compose` | 2026-04-19 |
| Ansible | node `initialization` & `configuration` | 2026-04-19 |
| Add Makefile | for `terraform + ansible` | 2026-04-19 |
| Terraform vs. Docker Compose | Experience : `狀態管理差異性 ; 可救回配置崩潰，提高 HA` | 2026-04-19 |
| Terraform & Ansible | Experience : `Ansible 如何補足 Terraform 的不足` | 2026-04-19 |
| Terraform Modularization | - | 2026-04-20 |
| Ansible Modularization | - | 2026-04-20 |
| Add `iot-platform` | MQTT Broker + Apache Kafka | 2026-04-25 |
| Simple Simulation | organizing old versions : `v1` | 2026-04-28 |
| Multi-Instance Simulation | like real-edge : `v2` | 2026-04-28 |
| MQTT Logic | for `command_platform` | 2026-04-28 |
| Kafka Connect | `source` : producer  | 2026-04-30 |
| Kafka Logic | for `instance` | 2026-05-03 |
| Kafka Connect | `sink` : consumers | 2026-05-04 |
| API Service Logic | - | - |
| `v2` make Dockerfile | - | - |
| Grafana Dashboard | update `htap_grafana.json` | - |
| Create Materialized View ( MV ) | - | - |
| Analytical Queries | - | - |
| Kubernetes | Beginner : `Minikube` | - |
| Kubernetes | Advanced : `K3s` + `VMware` | - |
| Kubernetes | Bottom Layer : `Kubeadm` + `VMware` | - |
| Kubernetes | Public Cloud : Google Kubernetes Engine ( `GKE` ) | - |
| K8s | Experience : `Pod` / `Service` / `Ingress` | - |
| K8s | Experience : `Lens` / `k9s` / `Kubernetes Dashboard` | - |

</ul>
</details>


<br>

### *B.　Service*
- #### *I.　Service List*
  |**Service**|**Description**|**Port**|
  |--:|:--|:--:|
  | PostgreSQL | for `Dev` | [5432](http:127.0.0.1:5432) |
  | PostgreSQL | for `Airflow` | [5433](http:127.0.0.1:5433) |
  | PostgreSQL UI Web | - | [5050](http:127.0.0.1:5050) |
  | Airflow | - | [8100](http:127.0.0.1:8100) |
  | ~~PostgreSQL~~ | for `PoWA` | [5431](http:127.0.0.1:5431) |
  | ~~PoWA UI Web~~ | for `PoWA` | [8888](http:127.0.0.1:8888) |
  | MQTT Broker | for `iot-platform` | [1883](http:127.0.0.1:1883) |
  | Kafka | for `iot-platform` | [9092](http:127.0.0.1:9092) |
  | Kafka UI | for `iot-platform` | [9093](http:127.0.0.1:9093) |
  | Schema Registry | for `iot-platform` | [8081](http:127.0.0.1:8081) |
  | Grafana | for `Monitoring` | [3000](http:127.0.0.1:3000) |
  | Prometheus | for `Monitoring` | [9090](http:127.0.0.1:9090) |
  | Node Exporter | for `Monitoring` | [9100](http:127.0.0.1:9100) |
  | Postgres Exporter | for `Monitoring` | [9187](http:127.0.0.1:9187) |
  | Portainer | for `Manage Containers` | [9000](http:127.0.0.1:9000) |


- #### *II.　[Service Startup Order](./docs/service_startup_order.md)*
- #### *III.　[WSL2 Startup Docker Engine](./docs/wsl2_startup_docker_engine.md)*
- #### *IV.　[Terraform & Ansible](./docs/terraform_ansible.md)*
- #### *V.　[About K8s](./docs/k8s.md)*

<br>

### *C.　Command Platform ( Makefile Execute )*

<details>
<summary><b><i>　I.　Docker Compose</i></b></summary>
<ul>

```bash
cd docker-compose

# initialization
make init
make build

# depends on 'Compose' service
make up

# service shutdown
make down
```
</ul>
</details>

<br>

<details>
<summary><b><i>　II.　Terraform + Ansible + Compose </i></b></summary>
<ul>

```bash
cd docker-compose

# initialization
make init
make build
make setup

# depends on 'Compose' service ( Postgresql + Airflow + MQTT + Kafka )
make postgresql
make airflow
make mqtt
make kafka

# depends on 'Terraform' + 'Ansible' services ( Monitoring + Portainer )
make all

# service shutdown
make down
make destroy
```
</ul>
</details>

<br>

<details>
<summary><b><i>　III.　K8s + Helm + Terraform + Ansible </i></b></summary>
<ul>

```bash
...
```
</ul>
</details>

<br>

<details open>
<summary><b><i>　Other </i></b></summary>
<ul>

```bash
# Common
make ps
make prune
make get-chown-all
make list-configs
make refresh

# Airflow
make copy-dag

# Terraform + Ansible
make graph
make infra
make config
make reload

# Kafka Connect
make kafka-connect-create
make kafka-connect-upsert
make kafka-connect-status
make kafka-connect-del
```
</ul>
</details>

<br>

### *D.　Implementation*
- ![PNG](./assets/roadmap.PNG)
- #### *I.　[About SQL Something Detail](./docs/sql.md)*

<details>
<summary><b><i>　II.　Project Tree </i></b></summary>
<ul>

  ```bash
  tree -I 'venv|.git|__pycache__|docs|logs|assets|kafka_data'
  tree -d -I 'venv|.git|__pycache__|docs|logs|assets|kafka_data'

  .
  ├── LICENSE
  ├── README.md
  ├── docker-compose
  │   ├── Makefile
  │   ├── ansible
  │   │   ├── inventory.ini
  │   │   ├── playbook.yml
  │   │   └── roles
  │   │       └── monitoring
  │   │           ├── handlers
  │   │           │   └── main.yml
  │   │           ├── tasks
  │   │           │   └── main.yml
  │   │           ├── templates
  │   │           │   └── prometheus.yml.j2
  │   │           └── vars
  │   │               └── main.yml
  │   ├── docker
  │   │   ├── airflow
  │   │   │   ├── airflow-webserver.pid
  │   │   │   ├── airflow.cfg
  │   │   │   ├── config
  │   │   │   ├── dags
  │   │   │   ├── deploy_dags.sh
  │   │   │   ├── docker-compose.yaml
  │   │   │   ├── plugins
  │   │   │   └── webserver_config.py
  │   │   ├── iot-platform
  │   │   │   ├── config
  │   │   │   │   ├── connectors
  │   │   │   │   │   ├── sink
  │   │   │   │   │   │   ├── sink-inst-prod-orders.json
  │   │   │   │   │   │   ├── sink-inst-prod-records.json
  │   │   │   │   │   │   └── sink-inst-status-logs.json
  │   │   │   │   │   └── source
  │   │   │   │   │       └── source-cp-mach-order.json
  │   │   │   │   ├── mosquitto.conf
  │   │   │   │   └── passwd
  │   │   │   ├── data
  │   │   │   │   └── mqtt_data
  │   │   │   │       └── mosquitto.db
  │   │   │   ├── dockerfile
  │   │   │   │   └── Dockerfile.kafka
  │   │   │   ├── kafka-compose.yaml
  │   │   │   └── mqtt-compose.yaml
  │   │   ├── monitoring
  │   │   │   ├── docker-compose.yaml
  │   │   │   ├── htap_grafana.json
  │   │   │   └── prometheus.yaml
  │   │   ├── portainer
  │   │   │   └── docker-compose.yaml
  │   │   ├── postgresql
  │   │   │   ├── Dockerfile
  │   │   │   ├── docker-compose.yaml
  │   │   │   └── init
  │   │   │       └── init.sql
  │   │   └── powa
  │   │       ├── Dockerfile
  │   │       ├── docker-compose.yaml
  │   │       └── init
  │   │           └── powa.sql
  │   ├── docker-compose.yaml
  │   ├── terraform
  │   │   ├── main.tf
  │   │   ├── modules
  │   │   │   ├── generic_docker_container
  │   │   │   │   ├── main.tf
  │   │   │   │   ├── outputs.tf
  │   │   │   │   └── variables.tf
  │   │   │   ├── monitoring
  │   │   │   │   ├── main.tf
  │   │   │   │   ├── outputs.tf
  │   │   │   │   └── variables.tf
  │   │   │   └── portainer
  │   │   │       ├── main.tf
  │   │   │       ├── outputs.tf
  │   │   │       └── variables.tf
  │   │   ├── outputs.tf
  │   │   ├── terraform.tfstate
  │   │   ├── terraform.tfstate.backup
  │   │   ├── terraform.tfvars
  │   │   └── variables.tf
  │   └── wsl2
  ├── kubernetes
  │   ├── gke
  │   ├── k3s
  │   ├── kubeadm
  │   └── minikube
  ├── requirements.txt
  └── src
      ├── __init__.py
      ├── config
      │   ├── __init__.py
      │   ├── constant.py
      │   ├── mqtt.py
      │   └── sink_format.py
      ├── modules
      │   ├── __init__.py
      │   ├── kafka_producer.py
      │   ├── log.py
      │   ├── mqtt.py
      │   └── simulator.py
      ├── scripts
      │   ├── __init__.py
      │   ├── dags
      │   │   ├── OP_SQL.py
      │   │   ├── WF_AUTO_PARTITION.py
      │   │   ├── WF_A_DATASET.py
      │   │   ├── WF_B_DATASET.py
      │   │   ├── WF_CREATE_TABLE.py
      │   │   ├── WF_C_DATASET.py
      │   │   ├── config
      │   │   │   ├── __init__.py
      │   │   │   ├── constants.py
      │   │   │   └── dag_config.py
      │   │   ├── sql
      │   │   │   ├── __init__.py
      │   │   │   ├── auto_partition
      │   │   │   │   ├── fact_production.sql
      │   │   │   │   ├── machine_status_logs.sql
      │   │   │   │   └── production_records.sql
      │   │   │   ├── dim_date.sql
      │   │   │   ├── dim_machine.sql
      │   │   │   ├── dim_product.sql
      │   │   │   ├── fact_machine_status.sql
      │   │   │   ├── fact_production.sql
      │   │   │   └── models
      │   │   │       ├── olap
      │   │   │       │   ├── dim_date.sql
      │   │   │       │   ├── dim_machine.sql
      │   │   │       │   ├── dim_product.sql
      │   │   │       │   ├── fact_machine_status.sql
      │   │   │       │   └── fact_production.sql
      │   │   │       └── oltp
      │   │   │           ├── machine.sql
      │   │   │           ├── machine_events.sql
      │   │   │           ├── machine_status_logs.sql
      │   │   │           ├── product.sql
      │   │   │           ├── production_orders.sql
      │   │   │           └── production_records.sql
      │   │   └── utils
      │   │       ├── __init__.py
      │   │       └── dag_tool.py
      │   ├── generic_benchmark
      │   │   ├── dashboard_benchmark.sql
      │   │   └── olap_benchmark.sql
      │   ├── simulator
      │   │   ├── __init__.py
      │   │   ├── v1
      │   │   │   ├── __init__.py
      │   │   │   ├── factory_config.yaml
      │   │   │   ├── init_factory_data.py
      │   │   │   └── simulate_factory_stream.py
      │   │   └── v2
      │   │       ├── __init__.py
      │   │       ├── api_service
      │   │       │   └── __init__.py
      │   │       ├── command_platform
      │   │       │   ├── __init__.py
      │   │       │   └── main.py
      │   │       ├── factory_config.yaml
      │   │       ├── instance
      │   │       │   ├── __init__.py
      │   │       │   └── main.py
      │   │       └── scripts
      │   │           ├── __init__.py
      │   │           ├── consumers.py
      │   │           ├── create_topic.py
      │   │           ├── init.py
      │   │           └── topics_config.json
      │   └── sql
      │       ├── auto_partition.py
      │       ├── delete_data.py
      │       └── drop_table.py
      └── utils
          ├── __init__.py
          ├── env_config.py
          ├── kafka_tools.py
          ├── postgre_tools.py
          ├── threading_tools.py
          └── tools.py
  ```
</ul>
</details>

<br>

### *E.　Benchmark*
| **Type** | **Objective** | **Methods** |
| :--: | :--: | :--: |
| *[Generic Benchmark](./docs/generic_benchmark.md)* | 資料庫極限 | 內建工具 |
| *[Workload Benchmark](./docs/workload_benchmark.md)* | 系統瓶頸 | 自訂腳本 |

<br>

### *F.　Notice*
- #### *⭐ 欲真正解決 OLTP / OLAP 衝突，詳見[另一解法](https://github.com/Junwu0615/OLTP-To-OLAP-Pipeline)*
- #### *I.　OLTP　VS.　OLAP　VS.　HTAP*
  | **Type** | **Core Objectives** | **Design Philosophy** | **Data Model** | **Query Features** |
  |:--:|:--|:--|:--|:--|
  | OLTP | 快速且正確地處理`交易` | 一致性優先 | [ 正規化 ]<br>3NF | 單筆查詢、低延遲 |
  | OLAP | 高效`分析`大量資料 | 查詢效率優先 | [ 非正規化 ]<br>Star Schema / Wide Table | 聚合分析、大量掃描 |
  | HTAP | 同時支援`交易`與`分析` | 負載平衡 | 混合模型 | 即時分析 + 交易 |
- #### *II.　若 OLTP/OLAP 都在同一 DB Instance 裡，Schema 分離優劣 ?*
  - #### *優 : `限制權限`, `分開 Connection Pool`, `分開 Query Routing`*
  - #### *劣 : `CPU / IO 共用`，它們還是彼此搶資源*
- #### *III.　Schema 分離 ≠ 解決 OLTP/OLAP 衝突*
  - #### *還是同一個 CPU*
  - #### *還是同一個 Disk*
  - #### *還是同一個 Buffer Cache*