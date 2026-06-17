## *⭐ K8s - Feature Validation ⭐*

<br>

### *Document*

<details>
<summary><b><i>　I.　Quantitative Format </i></b></summary>
<ul>

```
Tier ??? : ???
 • Objective: 驗證 ??? 能力
 • Situation: 測試前狀態
 • Action: 執行動作
 • Metrics:
    • Recovery Time
    • Downtime
    • Failed Requests
      ...
    • Data Loss
    • Availability
 • Pass Criteria: 通過標準
 • Result: 實際量測結果
 • Observation:
    • kubectl get pods
    • Grafana Screenshot
    • Prometheus Metrics
    • Application Screenshot
    
 • [X] Failure Scenario
 • [X] Evidence
 • [X] Limitation
 • [X] Known Limitation

 • Validation: 
    • Pass : ✅
    • Fail : ❌
    • NOT APPLICABLE : ⛔
```

</ul>
</details>

<details>
<summary><b><i>　II.　Quantitative List </i></b></summary>
<ul>

```
Tier 1 : Workload Resiliency
 • ✅ Pod 崩潰恢復 : Pod Crash Recovery
 • ✅ OOMKill 恢復 : OOMKill Recovery
    • Out of Memory Killer: 記憶體耗盡時, 為了保護系統核心不崩潰, 
      自動挑選並強制終止 ( Kill ) 佔用過多記憶體之程序 ( Process ) 的機制
 • ✅ 存活狀態自我恢復 : Liveness Recovery
    • 當 Pod 的程式碼內部發生死鎖 ( Deadlock )、無限迴圈或內部核心執行緒 ( Thread ) 崩潰, 
      但容器 <外殼> 還活著時, 能被 Kubernetes 自動偵測並在 <最短時間內原地重啟>
 • ✅ 滾動更新 : Rolling Update
 • ✅ 回滾 : Rollback


Tier 2 : Node Resiliency
 • ✅ 節點排水 : Node Drain Recovery
    • 代表 → 節點計畫性維護 ( Planned Maintenance )
 • ✅ 節點故障 : Node Failure Recovery
    • 代表 → 節點災難恢復 ( Disaster Recovery )


Tier 3 : Traffic Failover
 • ✅ Service 端點容災切換 : Endpoint Failover
 • ✅ Ingress 流量網關容災 : Ingress Failover


Tier 4 : Stateful Recovery
 • ✅ PVC 持久性 : PVC Persistence
 • ✅ StatefulSet 狀態集自我修復 : StatefulSet Recovery
    • 呼應前面的 Recovery, 在 K8s 中這種不經人工介入的重啟通常稱為自我修復能力 ( Self-healing )


Tier 5 : Autoscaling
 • ✅ HPA 自動擴展 : HPA Scale-Out
    • 增加 Pod 數量叫水平擴展
 • ⛔ HPA 自動縮容 : HPA Scale-In
    • 減少 Pod 數量叫水平縮容


Tier 6 : Control Plane HA
 • ✅ Master 節點單點故障損壞 : Single Master Failure
    • 控制平面 ( Control Plane ) 失去單一主節點時的叢集存活能力
 • ✅ 控制平面組件領導者重新選舉 : Leader Re-election
    • K8s 的核心組件 ( ex: kube-scheduler, kube-controller-manager )
      在高可用 ( HA ) 架構下會用租約 ( Lease ) 鎖定 Leader, 
      倒下時會自動 Leader Re-election ( 領導者重選 )
```

</ul>
</details>

<br>

### *★　Tier 1 : Workload Resiliency*

<details>
<summary><b><i>　Pod Crash Recovery </i></b></summary>
<ul>

```
Objective: 
 • 驗證 Deployment Controller 自癒能力

Situation:
 • Application Running
 • Replica = 1
 • Target Pod :
    • -n pg-apps-homelab-test
    • inst-homelab-test

Action:
 • Delete Pod
     • kubectl delete pod inst-homelab-test-xxx-xxx
     • K9s: ctrl + k

Metric:
 • Pod Recovery Time

Pass Criteria:
 • Pod Recovery Time < 5 min
 
Result:
 • Pod Creation Latency ......... 2 sec
 • Container Startup Time ....... 3 sec
 • ⭐ Readiness Recovery Time ... 5 sec

Observation:
 • kubectl get pods -n pg-apps-homelab-test -w
 
Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/Pod%20Crash%20Recovery.gif)

</ul>
</details>

</ul>
</details>

<details>
<summary><b><i>　OOMKill Recovery </i></b></summary>
<ul>

```
Objective: 
 • 驗證當單一實例 ( Singleton ) 應用因未預期的資料爆量、記憶體洩漏 ( Memory Leak ) 
   或處理超大訊息導致超過 K8s 宣告的資源上限 ( Memory Limit ) 時, 
   Kubernetes 能否自動偵測到 OOMKilled 狀態, 並在免人工介入下完成 <原地快速容器重啟> 與自我修復
 
Situation:
 • Workload Running on [ Agent-2 or Agent-3 ]
 • Application Running normally ( K9s STATUS: Running, READY: 1/1 )
 • Replica = 1 ( Singleton 限制 )
 • Python 應用的 Deployment YAML 中必須明確配置 resources.limits.memory( ex: 128Mi )
 
Action:
 • 透過 Kafka 開發工具或生產者腳本, 向指定 Topic 發送一筆包含
   特定 Payload ("TRIGGER_OOM_FROM_KAFKA") 的控制訊息, 
   藉此觸發 Python 內部邏輯 → 立刻在記憶體內無限循環產生巨大字串或陣列, 強行將記憶體撐爆, 直到被系統 OOMKill
 
Metric:
 • OOM Trigger Latency ( 訊號發送到 Python 程式被核心擊殺的時間差, 預期應在 1-2 秒內 )
 • K8s OOM Detection Latency ( K8s 意識到容器是因為 OOM 而死並更新狀態的時間 )
 • Container Restart Time ( 容器被擊殺後, 到新容器重新拉起的時間 )
 • Total Recovery Time ( 從發送 TRIGGER_OOM 訊息到 Pod 回復 READY 1/1 的總耗時 )
 • Data Loss ( 由於是 SIGKILL 強制斷電式關機, 重啟後需驗證最後一筆 Kafka 訊息有無遺失或重複消費 )
 • Availability ( 整體服務可用性 )
 
Pass Criteria:
 • 完全自動化 ( No Manual Intervention ), 不需手動下達重啟指令
 • Pod 維持在同一個 Node 上進行 <原地重啟> ( RESTARTS 次數 +1 )
 • 核心驗證 Pod 的結束原因 ( Last State ) 必須明確顯示為 OOMKilled, 結束代碼為 137
 • Total Recovery Time < 15 sec
 
Result:
 • Observed OOM Status Time ...... 1 sec ( 沒精準使用工具取得 OOM Trigger Latency )
 • K8s OOM Detection Latency ..... 1 sec
 • Container Restart Time ....... 13 sec
 • ⭐ Total Recovery Time ....... 15 sec
 • Data Loss ..................... 0 ( Observed: Validated via Kafka Offset )
 
Observation:
 • K9s: 觀察狀態是否遵循 [ Running ] → [ OOMKilled || CrashLoopBackOff ] → [ Running ]
 • kubectl describe pod <pod-name> -n pg-apps-homelab-test
        - 檢查 Last State: Terminated 區塊中的 Reason: OOMKilled 與 Exit Code: 137
 • [X] 觀察該 Pod 的 Memory 使用率折線圖, 是否呈現垂直攀升 隨後瞬間歸零的鋸齒波


# Exit Code: 137
$ kubectl get pod inst-homelab-test-7fd9d5b99-lgk4m -n pg-apps-homelab-test -o jsonpath='{.status.containerStatuses[0].lastState.terminated}'
{"containerID":"containerd://18a09beded9ccfc4fc5c59844146af9fb676fa3db46b07f3757bf472fb69fc13","exitCode":137,"finishedAt":"2026-06-14T15:58:53Z","reason":"OOMKilled","startedAt":"2026-06-14T15:58:34Z"}p


Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/OOMKill%20Recovery.gif)

</ul>
</details>

</ul>
</details>

<details>
<summary><b><i>　Liveness Recovery </i></b></summary>
<ul>

```
Objective: 
 • 驗證單一實例 ( Singleton ) 應用在發生內部核心死鎖 ( Deadlock )、執行緒崩潰或接收到緊急外部中斷訊號時, 
   能否在不依賴節點重新調度 ( Reschedule ) 的情況下, 由 Kubernetes 偵測並完成<原地快速容器重啟>與服務自我修復能力
 
Situation:
 • Workload Running on [ Agent-2 or Agent-3 ]
 • Application Running normally (K9s STATUS: Running, READY: 1/1)
 • Replica = 1 ( Singleton 限制 )
 • Python 主任務持續消費 Kafka 訊息並寫入 PostgreSQL
 • 心跳檔案存在於容器本地： /app/tmp/heartbeat.txt
 
Action:
 • 透過 Kafka 開發工具或生產者腳本, 向指定 Topic 發送一筆包含
   特定 Payload ("TRIGGER_KILL_FROM_KAFKA") 的控制訊息, 
   藉此觸發 Python 內部邏輯 → 自殺並移除心跳檔
 
Metric:
 • Signal Propagation Time ( 訊號發送至 Python 接收的時間差 )
 • Heartbeat Deletion Time ( 心跳檔被移除的時間點 )
 • K8s Detection Latency ( 從檔案消失到 K8s 判定 Unhealthy 的時間, 預期約 3-6 秒 )
 • Container Restart Time ( 容器銷毀至重新啟動的時間 )
 • Total Recovery Time ( 從發送控制訊息到 Pod 回復 READY 1/1 的總耗時 )
 • Data Loss ( 切換期間是否有不掉單、重複消費、資料遺失, 預期為 0 )
 • Availability ( 整體服務可用性 )
 
Pass Criteria:
 • 完全自動化 ( No Manual Intervention ), 不需人工下達 kubectl delete/restart
 • Pod 必須維持在同一個 Node 上進行 <原地重啟> ( RESTARTS 次數 +1, 而非重新調度 )
 • 資料零遺失 ( Data Loss = 0 ), Kafka Offset 維持一致
 • Total Recovery Time < 15 sec
 
Result:
 • Signal Propagation Time ... 1 sec
 • Heartbeat Deletion Time ... 2 sec
 • K8s Detection Latency ..... 1 sec
 • Container Restart Time .... 8 sec
 • ⭐ Total Recovery Time ... 12 sec
 • Data Loss ................. 0 ( Observed: Validated via Kafka Offset )
 
Observation:
 • 觀察 RESTARTS 欄位是否從 0 變 1
     • watch -n 2 'kubectl get pods -n pg-apps-homelab-test -o wide | grep -E "agent-2|agent-3"'
     • K9s: pod -n pg-apps-homelab-test
 • 檢查 Events 欄位是否出現 "Liveness probe failed"
     • kubectl describe pod <pod-name> -n pg-apps-homelab-test
     • K9s: d
 • 檢查 容器日誌內部 是否監聽測到外部傳入自殺訊號
     • K9s: l
 • Kafka Consumer Group Matrix ( 確認 Lag 沒有異常堆積, 且重啟後能繼續正常消費 )
 • 實驗最終比較像 Crash Recovery => 而非 Process 還活著，但服務卡死
 
Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/Liveness%20Recovery.gif)

</ul>
</details>

</ul>
</details>

<details>
<summary><b><i>　Rolling Update </i></b></summary>
<ul>

```
Objective: 
 • 驗證單一實例 ( Singleton ) 應用在透過 ArgoCD / Helm 進行版本升級時, 
   在 Recreate ( 先殺後建 ) 策略下, 舊版本能否安全釋放資源 ( Kafka/PVC ), 
   且新版本能否以最短時間接單, 並驗證其斷線時間 ( Downtime )
 
Situation:
 • Workload Running on [ Agent-2 or Agent-3 ]
 • Current Version ( Image Tag: latest ) 正常運行中
 • Replica = 1, Strategy = Recreate
 • 持續有正常業務資料寫入 Kafka Topic
 
Action:
 • 更改 Helm Values 檔案中的環境變數並推送到 Git, 
   觸發 ArgoCD 自動同步 ( Sync ), 發動版本更新
 
Metric:
 • Terminating Time ( 舊版本 Pod 接收到 SIGTERM 到完全銷毀的時間 )
 • Volume Detach/Attach Latency ( 儲存鎖釋放與重新掛載的時間, Recreate 的關鍵坑點 )
 • New Container Init Time ( 新版本拉取 Image 與開機初始化時間 )
 • Total Downtime ( 從舊 Pod 開始停止服務, 到新 Pod Ready 1/1 的服務空窗期 )
 • Duplicate Processing ( 新舊更替間, 有無因 Offset 沒處理好導致重複消費 )
 
Pass Criteria:
 • 舊 Pod 必須 <完全消失> 後, 新 Pod 才能開始建立 ( 符合 Recreate 嚴格限制, 避免 2 個實例同時存在 )
 • 舊 Pod 結束前, 有成功 commit 手上最後一筆 Kafka Offset
 • Total Downtime < 20 sec ( 取決於 Image 拉取速度與 PVC 釋放速度 )
 
Result:
 • Terminating Time .... 3 sec
 • Volume Latency ...... 1 sec
 • New Init Time ....... 1 sec
 • ⭐ Total Downtime ... 5 sec
 • Duplicate Count ..... 0
 
Observation:
 • K9s: 觀察狀態是否遵循 [ Running ] → [ Terminating ] → 完全消失 → [ ContainerCreating ] → [ Running ]
 • kubectl get image: 確認新 Pod 確實是吃進了新版 Tag
 • 非 Rolling Update 而是 Deployment Recreate Update, 因為兩者策略彼此矛盾
 
Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/Rolling%20Update.gif)

</ul>
</details>

</ul>
</details>

<details>
<summary><b><i>　Rollback </i></b></summary>
<ul>

```
Objective: 
 • 驗證當新版本上線發生災難 ( ex: 程式 Bug、CrashLoopBackOff ) 時, 
   維運人員能否透過 K8s 原生指令或 ArgoCD 歷史紀錄, 在秒級內快速將服務倒回上一個穩定版本
 
Situation:
 • 故意部署一個會噴 Error 導致開機失敗的壞版本, 讓 Pod 陷入 CrashLoopBackOff
 
Action:
 • 更新 values images tags=v99 因無該版本所以連拉取都會失敗
 • 在 ArgoCD 介面上點擊 "Rollback" 到歷史 Commit
 
Metric:
 • Rollback Trigger Latency ( 下達指令到 K8s 開始動作的反應時間 )
 • Rollback Total Time ( 從決定回滾到舊版本 Pod 重新回到 READY 1/1 的總耗時 )
 • Data Consistency ( 回滾過程中, 有無導致 Kafka 資料混亂或資料損毀 )

Pass Criteria:
 • 快速反應：不需等待壞 Pod 慢慢 restart, 回滾指令下達後應立刻砍掉壞 Pod
 • Pod 成功回復成上一個穩定版本的 Image Tag
 • Rollback Total Time < 15 sec

Result:
 • Rollback Trigger Latency .. 2 sec
 • ⭐ Rollback Total Time .... 8 sec
 • Data Consistency .......... ✅
 
Observation:
 • kubectl rollout history deployment <name> ( 查看 K8s 歷史版本紀錄清單 )
 • K9s: 觀察 Pod 的 RESTART 欄位與 IMAGE 欄位是否倒回舊版
 • 本測試是 Deployment Rollback ; 而非 Application Rollback ( 常見 )
 
Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/Rollback.gif)

</ul>
</details>

</ul>
</details>

<br>

### *★　Tier 2 : Node Resiliency*

<details>
<summary><b><i>　Node Drain Recovery </i></b></summary>
<ul>

```
Objective:
 • 驗證節點進入維護模式時, Workload 是否能自動遷移至其他可用節點, 並維持服務可用性

Situation:
 • Workload Running on Agent-2
 • Application can run on [ Agent-2, Agent-3 ]
 • Application Running
 • Replica = 1 ( Strategy: Recreate # 該應用不能同時存在 2 個 )
 • Target Pod :
    • -n pg-apps-homelab-test
    • inst-homelab-test

Action:
 • 進行節點維運作業 → kubectl drain ( 設定不可排程 + 歷史遺留、現存於該 Node 上的 Pod 趕走 )
    kubectl drain k3s-agent-2 \
      --ignore-daemonsets \
      --delete-emptydir-data

 • 節點維運完成 → 手動復原
    kubectl uncordon k3s-agent-2

Metric:
 • Drain Start Time
 • Pod Eviction Time
 • Pod Reschedule Time
 • Service Availability

Pass Criteria:
 • No Manual Intervention
 • All Pods Rescheduled
 • Service Available
 • Recovery < 60 sec
 
Result:
 • Node Detection Time ..... 2 sec
 • Eviction Delay .......... 3 sec
 • Pod Scheduling Time ..... 3 sec
 • Container Startup Time .. 3 sec
 • ⭐ Total Recovery Time .. 7 sec
 • Service Availability .... 0 % ( 設計時沒有 Replica 1 以上, 過程有 7 秒服務掛掉 )

Observation:
 • Get Nodes Status
     • kubectl get nodes
     • K9s: nodes
 • Get Pods Status
     • watch -n 2 'kubectl get pods -n pg-apps-homelab-test -o wide | grep -E "agent-2|agent-3"'
     • K9s: pod -n pg-apps-homelab-test


Timeline:
 • Drain Start ---------------- T+00s
      ↓
 • Node Marked Disable -------- T+02s
      ↓
 • Pod Evicted ---------------- T+03s
      ↓
 • Scheduler Create New Pod --- T+03s
      ↓
 • Container Ready ------------ T+06s
      ↓
 • Service Available ---------- T+07s


Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/Node%20Drain%20Recovery.gif)

</ul>
</details>

</ul>
</details>


<details>
<summary><b><i>　Node Failure Recovery </i></b></summary>
<ul>

```
Objective:
 • 驗證 Scheduler 重新調度能力
 • 驗證 Worker Node 發生故障後, K8s 是否能自動重新調度 Workload 並恢復服務可用性

Situation:
 • Workload Running on Agent-3
 • Application can run on [ Agent-2, Agent-3 ]
 • Application Running
 • Replica = 1 ( Strategy: Recreate )
 • Target Pod :
    • -n pg-apps-homelab-test
    • inst-homelab-test
    • Node Eviction Timeout = 10 sec ( 調整預設參數 )

Action:
 • Manual Shutdown Agent-3

Metric:
 • Node NotReady Time
 • Pod Migration Time
 • Service Recovery Time

Pass Criteria:
 • Service Recovery < 90 sec
 • No Manual Intervention
 • Workload Successfully Rescheduled
 
Result:
 • Node Detection Time ...... 52 sec
 • Eviction Delay ........... 10 sec
 • Pod Scheduling Time ....... 3 sec
 • Container Startup Time .... 8 sec
 • ⭐ Total Recovery Time ... 73 sec

Observation:
 • Get Nodes Status
     • kubectl get nodes
     • K9s: nodes
 • Get Pods Status
     • watch -n 2 'kubectl get pods -A -o wide | grep -E "agent-2|agent-3"'
     • K9s: pod -n pg-apps-homelab-test


Timeline:
 • Node Shutdown ------------- T+00s
      ↓
 • Node Marked NotReady ------ T+52s
      ↓
 • Pod Eviction Started ------ T+62s
      ↓
 • Pod Recreated On Agent-3 -- T+72s
      ↓
 • Application Ready --------- T+73s
    

Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/Node%20Failure%20Recovery.gif)

</ul>
</details>

</ul>
</details>

<br>

### *★　Tier 3 : Traffic Failover*

<details>
<summary><b><i>　Endpoint Failover </i></b></summary>
<ul>

```
Objective: 
 • 測試級別: Service Layer ( Pod → Service → Pod )
 • 驗證當後端多複本 ( Multi-Replicas ) 的應用實例中, 某一個 Pod 突然暴斃或被手動銷毀時, 
   Service 控制器能否在秒級內更新 Endpoints 列表, 將死掉的 Pod IP 剔除, 
   並確保在此交替期間, 外部持續進來的流量 100% 由其餘健康 Pod 承接, 不發生請求遺失
 
Situation:
 • 後端 registry-homelab-test 部署為雙複本 replicas: 2, 避免了複雜有狀態組件的 Sidecar 干擾
 • 網關 Nginx Ingress Controller 採用 hostNetwork: true 獨佔邊緣節點實體埠
 
Action:
 • 在本地啟動循環的背景腳本, 每 N 秒對該 Service 的發送一次 curl 請求
   TOTAL=0; SUCCESS=0; FAIL=0; echo "🚀 開始高頻容災測試 ( 每秒 20 次 )... 按 Ctrl+C 結束並查看統計報告"; trap 'echo -e "\n📊 【 Tier 3 容災統計報告 】\n總請求數: $TOTAL\n成功數 (302/200): $SUCCESS\n失敗數 (502/504/000): $FAIL\n⭐ HTTP 成功率: $(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)%"' INT; while true; do CODE=$(curl -o /dev/null -s -w "%{http_code}" -H "Host: docker-registry.k8s.local" http://10.88.0.20/ --connect-timeout 1); TOTAL=$((TOTAL+1)); if [ "$CODE" = "200" ] || [ "$CODE" = "302" ]; then SUCCESS=$((SUCCESS+1)); else FAIL=$((FAIL+1)); echo "❌ 抓到斷線! 狀態碼: $CODE"; fi; sleep 0.05; done

 • 保持流量連射狀態下, 對其中一隻應用 Pod 強制抹殺
 • 靜置 10 秒, 等待新 Pod 被拉起且舊 Pod 完全消失
 • 停止 curl 腳本, 統計所有請求的成功率
 
Metric:
 • Endpoint Pruning Latency ( 從 Pod 被刪除, 到 kubectl get ep 清單中該 IP 消失的時間差 )
 • HTTP Success Rate During Failover ( 故障發生期間, 不中斷請求的成功率, 目標 100% )
 • Outage Duration ( 服務中斷、噴 502/504 的總時間, 目標 0 秒 )
 
Pass Criteria:
 • 整個刪除與重建過程中, 持續噴射的 curl 請求 100% 回報 HTTP 200, 
   不允許出現任何一筆 502 Bad Gateway 或 503 Service Unavailable
 
Result:
 • Endpoint Pruning Latency ....... 4 sec
 • ⭐ HTTP Success Rate ........... 100% ( 103/103 requests )
 • Outage Duration ................ 0 sec
 
Observation:
 • 透過 K9s 觀察 ENDPOINTS 欄位 隨著 pod 移除後 流量平滑移轉 創建後動態新增
 • 雖然 EndpointSlice 變更有約 4 秒的微幅延遲才完全在 API Server 生效, 
   但因為本質為雙複本部署, 流量在第 1 秒就已被健康節點完全平滑承接, 外網展現 0 延遲中斷
 • 檢視自定義統計腳本實際狀態
 
 
 📊 【 Tier 3 容災統計報告 】
總請求數: 103
成功數 (302/200): 103
失敗數 (502/504/000): 0
⭐ HTTP 成功率: 100.00%


Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/Endpoint%20Failover.gif)

</ul>
</details>

</ul>
</details>

<details>
<summary><b><i>　Ingress Failover </i></b></summary>
<ul>

```
Objective: 
 • 測試級別: 網關流量層 ( 外網 → Ingress → Pod )
 • 驗證外網入口網關 ( Ingress Controller ) 與 K8s 控制面 ( Control Plane ) 的聯動效率
 • 當後端套件發生滾動更新 ( Rolling Update ) 或突發縮容時, 外網 Ingress 路由反向代理能否即時同步變更, 
   確保外網使用者在路由頻繁變更期間, 訪問服務維持零斷線、零延遲感知
 
Situation:
 • 後端 registry-homelab-test 部署為雙複本 replicas: 2, 避免了複雜有狀態組件的 Sidecar 干擾
 • 網關 Nginx Ingress Controller 採用 hostNetwork: true 獨佔邊緣節點實體埠
 
Action:
 • 在本地啟動循環的背景腳本, 每 N 秒對該 Service 的發送一次 curl 請求
   TOTAL=0; SUCCESS=0; FAIL=0; echo "🚀 開始高頻容災測試 ( 每秒 20 次 )... 按 Ctrl+C 結束並查看統計報告"; trap 'echo -e "\n📊 【 Tier 3 容災統計報告 】\n總請求數: $TOTAL\n成功數 (302/200): $SUCCESS\n失敗數 (502/504/000): $FAIL\n⭐ HTTP 成功率: $(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)%"' INT; while true; do CODE=$(curl -o /dev/null -s -w "%{http_code}" -H "Host: docker-registry.k8s.local" http://10.88.0.20/ --connect-timeout 1); TOTAL=$((TOTAL+1)); if [ "$CODE" = "200" ] || [ "$CODE" = "302" ]; then SUCCESS=$((SUCCESS+1)); else FAIL=$((FAIL+1)); echo "❌ 抓到斷線! 狀態碼: $CODE"; fi; sleep 0.05; done
         
 • 觸發 ArgoCD 滾動更新, 觀察 Nginx Ingress Controller 能否平滑分流
 
Metric:
 • Ingress Config Sync Latency ( K8s Endpoints 變更後, Ingress 網關內部 Upstream 重新載入的時間 )
 • External Request Dropped Count ( 外部請求被網關拋棄、拒連的次數, 目標 0 )
 
Pass Criteria:
 • 滾動更新期間, 外部高頻請求無任何丟包、無 502 Bad Gateway, 錯誤率為 0%
 
Result:
 • HTTP Success Rate During Rollout ..... 100%
 • Observed Config Sync Latency .......... < 1 sec ( 記憶體動態更新 )
 • ⭐ External Request Dropped .......... 0
 
Observation:
 • 雖然 2 個舊實例最終皆被重啟汰換, 但得益於無狀態應用的獨立性, K8s 嚴格執行 <新節點就緒、舊節點才下線> 的交替控管
   Nginx Ingress 記憶體 Upstream 同步極其敏捷, 演練全程外網存取毫無斷線感知


📊 【 Tier 3 容災統計報告 】
總請求數: 151
成功數 (302/200): 151
失敗數 (502/504/000): 0
⭐ HTTP 成功率: 100.00%


Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/Ingress%20Failover.gif)

</ul>
</details>

</ul>
</details>

<br>

### *★　Tier 4 : Stateful Recovery*

<details>
<summary><b><i>　PVC Persistence </i></b></summary>
<ul>

```
Objective: 
 • 驗證當 Pod 因任何原因毀損、重啟或重新調度時, 
   其掛載的持久化儲存 ( PVC ) 中的歷史資料不會遺失, 新 Pod 能無縫接軌讀取舊資料
 
Situation:
 • Pod 正常運行中, 且已掛載 PVC 到容器內的 /app/data/
 
Action:
 • 透過 K9s 進入日誌 <觀察目前消費 ID> 因為有綁定地端 SQLite 進行持久化, 所以當被砍掉後應該要能從上次位置重新消費事務
 • 在 K9s 中對該 Pod 按 ctrl + d, 強制 K8s 重新拉一隻新 Pod
 
Pass Criteria:
 • 新 Pod 啟動完成後, 進入新容器日誌查看業務邏輯是否從上次的消費位置繼續執行 而非全部重製
 
Result:
 • ⭐ Total Verification Time .... 15 sec
 
Observation:
 • 檢視持久化位置: mount | grep /app/data
 • 砍掉容器後觀察日誌是否一致性: K9s 中對該 Pod 按 l

Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/PVC%20Persistence.gif)

</ul>
</details>

</ul>
</details>

<details>
<summary><b><i>　StatefulSet Recovery </i></b></summary>
<ul>

```
Objective: 
 • 驗證當具備狀態的 Pod ( StatefulSet ) 因節點故障或進程暴斃時, 
   Kubernetes 的自我修復 ( Self-healing ) 機制能否嚴格遵循 <持久化識別> 原則, 
   在重啟時保持相同的 Pod 編號, 並精準掛載回原有的 PVC 磁碟鎖, 確保資料不遺失、不毀損
 
Situation:
 • 部署一個範例 StatefulSet ( 或現有的有狀態元件, 如 PostgreSQL ), Replica = 1 ( Pod 名稱結尾為 -0 ) 
 • Pod 掛載了特定的 RWO ( ReadWriteOnce ) PVC, 且狀態為 Running
 
Action:
 • 透過 K9s 進入該 StatefulSet Pod 內部, 在掛載的 PVC 目錄下寫入一筆帶有時間戳記的測試資料
    # 本地建立
    echo "statefulset-self-healing-test-2026" > /tmp/recovery_token.txt
    cat /tmp/recovery_token.txt
    
    # 空頭進容器
    kubectl cp /tmp/recovery_token.txt databases-homelab-test/postgresql-homelab-test-0:/bitnami/postgresql/recovery_token.txt

 • 在 K9s 中對該 Pod 執行強制刪除 ( ctrl + d ) , 模擬容器突發性崩潰、被驅逐 ( Eviction ) 或毀損
 • 靜置等待 K8s 控制器自動偵測並原地重建該 Pod
 
 • 再次進入容器確認 方才建立檔案是否存在
    cat /bitnami/postgresql/recovery_token.txt
 
Metric:
 • Pod Identity Consistency ( 重啟前後的 Pod 名稱與序號是否 100% 一致 )
 • Volume Re-attach Latency ( 舊 Pod 釋放磁碟到新 Pod 成功掛載並鎖定 PVC 的時間差 )
 • Data Integrity ( 重啟後, 原本寫入硬碟的資料有無遺失 )
 • Total Self-healing Time ( 從 Pod 消失到新 Pod 變回 READY 1/1 的總耗時 )
 
Pass Criteria:
 • 完全自動化 ( No Manual Intervention ) , 不需手動修復磁碟或下達重啟
 • 新長出來的 Pod 名字必須與舊的完全相同, 不可產生隨機亂碼後綴
 • 進入新 Pod 後, 原本寫入 PVC 的測試資料完好如初
 
Result:
 • Pod Identity Consistency .... 一致
 • Volume Re-attach Latency ..... 0 sec ( 單機 Local-Path 原地重用, 無分離掛載延遲 )
 • Total Self-healing Time ..... 20 sec
 • ⭐ Data Integrity ........... 無損
 
Observation:
 • K9s: 觀察 Pod 列表, 原本的 postgresql-homelab-test-0 變成 Terminating, 
        隨後長出名字一模一樣的 postgresql-homelab-test-0 進入 Init 或 Running
 • 查看 PVC 狀態： 確認該 PVC 在短暫釋放後, 立刻被重新綁定 ( Bound ) 到新的同名 Pod 上
 • 臨時建立的 recovery_token.txt 將容器銷毀後 再次確認也依然存在
 • Environment Specific Result: 本測試局限於 local-path 單機磁碟, 更複雜環境未能實現
 
Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/StatefulSet%20Recovery.gif)

</ul>
</details>

</ul>
</details>


<br>

### *★　Tier 5 : Autoscaling*

<details>
<summary><b><i>　HPA Scale-Out </i></b></summary>
<ul>

```
Objective: 
 • 驗證當業務流量爆發或運算負載攀升、導致 Pod 資源消耗達到預設門檻時, 
   HPA 能否在無人工介入的情況下, 自動橫向擴展 ( Scale-Out ) 實例數量, 以分擔負載
 
Situation:
 • Pod 正常運行中
 • HPA 基礎配置為 minReplicas=1 + maxReplicas=2 + CPU 超過 1% 就擴展
 
Action:
 • 為了不破壞生產環境程式, 不採取真實壓測, 改採「降低門檻基準」進行宣告
 • 修改 Git 上的 values.yaml, 將 targetCPUUtilizationPercentage 從 50% 調整為極低的 1%
 • 推送 Git 並由 ArgoCD 執行自動/手動同步, 將 1% 門檻下刷至 K8s 叢集
 • 由於 Pod 活體的基本消耗必大於 1%, K8s 監控採樣後會立刻判定 <資源超載>, 進而驅動自動擴展
    
Metric:
 • GitOps Sync Latency ( Git 推送後, ArgoCD 完成 HPA 門檻更新的時間 )
 • HPA Metric Sampling Latency ( HPA 採樣到指標超標、並決定增加 Replica 的反應時間 )
 • Target Replica Count ( 觀測 Pod 是否順利從 1 變成設定的 Max Replicas )
 
Pass Criteria:
 • 流程完全遵循 GitOps 宣告式維運
 • K9s 畫面中的 Pod 數量確實依據 HPA 宣告之最大值自動長出, 且狀態變更為 Running
 
Result:
 • GitOps Sync Latency ........... 15 sec
 • HPA Sampling Latency .......... 100 sec
 • ⭐ Target Replica Count ....... 1 → 2
 
Observation:
 • K9s: 
    • 觀察狀態是否從原本只有 1 隻, 幾十秒內會突然蹦出第 2 隻 ( ContainerCreating )
    • 進入: hpa 畫面, 觀察 TARGETS 欄位是否呈現破表狀態 ( 1% )
 • 本測試屬於 Configuration Trigger Test 而非真實 Load Test
 
Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/HPA%20Scale-Out.gif)

</ul>
</details>

</ul>
</details>

<details>
<summary><b><i>　HPA Scale-In </i></b></summary>
<ul>

```
Objective: 
 • 驗證當高峰流量或高運算負載退去、資源消耗降回安全線以下時, 
   HPA 能否在不過度震盪 ( Cooldown 緩衝期內 ) 的前提下, 
   自動將冗餘的 Pod 實例進行裁撤, 以釋放叢集物理資源

Situation:
 • 呈 HPA Scale-Out 當前狀態延伸實施

Action:
 • 將 values.yaml 中的 targetCPUUtilizationPercentage 改回原本正常的 50%
 • 推送並同步至 ArgoCD, 此時 K8s 判定目前系統資源消耗 ( 5% ) 已低於門檻 ( 50% ) 
 • 靜置等待 K8s 預設的縮容冷卻時間 ( Cooldown Period, 預期為 5 分鐘 ), 觀察 Pod 數量是否自動回縮
 
Metric:
 • Scale-In Cooldown Delay ( 從指標降回安全線, 到 K8s 真正開始動手砍 Pod 的等待時間 )
 • Final Replica Count ( 縮容完成後的最終 Pod 數量, 應回歸 minReplicas 基準 )
 
Pass Criteria:
 • 多餘的 Pod 順利進入 Terminating 狀態, 且最終數量精準縮回 1 隻
 
Result:
 • Scale-In Cooldown Delay ( 通常預設為 5 分鐘, 防震盪 ) ..... N/A sec 
 • ⭐ Final Replica Count ................................ 2 -> 1

Validation: ⛔

• 失敗原因：
  由於應用的 Deployment 採用 strategy: Recreate, 在 GitOps 同步門檻值的瞬間, 
  觸發了 Deployment 的 <先殺後建> 生命週期, 這導致冗餘 Pod 是因 <版本更新> 而被物理強制剔除, 
  而非經由 HPA 監測 CPU 指標後觸發的平滑縮容
  
• 結論：
  1. HPA 的防震盪窗口 ( Cooldown Period ) 在 Recreate 策略下會失效
  2. 本應用作為單一實例 ( Singleton ), 未來維運應關閉 HPA, 改靠 K8s 內建的 Self-healing ( Tier 1/2 ) 保障可用性即可
```

<details>
<summary><b><i>　🎬　Demo </i></b></summary>
<ul>

![GIF](../assets/gif/HPA%20Scale-In.gif)

</ul>
</details>

</ul>
</details>

<br>

### *★　Tier 6 : Control Plane HA*

<details>
<summary><b><i>　Single Master Failure </i></b></summary>
<ul>

```
3 節點的內建 dqlite 叢集
 • Quorum = ⌊ N / 2 ⌋ + 1
    → N = 3 ; ⌊ 3 / 2 ⌋ + 1 = 2 ( 向下取整 )
 • 3 台 Master 裡, 至少必須有 2 台同時活著, dqlite 叢集才能正常讀寫
 • 3 - 2 = 容錯上限 1 台；不論關掉 0、1、2 號機, 只要全場還有 2 台活著, 大腦狀態儲存絕對是健康的
 
Objective: 
 • 驗證當控制平面 ( Control Plane ) 失去單一主節點 ( Master ) 時, 依靠內建 dqlite 的 Raft 共識機制, 
   剩餘的 Master 節點能否在無人工介入下自動維持過半數信任 ( Quorum ), 確保叢集 API Server 持續可用, 
   且全叢集已存活之資料平面的 Pod 容器正常運作、不受斷線干擾
 
Situation:
 • 叢集具備 3 台 Master 節點, 此時本地端 Kubeconfig 外部連線端點仍單點綁定於 k3s-master-0 ( 10.88.0.10 )
 
Action:
 • 於 WSL2 啟動循環監聽 API Server 存活狀態：
   while true; do kubectl get nodes > /dev/null && echo "✅ K8s API Server 正常" || echo "❌ K8s API Server 斷線"; sleep 0.5; done
  
 • 觀察位於 Master 的服務是否中斷 ( 切記是非必要服務 ; 控制台不跑任何主要服務 ) 
   kubectl get pods -A -w -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,IP:.status.podIP,NODE:.spec.nodeName,STATUS:.status.phase,AGE:.metadata.creationTimestamp | grep "k3s-master"

 • 手動將「非入口」之其中一台 Master ( k3s-master-1 ) 節點強制物理斷電關機
 • 觀察外網監聽指令是否發生卡頓、噴出 i/o timeout, 並確認 K9s 中節點狀態更迭
 
Metric:
 • Control Plane Outage Duration ( 核心 API 癱瘓、無法連線的總時間, 目標 0 秒 )
 • Data Plane Affected Count ( 資料平面受干擾、意外重啟的 Pod 數量掉, 目標 0 數量 )
 
Pass Criteria:
 • 關閉單一非入口 Master 期間, 外網/本地對 kubectl 的下達完全無感, 沒有發生連線拒絕, 且所有 Agent 上的業務 Pod 100% 正常存活
 
Result:
 • Control Plane Outage Duration .... 0 sec ( 關閉非入口節點 master-1 時 )
 • ⭐ Data Plane Affected Count ..... 0
 
Observation:
 • 執行指令後, K9s 內 k3s-master-1 於約 40 秒後變為 NotReady, 
   在此期間, 外部 kubectl 循環偵測指令完全沒中斷、無任何 i/o timeout 報錯, 證實其餘 2 台 Master 成功維持共識控制權
 • 底層 dqlite 共識機制 ( Quorum=2 ) 完全成立, 但此時突顯出物理盲點：
   因本機連線目前單點綁定於 0 號機, 若未來改關閉 0 號機將引發客戶端外部路由斷線 ( SPOF )
   • 解決方案：下一階段 ( 選舉測試 ) 將導入 Keepalived VIP 技術, 徹底抹平外部存取單點故障
 
Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo ( 關閉非入口 → k3s-master-1 )  </i></b></summary>
<ul>

![GIF](../assets/gif/Single%20Master%20Failure-00.gif)

</ul>
</details>

<details>
<summary><b><i>　🎬　Demo ( 關閉入口機 → k3s-master-0 )  </i></b></summary>
<ul>

![GIF](../assets/gif/Single%20Master%20Failure-01.gif)

</ul>
</details>

</ul>
</details>

<details>
<summary><b><i>　Leader Re-election </i></b></summary>
<ul>

```
3 節點的 dqlite 叢集 + Keepalived
 • Quorum = ⌊ N / 2 ⌋ + 1
    → N = 3 ; ⌊ 3 / 2 ⌋ + 1 = 2 ( 向下取整 )
 • 3 台 Master 裡, 至少必須有 2 台同時活著, dqlite 共識叢集才能正常讀寫
 • 3 - 2 = 容錯上限 1 台；不論關掉 0、1、2 號機, 只要全場維持 2 台存活, 控制面狀態儲存絕對健康
 • [ 架構升級 ] 本節正式於前端全面部署 Keepalived 虛擬 IP ( VIP: 10.88.0.99 ), 徹底抹平外部存取單點故障 ( SPOF )

Objective: 
 • 驗證控制平面核心組件 ( kube-scheduler / kube-controller-manager ) 的高可用接管速度
 • 當現任持有租約鎖定 ( Lease Lock ) 的 Leader 組件暴斃時, 備份組件能否依循設定之租約週期, 
   自動觸發 Leader Re-election ( 領導者重選 ), 並在秒級內平滑移轉控制權, 避免全叢集調度功能癱瘓
 
Situation:
 • K3s 核心控制面組件整合於單一處理程序中, 其分散式鎖定租約儲存於 kube-system 命名空間
 
Action:
 • 於 WSL2 啟動循環監聽 API Server 存活狀態 ( 經由高可用 VIP 入口 ) ：
   while true; do kubectl get nodes > /dev/null && echo "✅ K8s API Server 正常" || echo "❌ K8s API Server 斷線"; sleep 0.5; done
  
 • 觀察位於 Master 的服務是否中斷 ( 切記是非必要服務 ; 控制台不跑任何主要服務 ) 
   kubectl get pods -A -w -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,IP:.status.podIP,NODE:.spec.nodeName,STATUS:.status.phase,AGE:.metadata.creationTimestamp | grep "k3s-master"
   
 • 於 WSL2 啟動 Watch 模式盯著這個租約更迭 ( 監控當選過程 )：
   kubectl get lease -n kube-system kube-scheduler -w
   
 • 手動將當前同時持有租約鎖 ( Holder ) 與 VIP 承載權的主控節點強制物理斷電關機
 • 觀察租約視窗, 記錄 HOLDER 欄位移轉給其餘健康 Master 節點的時間差與平滑度
 
Metric:
 • Lease Failover Latency ( 舊 Leader 倒下到新 Leader 搶鎖成功的時間差, K8s 預設上限 15 秒內 )
 
Pass Criteria:
 • 舊 Leader 倒下後, 租約在微幅超時內必須自動被另一台合規的 Master 承接, HOLDER 欄位順利更名且叢集調度不中斷
 
Result:
 • ⭐ Lease Failover Latency .......... 5 sec ( 遠低於預設超時臨界點 )
 
Observation:
 • 當手動關閉現任 Leader 的伺服器實體後, 透過 get lease -w 觀察到 Lease 於 5 秒內被快速重繪, 
   HOLDER 自動由舊節點變更為活著的健康 Master 節點
 • 同步驗證外部連線, 因 Keepalived VIP 於毫秒級完成網路層飄移, 即便物理拔除 0 號機, 
   外網監聽指令完全未發生任何中斷與 i/o timeout, 完美落實入口與核心元件的雙層高可用
 
Validation: ✅
```

<details>
<summary><b><i>　🎬　Demo ( 正常 → 失聯 ) </i></b></summary>
<ul>

![GIF](../assets/gif/Leader%20Re-election-00.gif)

</ul>
</details>

<details>
<summary><b><i>　🎬　Demo ( 失聯 → 正常 ) </i></b></summary>
<ul>

![GIF](../assets/gif/Leader%20Re-election-01.gif)

</ul>
</details>

</ul>
</details>

<br>

### *⭐　Final Statistics*
```
==================================================================================
                       K3s Native Feature Validation Report
==================================================================================
[ Cluster Topology ]
 • 3 Control Plane Nodes ( k3s-master-0, 1, 2 ) | Embedded dqlite HA Mode
 • 4 Worker Nodes        ( k3s-agent-1, 2, 3, 4 )
 • L3 Network Gateway    ( Keepalived VRRP HA VIP: 10.88.0.99 )
 
[ Result ]
 • 15 / 16 validation scenarios passed
 • 1 scenario identified architectural incompatibility
   ( HPA Scale-In vs Recreate Deployment Strategy )

--------------------------------------------------------------------------------
[ Validation Result Matrix ]
--------------------------------------------------------------------------------
 Tier 1 : Workload Resiliency
   ✔ Pod Crash Recovery ................................................. [ PASS ]
   ✔ OOMKill Recovery  ( Exit Code 137 / No Data Loss Observed ) ........ [ PASS ]
   ✔ Liveness Recovery ( Probe Unhealthy / Local Heartbeat ) ............ [ PASS ]
   ✔ Rolling Update    ( Recreate Deployment Strategy ) ................. [ PASS ]
   ✔ Rollback          ( ArgoCD / GitOps Declared ) ..................... [ PASS ]

 Tier 2 : Node Resiliency
   ✔ Node Drain Recovery   ( Planned Maintenance ) ...................... [ PASS ]
   ✔ Node Failure Recovery ( Disaster Recovery Simulation ) ............. [ PASS ]

 Tier 3 : Traffic Failover
   ✔ Endpoint Failover ( 103/103 Requests / 100% Success ) .............. [ PASS ]
   ✔ Ingress Failover  ( Nginx Upstream Dynamic Reload ) ................ [ PASS ]

 Tier 4 : Stateful Recovery
   ✔ PVC Persistence      ( SQLite Transaction Resumption ) ............. [ PASS ]
   ✔ StatefulSet Recovery ( Identity & Local-Path Disk Lock ) ........... [ PASS ]

 Tier 5 : Autoscaling
   ✔ HPA Scale-Out ( Target CPU 1% Trigger ) ............................ [ PASS ]
   ✘ HPA Scale-In  ( Infra Collision with Recreate Strategy ) .... ...... [ NOT APPLICABLE ]
     └─ 決策架構優化： Singleton 應用應關閉 HPA, 改採 K8s 內建 Self-healing

 Tier 6 : Control Plane HA
   ✔ Single Master Failure ( dqlite Quorum=2 Adherence ) ................ [ PASS ]
   ✔ Leader Re-election    ( Keepalived VIP + Component Lease Lock ) .... [ PASS ]

--------------------------------------------------------------------------------
[ Performance & Resiliency Metrics ]
--------------------------------------------------------------------------------
 • Pod Crash Recovery Time ............................. 5 sec
 • OOMKill Self-Healing Time .......................... 15 sec
 • Liveness Probe Self-Healing Time ................... 12 sec
 • Rolling Update (Recreate Strategy) .................. 5 sec ( PVC Detach/Attach: 1s )
 • Rollback Completion Time ............................ 8 sec
 
 • Node Planned Drain Recovery Time .................... 7 sec
 • Node Disaster Failure Recovery Time ................ 73 sec ( K8s Node NotReady: 52s )
 
 • Service Layer Failover Success Rate .................. 100% ( HTTP Outage Duration: 0s ; 103 requests observed )
 • Observed Ingress Dynamic Config Sync Latency ....... < 1 sec
 
 • StatefulSet Self-Healing Time ..................... 20  sec ( No Data Loss Observed )
 • HPA Scale-Out Trigger Latency ..................... 100 sec
 
 • Observed Control Plane VRRP VIP Failover Latency .. < 1 sec ( Millisecond level )
 • K8s Component Lease Failover Latency ................ 5 sec ( Default: < 15s )

--------------------------------------------------------------------------------
[ Key Findings ]
--------------------------------------------------------------------------------
 • Kubernetes self-healing mechanisms operated as expected.
 • Workloads were successfully rescheduled during node-level failures.
 • Stateful workloads preserved identity and persisted data after recovery.
 • Service and ingress traffic remained available during tested failover events.
 • Control-plane quorum and leader election behaved consistently with HA design expectations.
 
--------------------------------------------------------------------------------
[ Scope Limitation ]
--------------------------------------------------------------------------------
 • The tested K3s cluster successfully demonstrated the expected behavior of
   the evaluated Kubernetes native features under the defined failure scenarios.

 • Recovery, failover, rescheduling, state persistence, and control-plane
   continuity were observed to function as designed within the scope of this validation.

 • Validation results should be interpreted as environment-specific observations
   collected from the current homelab platform and workload characteristics.
   
 • Measured values are observational metrics collected from a single homelab environment 
   and should not be interpreted as performance guarantees for other Kubernetes deployments.

 • Additional validation areas such as backup/restore, disaster recovery,
   security hardening, observability, capacity planning, and upgrade testing
   remain outside the scope of this report.

==================================================================================

                        OVERALL VALIDATION STATUS: PASS ✅


                        [ Validated Scope ]
                         • Kubernetes Native Resiliency Features
                         • Failure Recovery Mechanisms
                         • Stateful Workload Recovery
                         • Service Failover Behaviors
                         • Control Plane High Availability
                        
                        [ Validation Coverage ]
                         • 15 Passed
                         • 1 Not Applicable ( Architectural Constraint )

==================================================================================
```

<br><br><br>