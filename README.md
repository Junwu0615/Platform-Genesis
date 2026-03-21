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
| Create OLTP DDL | 3NF | - |
| Create OLAP DDL | Star Schema ... etc. | - |
| Simulate Real-Time Data Script | - | - |
| Single Insert | - | - |
| Batch Insert | - | - |
| Multi-Instance Simulate | - | - |
| Stress Test | - | - |

<br>

### *B.　Service List*
|**Service**|**Description**|**Port**|
|:--:|:--:|:--:|
| PostgreSQL | - | [5432](http:127.0.0.1:5432) |
| PostgreSQL UI Web | - | [5050](http:127.0.0.1:5050) |

<br>

### *C.1.　Event Diagram*
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

<br>

### *C.2.　Event Description*
```
工廠情境：
  - 多台機台
  - 生產訂單
  - 機台狀態 ( 運轉 / 停機 / 故障 )
  - 生產產出 ( 良品 / 不良品 )
```

<br>

### *D.　OLTP　VS.　OLAP　VS.　HTAP*
| **Type** | **Core Objectives** | **Design Philosophy** | **Data Model** | **Query Features** |
|:--:|:--:|:--:|:--:|:--:|
| OLTP | 快速且正確地處理`交易` | 一致性優先 | 3NF 正規化 | 單筆查詢、低延遲 |
| OLAP | 高效`分析`大量資料 | 查詢效率優先 | Star Schema / Wide Table | 聚合分析、大量掃描 |
| HTAP | 同時支援`交易`與`分析` | 負載平衡 | 混合模型 | 即時分析 + 交易 |

<br>

### *E.　Notice*
- #### *⭐ 欲真正解決 OLTP/OLAP 衝突，詳見[企業級解法](https://github.com/Junwu0615/OLTP-To-OLAP-Pipeline)*
- #### *a. 若 OLTP/OLAP 都在同一 DB Instance 裡，Schema 分離優劣 ?*
  - #### *優 : `限制權限`, `分開 Connection Pool`, `分開 Query Routing`*
  - #### *劣 : `CPU / IO 共用`，它們還是彼此搶資源*
- #### *b. Schema 分離 ≠ 解決 OLTP/OLAP 衝突*
  - #### *還是同一個 CPU*
  - #### *還是同一個 Disk*
  - #### *還是同一個 Buffer Cache*
- #### *c. Define Table DDL*
  - #### *1. OLTP of DDL*
    - #### *1.1. 1NF*
    - #### *1.2. 2NF*
    - #### *1.3. 3NF*
  - #### *2. OLAP of DDL*
    - #### *2.1. Star Schema*
      - #### *Fact Table*
      - #### *Dimension Table*
    - #### *2.2. Snowflake Schema*
      - #### *Fact Table*
      - #### *Dimension Table*
      - #### *Sub-Dimension Table ... etc.*
    - #### *2.3. Wide Table*
- #### *d. Check Define Table List*
  - #### *1. OLTP*
    - #### *是否有主鍵 ? ( PK )*
    - #### *是否有外鍵 ? ( FK )*
    - #### *是否有 index ? ( PK / FK / 常用查詢條件 )*
    - #### *是否有 transaction ? ( ACID )*
    - #### *是否有適當的 normal form ? ( 1NF / 2NF / 3NF )*
    - #### *是否避免資料冗餘 ?*
  - #### *2. OLAP*
    - #### *是否有 fact table ?*
    - #### *是否有 dimension ?*
    - #### *是否避免複雜 join ?*
    - #### *是否支援時間分析 ?*
    - #### *是否能快速做 aggregation ?*