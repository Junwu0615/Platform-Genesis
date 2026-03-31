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
| 1 | Query Benchmark | direct query method |
| 2 | OLTP Workload Benchmark | pgbench by docker |
| 3 | OLAP Workload Benchmark | pgbench by docker |
| 4 | HTAP Workload Benchmark | pgbench by docker |
| 5 | Saturation Benchmark | pgbench by docker |

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
  ### INITIALIZE ONCE ⬇️
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
  TPS ≈ 1460：在 20 個並發用戶下，每秒能處理約 1460 筆交易。
  在一般的開發級 Docker 環境（非生產級實體機）中，這代表資料庫對簡單讀寫的反應良好。
  總交易數 (Transactions)：30 秒內處理了近 4.4 萬筆交易且 零失敗 (0.000%)，
  顯示系統在高負載下具有高度穩定性。
  
  2. 回應延遲 (Latency)
  平均延遲 13.7 ms：這是一個健康的數據。對於 OLTP 系統來說，延遲低於 20ms 通常被認為是「流暢」的。
  連線開銷：initial connection time (8.2 ms) 佔比不低，這反映了 Docker 網路橋接（Bridge）
  或身分驗證的一點點初始開銷。
  
  3. 資源調度 (Threads & Clients)
  並發效率：你使用了 4 個執行緒處理 20 個用戶（1:5 的比例），pgbench 運行順暢。
  這代表你的 CPU 核心足以應付當前的並發量，沒有發生嚴重的 Context Switch（上下文切換）瓶頸。
  ```

- #### *3.　OLAP Workload Benchmark*
  ```
  ### 1. COPY SQL SCRIPT IN CONTAINER ⬇️
  docker cp ".\src\sql\scripts\olap_benchmark.sql" postgres_sql_container:/tmp/olap_benchmark.sql
  
  ### 2. 一次性清理 BOM 與 Windows 換行符 (CRLF -> LF) ⬇️
  docker exec -it postgres_sql_container sh -c "sed -i '1s/^\xef\xbb\xbf//; s/\r$//' /tmp/olap_benchmark.sql"
  
  ### 3. CHECK SCRIPT ⬇️
  docker exec -it postgres_sql_container cat /tmp/olap_benchmark.sql
  
  
  ### ACTION ⬇️
  docker exec -it postgres_sql_container pgbench -c 8 -j 2 -T 60 -f /tmp/olap_benchmark.sql -U pguser -d pgdatabase
  
  
  ### RETURN ⬇️
  transaction type: /tmp/olap_benchmark.sql
  scaling factor: 1
  query mode: simple
  number of clients: 8
  number of threads: 2
  maximum number of tries: 1
  duration: 60 s
  number of transactions actually processed: 51344
  number of failed transactions: 0 (0.000%)
  latency average = 9.349 ms
  initial connection time = 5.900 ms
  tps = 855.705109 (without initial connection time)
  
  
  ### DESCRIPTION ⬇️
  1. 查詢效率與吞吐量 (Throughput)
  TPS ≈ 856：相較於純 OLTP 的 1460 TPS，效能下降了約 41%。這在預期範圍內，因為 GROUP BY 與 AVG 需要更多的 CPU 運算與記憶體暫存，而非簡單的索引跳轉。
  穩定性：60 秒內處理了超過 5.1 萬次複雜查詢且 零失敗，代表你的分區表（Partitioning）與索引配置在 8 個並發連線下依然非常穩健。
  
  2. 延遲表現 (Latency)
  平均延遲 9.35 ms：出乎意料地，這個數值比你之前的 OLTP 測試 (13.7ms) 還低。
  數據解讀： 這代表你的 production_records 表在 event_time 上的索引效率極高，或者該月份的資料量目前尚在 記憶體快取 (Shared Buffers) 的覆蓋範圍內，幾乎沒有發生昂貴的實體磁碟 I/O。
  同時，因為 clients 只有 8 個（之前是 20 個），系統的資源爭用（Contention）較少，導致單次反應速度更快。
  
  3. 資源利用率
  Threads (2) vs Clients (8)：每個執行緒處理 4 個用戶連線，任務調度效率良好。
  Connection Overhead：初始連線時間從 8.2ms 降至 5.9ms，顯示在壓力較小時，Docker 網路的握手（Handshake）速度有所提升。
  ```

- #### *4.　HTAP Workload Benchmark*
  ```
  ### CLEAN UP CONTAINER ENV ⬇️ 
  docker restart postgres_sql_container
  
  
  ### ACTION ⬇️
  docker exec -it postgres_sql_container pgbench -c 20 -j 4 -T 60 -b tpcb-like@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  
  ### RETURN ⬇️
  transaction type: multiple scripts
  scaling factor: 50
  query mode: simple
  number of clients: 20
  number of threads: 4
  maximum number of tries: 1
  duration: 60 s
  number of transactions actually processed: 78316
  number of failed transactions: 0 (0.000%)
  latency average = 15.323 ms
  initial connection time = 8.491 ms
  tps = 1305.185332 (without initial connection time)
  SQL script 1: <builtin: TPC-B (sort of)>
   - weight: 9 (targets 90.0% of total)
   - 70614 transactions (90.2% of total, tps = 1176.826664)
   - number of failed transactions: 0 (0.000%)
   - latency average = 14.176 ms
   - latency stddev = 31.767 ms
  SQL script 2: /tmp/olap_benchmark.sql
   - weight: 1 (targets 10.0% of total)
   - 7702 transactions (9.8% of total, tps = 128.358668)
   - number of failed transactions: 0 (0.000%)
   - latency average = 13.764 ms
   - latency stddev = 32.800 ms
  
  
  ### DESCRIPTION ⬇️
  1. 混合負載下的效能損耗 (HTAP Impact)
  TPS 跌幅 ≈ 10.6%：對比純 OLTP 的 1460 TPS，加入 10% 的 OLAP 查詢後，總 TPS 降至 1305。
  結論： 這是一個非常優秀的表現。通常在沒有優化（如分區或索引）的系統中，10% 的 OLAP 往往會拖垮 30-50% 的交易效能。這證明了你的「分區表」架構成功隔離了大部分的 IO 衝突。
  
  2. 延遲的「拉鋸戰」 (Latency Dynamics)
  OLTP 延遲上升：從 13.7ms 增加到 14.17ms。
  OLAP 延遲增加：從 9.35ms 顯著增加到 13.76ms（增幅約 47%）。
  分析：這顯示了典型的 CPU 與 Buffer Cache 競爭。當 OLTP 頻繁更新索引時，OLAP 的 GROUP BY 計算必須等待 CPU 週期，且其掃描的資料塊可能被 OLTP 的寫入動作擠出快取。
  
  3. 穩定性警訊：標準差 (Stddev)
  高抖動 (Stddev ≈ 32ms)：無論是 OLTP 還是 OLAP，標準差都大於平均延遲（> 2 倍）。
  解讀：這代表系統出現了「效能不平均」的現象。有些查詢很快，但有些查詢因為等待 WAL (預寫日誌) 鎖定 或 Checkpoint (檢查點) 寫入磁碟而卡住了。在高並發的 HTAP 場景中，這通常是磁碟 IOPS 到達瓶頸的前兆。
  ```

- #### *5.　Saturation Benchmark*
```

```

<br>