### *A.　Benchmark Methods*
- #### *1.　OLTP 壓力測試 ( Write )*
  ```
  測試特徵 :
  大量 INSERT / UPDATE
  短 transaction
  高 concurrency
  
  指標 :
  TPS (Transactions Per Second)
  p95 / p99 latency
  lock wait
  WAL write rate
  CPU usage
  IO write throughput
  
  常用工具 :
  ⭐ pgbench
  sysbench
  HammerDB
  
  常見 benchmark :
  TPC-C
  ```
- #### *2.　OLAP 壓力測試 ( Read )*
  ```
  測試特徵 :
  大量 SELECT
  complex query
  aggregation
  scan / join
  
  指標 :
  QPS (Queries Per Second)
  query latency
  scan throughput
  CPU utilization
  memory usage
  
  常見 benchmark :
  ⭐ TPC-H
  TPC-DS
  ```
- #### *3.　HTAP 壓力測試 ( Mix )*
  ```
  同時跑 :
  transaction workload
  analytic workload
  
  觀察 :
  OLTP TPS drop
  OLAP latency spike
  buffer cache eviction
  IO contention
  
  常見 benchmark :
  ⭐ CH-BenCHmark
  ```

<br>

### *B.　Generic DB Benchmark*
| **Step** | **Description** | **Tool** |
| :--: | :-- | :--: |
| 1 | Query Benchmark | 直接查詢方式 |
| 2 | OLTP Workload Benchmark | pgbench by docker |
| 3 | OLAP Workload Benchmark | pgbench by docker |
| 4 | HTAP Workload Benchmark | pgbench by docker |
| 5 | Saturation Benchmark | pgbench by docker |

- #### *1.　Query Benchmark # 以查詢方式*
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
  動態掃描：查詢自動識別出 machine_status_logs 是一個分區母表，並同時檢索了 2026_03 與 2026_04 兩個子表（Append 節點）。
  優勢：這能有效隔離不同月份的資料，減少單一資料表過大導致的 IO 壓力。
  
  2. 索引狀態：精準打擊 (Index Usage)
  複合索引生效：資料庫成功使用了 machine_id_event_time_idx。
  查詢模式：採用了 Bitmap Index Scan。這代表資料庫先在索引中標記出符合條件的資料位置（Bitmap），再回頭去抓取實際資料（Heap Scan），這比逐行掃描快得多。
  數據分佈：在 3 月的分區中找到了 16 筆資料，且這些資料散落在 8 個不同的資料區塊（Heap Blocks: exact=8）。
  
  3. 效能表現：極速反應
  規劃時間 (Planning Time)：0.077 ms。資料庫判斷如何查詢的速度飛快。
  執行時間 (Execution Time)：0.074 ms。實際抓取資料的時間不到 1 毫秒。
  
  4. 總結：目前資料量下，索引與分區配置完美，幾乎沒有任何延遲。
  ```

- #### *2.　OLTP Workload Benchmark*
  ```
  進入容器執行 pgbench 壓力測試
  
  ### 初始化一次 ⬇️
   -s 1: 約 10 萬筆資料
   ⭐ -s 50: 約 500 萬筆資料
  docker exec -it postgres_sql_container pgbench -i -s 50 -U pguser -d pgdatabase
  
  
  ### ACTION ⬇️
   c: client 數量
   j: thread 數量
   T: 測試秒數
  docker exec -it postgres_sql_container pgbench -c 20 -j 4 -T 30 -U pguser -d pgdatabase
  
  
  ### RETURN ⬇️
  transaction type: <builtin: TPC-B (sort of)>
  scaling factor: 50
  query mode: simple
  number of clients: 20
  number of threads: 4
  maximum number of tries: 1
  duration: 30 s
  number of transactions actually processed: 43797
  number of failed transactions: 0 (0.000%)
  latency average = 13.701 ms
  initial connection time = 8.217 ms
  tps = 1459.753149 (without initial connection time)
  
  
  ### DESCRIPTION ⬇️
  1. 吞吐量效能 (Throughput)
  TPS ≈ 1460：在 20 個並發用戶下，每秒能處理約 1460 筆交易。在一般的開發級 Docker 環境（非生產級實體機）中，這代表資料庫對簡單讀寫的反應良好。
  總交易數 (Transactions)：30 秒內處理了近 4.4 萬筆交易且 零失敗 (0.000%)，顯示系統在高負載下具有高度穩定性。
  
  2. 回應延遲 (Latency)
  平均延遲 13.7 ms：這是一個健康的數據。對於 OLTP 系統來說，延遲低於 20ms 通常被認為是「流暢」的。
  連線開銷：initial connection time (8.2 ms) 佔比不低，這反映了 Docker 網路橋接（Bridge）或身分驗證的一點點初始開銷。
  
  3. 資源調度 (Threads & Clients)
  並發效率：你使用了 4 個執行緒處理 20 個用戶（1:5 的比例），pgbench 運行順暢。這代表你的 CPU 核心足以應付當前的並發量，沒有發生嚴重的 Context Switch（上下文切換）瓶頸。
  ```

- #### *3.　OLAP Workload Benchmark*
```

```

- #### *4.　HTAP Workload Benchmark*
```

```

- #### *5.　Saturation Benchmark*
```

```

<br>