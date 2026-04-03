## *🪛 shm_size: 16 GB*
### *Settings ( shared_buffers / work_mem / synchronous_commit )*
![PNG](../assets/generic_result_2.png)

<br>

### *Generic DB Benchmark*
| **Step** | **Description** | **Tool** |
| :--: | :-- | :--: |
| [0](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#0initialize-pgbench-benchmark-data) | Initialize pgbench Benchmark Data | - |
| [1](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#1query-benchmark) | Query Benchmark | direct query method |
| [2](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#-skip--2oltp-workload-benchmark) | OLTP Workload Benchmark | use pgbench |
| [3](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#3olap-workload-benchmark) | OLAP Workload Benchmark | use pgbench |
| [4](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#4htap-workload-benchmark) | HTAP Workload Benchmark | use pgbench |
| [5](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#5saturation-benchmark) | Saturation Benchmark | use pgbench |

<br>

### *DB Dedicated Machine Settings*
![PNG](../assets/shm_size.png)

<br>

### *Settings Before Action*
```
-- 從 Docker-Desktop 移進 WSL2
-- 由 /home 使用檔案 + compose up 避免遇到
  -- 9P 協定瓶頸: 這層通訊開銷極大，比 Windows 本生虛擬化還慢
  -- I/O 延遲爆炸: 頻繁切換寫入 WAL 和 Data blocks
mkdir -p ~/OLTP-OLAP-Unified-DB
cp -r /mnt/c/專案路徑/* ~/OLTP-OLAP-Unified-DB/
cp -r /mnt/c/Users/PC/Code/Python/Publish-To-Git/OLTP-OLAP-Unified-DB/src ~/OLTP-OLAP-Unified-DB/


-- 用 WSL2 確認容器資源限制 ( 預期32 )
nproc


-- 建立 'pgbench_accounts' 索引
docker exec -it postgres_sql_container psql -U pguser -d pgdatabase -c "
-- CREATE INDEX idx_accounts_aid_mod10 ON pgbench_accounts ((aid % 10));
CREATE INDEX idx_ultra_fast ON pgbench_accounts ((aid % 10), abalance);
ANALYZE pgbench_accounts;
"


-- 避免高並發時崩潰
-- TPS: 穩定性提升
docker-compose setting shm_size


-- 提升快取與工作記憶體
-- 減少實體 IO 讀取
-- TPS: +20% ~ 50%
ALTER ROLE pguser SET shared_buffers = '10GB';
ALTER ROLE pguser SET work_mem = '128MB'; # 100(conn) * 128(MB) = 12.5(GB)


-- 暴力提升寫入吞吐量 (實驗專用)
-- 消除 WAL 寫入延遲
-- TPS: +100% ~ 300%
ALTER ROLE pguser SET synchronous_commit = 'off';
ALTER ROLE pguser SET checkpoint_completion_target = '0.9';


-- 允許更多背景工作人員處理 OLAP
-- 充分利用多核心 CPU
-- TPS: OLAP 加速
ALTER ROLE pguser SET max_parallel_workers_per_gather = 4;


-- 確認設定已生效
docker exec -it postgres_sql_container psql -U pguser -d pgdatabase

SHOW shared_buffers;
SHOW work_mem;
SHOW synchronous_commit;


-- 持續監控容器資源使用狀況
docker stats postgres_sql_container --no-stream
```

<br>

- #### *0.　Initialize pgbench Benchmark Data*
  ```
  ### INITIALIZE ONCE ⬇️
   -s 1: 約 10 萬筆資料
   -s 50: 約 500 萬筆資料
   ⭐ -s 500: 約 5000 萬筆資料
  
  docker exec -it postgres_sql_container pgbench -i -s 500 -U pguser -d pgdatabase
  ```

- #### *~~1.　Query Benchmark~~*
- #### *~~2.　OLTP Workload Benchmark~~*
- #### *~~3.　OLAP Workload Benchmark~~*
- #### *~~4.　HTAP Workload Benchmark~~*
- #### *~~5.　Saturation Benchmark~~*
  ```
  ### ACTION 1 ⬇️
  docker exec -it postgres_sql_container pgbench -c 30 -j 8 -T 60 -b tpcb-like@99 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  ### RETURN 1 ⬇️
  transaction type: multiple scripts
  scaling factor: 50
  query mode: simple
  number of clients: 30
  number of threads: 8
  maximum number of tries: 1
  duration: 60 s
  number of transactions actually processed: 82096
  number of failed transactions: 0 (0.000%)
  latency average = 21.929 ms
  initial connection time = 11.008 ms
  tps = 1368.021608 (without initial connection time)
  SQL script 1: <builtin: TPC-B (sort of)>
   - weight: 9 (targets 90.0% of total)
   - 74020 transactions (90.2% of total, tps = 1233.445715)
   - number of failed transactions: 0 (0.000%)
   - latency average = 20.716 ms
   - latency stddev = 10.149 ms
  SQL script 2: /tmp/olap_benchmark.sql
   - weight: 1 (targets 10.0% of total)
   - 8075 transactions (9.8% of total, tps = 134.559229)
   - number of failed transactions: 0 (0.000%)
   - latency average = 14.318 ms
   - latency stddev = 3.772 ms
  
  
  ### ACTION 2 ⬇️
  docker exec -it postgres_sql_container pgbench -c 50 -j 8 -T 60 -b tpcb-like@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  ### RETURN 2 ⬇️
  transaction type: multiple scripts
  scaling factor: 50
  query mode: simple
  number of clients: 50
  number of threads: 8
  maximum number of tries: 1
  duration: 60 s
  number of transactions actually processed: 79764
  number of failed transactions: 0 (0.000%)
  latency average = 37.613 ms
  initial connection time = 15.248 ms
  tps = 1329.315810 (without initial connection time)
  SQL script 1: <builtin: TPC-B (sort of)>
   - weight: 9 (targets 90.0% of total)
   - 71932 transactions (90.2% of total, tps = 1198.790743)
   - number of failed transactions: 0 (0.000%)
   - latency average = 34.641 ms
   - latency stddev = 35.182 ms
  SQL script 2: /tmp/olap_benchmark.sql
   - weight: 1 (targets 10.0% of total)
   - 7830 transactions (9.8% of total, tps = 130.491736)
   - number of failed transactions: 0 (0.000%)
   - latency average = 19.225 ms
   - latency stddev = 24.777 ms
  
  
  ### ACTION 3 ⬇️
  docker exec -it postgres_sql_container pgbench -c 100 -j 8 -T 60 -b tpcb-like@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  # ⚠️ 使用 -M prepared (預編譯語句) 可以減少 SQL 解析時間，通常能提升 10-20% TPS
  docker exec -it postgres_sql_container pgbench -c 100 -j 8 -T 60 -M prepared -b tpcb-like@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  # ⚠️ 使用 -b select-only (只執行 SELECT 查詢) 可以減少寫入操作的鎖競爭，通常能提升 20-50% TPS，特別是在高併發情況下
  docker exec -it postgres_sql_container pgbench -c 100 -j 8 -T 60 -b select-only@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  ### RETURN 3 ⬇️
  transaction type: multiple scripts
  scaling factor: 50
  query mode: simple
  number of clients: 100
  number of threads: 8
  maximum number of tries: 1
  duration: 60 s
  number of transactions actually processed: 83229
  number of failed transactions: 0 (0.000%)
  latency average = 72.044 ms
  initial connection time = 74.120 ms
  tps = 1388.035173 (without initial connection time)
  SQL script 1: <builtin: TPC-B (sort of)>
   - weight: 9 (targets 90.0% of total)
   - 75059 transactions (90.2% of total, tps = 1251.781615)
   - number of failed transactions: 0 (0.000%)
   - latency average = 68.311 ms
   - latency stddev = 42.065 ms
  SQL script 2: /tmp/olap_benchmark.sql
   - weight: 1 (targets 10.0% of total)
   - 8169 transactions (9.8% of total, tps = 136.236881)
   - number of failed transactions: 0 (0.000%)
   - latency average = 25.134 ms
   - latency stddev = 9.421 ms
  ```

  | **Evaluation** | **30 Clients ( Sweet Spot )** | **50 Clients ( Medium-load )** | **100 Clients ( High-load )** | **Trend ( 30 vs 100 )** |
  | :--: | :--: | :--: | :--: | :--: |
  | AVG TPS | - | - | - | - |
  | AVG Latency ( ms ) | - | - | - | - |
  | OLTP Std Dev ( ms ) | - | - | - | - |
  | OLAP Std Dev ( ms ) | - | - | - | - |
  | Conn Overhead ( ms ) | - | - | - | - |

  ```
  ### DESCRIPTION ⬇️

  ### OPTIMIZATION PLAN ⬇️
  ```

<br>