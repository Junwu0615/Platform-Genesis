### *1.　Startup PostgreSQL*
- #### *a.　背景啟動*
  ```
  docker-compose build --no-cache
  docker-compose up -d
  ```
- #### *b.　確認相關設定*
  ```
  -- 確認擴充功能版本
  SELECT name, installed_version 
  FROM pg_available_extensions 
  WHERE installed_version IS NOT NULL;
  
  -- 確認 ??? 是否啟動
  SHOW pg_stat_statements.track;
  SHOW shared_buffers;
  SHOW work_mem;
  SHOW synchronous_commit; -- 用 python client 控制設定 off

  -- 確認 Monitoring 角色 ( has_pg_monitor => true, has_read_stats => true )
  SELECT
      r.rolname,
      m.rolname as member_of,
      r.rolcanlogin AS can_login,
      CASE WHEN r.rolsuper THEN 'YES' ELSE 'NO' END AS is_superuser,
      -- 檢查是否擁有 pg_monitor 權限
      pg_has_role(r.rolname, 'pg_monitor', 'USAGE') AS has_pg_monitor,
      -- 檢查是否擁有 pg_read_all_stats 權限
      pg_has_role(r.rolname, 'pg_read_all_stats', 'USAGE') AS has_read_stats,
      r.rolconnlimit AS conn_limit
  FROM pg_roles r
  LEFT JOIN pg_auth_members am ON r.oid = am.member
  LEFT JOIN pg_roles m ON am.roleid = m.oid
  WHERE r.rolname = 'postgres_exporter';
  
  -- 試著下面語句，確認現在資料庫在「等什麼」
  SELECT * FROM pg_wait_sampling_current;
  ```

<br>

### *~~2.　Setting Account to Airflow in PostgreSQL~~*
- #### *a.　進入 PostgreSQL container*
  ```
  # -U : 使用已存在的使用者
  # -d : 連到對應資料庫
  
  docker exec -it postgres_sql_container psql -U pguser -d pgdatabase
  ```
- #### *b.　創建資料庫*
  ```
  CREATE DATABASE airflow;
  ```
- #### *c.　創建使用者*
  ```
  CREATE USER airflow WITH PASSWORD 'airflow';
  ```
- #### *d.　給使用者權限*
  ```
  GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
  ```
- #### *e.　驗證*
  ```
  # 確認是否連上資料庫
  docker exec -it postgres_sql_container psql -U airflow -d airflow
  ```

<br>

### *3.　Startup Airflow*
- #### *a.　初始化*
  ```
  docker-compose up airflow-init
  ```
- #### *b.　背景啟動*
  ```
  docker-compose up -d
  ```
- #### *c.　移除服務*
  ```
  # 停止且移除 :「容器」、「沒定義的孤兒」、「資料庫內容」
  docker-compose down --volumes --remove-orphans
  
  # 清理所有「已停止」的容器
  docker container prune -f
  
  # 清理所有「未被掛載」的 Volume
  docker volume prune -f
  ```

<br>

### *~~4.　Startup PoWA~~*
- #### *a.　背景啟動*
  ```
  docker-compose up -d --build powa-postgres powa-web
  ```

- #### *b.　確認擁有角色權限 + Schema 是否建立*
  ```
  # 進入容器
  docker exec -it powa-postgres psql -U powa -d powa
  
  # 確認角色權限
  \du
  
  # 確認 schema
  \dn
  ```

- #### *c.　檢查 Extensions*
  ```
  # 確認 \dx # 應該要有 (5 rows) : [pg_stat_statements, btree_gist, hypopg, plpgsql, powa]
  \dx
  
  # 若無，手動執行
  docker exec -it powa-postgres psql -U powa -d powa -f /docker-entrypoint-initdb.d/01_powa.sql
  ```

- #### *d.　確保已經建立 Server*
  ```
  SELECT * FROM powa_servers;
  ```

- #### *e.　測試 Web 使用者能登入 sql*
  ```
  docker exec -it powa-postgres psql -U powa -d powa
  ```

- #### *f.　Web UI 登入資訊*
  ```
  username : powa
  password : powa
  server   : powa-db
  ```
  
<br>

### *5.　Startup Monitoring*
- #### *a.　背景啟動*
  ```
  docker-compose up -d
  ```
  
- #### *b.　Grafana 設定*
  ```
  # Login Grafana Web UI
    - acc: admin
    - pwd: admin
  
  # 新增 Prometheus datasource: http:127.0.0.1:9090
  
  # 快速導入 Dashboard ( Dashboards -> New -> Import )
    - Import via grafana.com :
      - PostgreSQL: 9628 ( TPS, Transactions, Locks, Cache hit, Connections, Database size )
      - Node Exporter: 1860 ( CPU, RAM, Disk IO, Disk usage, Network, Load average )
      - PostgreSQL Table: 12485 ( Table size, Table growth, Index size, Sequential scans, Index scans )
  
  # 觀測重點 ( ⭐htap_grafana.json )
  HTAP Monitoring
    System Layer ( Node Exporter )
    - CPU
    - RAM
    - Disk IO
    - Disk usage
  
    PostgreSQL Layer ( Postgres Exporter )
    - TPS
    - Connections
    - Locks
    - WAL rate
    - Cache hit ratio
    - Checkpoints
  
    Table Layer
    - Top 10 table size
    - Top 10 seq scan
    - Top 10 index scan
    - Table growth
  ```
- ![PNG](../assets/grafana_1.PNG)
- ![PNG](../assets/grafana_2.PNG)
- ![PNG](../assets/grafana_3.PNG)

- #### *c.　壓測觀察重點*
  ```
  TPS           穩定上升
  WAL rate      線性上升
  Cache hit     > 95%
  Locks         低
  Checkpoint    平穩
  ```

- #### *d.　監控位置*
  - #### *⭐ 1.　TPS: 每秒 Commit + Rollback 數*
  - ![PNG](../assets/grafana_01.PNG)
    ```
    -- Equivalent SQL ⬇️ 
    SELECT
    xact_commit,
    xact_rollback
    FROM pg_stat_database;
    ```
    ```
    壓測觀察重點： 
    預期 : 逐漸上升 -> 穩定
    非預期 : TPS 上升 → 突然下降
      - WAL Flush -> Disk IO Saturation
      - Lock Contention -> Transaction Locks
      - CPU Saturation -> Transaction waiting for CPU
      - Memory Saturation -> Transaction waiting for Memory
      - Network Saturation -> Transaction waiting for Network
      - Checkpoint -> Checkpoint Frequency too High
    ```
  - #### *⭐ 2.　WAL Rate*
    ```
    -- Equivalent SQL ⬇️ 
    None
    ```
    ```
    壓測觀察重點： 
    預期 : None
    非預期 : 突然暴增 ( WAL 持續線性成長 )
     - Numerous INSERTs
     - Numerous UPDATEs
     - Checkpoint ( WAL Rate Spike )
    ```
  - #### *3.　IO Saturation*
    ```
    -- Equivalent SQL ⬇️ 
    None
    ```
    ```
    壓測觀察重點： IO Wait
    預期 : None
    非預期 : IO Full -> TPS 突然下降
    ```
  - #### *⭐ 4.　Lock Contention*
  - ![PNG](../assets/grafana_04.PNG)
    ```
    -- Equivalent SQL ⬇️ 
    SELECT *
    FROM pg_locks;
    ```
    ```
    壓測觀察重點： 
    預期 : None
    非預期 :
        - Update Contention -> 多 Transaction 更新同 Row
        - Index Page Lock -> 多 Transaction 更新同 Index Page
        - DDL Lock -> Schema Change
        - OLAP Query -> AccessShareLock
    ```
  - #### *5.　Connections*
  - ![PNG](../assets/grafana_05.PNG)
    ```
    -- Equivalent SQL ⬇️ 
    SELECT count(*)
    FROM pg_stat_activity;
    ```
    ```
    壓測觀察重點： 
    預期 : Connections 穩定
    非預期 : Connections 持續上升
        - Connection Leak -> Client Connections Not Being Released
        - Connection Storm -> Sudden Surge in Connection Attempts
        - Pool Misconfiguration -> Connection Pooling Exploded
    ```
  - #### *⭐ 6.　Cache Hit Ratio*
  - ![PNG](../assets/grafana_06.PNG)
    ```
    -- Equivalent SQL ⬇️ 
    None
    ```
    ```
    壓測觀察重點： 
    預期 : > 0.95
    非預期 : < 0.90
      - shared_buffers 不夠 ??? 
      - dataset > RAM ???
    ```
  - #### *⭐ 7.　WAL Flush / Checkpoint*
  - ![PNG](../assets/grafana_07.PNG)
    ```
    -- Equivalent SQL ⬇️ 
    None
    ```
    ```
    壓測觀察重點： 
    預期 : None
    非預期 :
      - checkpoints_req -> WAL segment filled up -> max_wal_size too small
    ```
    
  - #### *8.　...*
    ```
    http://127.0.0.1:9187/metrics
    ```

<br>