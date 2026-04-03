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
-- ex: cp -r /mnt/c/Users/PC/Code/Python/Publish-To-Git/OLTP-OLAP-Unified-DB/src ~/OLTP-OLAP-Unified-DB/


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
  -- docker cp "src/sql/scripts/olap_benchmark.sql" postgres_sql_container:/tmp/olap_benchmark.sql
  docker cp "src/sql/scripts/dashboard.sql" postgres_sql_container:/tmp/dashboard.sql
  docker cp "src/sql/scripts/olap.sql" postgres_sql_container:/tmp/olap.sql
  
  ### 2. 一次性清理 BOM 與 Windows 換行符 (CRLF -> LF) ⬇️
  -- docker exec -it postgres_sql_container sh -c "sed -i '1s/^\xef\xbb\xbf//; s/\r$//' /tmp/olap_benchmark.sql"
  docker exec -it postgres_sql_container sh -c "sed -i '1s/^\xef\xbb\xbf//; s/\r$//' /tmp/dashboard.sql"
  docker exec -it postgres_sql_container sh -c "sed -i '1s/^\xef\xbb\xbf//; s/\r$//' /tmp/olap.sql"
  
  ### 3. CHECK SCRIPT ⬇️
  -- docker exec -it postgres_sql_container cat /tmp/olap_benchmark.sql
  docker exec -it postgres_sql_container cat /tmp/dashboard.sql
  docker exec -it postgres_sql_container cat /tmp/olap.sql
  ```

- #### *~~1.　Query Benchmark~~*
- #### *~~2.　OLTP Workload Benchmark~~*
- #### *~~3.　OLAP Workload Benchmark~~*
- #### *~~4.　HTAP Workload Benchmark~~*
- #### *~~5.　Saturation Benchmark~~*
  | Layer | Item | % |
  | :--: | :-- | :--: |
  | 1 | OLTP ( Source of Truth ) | 90 |
  | 2 | Near-Real-Time Analytics ( Dashboard ) | 9 |
  | 3 | OLAP ( BI ) | 1 |

  ```
  ### ACTION 1 ⬇️
  -- docker exec -it postgres_sql_container pgbench -c 30 -j 8 -T 60 -b tpcb-like@99 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  docker exec -it postgres_sql_container pgbench -c 30 -j 8 -T 300 -b tpcb-like@90 -f /tmp/dashboard.sql@9 -f /tmp/olap.sql@1 -U pguser -d pgdatabase

  
  ### RETURN 1 ⬇️

  
  
  ### ACTION 2 ⬇️
  docker exec -it postgres_sql_container pgbench -c 50 -j 8 -T 60 -b tpcb-like@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  ### RETURN 2 ⬇️

  
  
  ### ACTION 3 ⬇️
  # ⚠️ 使用 -b tpcb-like@9 (90% OLTP, 10% OLAP) 可以模擬更真實的混合負載，通常能提供更全面的性能評估
  docker exec -it postgres_sql_container pgbench -c 100 -j 8 -T 60 -b tpcb-like@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  # ⚠️ 使用 -M prepared (預編譯語句) 可以減少 SQL 解析時間，通常能提升 10-20% TPS
  docker exec -it postgres_sql_container pgbench -c 100 -j 8 -T 60 -M prepared -b tpcb-like@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase

  
  ### RETURN 3 ⬇️
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