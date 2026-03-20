<a href='https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/OLTP-OLAP-UNIFIED-DB.svg'>
[![](https://img.shields.io/badge/Operating_System-Windows_11-blue.svg?style=plastic)](https://www.microsoft.com/zh-tw/software-download/windows10) <br> 
[![](https://img.shields.io/badge/Technology-Python-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-PostgreSQL-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-Docker-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>
[![](https://img.shields.io/badge/Technology-OLTP-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-OLAP-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB)
[![](https://img.shields.io/badge/Technology-HTAP-yellow.svg?style=plastic)](https://github.com/Junwu0615/OLTP-OLAP-UNIFIED-DB) <br>

<br>

## *⭐ OLTP-OLAP-UNIFIED-DB ⭐*

Simulating HTAP workload using a single PostgreSQL instance with schema isolation, analyzing contention between transactional and analytical queries.


### *A.　Current Progress*
|**Item**|**Description**|**Finish Time**|
|:--:|:--:|:--:|
| Create Project | - | 2026-03-20 |
| Add PostgreSQL | By Docker | 2026-03-20 |
| Create OLTP DDL | 3NF | - |
| Create OLAP DDL | - | - |
| 模擬即時數據腳本 | - | - |
| 壓力測試 | - | - |

<br>

### *B. Service List*
|**Service**|**Description**|**Port**|
|:--:|:--:|:--:|
| PostgreSQL | - | [5432](http:127.0.0.1:5432) |
| PostgreSQL UI Web | - | [5050](http:127.0.0.1:5050) |

<br>

### *C. OLTP VS OLAP VS HTAP*
|**Type**|**Description**|**Feature**|**Query Type**|**Latency**|**Schema Mode**|**Index**|**Data Layout**|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| OLTP | Online Transaction Processing | 高併發、低延遲、寫多、正規化 | point query (by id) | ms | 專注於寫入與一致性 | 精準 index | row-based |
| OLAP | Analytical Processing | 大量掃描、聚合、讀多、反正規化 | scan + aggregation | ms ~ s | 專注於查詢效率 | 少 index / columnar | column-based |
| HTAP | Hybrid Transactional | 同時支援兩者 | - | - | - | - | - |

<br>

### *D. Notice*
- #### *若 OLTP/OLAP 都在同一 DB Instance 裡，Schema 分離優劣 ?*
  - #### *優 : `限制權限`, `分開 connection pool`, `分開 query routing`*
  - #### *劣 : `CPU / IO 還是共用`，它們還是彼此搶資源*
- #### *Schema 分離 ≠ 解決 OLTP/OLAP 衝突*
  - #### *還是同一個 CPU*
  - #### *還是同一個 Disk*
  - #### *還是同一個 Buffer Cache*
