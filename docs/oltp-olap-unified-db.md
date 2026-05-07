## *OLTP-OLAP-Unified-DB*

Simulating HTAP workload using a single PostgreSQL instance with schema isolation, analyzing contention between transactional and analytical queries.
```
* Database architecture should be driven by workload.
 ↪︎ * Workload defines query patterns.
 ↪︎ * Query patterns define schema design.
 ↪︎ * Schema design defines indexing and storage strategy.


OLTP 與 OLAP 的本質差異不在【 資料結構 】，而在【 工作負載 】； Schema 設計只是為了【 服務該負載 】的結果。
```

<br>

| **Type** | **Core Objectives** | **Design Philosophy** | **Data Model** | **Query Features** |
|--:|:--|:--|:--|:--|
| OLTP | 快速且正確地處理`交易` | 一致性優先 | [ 正規化 ]<br>3NF | 單筆查詢、低延遲 |
| OLAP | 高效`分析`大量資料 | 查詢效率優先 | [ 非正規化 ]<br>Star Schema / Wide Table | 聚合分析、大量掃描 |
| HTAP | 同時支援`交易`與`分析` | 負載平衡 | 混合模型 | 即時分析 + 交易 |

<br>

### *Benchmark*
|**Type**|**Objective**|**Methods**|
|:--:|:--:|:--:|
|*[Generic Benchmark](./generic_benchmark.md)* | 資料庫極限 | 內建工具 |
|*[Workload Benchmark](./workload_benchmark.md)* | 系統瓶頸 | 自訂腳本 |


<br>

- #### *1.　若 OLTP/OLAP 都在同一 DB Instance 裡，Schema 分離優劣 ?*
  - #### *優 : `限制權限`, `分開 Connection Pool`, `分開 Query Routing`*
  - #### *劣 : `CPU / IO 共用`，它們還是彼此搶資源*

- #### *2.　Schema 分離 ≠ 解決 OLTP/OLAP 衝突*
  - #### *還是同一個 CPU*
  - #### *還是同一個 Disk*
  - #### *還是同一個 Buffer Cache*

