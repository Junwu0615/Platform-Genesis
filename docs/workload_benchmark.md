### *A.　Event Description*
```
# 以製造工廠為主題情境
  - 定義機台 [mach] : machines
  - 定義訂單 [prod] : products
  - 生產訂單 [prod_order] : production_orders <- [products]
  - 機台狀態 [mach_st_log] : machine_status_logs
  - 生產產出 [prod_recd] : production_records <- [production_orders, machines, products]


   建立訂單 [prod_order]
      │
      ▼
   開始生產 [prod_order.start_at]
      │
      ▼
  狀態發生變化 [mach_st_log.status]
      ▲
      │
      ▼
   持續生產 [prod_recd.quantity]
      │
      ▼
    達到 [prod_order.quantity]
      │
      ▼
   完成訂單 [prod_order.end_at]
```

<br>

### *B.　Table Features*
- #### *OLTP*
|**Name**|**Type**|**Streaming**|**Description**|**Remark**|
|--:|:--:|:--:|:--|:--:|
| machines | 靜態 | - | 機台基本資訊 | ⚠ 預處理 |
| products | 靜態 | - | 產品基本資訊 | ⚠ 預處理 |
| 🗑️ machine_events | 動態 | 低頻 | 記錄機台運行過程中的各類事件 | - |
| machine_status_logs | 動態 | 低頻 | 持續記錄機台狀態變化 | - |
| production_orders | 動態 | 低頻 | 記錄生產訂單資訊 | - |
| production_records | 動態 | 高頻 | 記錄實際生產結果 | - |

- #### *OLAP*
|**Name**| **Description**|**Remark**|
|--:|:--|:--:|
| dim_machine | 機台維度表 | - |
| dim_product | 產品維度表 | - |
| dim_time | 時間維度表 | - |
| fact_machine_status | 機台狀態事實表 | - |
| fact_production | 生產事實表 | - |

<br>

### *C.　Settings Before Action*
```
# 定義監控目標
  - OS 層監控： CPU、Memory、Disk I/O、Network I/O、Load
  - DB 層監控： TPS、Latency、Lock、Connection Count、Buffer Cache Hit Ratio
  - WAL 壓力監控： WAL 生成速率、WAL 傳輸速率、WAL 傳輸延遲
  - Table bloat / vacuum 監控： bloat ratio、vacuum 活動頻率、dead tuples 數量
  
# 導入監控工具： Prometheus + Grafana + Postgres-Exporter

# 多開腳本壓測： 漸進式開腳本，觀測同時對同一個資料庫灌資料的影響
  - 開到第 N 個 Python 實例，BATCH_SIZE 的提交速度開始變慢？
  - 加入 OLAP 查詢時，production_records 的插入延遲是否翻倍？
```

<br>

### *D.　Simulation Data Volume*
```
Products:            5
Machines:            20
Orders:              30
Status logs:         ~5000+
Production records:  500
Machine events:      100


# OLTP TPS
OFF_PEAK : ~3/sec
NORMAL   : ~10/sec
PEAK     : ~25/sec


# By Day
| table               | rows/day |
| ------------------- | -------- |
| machine_status_logs | ~200k    |
| production_records  | ~80k     |
| machine_events      | ~10k     |
```

<br>

### *E.　Startup Simulate Script*
- #### *1.　Go to Env*
    ```
    .\.venv\Scripts\activate
    ```
- #### *2.　Initialize Factory Data*
    ```
    python src/scripts/init_factory_data.py
    ```
- #### *3.　Simulate Factory Stream*
    ```
    python src/scripts/simulate_factory_stream.py
    ```

<br>

### *F.　Benchmark*

<br>