## *🪛 shm_size: 64 MB*
### *Settings ( shared_buffers / work_mem / synchronous_commit )*
![PNG](../assets/generic_result_1.png)

<br>

### *Generic DB Benchmark*
| **Step** | **Description** | **Tool** |
| :--: | :-- | :--: |
| [0](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_1.md#0initialize-pgbench-benchmark-data) | Initialize pgbench Benchmark Data | - |
| [1](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_1.md#1query-benchmark) | Query Benchmark | direct query method |
| [2](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_1.md#2oltp-workload-benchmark) | OLTP Workload Benchmark | use pgbench |
| [3](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_1.md#3olap-workload-benchmark) | OLAP Workload Benchmark | use pgbench |
| [4](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_1.md#4htap-workload-benchmark) | HTAP Workload Benchmark | use pgbench |
| [5](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_1.md#5saturation-benchmark) | Saturation Benchmark | use pgbench |

<br>

- #### *0.1　Initialize pgbench Benchmark Data*
  ```
  ### INITIALIZE ONCE ⬇️
   -s 1: 約 10 萬筆資料
   -s 50: 約 500 萬筆資料
   ⭐ -s 500: 約 5000 萬筆資料
  
  docker exec -it postgres_sql_container pgbench -i -s 500 -U pguser -d pgdatabase
  ```
- ![PNG](../assets/initialize_data_1.png)

- #### *0.2　Prepare Benchmark Scripts*
  ```
  ### 1. COPY SQL SCRIPT IN CONTAINER ⬇️
  docker cp ".\src\sql\scripts\dashboard_benchmark.sql" postgres_sql_container:/tmp/dashboard_benchmark.sql
  docker cp ".\src\sql\scripts\olap_benchmark.sql" postgres_sql_container:/tmp/olap_benchmark.sql
  
  ### 2. 一次性清理 BOM 與 Windows 換行符 (CRLF -> LF) ⬇️
  docker exec -it postgres_sql_container sh -c "sed -i '1s/^\xef\xbb\xbf//; s/\r$//' /tmp/dashboard_benchmark.sql"
  docker exec -it postgres_sql_container sh -c "sed -i '1s/^\xef\xbb\xbf//; s/\r$//' /tmp/olap_benchmark.sql"
  
  ### 3. CHECK SCRIPT ⬇️
  docker exec -it postgres_sql_container cat /tmp/dashboard_benchmark.sql
  docker exec -it postgres_sql_container cat /tmp/olap_benchmark.sql
  ```

- #### *1.　Query Benchmark*
  ```
  ### ACTION ⬇️
  EXPLAIN ANALYZE
  SELECT *
  FROM oltp.machine_status_logs
  WHERE machine_id = 10;
  
  
  ### RETURN ⬇️
  Append  (cost=4.40..26.34 rows=20 width=36) (actual time=0.018..0.028 rows=16 loops=1)
    ->  Bitmap Heap Scan on machine_status_logs_2026_03 machine_status_logs_1  (cost=4.40..13.60 rows=16 width=26) (actual time=0.017..0.026 rows=16 loops=1)
          Recheck Cond: (machine_id = 10)
          Heap Blocks: exact=8
          ->  Bitmap Index Scan on machine_status_logs_2026_03_machine_id_event_time_idx  (cost=0.00..4.40 rows=16 width=0) (actual time=0.013..0.013 rows=16 loops=1)
                Index Cond: (machine_id = 10)
    ->  Bitmap Heap Scan on machine_status_logs_2026_04 machine_status_logs_2  (cost=4.18..12.64 rows=4 width=78) (actual time=0.001..0.001 rows=0 loops=1)
          Recheck Cond: (machine_id = 10)
          ->  Bitmap Index Scan on machine_status_logs_2026_04_machine_id_event_time_idx  (cost=0.00..4.18 rows=4 width=0) (actual time=0.000..0.000 rows=0 loops=1)
                Index Cond: (machine_id = 10)
  Planning Time: 0.077 ms
  Execution Time: 0.074 ms
  
  
  ### DESCRIPTION ⬇️
  1. 核心架構：表分區 (Table Partitioning)
  動態掃描：查詢自動識別出 machine_status_logs 是一個分區母表，
  並同時檢索了 2026_03 與 2026_04 兩個子表（Append 節點）。
  優勢：這能有效隔離不同月份的資料，減少單一資料表過大導致的 IO 壓力。
  
  2. 索引狀態：精準打擊 (Index Usage)
  複合索引生效：資料庫成功使用了 machine_id_event_time_idx。
  查詢模式：採用了 Bitmap Index Scan。這代表資料庫先在索引中標記出符合條件的資料位置（Bitmap），
  再回頭去抓取實際資料（Heap Scan），這比逐行掃描快得多。
  數據分佈：在 3 月的分區中找到了 16 筆資料，且這些資料散落在 8 個不同的資料區塊（Heap Blocks: exact=8）。
  
  3. 效能表現：極速反應
  規劃時間 (Planning Time)：0.077 ms。資料庫判斷如何查詢的速度飛快。
  執行時間 (Execution Time)：0.074 ms。實際抓取資料的時間不到 1 毫秒。
  
  4. 總結：目前資料量下，索引與分區配置完美，幾乎沒有任何延遲。
  ```

- #### *2.　OLTP Workload Benchmark*
  ```
  ### ACTION ⬇️
   c: client 數量
   j: thread 數量
   T: 測試秒數
  docker exec -it postgres_sql_container pgbench -c 20 -j 4 -T 30 -U pguser -d pgdatabase
  
  
  ### RETURN ⬇️
  ```

- #### *3.　OLAP Workload Benchmark*
  ```
  ### ACTION ⬇️
  
  
  ### RETURN ⬇️

  
  ### DESCRIPTION ⬇️
  ```

- #### *4.　HTAP Workload Benchmark*
  | Layer | Item | % |
  | :--: | :-- | :--: |
  | 1 | OLTP ( Source of Truth ) | 90 |
  | 2 | Near-Real-Time Analytics ( Dashboard ) | 9 |
  | 3 | OLAP ( BI ) | 1 |

  ```
  ### 連線數固定 30
  ### 用 300s 模擬真實的混合負載，讓系統在穩定狀態下表現出真實的性能指標
  
  ### ACTION 1 ⬇️
  # ⚠️ 以 (90% OLTP, 9% Dashboard, 1% OLAP) 模擬更真實的混合負載，通常能提供更全面的性能評估
  docker exec -it postgres_sql_container pgbench -c 30 -j 8 -T 300 -b tpcb-like@90 -f /tmp/dashboard_benchmark.sql@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  ### RETURN 1 ⬇️
  
  
  ### ACTION 2 ⬇️
  # ⚠️ 使用 -M prepared (預編譯語句) 可以減少 SQL 解析時間，通常能提升 10-20% TPS
  docker exec -it postgres_sql_container pgbench -c 30 -j 8 -T 300 -M prepared -b tpcb-like@90 -f /tmp/dashboard_benchmark.sql@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  ### RETURN 2 ⬇️
  ```

  | **Evaluation** | **30 Clients ( Generic )** | **30 Clients ( Prepared )** | **Trend ( Generic vs Prepared )** |
  | :--: | :--: | :--: | :--: |
  | AVG TPS | - | - | - |
  | AVG Latency ( ms ) | - | - | - |
  | OLTP Std Dev ( ms ) | - | - | - |
  | OLAP Std Dev ( ms ) | - | - | - |
  | Conn Overhead ( ms ) | - | - | - |

  ```
  ### DESCRIPTION ⬇️

  ```


- #### *~~5.　Saturation Benchmark~~*
  | **Evaluation** | **30 Clients ( Sweet Spot )** | **50 Clients ( Medium-load )** | **100 Clients ( High-load )** | **Trend ( 30 vs 100 )** |
  | :--: | :--: | :--: | :--: | :--: |
  | AVG TPS | - | - | - | - |
  | AVG Latency ( ms ) | - | - | - | - |
  | OLTP Std Dev ( ms ) | - | - | - | - |
  | OLAP Std Dev ( ms ) | - | - | - | - |
  | Conn Overhead ( ms ) | - | - | - | - |

<br>