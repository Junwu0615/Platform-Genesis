## *🪛 shm_size: 16 GB*
![PNG](../assets/generic_result_2.png)

<br>

### *Generic DB Benchmark*
| **Step** | **Description** | **Tool** |
| :--: | :-- | :--: |
| [1](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#1query-benchmark) | Query Benchmark | direct query method |
| [2](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#2oltp-workload-benchmark) | OLTP Workload Benchmark | use pgbench by docker |
| [3](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#3olap-workload-benchmark) | OLAP Workload Benchmark | use pgbench by docker |
| [4](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#4htap-workload-benchmark) | HTAP Workload Benchmark | use pgbench by docker |
| [5](https://github.com/Junwu0615/OLTP-OLAP-Unified-DB/blob/main/docs/generic_result_2.md#5saturation-benchmark) | Saturation Benchmark | use pgbench by docker |

<br>

### *DB Dedicated Machine Settings*
![PNG](../assets/shm_size.png)

<br>

### *Settings Before Action*
```
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
```

<br>

- #### *[ SKIP ] 1.　Query Benchmark*
- #### *[ SKIP ] 2.　OLTP Workload Benchmark*
- #### *[ SKIP ] 3.　OLAP Workload Benchmark*
- #### *[ SKIP ] 4.　HTAP Workload Benchmark*
- #### *5.　Saturation Benchmark*
  ```
  ### ACTION 1 ⬇️
  docker exec -it postgres_sql_container pgbench -c 30 -j 8 -T 60 -b tpcb-like@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  ### RETURN 1 ⬇️
  
  
  ### ACTION 2 ⬇️
  docker exec -it postgres_sql_container pgbench -c 50 -j 8 -T 60 -b tpcb-like@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
  
  ### ACTION 3 ⬇️
  docker exec -it postgres_sql_container pgbench -c 100 -j 8 -T 60 -b tpcb-like@9 -f /tmp/olap_benchmark.sql@1 -U pguser -d pgdatabase
  
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