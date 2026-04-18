<a href='https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/OLTP-OLAP-UNIFIED-DB.svg'>
[![](https://img.shields.io/badge/Operating_System-Windows_11-blue.svg?style=plastic)](https://www.microsoft.com/zh-tw/software-download/windows10) <br> 
[![](https://img.shields.io/badge/Technology-Python-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-PostgreSQL-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-Docker-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>
[![](https://img.shields.io/badge/Technology-OLTP-critical.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-OLAP-critical.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-HTAP-critical.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-Terraform-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>
[![](https://img.shields.io/badge/Technology-Grafana-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) 
[![](https://img.shields.io/badge/Technology-Prometheus-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) 
[![](https://img.shields.io/badge/Technology-PoWA-inactive.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) 
[![](https://img.shields.io/badge/Technology-Apache_Airflow-important.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>

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
|**Item**|**Description**|**Time**|
|--:|:--|:--:|
| Create Project | - | 2026-03-20 |
| Add PostgreSQL | By Docker | 2026-03-20 |
| Define Process | - | 2026-03-20 |
| Define Event Story | - | 2026-03-21 |
| Define Project Directory | - | 2026-03-21 |
| Define Table DDL | - | 2026-03-21 |
| Create OLTP DDL ( 6 ) | 3NF | 2026-03-21 |
| Add Airflow | By Docker | 2026-03-21 |
| DB Settings | Permission Settings | 2026-03-23 |
| Add PoWA | By Docker | 2026-03-23 |
| PoWA Web Login Failed | ⚠️no reason found yet | 2026-03-23 |
| Add New Role | Migration User | 2026-03-24 |
| Script | delete_data.py | 2026-03-24 |
| Script | drop_table.py | 2026-03-24 |
| Script | factory_config.yaml | 2026-03-24 |
| Script | init_factory_data.py | 2026-03-24 |
| Script | simulate_factory_stream.py | 2026-03-24 |
| Single to Batch Insert | 批次發送 | 2026-03-26 |
| Generate Rigorous Static Data | - | 2026-03-26 |
| Rigorous Calibration of Dynamic Data | 單一機台同時間只允許做一件事 /<br>排隊消化訂單 / 訂單生產週期戳記 | 2026-03-27 |
| Adjusting Contextual Logic | 插入機台事件 : 🗑️ machine_events | 2026-03-28 |
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
| Add Monitoring | Postgres Exporter + Prometheus + Grafana | 2026-04-04 |
| Add Monitoring | Node Exporter | 2026-04-05 |
| Grafana Dashboard | Organize Observation Indicators | 2026-04-05 |
| Add WSL2 Settings | `.wslconfig` | 2026-04-06 |
| Create OLAP DDL ( 5 ) | Star Schema | 2026-04-06 |
| Partition Settings | `default_partition` | 2026-04-06 |
| Auto Partition | `dags/sql/auto_partition/*` | 2026-04-06 |
| OLTP to OLAP | `dags/sql/*` | 2026-04-06 |
| Build DAGs Coding Style | - | 2026-04-06 |
| DAG ETL Script | Fan-out Queue Pattern | 2026-04-06 |
| DAG | Try `Param` | 2026-04-07 |
| DAG | Try `Dataset` | 2026-04-08 |
| Add Portainer | By Docker | 2026-04-11 |
| Docker Compose Profiles | compose 模組化，整套 lab 一鍵部署 | 2026-04-11 |
| Add Makefile | - | 2026-04-11 |
| Add Airflow Config UI | `Trigger w/ Config` | 2026-04-18 |
| Update DAGs Coding Style | - | - |
| Create Materialized View ( MV ) | 建立物化檢視表 | - |
| Grafana Dashboard | update `htap_grafana.json` | - |
| Analytical Queries | - | - |
| Multi-Instance Simulate | like Edge Machine | X |
| Add Terraform | 基礎設施供應 : 負責變出資源。<br>ex：雲端開 VM、設定網路、建立 S3 Bucket ... | - |
| Add Ansible | 組態管理 : 負責進入主機。<br>ex：安裝 Docker、設定權限、拉 Git 專案、啟動服務 ... | - |
| Upload GCP | - | - |

<br>

### *B.　Service*
- #### *1.　Service List*
  |**Service**|**Description**|**Port**|
  |--:|:--|:--:|
  | PostgreSQL | for `Dev` | [5432](http:127.0.0.1:5432) |
  | PostgreSQL | for `Airflow` | [5433](http:127.0.0.1:5433) |
  | PostgreSQL UI Web | - | [5050](http:127.0.0.1:5050) |
  | Airflow | - | [8100](http:127.0.0.1:8100) |
  | ~~PostgreSQL~~ | for `PoWA` | [5431](http:127.0.0.1:5431) |
  | ~~PoWA UI Web~~ | for `PoWA` | [8888](http:127.0.0.1:8888) |
  | Grafana | for `Monitoring` | [3000](http:127.0.0.1:3000) |
  | Prometheus | for `Monitoring` | [9090](http:127.0.0.1:9090) |
  | Node Exporter | for `Monitoring` | [9100](http:127.0.0.1:9100) |
  | Postgres Exporter | for `Monitoring` | [9187](http:127.0.0.1:9187) |
  | Portainer | for `Manage Containers` | [9000](http:127.0.0.1:9000) |


- #### *2.　[Service Startup Order](./docs/service_startup_order.md)*
- #### *3.　[WSL2 Startup Docker Engine](./docs/wsl2_startup_docker_engine.md)*

- #### *4.　Makefile Execute*
  ```
  make init
  make build
  make up
  ```


<br>

### *C.　Implementation*
- #### *1.　Roadmap*
  ```
  # 待生成完整流程圖
  
  1. [Schema Design]
           ↓
  2. [Data Generator]
           ↓
  3. [OLTP Schema (3NF)]
           ↓
  4. [ETL] # ETL : Extract → Transform → Load
           ↓
  5. [OLAP Schema (Star Schema)]
           ↓
  6. [Analytical Queries]
           ↓
  7. [Benchmark & Metrics]
  ```

- #### *2.　[About SQL Something Detail](./docs/sql.md)*

<br>

### *D.　Benchmark*
| **Type** | **Objective** | **Methods** |
| :--: | :--: | :--: |
| *[Generic Benchmark](./docs/generic_benchmark.md)* | 找「資料庫」極限   | 內建工具 |
| *[Workload Benchmark](./docs/workload_benchmark.md)* | 找「指定系統」瓶頸 | 自訂腳本 |

<br>

### *E.　Notice*
- #### *⭐ 欲真正解決 OLTP / OLAP 衝突，詳見[另一解法](https://github.com/Junwu0615/OLTP-To-OLAP-Pipeline)*
- #### *1.　OLTP　VS.　OLAP　VS.　HTAP*
  | **Type** | **Core Objectives** | **Design Philosophy** | **Data Model** | **Query Features** |
  |:--:|:--:|:--:|:--:|:--:|
  | OLTP | 快速且正確地處理`交易` | 一致性優先 | [ 正規化 ]<br>3NF | 單筆查詢、低延遲 |
  | OLAP | 高效`分析`大量資料 | 查詢效率優先 | [ 非正規化 ]<br>Star Schema / Wide Table | 聚合分析、大量掃描 |
  | HTAP | 同時支援`交易`與`分析` | 負載平衡 | 混合模型 | 即時分析 + 交易 |
- #### *2.　若 OLTP/OLAP 都在同一 DB Instance 裡，Schema 分離優劣 ?*
  - #### *優 : `限制權限`, `分開 Connection Pool`, `分開 Query Routing`*
  - #### *劣 : `CPU / IO 共用`，它們還是彼此搶資源*
- #### *3.　Schema 分離 ≠ 解決 OLTP/OLAP 衝突*
  - #### *還是同一個 CPU*
  - #### *還是同一個 Disk*
  - #### *還是同一個 Buffer Cache*