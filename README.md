<a href='https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/OLTP-OLAP-UNIFIED-DB.svg'>
[![](https://img.shields.io/badge/Operating_System-Windows_11-blue.svg?style=plastic)](https://www.microsoft.com/zh-tw/software-download/windows10) <br> 
[![](https://img.shields.io/badge/Technology-Python-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-PostgreSQL-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-Docker-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>
[![](https://img.shields.io/badge/Technology-OLTP-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-OLAP-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-HTAP-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>

<br>

## *⭐ OLTP-OLAP-Unified-DB ⭐*

Simulating HTAP workload using a single PostgreSQL instance with schema isolation, analyzing contention between transactional and analytical queries.
```
OLTP 與 OLAP 的本質差異不在資料結構，而在工作負載 ( Workload )；
Schema 設計只是為了服務該負載的結果。
```

<br>

### *A.　Current Progress*
|**Item**|**Description**|**Finish Time**|
|:--:|:--:|:--:|
| Create Project | - | 2026-03-20 |
| Add PostgreSQL | By Docker | 2026-03-20 |
| Define Process | - | 2026-03-20 |
| Define Event Story | - | 2026-03-21 |
| Define Project Directory | - | 2026-03-21 |
| Define Table DDL | - | 2026-03-21 |
| Create OLTP DDL ( 6 ) | 3NF | 2026-03-21 |
| SQL Script | next_month_partition.sql | 2026-03-21 |
| Simulate Real-Time Data Script | - | 2026-03-21 |
| Add Airflow | By Docker | 2026-03-21 |
| SQL Script | this_month_partition.sql | 2026-03-22 |
| DB Settings | 權限切割設置 | 2026-03-23 |
| Add PoWA | By Docker | 2026-03-23 |
| PoWA Web 登入失敗 | 暫找無原因 | - |
| Add New Role | Migration User | 2026-03-24 |
| Simulate Test Run | - | 2026-03-24 |
| Create OLAP DDL ( 5 ) | Star Schema | - |
| OLTP to OLAP By ETL | - | - |
| Analytical Queries | - | - |
| Single to Batch Insert | - | - |
| Multi-Instance Simulate | - | - |
| Benchmark | - | - |
| Metrics | - | - |

<br>

### *B.1.　Service List*
|**Service**|**Description**|**Port**|
|:--:|:--:|:--:|
| PostgreSQL | for dev | [5432](http:127.0.0.1:5432) |
| PostgreSQL | for Airflow | [5433](http:127.0.0.1:5433) |
| PostgreSQL UI Web | - | [5050](http:127.0.0.1:5050) |
| Airflow | - | [8080](http:127.0.0.1:8080) |
| PoWA | 防屎 SQL 神器 | [5431](http:127.0.0.1:5431) |
| PoWA UI Web | - | [8888](http:127.0.0.1:8888) |

### *B.2.　[Service Startup Order](./docs/service_startup_order.md)*


<br>

### *C.1.　Project Implementation Roadmap*
```
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

### *C.2.　Event Description*
```
# 待生成完整流程圖

工廠情境：
  - 多台機台
  - 生產訂單
  - 機台狀態 ( 運轉 / 停機 / 故障 )
  - 生產產出 ( 良品 / 不良品 )
```

### *C.3.　[SQL Detail](./docs/sql.md)*

### *C.4.　[Simulate Result](./docs/simulate.md)*

### *C.5.　[Benchmark Result](./docs/benchmark.md)*

<br>

### *D.　OLTP　VS.　OLAP　VS.　HTAP*
| **Type** | **Core Objectives** | **Design Philosophy** | **Data Model** | **Query Features** |
|:--:|:--:|:--:|:--:|:--:|
| OLTP | 快速且正確地處理`交易` | 一致性優先 | [ 正規化 ]<br>3NF | 單筆查詢、低延遲 |
| OLAP | 高效`分析`大量資料 | 查詢效率優先 | [ 非正規化 ]<br>Star Schema / Wide Table | 聚合分析、大量掃描 |
| HTAP | 同時支援`交易`與`分析` | 負載平衡 | 混合模型 | 即時分析 + 交易 |

<br>

### *E.　Notice*
- #### *⭐ 欲真正解決 OLTP/OLAP 衝突，詳見[另一解法](https://github.com/Junwu0615/OLTP-To-OLAP-Pipeline)*
- #### *a.　若 OLTP/OLAP 都在同一 DB Instance 裡，Schema 分離優劣 ?*
  - #### *優 : `限制權限`, `分開 Connection Pool`, `分開 Query Routing`*
  - #### *劣 : `CPU / IO 共用`，它們還是彼此搶資源*
- #### *b.　Schema 分離 ≠ 解決 OLTP/OLAP 衝突*
  - #### *還是同一個 CPU*
  - #### *還是同一個 Disk*
  - #### *還是同一個 Buffer Cache*