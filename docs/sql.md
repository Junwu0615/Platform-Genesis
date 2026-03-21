### *A.1.　Table Description*
- #### *OLTP*
  |**Name**|**Description**|**Remark**|
  |--:|:--:|:--:|
  | machine_events | 記錄機台運行過程中的各類事件，例如故障、維修、警報、重新啟動等事件，用於追蹤設備歷史行為。 | 用於事件追蹤與維修分析 |
  | machine_status_logs | 持續記錄機台狀態變化，例如 RUNNING、IDLE、DOWN 等，形成時間序列資料。 | 依 event_time 進行時間分區 ( Partition Table ) |
  | machines | 儲存機台基本資訊，例如機台編號、機台名稱、機台型號、所屬產線等。 | 機台主資料表 |
  | production_orders | 記錄生產訂單資訊，例如訂單編號、生產產品、目標產量、開始時間與結束時間。 | 生產排程與訂單管理 |
  | production_records | 記錄實際生產結果，例如某台機台在某時間段生產的產品與產量。 | 生產履歷資料 |
  | products | 儲存產品基本資訊，例如產品名稱、產品型號與規格。 | 產品主資料表 |
- #### *OLAP*
  |**Name**|**Description**|**Remark**|
  |--:|:--:|:--:|
  | dim_machine | 機台維度表，提供機台相關屬性，例如機台名稱、型號、產線等，用於分析時的維度資訊。 | Dimension Table |
  | dim_product | 產品維度表，包含產品名稱、產品類型與其他產品屬性，用於分析生產狀況。 | Dimension Table |
  | dim_time | 時間維度表，將時間拆分為年、月、日、小時等欄位，方便進行時間分析。 | 常見 OLAP 維度 |
  | fact_machine_status | 機台狀態事實表，記錄機台在各時間點的運行狀態統計資料，例如運行時間、停機時間等。 | Fact Table |
  | fact_production | 生產事實表，記錄機台生產產品的統計資料，例如產量、生產時間等。 | Fact Table |

  ```
  olap
   │
   ├── dim_machine
   ├── dim_product
   ├── dim_time
   │
   ├── fact_machine_status
   └── fact_production

  # ---------- Star Schema ---------- #
  
               dim_machine
                   │
                   │
  dim_time ── fact_machine_status
                   │
                   │
               dim_product
                   │
                   │
              fact_production
  ```

<br>

### *A.2.　Table Description*
- #### *a.　Define Table DDL*
  - #### *1.　OLTP*
    - #### *1.1.　1NF*
    - #### *1.2.　2NF*
    - #### *1.3.　3NF*
  - #### *2.　OLAP*
    - #### *2.1.　Star Schema*
      - #### *Fact Table*
      - #### *Dimension Table*
    - #### *2.2.　Snowflake Schema*
      - #### *Fact Table*
      - #### *Dimension Table*
      - #### *Sub-Dimension Table ... etc.*
    - #### *2.3.　Wide Table*
- #### *b.　Check Define Table List*
  - #### *1.　OLTP*
    - #### *是否有主鍵 ? ( PK ) 唯一識別一筆資料*
    - #### *是否有外鍵 ? ( FK ) 強制資料一致*
    - #### *是否有 index ? ( PK / FK / 常用查詢條件 )*
    - #### *是否有 transaction ? ( ACID )*
    - #### *是否有適當的 normal form ? ( 1NF / 2NF / 3NF )*
    - #### *是否避免資料冗餘 ?*
  - #### *2.　OLAP*
    - #### *是否有 fact table ?*
    - #### *是否有 dimension ?*
    - #### *是否避免複雜 join ?*
    - #### *是否支援時間分析 ?*
    - #### *是否能快速做 aggregation ?*
    
<br>

### *B.　Settings Schema Mode*
```
CREATE SCHEMA IF NOT EXISTS oltp;
CREATE SCHEMA IF NOT EXISTS olap;
```
![PNG](../assets/create_schema.png)

<br>

### *C.　Create Table*
```
oltp.machine_events
oltp.machine_status_logs
oltp.machines
oltp.production_orders
oltp.production_records
oltp.products

olap.dim_machine
olap.dim_product
olap.dim_time
olap.fact_machine_status
olap.fact_production
```
![PNG](../assets/all_table.png)

<br>

### *D.　Index 加速查詢*
```
# 索引是透過「空間換取時間」，讓資料庫從漫無目的的搜尋，進化為有邏輯的快速定位。
  # 創建目的: 為常見查詢模式服務
  # 優: 大幅提升查詢效率，尤其在大量資料中；
  # 缺: 會佔用額外儲存空間，且在寫入資料時可能會降低性能。
 
# 有無 INDEX 差異對於查詢效率的影響 ( 1000 W rows )：
  # 有: 直接定位 ( 0.02 s )
  # 無: 掃描整個 partition ( 8 s )

# 其他
  # INDEX 定義順序有差
    # 快: (machine_id, event_time) : 先定位 machine_id，再掃時間範圍
    # 慢: (event_time, machine_id) : 先掃整段時間，再過濾 machine
  # 拆分區間
    # 按日: metadata overhead
    # 按月是最折衷作法
    # 按年: table 太大

X -> oltp.products # product_id SERIAL PRIMARY KEY 已經建立
idx_machines_line -> oltp.machines
idx_orders_product -> oltp.production_orders
idx_production_machine_time -> oltp.production_records
idx_events_machine_time -> oltp.machine_events
idx_status_machine_time -> oltp.machine_status_logs
```

<br>

### *E.　常見查詢*
- ### *OLAP : 每台機器運行時間*
  ```
  SELECT
      m.machine_name,
      t.year,
      t.month,
      COUNT(*)
  FROM olap.fact_machine_status f
  JOIN olap.dim_machine m
  ON f.machine_key = m.machine_key
  JOIN olap.dim_time t
  ON f.time_key = t.time_key
  WHERE f.status = 'RUNNING'
  GROUP BY m.machine_name, t.year, t.month;
  ```
- ### *OLAP : 每個產品產量*
  ```
  SELECT
      p.product_name,
      SUM(quantity)
  FROM olap.fact_production f
  JOIN olap.dim_product p
  ON f.product_key = p.product_key
  GROUP BY p.product_name;
  ```