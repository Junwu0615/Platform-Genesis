## *⭐ K8s - Deployment Delivery Baseline ⭐*

### *A.　Delivery Model Comparison*

<br>

<details>
<summary><b><i>　a.1.　Tradition </i></b></summary>
<ul>

<br>

<details>
<summary><b><i>　I.　Explain </i></b></summary>
<ul>

```
# 實現方式:
    • [1] GitLab CI
    • [2] GitLab CI + Jenkins
    
# 優劣特性: 
    • Pipeline-Driven
    • Imperative Workflow
    • 適用於小型團隊與 Legacy 環境
    • 可支援平台 ( VM / Docker / K8s )
    • 需自行維護 Deploy Script
    • Rollback 通常依賴 Pipeline
    • 相對唯一事實 → Deploy State 分散
        - 分散於 Git, CI Pipeline, Cluster
        - 難以確認哪個版本實際運行中
            Git Repository : v1.2
            CI Pipeline    : v1.3
            K8s Cluster    : v1.1
    • 權限管理較複雜 → 延伸安全性問題
        - CI Pipeline 需持有 K8s Deploy 權限
        - GitLab Runner 通常需存放 KubeConfig 或 Token
    • 其他:
        - GitLab Runner: 可依賴 K8s Pod 啟動一次性 || 簡易 docker 啟動

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
<summary><b><i>　II.　Showcase </i></b></summary>
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
<summary><b><i>　I.　Explain </i></b></summary>
<ul>

```
# 實現方式:
    • [1] GitLab CI + Argo CD

# 優劣特性:
    • State-Driven
    • Declarative Workflow
        - 需要嚴格定義結構樹 ( Env Ver / Helm Chart / App / ... )
    • 適合中大型團隊
    • 可支援平台 ( K8s )
    • Drift Detection
    • Deploy Audit Trail
    • 僅需定義 Build Pipeline
        - 僅需定義 Build Pipeline → Image Build 與 Deploy 解耦
        - Deploy 由 Argo CD 自動同步 → 不直接操作 K8s
    • Rollback 流程標準化 → Git Revert 即可恢復至指定版本
    • Single Source of Truth ( Git )
        - K8s 狀態可追溯
    • Centralized RBAC ( 權限集中於 Argo CD ) → 安全性較高
    • Disaster Recovery
    • 開發維運實質上不分家
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
    Argo CD Detect Drift
      ↓
    Sync
      ↓
    K8s Apply
      ↓
    Pod Service Running
    
    
# Disaster Recovery:

    Cluster 壞掉
      ↓
    重建 Cluster
      ↓
    安裝 Argo CD
      ↓
    Sync Git
      ↓
    恢復服務


# Rollback:

    Git Revert ( ≠ 真正恢復完成 )
      ↓
    Git Push
      ↓
    Argo CD Sync
      ↓
    Rolling Update
```

</ul>
</details>

<details open>
<summary><b><i>　II.　Showcase </i></b></summary>
<ul>

![PNG](../assets/argocd_00.png)
![PNG](../assets/argocd_01.png)
![PNG](../assets/argocd_02.png)

</ul>
</details>


</ul>
</details>

<br>

### *B.　Quantitative*
#### *b.1.　Experimental Conditions*
```
 [ 量測邊界說明 ]
 1. 本階段僅比較 Deployment Delivery Lifecycle，映像檔之編譯、打包與 CI 管道執行等待時間，兩案皆扣除不計入。
 2. Manual 情境： 未導入任何軟體層面管道輔助，採傳統模式以第三方遠端軟體逐台登入裝置、傳檔、手動調整 Config 並執行。
    → 過往真實經歷有遇到如此極端作業環境 ( 基礎設施幾乎無搭建 )
    ⭐ 藉由當時情境 → 導入新方案後帶來的整體交付提升為何 ?
 3. GitOps 情境： 採用 Argo CD 自動化聲明式部署。


 [ 測試環境 ]
 Node Count        : 6
 Application       : pg-python-inst
 Replica           : 1
 Image Size        : 296 MB
     ↓
 [ 測試工具 ]
 Git Repository    : GitLab
 Images Repository : Docker Registry
 GitOps Tool       : Argo CD
     ↓
 [ 測試次數 ]
 Manual Deploy     : 10 次
 GitOps Deploy     : 10 次
     ↓
 [ 取平均值 ]
```

<br>

#### *b.2.　Single Deployment Measurement*
```
 [ Scope ]
 This Measurement Only Compares the Deployment Delivery Lifecycle

 [ The following items are not included in the statistics ]
 • Source Code Compilation
 • Container Image Build
 • Container Image Push
 • CI Queue Waiting Time

 [ Measurement Startpoint ]
 • Deployment Change Ready

 [ Measurement Endpoint ]
 • Application Ready

 [ Additional Observation ]
 The following values were observed during testing
 but were excluded from deployment lifecycle measurements.

 • Manual Image Build ............. 85 sec
 • GitLab CI Pipeline Runtime .... 105 sec
```

| Item | Manual ( sec ) | GitOps ( sec ) |
|--:|--:|--:|
| Remote Access | 15 | 0 |
| File Transfer | 20 | 0 |
| Configuration Update | 60 | 0 |
| Deployment Execution | 20 | 0 |
| Health Verification | 30 | 30 |
| Functional Verification | 60 | 60 |
| Service Recovery | 20 | 15 |
| Total Delivery Time | 225 | 105 |

<br>

#### *b.3.　Deployment Scalability Estimation*
```
The following values are estimated projections derived
from ⭐ b.2. Single Deployment Measurement.

These values do not include:
 • Human error
 • Context switching
 • Operational fatigue
 • Concurrent deployment optimization
```

| Node | Manual ( min ) | GitOps ( min ) |
|--:|--:|--:|
| 1 | 3.75 | 1.75 |
| 3 | 11.25 | 1.75 |
| 6 | 22.50 | 1.75 |
| 12 | 45.00 | 1.75 |
| 72 | 270.00 | 1.75 |

<br>

#### *b.4.1.　Post-Adoption Risk Assessment*
| Risk Item | Manual | GitOps |
|--:|:--:|:--:|
| Configuration Consistency Risk | High | Reduced |
| Deployment Error Risk | High | Reduced |
| Version Traceability Risk | High | Reduced |
| Unauthorized Change Risk | Medium | Reduced |
| Key-Person Dependency Risk | High | Reduced |

<br>

#### *b.4.2.　Post-Adoption Operational Comparison*
| Item | Manual | GitOps |
|--:|:--:|:--:|
| Git Push | Y | Y |
| Docker Build on Local | Y | N |
| Manually Push Image<br>to Repository | Y | N |
| Remote Access | Y | N |
| Pull File | Y | N |
| Configuration Update | Y | N |
| Deployment Execution | Y | N |
| Health Verification | Y | Y |
| Functional Verification | Y | Y |
| Update Infrastructure<br>Version History | Y | N |
| Number of Operation Steps | 10 | 3 |
| Reduction ( % ) | 0 | 70 |

<br>

#### *⭐ b.4.3.　Industry Delivery Model Comparison*
| Item | SSH | CI/CD | GitOps |
|--:|:--:|:--:|:--:|
| Build | Manual | Automated | Automated |
| Deployment | Manual | GitLab CI | Argo CD |
| Rollback | Manual | Pipeline-Driven | Git-Based Reconciliation |
| Drift Detection | N | N | Y |
| Audit Trail | Partial | Partial | Complete |
| Desired-State Recovery | Manual | Manual | Automated |

<br>

#### *⭐ b.4.4.　Capability Comparison Matrix*
| Capability | SSH | CI/CD | GitOps |
|--:|:--:|:--:|:--:|
| Automated Deployment | N | Y | Y |
| Git Traceability | N | Partial | Y |
| Drift Detection | N | N | Y |
| Self Healing | N | N | Y |
| Disaster Recovery | Partial | Partial | Y |
| RBAC Centralization | N | Partial | Y |

<br>

### *⭐ Baseline Findings*
| Item | Manual → GitOps |
|--:|:--|
| Measured Deployment<br>Time Reduction | 53.3%<br>( 225 sec → 105 sec ) |
| Estimated Multi-Node Operational Scaling Benefit | Derived from single-deployment measurements<br>and linear operational effort assumptions |
| Post-Adoption<br>Operational Comparison | 70% ( Steps: 10 → 3 ) |
| Deployment<br>Access Centralization | 移除個人 KubeConfig / 直接 Cluster 存取權限<br>/ 部署操作統一經由 Argo CD RBAC 控管<br><br>• 補充 GitLab 尚有權限 ( Registry / Repo / Pipeline ) |
| Rollback<br>Process Simplification | Manual rollback procedures replaced<br>by Git-based version reversion workflow |
| Multi-node Deployment<br>Efficiency Improvement | Linear → Near-constant |

<br>

```
==================================================================================
                  Deployment Delivery Baseline Validation Report
==================================================================================

[ Measured Results ]
 • Deployment delivery time decreased from 225 sec to 105 sec
   under the defined validation scope.
 • Manual operational activities were reduced from 10 steps to 3 steps.
 • Deployment execution became independent of direct cluster access 
   and manual host operations.

[ Observed Benefits ]
 • Reduced operational overhead during application deployment.
 • Improved deployment traceability through Git-based workflows.
 • Centralized deployment permissions through Argo CD RBAC.
 • Consistent deployment process across multiple Kubernetes nodes.

[ Scope Limitation ]
 • Measurements were collected from a single homelab environment.
 • Multi-node scalability results are estimated projections,
   not directly measured observations.
 • Build time, image push time, and CI queue latency were excluded
   from deployment lifecycle measurements.
 • Disaster recovery capability was not validated in this report.

[ Conclusion ]
 • The evaluated GitOps workflow reduced manual deployment effort
   and improved deployment consistency within the defined validation scope.

 • Results indicate operational efficiency improvements compared
   with the manually executed deployment workflow, while providing
   additional governance capabilities that will be evaluated in
   the GitOps Deployment Governance validation report.
   
==================================================================================

```

<br><br><br>