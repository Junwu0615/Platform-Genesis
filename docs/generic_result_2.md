## *🪛 shm_size: 16 GB*
### *Settings ( shared_buffers / work_mem / synchronous_commit )*
![PNG](../assets/generic_result_2.png)

<br>

### *DB Dedicated Machine Settings*
![PNG](../assets/shm_size.png)

<br>

### *Settings Before Action*
```
# 從 Docker-Desktop 移進 WSL2
# 由 /home 使用檔案 + compose up 避免遇到
  1. 9P 協定瓶頸: 這層通訊開銷極大，比 Windows 本生虛擬化還慢
  2. I/O 延遲爆炸: 頻繁切換寫入 WAL 和 Data blocks

mkdir -p ~/OLTP-OLAP-Unified-DB
cp -r /mnt/c/專案路徑/* ~/OLTP-OLAP-Unified-DB/
# ex: cp -r /mnt/c/Users/PC/Code/Python/Publish-To-Git/OLTP-OLAP-Unified-DB/src ~/OLTP-OLAP-Unified-DB/


# 用 WSL2 確認容器資源限制 ( 預期32 )
nproc


# 設定 docker-compose.yaml
shm_size: '16gb' -- 避免高並發時崩潰 / TPS: 穩定性提升
command: >
  postgres
  -c shared_buffers=10GB -- 提升快取與工作記憶體 / 減少實體 IO 讀取 / TPS: +20% ~ 50%
  -c work_mem=128MB -- 同上
  -c maintenance_work_mem=512MB
  -c synchronous_commit=off -- 暴力提升寫入吞吐量 (實驗專用) / 消除 WAL 寫入延遲 / TPS: +100% ~ 300%
  -c checkpoint_completion_target=0.9 -- 同上
  -c max_connections=100


# 確認設定已生效
docker exec -it postgres_sql_container psql -U pguser -d pgdatabase

SHOW shared_buffers;
SHOW work_mem;
SHOW synchronous_commit;


# 持續監控容器資源使用狀況
docker stats postgres_sql_container --no-stream
```

<br>

### *Generic DB Benchmark*
| **Step** | **Description** | **Tool** |
| :--: | :-- | :--: |
| [0](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#01initialize-pgbench-benchmark-data) | Initialize pgbench Benchmark Data | - |
| [1](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#1query-benchmark) | Query Benchmark | direct query method |
| [2](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#-skip--2oltp-workload-benchmark) | OLTP Workload Benchmark | use pgbench |
| [3](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#3olap-workload-benchmark) | OLAP Workload Benchmark | use pgbench |
| [4](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#4htap-workload-benchmark) | HTAP Workload Benchmark | use pgbench |
| [5](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#5saturation-benchmark) | Saturation Benchmark | use pgbench |

<br>

- #### *0.1　Initialize pgbench Benchmark Data*
  ```
  ### INITIALIZE ONCE ⬇️
   -s 1: 約 10 萬筆資料
   -s 50: 約 500 萬筆資料
   ⭐ -s 500: 約 5000 萬筆資料
  
  docker exec -it postgres_sql_container pgbench -i -s 500 -U pguser -d pgdatabase
  ```
- ![PNG](../assets/initialize_data_2.png)

- #### *0.2　Prepare Benchmark Scripts*
  ```
  ### 1. COPY SQL SCRIPT IN CONTAINER ⬇️
  docker cp "src/sql/scripts/dashboard_benchmark.sql" postgres_sql_container:/tmp/dashboard_benchmark.sql
  docker cp "src/sql/scripts/olap_benchmark.sql" postgres_sql_container:/tmp/olap_benchmark.sql
  
  
  ### 2. 一次性清理 BOM 與 Windows 換行符 (CRLF -> LF) ⬇️
  docker exec -it postgres_sql_container sh -c "sed -i '1s/^\xef\xbb\xbf//; s/\r$//' /tmp/dashboard_benchmark.sql"
  docker exec -it postgres_sql_container sh -c "sed -i '1s/^\xef\xbb\xbf//; s/\r$//' /tmp/olap_benchmark.sql"
  
  
  ### 3. CHECK SCRIPT ⬇️
  docker exec -it postgres_sql_container cat /tmp/dashboard_benchmark.sql
  docker exec -it postgres_sql_container cat /tmp/olap_benchmark.sql
  ```

<br>

- #### *~~1.　Query Benchmark~~*
- #### *2.　OLTP Workload Benchmark*
  ```
  ### ACTION ⬇️
  docker exec -it postgres_sql_container pgbench -c 30 -j 8 -T 300 -b tpcb-like@100 -U pguser -d pgdatabase
  
  
  ### RETURN ⬇️
  transaction type: <builtin: TPC-B (sort of)>
  scaling factor: 500
  query mode: simple
  number of clients: 30
  number of threads: 8
  maximum number of tries: 1
  duration: 300 s
  number of transactions actually processed: 633601
  number of failed transactions: 0 (0.000%)
  latency average = 14.205 ms
  initial connection time = 7.322 ms
  tps = 2111.920631 (without initial connection time)
  
  
  ### ACTION 2 ( 測試 純讀取 負載 ) ⬇️
  docker exec -it postgres_sql_container pgbench -S -c 30 -j 8 -T 300 -U pguser -d pgdatabase
  
  
  ### RETURN 2 ⬇️
  transaction type: <builtin: select only>
  scaling factor: 500
  query mode: simple
  number of clients: 30
  number of threads: 8
  maximum number of tries: 1
  duration: 300 s
  number of transactions actually processed: 3473412
  number of failed transactions: 0 (0.000%)
  latency average = 2.591 ms
  initial connection time = 7.304 ms
  ⭐ tps = 11577.754184 (without initial connection time)
  
  
  ### ACTION 3 ( 極限測試 純讀取 負載 ) ⬇️
  docker exec -it postgres_sql_container pgbench -S -c 100 -j 32 -T 300 -M prepared -U pguser -d pgdatabase
  
  ### RETURN 3 ⬇️
  transaction type: <builtin: select only>
  scaling factor: 500
  query mode: prepared
  number of clients: 100
  number of threads: 32
  maximum number of tries: 1
  duration: 300 s
  number of transactions actually processed: 3529519
  number of failed transactions: 0 (0.000%)
  latency average = 8.500 ms
  initial connection time = 91.631 ms
  ⭐ tps = 11764.198508 (without initial connection time)
  ```

<br>

- #### *3.　OLAP Workload Benchmark*
  ```
  ### ACTION ⬇️
  docker exec -it postgres_sql_container pgbench -c 30 -j 8 -T 300 -f /tmp/olap_benchmark.sql@100 -U pguser -d pgdatabase
  
  
  ### RETURN ⬇️
  transaction type: /tmp/olap.sql
  scaling factor: 1
  query mode: simple
  number of clients: 30
  number of threads: 8
  maximum number of tries: 1
  duration: 300 s
  number of transactions actually processed: 1201
  number of failed transactions: 0 (0.000%)
  latency average = 7622.358 ms
  initial connection time = 8.877 ms
  tps = 3.935790 (without initial connection time)
  ```

<br>

- #### *4.　HTAP Workload Benchmark*
  | Layer | Item | % |
  | :--: | :-- | :--: |
  | 1 | OLTP ( Source of Truth ) | 90 |
  | 2 | Near-Real-Time Analytics ( Dashboard ) | 9 |
  | 3 | OLAP ( BI ) | 1 |

  ```
  ### ACTION 1 ⬇️
  docker exec -it postgres_sql_container pgbench -c 30 -j 8 -T 300 -b tpcb-like@90 -f /tmp/dashboard_benchmark.sql@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  
  ### RETURN 1 ⬇️
  transaction type: multiple scripts
  scaling factor: 500
  query mode: simple
  number of clients: 30
  number of threads: 8
  maximum number of tries: 1
  duration: 300 s
  number of transactions actually processed: 77195
  number of failed transactions: 0 (0.000%)
  latency average = 118.131 ms
  initial connection time = 8.340 ms
  tps = 253.955567 (without initial connection time)
  SQL script 1: <builtin: TPC-B (sort of)>
   - weight: 90 (targets 90.0% of total)
   - 69326 transactions (89.8% of total, tps = 228.068186)
   - number of failed transactions: 0 (0.000%)
   - latency average = 2.084 ms
   - latency stddev = 1.813 ms
  SQL script 2: /tmp/dashboard_benchmark.sql
   - weight: 9 (targets 9.0% of total)
   - 7109 transactions (9.2% of total, tps = 23.387138)
   - number of failed transactions: 0 (0.000%)
   - latency average = 274.741 ms
   - latency stddev = 55.187 ms
  SQL script 3: /tmp/olap_benchmark.sql
   - weight: 1 (targets 1.0% of total)
   - 759 transactions (1.0% of total, tps = 2.496953)
   - number of failed transactions: 0 (0.000%)
   - latency average = 9146.638 ms
   - latency stddev = 770.821 ms
  
  
  ### ACTION 2 ⬇️
  docker exec -it postgres_sql_container pgbench -c 30 -j 8 -T 300 -M prepared -b tpcb-like@90 -f /tmp/dashboard_benchmark.sql@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  
  ### RETURN 2 ⬇️
  transaction type: multiple scripts
  scaling factor: 500
  query mode: prepared
  number of clients: 30
  number of threads: 8
  maximum number of tries: 1
  duration: 300 s
  number of transactions actually processed: 78386
  number of failed transactions: 0 (0.000%)
  latency average = 116.468 ms
  initial connection time = 7.347 ms
  tps = 257.581563 (without initial connection time)
  SQL script 1: <builtin: TPC-B (sort of)>
   - weight: 90 (targets 90.0% of total)
   - 70635 transactions (90.1% of total, tps = 232.111266)
   - number of failed transactions: 0 (0.000%)
   - latency average = 1.437 ms
   - latency stddev = 1.581 ms
  SQL script 2: /tmp/dashboard_benchmark.sql
   - weight: 9 (targets 9.0% of total)
   - 6965 transactions (8.9% of total, tps = 22.887449)
   - number of failed transactions: 0 (0.000%)
   - latency average = 270.862 ms
   - latency stddev = 29.747 ms
  SQL script 3: /tmp/olap_benchmark.sql
   - weight: 1 (targets 1.0% of total)
   - 785 transactions (1.0% of total, tps = 2.579562)
   - number of failed transactions: 0 (0.000%)
   - latency average = 9001.754 ms
   - latency stddev = 666.161 ms
  ```

<br>

- #### *Docker Desktop vs. WSL2 ( Pure Read Performance )*
  | **Evaluation** | **Docker Desktop<br>( Windows 虛擬層 )** | **WSL2<br>( 原生 Linux 核心 )** | **WSL2<br>( 極限測試 )** | **Performance Improvement ( 非極限比較 )** |
  | :--: | :--: | :--: | :--: | :--: |
  | TPS | 7,499 | 11,577 | 11,764 | + 54.3% |
  | Latency | 4.000 ms | 2.591 ms | 8.500 ms | - 35.2% |
  | Total Transactions | 2.55 million times | 3.47 million times | 3.52 million times | + 1.22 million times |

  ```
  ### DESCRIPTION ⬇️
  # OLTP 的核心確實是 事務（Transaction），包含大量的 UPDATE、INSERT。但為什麼我們還要測純讀取？
  - 排除磁碟干擾： 寫入測試（TPC-B）受限於磁碟 I/O 延遲和 WAL 寫入速度。純讀取可以告訴你：「如果排除掉慢速硬碟，這台機器的 CPU 與記憶體溝通效率極限在哪？」
  - 測試併發處理能力： 即使是純讀取，30 個 Client 還是會競爭 共享緩衝區（Shared Buffers）的內存鎖（LWLocks）。如果這部分的 TPS 上不去，代表你的虛擬化環境（Docker Desktop）在處理內存分頁切換時效率極低。
  - 結論： 純讀取不是重點，但它證明了 WSL2 的系統呼叫損耗比 Docker Desktop 低了 50% 以上。在真實 OLTP 壓力下，這 50% 的優勢會轉化為更快的索引查詢與快取命中處理。
  
  
  # 極限測試
  -c 128: 餵飽 32 核心（每個核心處理 4 個連線）
  -j 32: 讓 pgbench 壓測工具也用滿 32 執行緒
  -M prepared: 測試真正的「記憶體檢索速度」，而不是測試「SQL 解析速度」
  - 總結 : 在 32 核機器上只跑出 1.1 萬 TPS 是不科學的。這通常是因為 Windows 的核心調度器 (Scheduler) 無法有效地把高頻率的虛擬機請求分發給 32 個物理核心。
  若把同樣的配置搬到純 Linux（非虛擬化）環境，數字通常會直接噴發到 10 萬以上。WSL2 雖強，但在「超高併發」的極限壓測下，虛擬化層的代價會變得很明顯。
  ```

<br>

- #### *Performance Comparison of Load Modes*
  | **Load Modes** | **Evaluation ( TPS )** | **Description** |
  | :--: | :--: | :-- |
  | OLTP | 2111 | 高併發小事務，平均延遲僅 14.2 ms |
  | OLAP | 3.9 | 複雜查詢，平均延遲高達 7,622 ms |
  | HTAP | 253.9 | 受到 1% OLAP 查詢的資源佔用影響，總吞吐量大幅下降 |
  
  ```
  ### DESCRIPTION ⬇️
  # 在混合負載（90% OLTP / 9% Dashboard / 1% OLAP）的場景下，數據呈現明顯的「木桶效應」：
  - OLTP (Layer 1): 表現最穩定，延遲從純負載的 14ms 降至 1.4ms ~ 2ms（因為總請求量受限於長查詢，單次處理速度反而變快）。
  - Near-Real-Time (Layer 2): 提供儀表板使用的中度查詢，延遲落在 270ms ~ 274ms。
  - OLAP (Layer 3): 雖然僅佔 1% 的比例，但其延遲高達 9,000ms+。這 1% 的重量級查詢是拖慢整體 TPS（從 2111 降至 253）的主要原因。
  
  
  # 測試中對比了「簡單查詢 (Simple)」與「預編譯查詢 (Prepared)」對混合負載的影響：
  - TPS 提升: 從 253.9 微幅增加至 257.5 (+1.4%)。
  - OLTP 延遲優化: 在 Prepared 模式下，OLTP 的平均延遲從 2.084ms 降至 1.437ms，優化效果達 31%。
  - 結論: 對於高比例的 OLTP 混合場景，開啟 prepared 模式能顯著降低解析開銷，讓短指令處理更高效。
  
  
  # 關鍵洞察與建議
  - 資源爭搶明顯: 當 OLAP 佔比僅 1% 時，整體的 TPS 就產生了劇烈下滑。這證明了在單機 PostgreSQL 中執行 HTAP 時，長查詢會產生嚴重的 I/O 或 CPU 鎖定，影響 OLTP 的處理頻率。
  - 延遲落差極大: 最快與最慢的請求延遲相差約 6,000 倍 (1.4ms vs 9,000ms)，這在實務上可能導致連線池（Connection Pool）被長查詢佔滿。
  - 後續建議: 
      1.  讀寫分離: 考慮引入副本（Replica）處理那 1% 的 OLAP 與 9% 的 Dashboard 請求。
      2.  資源隔離: 若必須在同一台機器，建議調整 max_parallel_workers 或使用 cgroups 限制背景分析任務的資源。
      3.  索引優化: 針對 Layer 2 (Dashboard) 的查詢進行特定索引優化，降低其 270ms 的延遲，以釋放更多 worker 給 OLTP 使用。
  ```

<br>

- #### *~~5.　Saturation Benchmark~~*
  | **Evaluation** | **30 Clients ( Sweet Spot )** | **50 Clients ( Medium-load )** | **100 Clients ( High-load )** | **Trend ( 30 vs 100 )** |
  | :--: | :--: | :--: | :--: | :--: |
  | AVG TPS | - | - | - | - |
  | AVG Latency ( ms ) | - | - | - | - |
  | OLTP Std Dev ( ms ) | - | - | - | - |
  | OLAP Std Dev ( ms ) | - | - | - | - |
  | Conn Overhead ( ms ) | - | - | - | - |

<br>