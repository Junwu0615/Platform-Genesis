## *K8s - CI/CD*

### *A.　方案比較*

<br>

<details>
<summary><b><i>　a.1.　Tradition </i></b></summary>
<ul>

<br>

<details>
<summary><b><i>　I.　說明細節 </i></b></summary>
<ul>

```
# 實現方式:
    * [1] Gitlab CI
    * [2] Gitlab CI + Jenkins
    
# 優劣特性: 
    * Pipeline-Driven
    * Imperative Workflow
    * 適用於小型團隊與 Legacy 環境
    * 可支援平台 ( VM / Docker / K8s )
    * 需自行維護 Deploy Script
    * Rollback 通常依賴 Pipeline
    * 相對唯一事實 → Deploy State 分散
        - 分散於 Git, CI Pipeline, Cluster
        - 難以確認哪個版本實際運行中
            Git Repository : v1.2
            CI Pipeline    : v1.3
            K8s Cluster    : v1.1
    * 權限管理較複雜 → 延伸安全性問題
        - CI Pipeline 需持有 K8s Deploy 權限
        - GitLab Runner 通常需存放 KubeConfig 或 Token
    * 其他:
        - Gitlab Runner: 可依賴 K8s Pod 啟動一次性 || 簡易 docker 啟動

# Work Flow:

    Git Push
      ↓
    GitLab CI
      ↓
    Build Image
      ↓
    Push Registry
      ↓
    Update values.yaml
      ↓
    K8s Apply
      ↓
    Pod Service Running
```

</ul>
</details>

<details open>
<summary><b><i>　II.　展示內容 </i></b></summary>
<ul>

![PNG](../assets/ci-cd_00.png)
![PNG](../assets/ci-cd_01.png)

</ul>
</details>

</ul>
</details>


<details>
<summary><b><i>　a.2.　GitOps </i></b></summary>
<ul>

<br>

<details>
<summary><b><i>　I.　說明細節 </i></b></summary>
<ul>

```
# 實現方式:
    * [1] Gitlab CI + ArgoCD

# 優劣特性:
    * State-Driven
    * Declarative Workflow
        - 需要嚴格定義結構樹 ( Env Ver / Helm Chart / App / ... )
    * 適合中大型團隊
    * 可支援平台 ( K8s )
    * Drift Detection
    * Deploy Audit Trail
    * 僅需定義 Build Pipeline
        - 僅需定義 Build Pipeline → Image Build 與 Deploy 解耦
        - Deploy 由 ArgoCD 自動同步 → 不直接操作 K8s
    * Rollback 流程標準化 → Git Revert 即可恢復至指定版本
    * Single Source of Truth ( Git )
        - K8s 狀態可追溯
    * Centralized RBAC ( 權限集中於 ArgoCD ) → 安全性較高
    * Disaster Recovery
    * 開發維運實質上不分家
        - 降低人工介入需求
        - 提高開發團隊自主交付能力

# Work Flow:

    Git Push
      ↓
    GitLab CI
      ↓
    Build Image
      ↓
    Push Registry
      ↓
    Update values.yaml
      ↓
    ArgoCD Detect Drift
      ↓
    Sync
      ↓
    K8s Apply
      ↓
    Pod Service Running
    
    
* Disaster Recovery:

    Cluster 壞掉
      ↓
    重建 Cluster
      ↓
    安裝 ArgoCD
      ↓
    Sync Git
      ↓
    恢復服務
```

</ul>
</details>

<details open>
<summary><b><i>　II.　展示內容 </i></b></summary>
<ul>

![PNG](../assets/argocd_00.png)
![PNG](../assets/argocd_01.png)

</ul>
</details>


</ul>
</details>

<br>

### *B.　量化測試*
- #### *b.1.　實驗條件*
    ```
    測試環境
    Node Count     : 6
    Application    : SpringBoot Demo
    Replica        : 3
    Image Size     : 800 MB
    Registry       : Docker Registry
    Git Repository : Gitlab
    GitOps Tool    : ArgoCD
      ↓
    測試次數
    Manual Deploy : 10 次
    GitOps Deploy : 10 次
      ↓
    取平均值
    ```

- #### *b.2.　單次部署量測*
    | Item | Manual ( s ) | GitOps ( s ) |
    |--:|:--:|:--:|
    | 登入裝置 | - | 0 |
    | 傳輸檔案 | - | 0 |
    | 修改設定 | - | 0 |
    | 執行部署 | - | 0 |
    | 管道執行等待 | - | - |
    | 驗證健康狀態 | - | - |
    | 人工測試環節 | - | - |
    | 總耗時 | - | - |
    | 服務恢復時間 | - | - |

- #### *b.3.　多節點擴展測試*
    | Node | Manual ( min ) | GitOps ( min ) |
    |--:|:--:|:--:|
    | 1 | - | - |
    | 3 | - | - |
    | 6 | - | - |
    | 12 | - | - |

- #### *b.4.1.　人為量測 : 可能性風險*
    | Risk Item | Manual | GitOps |
    |--:|:--:|:--:|
    | 忘記更新 Config | 高 | 低 |
    | 操作錯誤 | 高 | 極低 |
    | 部署版本錯誤 | 中 | 低 |
    | 無法追溯 | 高 | 低 |
    | 未經授權修改 | 中 | 低 |
    | 關鍵人員依賴 | 高 | 低 |
    | 非工作時段介入需求 | 中 | 低 |

- #### *b.4.2.　人為量測 : 操作步驟下降*
    | Item | Manual | GitOps |
    |--:|:--:|:--:|
    | Git Push | Y | Y |
    | SSH Login | Y | N |
    | Pull File | Y | N |
    | Modify Config | Y | N |
    | Upload File | Y | N |
    | Kubectl Apply | Y | N |
    | Health Check | Y | Y |
    | Stability Observe | Y | Y |
    | Record Result | Y | N |
    | 操作步驟數 | 9 | 3 |
    | 降低比例(%) | 0 | 66.7 |

- #### *b.5.　Drift Recovery*
    ```
    if git define → replicas: 3
  
    kubectl scale deploy app --replicas=10
    ```
    | Item | Manual | GitOps |
    |--:|:--:|:--:|
    | 偵測 Drift | 人為 | 自動 |
    | 修復 Drift | 人為 | 自動 |
    | 恢復時間 | 不固定 | < 1 min |


- #### *b.6.　最終統計*
    | Item | Manual → GitOps |
    |--:|:--:|
    | 平均部署時間下降 | - % |
    | 人為操作步驟下降 | - % |
    | Deploy 權限管理集中 | - % |
    | Drift 自動修復 | Y |
    | Rollback 時間下降 | - % |
    | 多節點部署效率提升 | 線性 → 固定成本 |
    
    ```
    CI/CD 主目的是為了解決 ...
     * 部署頻率 ( Deployment Frequency ) ↑
     * 交貨時間 ( Lead Time ) ↓
     * 恢復時間 ( Recovery Time ) ↓


    在 - Node K3s 環境中 ...
     * Manual Deploy 平均耗時 - 分鐘
     * GitOps Deploy 平均耗時 - 分鐘
    
       → 部署效率提升 - %
  
  
      * 人工操作步驟由 9 步降至 3 步
       → 降低步驟比例 66.7 %
       → 顯著降低維運風險與人為操作成本
    
  
    此外 GitOps 提供 ...
     * Single Source of Truth
     * Drift Detection
     * Deploy Audit Trail
     * Centralized RBAC
     * Disaster Recovery
    
       → 使部署流程具備可追溯性
       → 可重複性與自動修復能力
       → 有效降低維運成本並提升交付效率
    ```


<br><br><br>