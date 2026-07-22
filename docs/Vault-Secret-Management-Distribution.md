## *⭐ Vault Secret Management & Distribution ⭐*

<br>

### *A.　Task Description*
```
情境模擬 ( Scenario Description )
 • 模擬雲原生與零信任架構下的動態密鑰派發與生命週期管理：
   透過 HashiCorp Vault 的 Database Secrets Engine，實作用完即焚 ( Just-In-Time ) 與最小權限原則，
   確保應用程式或背景服務不需硬編碼 ( Hardcode ) 任何長期有效的資料庫密碼。

實施機制 ( Implementation Mechanism )
 • 技術堆疊: HashiCorp Vault + PostgreSQL + Python ( Script-based Validation )
 • 核心流程: 
   1. 定時索取 ( Dynamic Request ) : 測試腳本定期向 Vault 發送憑證申請，Vault 透過資料庫外掛 ( Plugin ) 
      自動在 PostgreSQL 中動態建立具備時效性 ( TTL ) 的短效期帳號。
   2. 自動回收 ( Revocation / Cleanup ) : 任務結束後主動斷線或等待 TTL 到期，Vault 自動執行回收與刪除。
   3. 異動監控 ( Audit & Verification ) : 同步透過監控腳本檢視 PostgreSQL 系統檢視表 ( pg_roles / pg_stat_activity )，
      即時驗證資料庫動態帳號的【 新增 】➔【 使用 】➔【 自動刪除 】生命週期完整性。

預期驗證目標 ( Expected Outcomes & Verification )
 • Dynamic Credentialing ( 動態憑證 ) : 驗證 Vault 能依據請求即時產生不同帳號密碼，而非共用同一組靜態密鑰。
 • Lifecycle Management ( 生命週期管理 ) : 確認短效期帳號在逾時或斷線後，確實被資料庫端清除，無孤兒帳號殘留。
 • Zero-Trust Compliance ( 零信任合規 ) : 實踐憑證最小化與短期有效特性，大幅降低憑證外洩風險。
```

<br>

### *B.　Architecture & Verification Flow*
> *Read from Top to Bottom ↓ | Arrows Indicate the Course of Events | MVP Validation Pipeline*

```mermaid
sequenceDiagram
    autonumber
    participant S1 as Script A ( Requester )
    participant V as HashiCorp Vault
    participant DB as PostgreSQL ( DB )
    participant S2 as Script B ( Monitor )

    Note over S1, DB: Phase 1 : 動態憑證配置與 Vault 整合
    S1->>V: 呼叫 API 索取暫時密鑰 ( v1/database/creds/... )
    V->>DB: 動態執行 CREATE USER ( 建立短效期帳號 )
    DB-->>V: 回應建立成功
    V-->>S1: 回傳隨機 v-token 帳號與密碼 ( 帶有 TTL )
    S1->>DB: 使用動態憑證登入並進行簡單查詢
    S1->>DB: 主動斷開連線 ( Disconnect )

    Note over S1, DB: Phase 2 : 即時角色稽核與監控
    S2->>DB: 輪詢檢視 ( SELECT pg_roles WHERE v-token-% )
    DB-->>S2: 捕捉新增記錄：顯示 v-token-xxx 存在
    Note over V, DB: TTL 逾時或租約到期
    V->>DB: 自動執行 DROP USER 清理帳號
    DB-->>S2: 捕捉刪除記錄：v-token-xxx 自 pg_roles 徹底消失
```

<br><br>

#### *★　Phase 1 : Dynamic Credential Provisioning & Vault Integration*
> *本階段驗證 Vault Database Secrets Engine 的基礎連線設定，並透過測試腳本發起第一次的動態帳號索取。*

<details>
<summary><b><i>　Detail </i></b></summary>
<ul>

```
 • [容器內設定] 啟用 Database Secret Engine
   vault secrets enable database
   
 • [容器內設定] 設定 PostgreSQL 連線介面 (Connection Configuration)
   vault write database/config/postgresql-prod \
       plugin_name=postgresql-database-plugin \
       allowed_roles="dynamic-app-role" \
       connection_url="postgresql://{{username}}:{{password}}@postgresql-homelab-test.databases-homelab-test.svc.cluster.local:5432/pgdatabase?sslmode=disable" \
       username="pguser" \
       password="pgsecretpassword"
   # ✅ 預期反饋 : Success! Data written to: database/config/postgresql-prod
       
 • [容器內設定] 建立動態角色對應 (Create Role with TTL)
   vault write database/roles/dynamic-app-role \
       db_name=postgresql-prod \
       creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL 'infinity'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
       default_ttl="2m" \
       max_ttl="5m"
   # ✅ 預期反饋 : Success! Data written to: database/roles/dynamic-app-role

 • 啟動 K3s 叢集內部 Vault 管道
   make open-pipeline

 • 執行腳本向 Vault 索取暫時密鑰並進行短暫連線
   python3 request_secret.py
   
 • 運作行為
   - 腳本呼叫 Vault API 取得 v1/database/creds/dynamic-app-role
   - 取得一組隨機產生的 username (如 v-token-dynamic-app-role-xxx) 與 password
   - 立即使用該組帳密登入 PostgreSQL 進行簡單查詢，隨即主動斷開連線
```

</ul>
</details>

#### *★　Phase 2 : Real-time Role Auditing & Monitoring*
> *本階段利用第二支監控腳本，即時捕捉資料庫中帳號的建立與消滅，驗證最小 MVP 下動態憑證的生命週期。*

<details>
<summary><b><i>　Detail </i></b></summary>
<ul>

```
 • 啟動資料庫角色監控腳本
   python3 monitor_roles.py
   
 • 監控核心 SQL 邏輯
   SELECT rolname, rolvaliduntil FROM pg_roles WHERE rolname LIKE 'v-token-%';
   
 • 觀察結果
   - 當 Script A 發起請求時，監控端立即捕捉到畫面上新增一筆 v-token-xxx 記錄
   - 當 Script A 斷線且 TTL 到期後，監控端即時捕捉到該筆記錄自 pg_roles 中被徹底刪除
   - 確保無任何長期殘留帳號，達成零信任動態防護目標
```

</ul>
</details>

<br><br>

### *C.　MVP Verification Summary*

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/Dynamic-Secret-Injection.gif)

</ul>
</details>

| **Validation Step** | **Action Performed** | **Expected Result** | **Status** |
|:--|:--|:--|:--|
| *1.　Request* | *Script A 請求 Vault 產生憑證* | *成功回傳短效期動態帳密* | *✅ PASS* |
| *2.　Connect* | *使用動態帳密存取 PostgreSQL* | *順利建立連線並完成資料操作* | *✅ PASS* |
| *3.　Audit* | *Script B 輪詢 pg_roles 檢視* | *確實捕捉到動態帳號的即時新增* | *✅ PASS* |
| *4.　Revoke* | *斷線與 TTL 屆滿自動回收* | *資料庫確實執行 Drop User，無殘留* | *✅ PASS* |

<br><br><br>