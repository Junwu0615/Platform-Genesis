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
- #### *去除乾淨*
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
  acc: admin
  pwd: admin
  
  新增 Prometheus datasource: http:127.0.0.1:9090
  ```

<br>