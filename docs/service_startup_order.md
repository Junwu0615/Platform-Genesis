### *1.　Startup PostgreSQl*
- #### *a.　背景啟動*
  ```
  docker-compose up -d
  ```

<br>

### *2.　[ Please Skip ] Setting Account to Airflow in PostgreSQl*
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

### *4.　Startup PoWA*
- #### *a.　背景啟動*
  ```
  docker-compose up --build -d
  ```
- #### *b.　確認擁有角色權限*
  ```
  # 進入容器
  docker exec -it powa-repository psql -U postgres -d powa
  
  # 確認角色權限
  \du
  ```
- #### *c.　檢查 Extensions*
  ```
  \dx
  # 若只有 (1 rows) # 則需要繼續執行 d. 步驟
  ```
- #### *d.　安裝 Extensions*
  ```
  CREATE EXTENSION IF NOT EXISTS btree_gist;
  CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
  CREATE EXTENSION IF NOT EXISTS pg_qualstats;
  CREATE EXTENSION IF NOT EXISTS pg_stat_kcache;
  CREATE EXTENSION IF NOT EXISTS powa;
  
  # 再次確認 \dx, 總共會有 (6 rows)
  ```