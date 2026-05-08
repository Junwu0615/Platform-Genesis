### *A.1.　Table Description*
- #### *a.　OLTP*
  |**Name**|**Description**|**Remark**|
  |--:|:--|:--|
  | machine | 儲存機台基本資訊，例如機台編號、機台名稱、機台型號、所屬產線等 | - |
  | product | 儲存產品基本資訊，例如產品名稱、產品型號與規格 | - |
  | 🗑️ machine_events | 記錄機台運行過程中的各類事件，例如故障、維修、警報、重新啟動等事件，用於追蹤設備歷史行為 | - |
  | machine_status_logs | 持續記錄機台狀態變化，例如 RUNNING、IDLE、ALARM 等，形成時間序列資料 | OLAP 建立後，超過 3 個月的資料就可以考慮封存或刪除，以維持生產庫的輕量化 |
  | production_orders | 記錄生產訂單資訊，例如訂單編號、生產產品、目標產量、開始時間與結束時間 | - |
  | production_records | 記錄實際生產結果，例如某台機台在某時間段生產的產品與產量 | OLAP 建立後，超過 3 個月的資料就可以考慮封存或刪除，以維持生產庫的輕量化 |

  ```
  product
     │
     │ product_id
     │
     ▼
  production_orders
     │
     │ order_id
     │
     ▼
  production_records
     ▲
     │
     │  machine_id
     │
  machine ————▶ machine_events
     │
     └──────── machine_status_logs
  ```

 #### *b.　OLAP*
  |**Name**|**Description**|**Remark**|
  |--:|:--|:--|
  | dim_date | 時間維度表，將時間拆分為年、月、日、小時等欄位，方便進行時間分析 | 常見 OLAP 維度 |
  | dim_machine | 機台維度表，提供機台相關屬性，例如機台名稱、型號、產線等，用於分析時的維度資訊 | - |
  | dim_product | 產品維度表，包含產品名稱、產品類型與其他產品屬性，用於分析生產狀況 | - |
  | fact_machine_status | 機台狀態事實表，記錄機台在各時間點的運行狀態統計資料，例如運行時間、停機時間等 | - |
  | fact_production | 生產事實表，記錄機台生產產品的統計資料，例如產量、生產時間等 | - |

  ```
  olap
   │
   ├── dim_machine
   ├── dim_product
   ├── dim_date
   │
   ├── fact_machine_status
   └── fact_production

  # ------------------------ Star Schema ------------------------ #
  
                             dim_machine
                                  │
                                  │  machine_key
                                  │  
            time_key              ▼
  dim_date ──────────▶ fact_machine_status
                                  │
                                  │
                             dim_product
                                  │
                                  │  product_key
                                  │
                                  ▼
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
      - #### *Sub-Dimension Table ...etc.*
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

### *⭐ C.　權限設置*
| 角色層級 | 帳號 | LOGIN | 核心能力 | 風險程度 |
| :--: | :--: | :--: | :--: | :--: |
| superuser | `postgres / pguser` | ✔ | 系統維護、DB 配置、建立資料庫 | 🔴 |
| deployment | `migration_user` | ✔ | schema migration、DDL 部署 | 🟡 |
| owner | `oltp_owner` / `olap_owner` | ❌ | 擁有 schema / table / view | 🟡 |
| user | `oltp_user` / `olap_user` | ✔ | CRUD 資料操作 | 🟢 |

- ### *1.　Create Role*
  - #### *1.1.　OLTP Role*
    ```
    -- oltp_owner: 擁有者權限 + 不允許登入
    CREATE ROLE oltp_owner NOLOGIN;
    
    -- oltp_user: 讀/寫權限
    CREATE ROLE oltp_user LOGIN PASSWORD 'oltp_pwd';
    ```
  - #### *1.2.　OLAP Role*
    ```
    -- olap_owner: 擁有者權限 + 不允許登入
    CREATE ROLE olap_owner NOLOGIN;
    
    -- olap_user: 只讀權限
    CREATE ROLE olap_user LOGIN PASSWORD 'olap_pwd';
    ```
  - #### *1.3.　Migration Role*
    ```
    -- migration_user: 允許使用 owner 權限
    CREATE ROLE migration_user LOGIN PASSWORD 'migration_pwd';
    ```
- ### *2.　Schema 權限隔離*
  - #### *2.1.　OLTP Role*
    ```
    -- 1. 確保 oltp_owner 為 oltp schema 擁有者
    ALTER SCHEMA oltp OWNER TO oltp_owner;
  
    -- 2. 確保 oltp_user 只能在 oltp schema 讀/寫資料，但不能改結構
    GRANT USAGE ON SCHEMA oltp TO oltp_user;
    -- 針對表格
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA oltp TO oltp_user;
    -- 針對序號
    GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA oltp TO oltp_user;
    
    -- 3. 設定未來新建表格的預設權限
    -- 針對表格： 確保以後新創的表, oltp_user 都能讀寫
    ALTER DEFAULT PRIVILEGES FOR ROLE oltp_owner IN SCHEMA oltp
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO oltp_user;
    -- 針對序號： 確保以後新創的自增 ID, oltp_user 都能使用
    ALTER DEFAULT PRIVILEGES FOR ROLE oltp_owner IN SCHEMA oltp
    GRANT USAGE, SELECT ON SEQUENCES TO oltp_user;
    ```
  - #### *2.2.　OLAP Role*
    ```
    -- 1. 確保 olap_owner 為 olap schema 擁有者
    ALTER SCHEMA olap OWNER TO olap_owner;
  
    -- 2. 確保 olap_user 只能在 olap schema 讀/寫資料，但不能改結構
    GRANT USAGE ON SCHEMA olap TO olap_user;
    -- 針對表格
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA olap TO olap_user;
    -- 針對序號
    GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA olap TO olap_user;
  
    -- 3. 設定未來新建物件的預設權限
    -- 針對表格： 確保以後新創的表, olap_user 都能讀寫
    ALTER DEFAULT PRIVILEGES FOR ROLE olap_owner IN SCHEMA olap
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO olap_user;
    -- 針對序號： 確保以後新創的自增 ID, olap_user 都能使用
    ALTER DEFAULT PRIVILEGES FOR ROLE olap_owner IN SCHEMA olap
    GRANT USAGE, SELECT ON SEQUENCES TO olap_user;
  
    -- 4. 確保 olap_user 只能在 oltp schema 讀取資料
    GRANT USAGE ON SCHEMA oltp TO olap_user;
    GRANT SELECT ON ALL TABLES IN SCHEMA oltp TO olap_user;
    ```
  - #### *2.3.　Migration Role*
    ```
    -- 1. 角色關係與繼承
    GRANT oltp_owner TO migration_user;
    GRANT olap_owner TO migration_user;
    
    -- 2. Schema 權限
    GRANT USAGE, CREATE ON SCHEMA oltp TO oltp_owner;
    GRANT USAGE, CREATE ON SCHEMA olap TO olap_owner;
    
    -- 3. 修正「舊表」的所有權 ( 若原本是 superuser 建的 ) 把整個 Schema 的擁有者直接改掉
    ALTER SCHEMA oltp OWNER TO oltp_owner;
    ALTER SCHEMA olap OWNER TO olap_owner;
    
    -- 4. 設定預設權限 : 確保 migration_user 進去建立的表，自動讓 owner 擁有完整權限
    ALTER DEFAULT PRIVILEGES FOR ROLE migration_user IN SCHEMA oltp
    GRANT ALL ON TABLES TO oltp_owner;
    ALTER DEFAULT PRIVILEGES FOR ROLE migration_user IN SCHEMA oltp
    GRANT ALL ON SEQUENCES TO oltp_owner;

    ALTER DEFAULT PRIVILEGES FOR ROLE migration_user IN SCHEMA olap
    GRANT ALL ON TABLES TO olap_owner;
    ALTER DEFAULT PRIVILEGES FOR ROLE migration_user IN SCHEMA olap
    GRANT ALL ON SEQUENCES TO olap_owner;
    ```
  - #### *2.4.　Remove Public Role 預設權限*
    ```
    REVOKE ALL ON SCHEMA oltp FROM PUBLIC;
    REVOKE ALL ON SCHEMA olap FROM PUBLIC;
    ```

- ### *3.　設定 Default Schema*
  ```
  ALTER ROLE oltp_owner
  SET search_path = oltp;
  
  ALTER ROLE oltp_user
  SET search_path = oltp;
  
  ALTER ROLE olap_owner
  SET search_path = olap;
  
  ALTER ROLE olap_user
  SET search_path = olap;
  ```
  
- ### *4.　設定使用時區*
  ```
  -- 數據保持 +0 時區 ; 讀取操作顯示 +8 時區
  -- 1. 任何連線進來的用戶，如果沒有額外設定，則顯示+8
  ALTER DATABASE pgdatabase SET timezone TO 'Asia/Taipei';
  
  -- 2. 確保特定用戶登入時一定是+8
  ALTER ROLE pguser SET timezone TO 'Asia/Taipei';
  ALTER ROLE migration_user SET timezone TO 'Asia/Taipei';
  ALTER ROLE oltp_owner SET timezone TO 'Asia/Taipei';
  ALTER ROLE olap_owner SET timezone TO 'Asia/Taipei';
  ALTER ROLE oltp_user SET timezone TO 'Asia/Taipei';
  ALTER ROLE olap_user SET timezone TO 'Asia/Taipei';
  ```

- ### *5.　設定使用者資源使用上限 ( 避免屎 SQL 拖垮整個實例 )*
  - #### *⭐ 5.1.　Query 執行時間限制*
    ```
    -- 避免使用者寫出無限迴圈的 SQL，或是拖垮整個實例的 SQL
    -- statement_timeout: query 最長執行時間 → 自動 kill query
  
    -- 正在進行 stream 級別的寫入，給予一個【 寬裕 】但【 有上限 】的保護
    ALTER ROLE oltp_user
    SET statement_timeout = '10s';
  
    ALTER ROLE olap_user
    SET statement_timeout = '60s';
    ```

  - #### *5.2.　Query planning 限制*
    ```
    -- lock_timeout: 等鎖最長時間 → 直接失敗
  
    ALTER ROLE oltp_user
    SET lock_timeout = '3s';
  
    ALTER ROLE olap_user
    SET lock_timeout = '10s';
    ```

  - #### *5.3.　idle 連線限制*
    ```
    -- idle_in_transaction_session_timeout: 忘記 commit 的 session → kill session
  
    ALTER ROLE oltp_user
    SET idle_in_transaction_session_timeout = '30s';
  
    ALTER ROLE olap_user
    SET idle_in_transaction_session_timeout = '60s';
    ```

  - #### *⭐ 5.4.　Memory 限制*
    ```
    -- 避免一個 query 吃爆 RAM 
    -- 最常拖垮系統的原因就是 work_mem 設定過大 → 大量資料排序/聚合 → 吃爆記憶體 → 整個實例當掉
  
    ALTER ROLE oltp_user
    SET work_mem = '8MB';
  
    ALTER ROLE olap_user
    SET work_mem = '64MB';
    ```

  - #### *5.5.　Parallel query 限制*
    ```
    -- Parallel 只有在 large scan / aggregation 才有用
  
    ALTER ROLE oltp_user
    SET max_parallel_workers_per_gather = 0;
    
    -- 允許更多人員處理 OLAP / 充分利用多核心 CPU / TPS: OLAP 加速
    ALTER ROLE olap_user
    SET max_parallel_workers_per_gather = 4;
    ```

  - #### *⭐ 5.6.　連線數限制*
    ```
    -- 直接限制 user 連線數
  
    ALTER ROLE oltp_user
    CONNECTION LIMIT 100;
  
    ALTER ROLE olap_user
    CONNECTION LIMIT 5;
    ```

  - #### *⭐ 5.7.　temp file 限制*
    ```
    -- temp_file_limit: query 可用 disk 上限
    -- 避免 query 做大量 sort / hash 吃爆磁碟空間, 導致整個實例當掉 
  
    ALTER ROLE oltp_user
    SET temp_file_limit = '0.5GB';
  
    ALTER ROLE olap_user
    SET temp_file_limit = '2GB';
    ```

<br>

### *D.　Create Table & Index Settings*
- ### *1.　Create Table List*
  ```
  oltp.machine_events
  oltp.machine_status_logs
  oltp.machine
  oltp.production_orders
  oltp.production_records
  oltp.product
  
  olap.dim_machine
  olap.dim_product
  olap.dim_date
  olap.fact_machine_status
  olap.fact_production

  ### 懶人建表指令 ###
  docker cp "dags/sql/models/oltp" pg-cluster-dev-db-1:/tmp
  docker cp "dags/sql/models/olap" pg-cluster-dev-db-1:/tmp
  
  docker exec -it pg-cluster-dev-db-1 psql -U migration_user -d pgdatabase
  
  SET ROLE oltp_owner;
  SELECT current_user, session_user;
  
  \i /tmp/oltp/machine.sql
  \i /tmp/oltp/product.sql
  \i /tmp/oltp/machine_status_logs.sql
  \i /tmp/oltp/production_orders.sql
  \i /tmp/oltp/production_records.sql
  
  SET ROLE olap_owner;
  SELECT current_user, session_user;
  
  \i /tmp/olap/dim_machine.sql
  \i /tmp/olap/dim_product.sql
  \i /tmp/olap/dim_date.sql
  \i /tmp/olap/fact_machine_status.sql
  \i /tmp/olap/fact_production.sql
  ```
  ![PNG](../assets/all_table.png)

- ### *⭐ 2.　Index 加速查詢*
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
  
  X -> oltp.product # product_id SERIAL PRIMARY KEY 已經建立
  idx_machine_line -> oltp.machine
  idx_orders_product -> oltp.production_orders
  idx_production_machine_time -> oltp.production_records
  idx_events_machine_time -> oltp.machine_events
  idx_status_machine_time -> oltp.machine_status_logs
  ```

<br>

### *E.　建立物化檢視表 ( Materialized View, MV )*

<br>

### *F.　常見查詢*
- ### *⭐ Notice : 檢查特定用戶對所有表的權限*
  ```
  SELECT 
      schemaname, 
      tablename, 
      has_table_privilege('olap_user', schemaname || '.' || tablename, 'SELECT') AS can_select,
      has_table_privilege('olap_user', schemaname || '.' || tablename, 'INSERT') AS can_insert,
      has_table_privilege('olap_user', schemaname || '.' || tablename, 'UPDATE') AS can_update,
      has_table_privilege('olap_user', schemaname || '.' || tablename, 'DELETE') AS can_delete
  FROM pg_tables
  WHERE schemaname IN ('olap', 'oltp')
  ORDER BY schemaname, tablename;
  ```

- ### *⭐ Notice : 檢視 Schema 層級的權限 ( Usage/Create )*
  ```
  r: SELECT
  a: INSERT
  w: UPDATE
  d: DELETE
  D: TRUNCATE
  x: REFERENCES
  t: TRIGGER
  U: USAGE (for Schema or Sequence)
  
  SELECT 
      n.nspname AS schema_name,
      pg_catalog.pg_get_userbyid(n.nspowner) AS owner,
      pg_catalog.obj_description(n.oid, 'pg_namespace') AS description,
      n.nspacl AS access_privileges -- 顯示 ACL 字符串
  FROM pg_catalog.pg_namespace n
  WHERE n.nspname IN ('olap', 'oltp');
  ```

- ### *⭐ Notice : Default Privileges*
  ```
  SELECT 
      pg_get_userbyid(defaclrole) AS grantor_role, -- 誰建立物件會觸發
      defaclnamespace::regnamespace AS schema_name,
      defaclobjtype AS object_type, -- T 代表 Table, S 代表 Sequence
      defaclacl AS default_permissions
  FROM pg_default_acl;
  ```

- ### *⭐ Notice : 檢查表格擁有者*
  ```
  SELECT
    schemaname,
    tablename, 
    tableowner
  FROM pg_tables 
  WHERE 1=1
  -- AND schemaname = 'oltp' 
  AND schemaname = 'olap'
  ```
  
- ### *⭐ Notice : 轉移表格擁有權限*
  ```
  -- 轉移 oltp.product 擁有權給 oltp_owner
  ALTER TABLE oltp.product OWNER TO oltp_owner;
  
  -- 轉移 olap.dim_product 擁有權給 olap_owner
  ALTER TABLE olap.dim_product OWNER TO olap_owner;
  ```
  
- ### *⭐ Notice : 查詢卡住的 PID 並殺掉*
  ```
  -- 查詢正在執行的 SQL，找出卡在 target_table 的 PID
  SELECT pid, state, query, wait_event_type, wait_event 
  FROM pg_stat_activity 
  WHERE 1=1
  AND query ILIKE '%target_table%'
  AND pid <> pg_backend_pid();
  
  -- 強制結束該查詢
  SELECT pg_terminate_backend(???);
  ```
  
- ### *⭐ Notice : 刪除表格資料*
  ```
  -- TRUNCATE 是 DDL 指令，它不記錄每一行的刪除，而是直接把資料檔案「截斷」歸零
  -- TRUNCATE 速度比 DELETE 快 100 倍以上
  -- TRUNCATE 本身不允許刪除被引用的表格，除非加上 CASCADE
  -- 加上 CASCADE 會連同那些引用它的子表也一併清空
  -- [ 建議 ] 若要移除表格，可先 TRUNCATE 清空資料，再 DROP 刪除結構
  
  -- 清空資料但保留結構(引用的子表也一併清空)，並重置自增 ID
  TRUNCATE TABLE oltp.table RESTART IDENTITY CASCADE;
  
  -- 清空資料但保留結構(引用的子表也一併清空)，不重置自增 ID
  TRUNCATE TABLE oltp.table CASCADE;
  
  -- 慎用 ! 會逐行刪除資料，速度慢，且可能導致鎖表
  DELETE FROM oltp.table; 
  ```
  
- ### *Notice : 殺掉所有除了自己以外的連線*
  ```
  SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
  WHERE 1=1
  AND pid <> pg_backend_pid()
  AND datname = 'pgdatabase';
  ```

- ### *Notice : 查詢誰正在占用位置*
  ```
  SELECT pid, usename, datname, state, query, backend_start
  FROM pg_stat_activity
  WHERE 1=1
  AND state IS NOT NULL
  ORDER BY state, backend_start;
  ```

- ### *Notice : 查詢總連線數 + 連線設置上限*
  ```
  SELECT
      state,
      count(*),
      sum(count(*)) OVER() as total_connections,
      (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') as max_limit
  FROM pg_stat_activity
  GROUP BY state;
  ```
  
- ### *Notice : 查詢所有閒置連線（包含詳細資訊）*
  ```
  SELECT
      pid,                     -- 進程 ID (殺掉連線時需要)
      usename,                 -- 登入用戶
      datname,                 -- 資料庫名稱
      state,                   -- 狀態
      backend_start,           -- 連線建立時間
      state_change,            -- 最後一次操作的時間
      now() - state_change 
             AS idle_duration, -- 閒置多久
      query                    -- 最後執行的 SQL
  FROM pg_stat_activity
  WHERE 1=1
  AND state = 'idle'           -- 鎖定閒置
  AND pid <> pg_backend_pid(); -- 排除「正在執行這條查詢」的自己
  ```

- ### *⭐ Migration User : 建表時要切換角色*
  ```
  -- 1. 切換身分
  SET ROLE oltp_owner;
  -- SET ROLE olap_owner;
  
  -- 2. 確認目前身分 ( 確保已經切換成功 )
  SELECT current_user, session_user;
  
  -- 3. 操作指令
  CREATE TABLE oltp.table (...);
  -- CREATE TABLE olap.table (...);
  
  -- 4. [ 可選 ] 操作完畢後切回原始身分
  RESET ROLE;
  ```

- ### *OLTP : 查詢生產完畢的訂單*
  ```
  SELECT *
  FROM oltp.production_orders
  WHERE 1=1
  -- AND start_at IS NULL
  -- AND start_at IS NOT NULL
  AND end_at IS NOT NULL
  ORDER BY created_at DESC
  ```

- ### *OLTP : 查詢指定機台生產狀況*
  ```
  SELECT *
  FROM oltp.machine_status_logs
  WHERE 1=1
  AND machine_id = 331
  -- AND status = 'ALARM'
  ORDER BY event_time ASC
  ```

- ### *OLAP : 每台機器運行時間*
  ```
  SELECT
      m.machine_name,
      t.year,
      t.month,
      COUNT(*)
  FROM olap.fact_machine_status f
  JOIN olap.dim_machine m
  ON 1=1
    AND f.machine_key = m.machine_key
  JOIN olap.dim_date t
  ON 1=1
    AND f.time_key = t.time_key
  WHERE 1=1
    AND f.status = 'RUNNING'
  GROUP BY m.machine_name, t.year, t.month;
  ```
  
- ### *OLAP : 每個產品產量*
  ```
  SELECT
      p.product_name,
      SUM(quantity)
  FROM olap.fact_production f
  JOIN olap.dim_product p
  ON 1=1
    AND f.product_key = p.product_key
  GROUP BY p.product_name;
  ```
  

<br><br><br>