## *⭐ K8s - 原生能力驗證 ( Feature Validation ) ⭐*

<br>

### *A.　Document*

<details>
<summary><b><i>　I.　Quantitative Format </i></b></summary>
<ul>

```
Tier ??? : ???
 • Objective: 驗證什麼能力
 • Situation: 測試前狀態
 • Action: 執行動作
 • Metric:
    • Recovery Time
    • Downtime
    • Failed Requests
    • Data Loss
      ...
    • Availability
 • Pass Criteria: 通過標準
 • Result: 實際量測結果
 • Observation:
    • kubectl get pods
    • Grafana Screenshot
    • Prometheus Metrics
    • Application Screenshot
  • Validation: 
    • Pass : ✅
    • Fail : ❌
```

</ul>
</details>

<details>
<summary><b><i>　II.　Quantitative List </i></b></summary>
<ul>

```
Tier 1 : Workload
 • ✅ Pod 崩潰恢復 : Pod Crash Recovery
 • OOMKill 恢復 : OOMKill Recovery
    • Out of Memory Killer: 記憶體耗盡時，為了保護系統核心不崩潰，
      自動挑選並強制終止（Kill）佔用過多記憶體之程序（Process）的機制
 • ✅ 存活狀態自我恢復 : Liveness Recovery
    • 當 Pod 的程式碼內部發生死鎖（Deadlock）、無限迴圈或內部核心執行緒（Thread）崩潰，
      但容器「外殼」還活著時，能被 Kubernetes 自動偵測並在「最短時間內原地重啟」。
 • 滾動更新 : Rolling Update
 • 回滾 : Rollback


Tier 2 : Node
 • ✅ 節點排水 : Node Drain Recovery
    • 代表 → 節點計畫性維護 ( Planned Maintenance )
 • ✅ 節點故障 : Node Failure Recovery
    • 代表 → 節點災難恢復 ( Disaster Recovery )


Tier 3 : Service
 • 端點故障轉移 : Endpoint Failover
 • 入口故障轉移 : Ingress Failover


Tier 4 : Storage
 • PVC 持久性 : PVC Persistence
 • 狀態集恢復 : StatefulSet Recovery


Tier 5 : Autoscaling
 • HPA 輸出 : HPA Out
 • HPA 輸入 : HPA In


Tier 6 : Control Plane
 • 單主故障 : Single Master Failure
 • ??? : Leader Re-election
```

</ul>
</details>

<br>

### *★　Tier 1 : Workload*

<details>
<summary><b><i>　Pod Crash Recovery </i></b></summary>
<ul>

![GIF](../assets/gif/Pod%20Crash%20Recovery.gif)

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
     • K9s : ctrl + k

Metric:
 • Pod Recovery Time

Pass Criteria:
 • Pod Recovery Time < 5 min
 
Result:
 • New Pod Created : 2 sec
 • ⭐ Total Recovery Time : 5 sec

Observation:
 • kubectl get pods -n pg-apps-homelab-test -w
 
Validation: ✅
```

</ul>
</details>

<details>
<summary><b><i>　OOMKill Recovery </i></b></summary>
<ul>

```
```

</ul>
</details>

<details>
<summary><b><i>　Liveness Recovery </i></b></summary>
<ul>

![GIF](../assets/gif/Liveness%20Recovery.gif)

```
Objective: 
 • 驗證單一實例 ( Singleton ) 應用在發生內部核心死鎖 ( Deadlock )、執行緒崩潰或接收到緊急外部中斷訊號時，
   能否在不依賴節點重新調度 ( Reschedule ) 的情況下，由 Kubernetes 偵測並完成<原地快速容器重啟>與服務自我修復能力
 
Situation:
 • Workload Running on [ Agent-2 or Agent-3 ]
 • Application Running normally (K9s STATUS: Running, READY: 1/1)
 • Replica = 1 ( Singleton 限制 )
 • Python 主任務持續消費 Kafka 訊息並寫入 PostgreSQL
 • 心跳檔案存在於容器本地： /app/tmp/heartbeat.txt
 
Action:
 • 透過 Kafka 開發工具或生產者腳本，向指定 Topic 發送一筆包含
   特定 Payload ("TRIGGER_KILL_FROM_KAFKA") 的控制訊息，
   藉此觸發 Python 內部邏輯自殺並移除心跳檔。
 
Metric:
 • Signal Propagation Time ( 訊號發送至 Python 接收的時間差 )
 • Heartbeat Deletion Time ( 心跳檔被移除的時間點 )
 • K8s Detection Latency ( 從檔案消失到 K8s 判定 Unhealthy 的時間，預期約 3~6 秒 )
 • Container Restart Time ( 容器銷毀至重新啟動的時間 )
 • Total Recovery Time ( 從發送控制訊息到 Pod 回復 READY 1/1 的總耗時 )
 • Data Loss ( 切換期間是否有不掉單、重複消費、資料遺失，預期為 0 )
 • Availability ( 整體服務可用性 )
 
Pass Criteria:
 • 完全自動化 ( No Manual Intervention )，不需人工下達 kubectl delete/restart
 • Pod 必須維持在同一個 Node 上進行<原地重啟> ( RESTARTS 次數 +1，而非重新調度 )
 • 資料零遺失 ( Data Loss = 0 )，Kafka Offset 維持一致
 • Total Recovery Time < 15 秒
 
Result:
 • Signal Propagation Time : 1 sec
 • Heartbeat Deletion Time : 2 sec
 • K8s Detection Latency   : 1 sec
 • Container Restart Time  : 8 sec
 • ⭐ Total Recovery Time  : 12 sec
 • Data Loss               : 0 ( Validated via Kafka Offset / PG Count )
 
Observation:
 • 觀察 RESTARTS 欄位是否從 0 變 1
     • watch -n 2 'kubectl get pods -n pg-apps-homelab-test -o wide | grep -E "agent-2|agent-3"'
     • K9s: pod -n pg-apps-homelab-test
 • 檢查 Events 欄位是否出現 "failed liveness probe, will be restarted"
     • kubectl describe pod <pod-name> -n pg-apps-homelab-test
     • K9s: d
 • Kafka Consumer Group Matrix ( 確認 Lag 沒有異常堆積，且重啟後能繼續正常消費 )
 
Validation: ✅
```

</ul>
</details>

<details>
<summary><b><i>　Rolling Update </i></b></summary>
<ul>

```

```

</ul>
</details>

<details>
<summary><b><i>　Rollback </i></b></summary>
<ul>

```

```

</ul>
</details>

<br>

### *★　Tier 2 : Node*

<details>
<summary><b><i>　Node Drain Recovery </i></b></summary>
<ul>

![GIF](../assets/gif/Node%20Drain%20Recovery.gif)

```
Objective:
 • 驗證節點進入維護模式時，Workload 是否能自動遷移至其他可用節點，並維持服務可用性

Situation:
 • Workload Running on Agent-2
 • Application can run on [ Agent-2, Agent-3 ]
 • Application Running
 • Replica = 1 ( Strategy: Recreate # 該應用不能同時存在 2 個 )
 • Target Pod :
    • -n pg-apps-homelab-test
    • inst-homelab-test

Action:
 • 進行節點維運作業 => kubectl drain ( 設定不可排程 + 歷史遺留、現存於該 Node 上的 Pod 趕走 )
    kubectl drain k3s-agent-2 \
      --ignore-daemonsets \
      --delete-emptydir-data
 • 節點維運完成 => 手動復原
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
 • Node Detection Time : 2 sec
 • Eviction Delay : 3 sec
 • Pod Scheduling Time : 3 sec
 • Container Startup Time : 3 sec
 • ⭐ Total Recovery Time : 7 sec

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

</ul>
</details>


<details>
<summary><b><i>　Node Failure Recovery </i></b></summary>
<ul>

![GIF](../assets/gif/Node%20Failure%20Recovery.gif)

```
Objective:
 • 驗證 Scheduler 重新調度能力
 • 驗證 Worker Node 發生故障後，K8s 是否能自動重新調度 Workload 並恢復服務可用性

Situation:
 • Workload Running on Agent-3
 • Application can run on [ Agent-2, Agent-3 ]
 • Application Running
 • Replica = 1 ( Strategy: Recreate )
 • Target Pod :
    • -n pg-apps-homelab-test
    • inst-homelab-test
    • Node Eviction Timeout = 10 sec

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
 • Node Detection Time : 52 sec
 • Eviction Delay : 10 sec
 • Pod Scheduling Time : 3 sec
 • Container Startup Time : 8 sec
 • ⭐ Total Recovery Time : 73 sec

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

</ul>
</details>

<br>

### *★　Tier 3 : Service*

<details>
<summary><b><i>　Endpoint Failover </i></b></summary>
<ul>

```

```

</ul>
</details>

<details>
<summary><b><i>　Ingress Failover </i></b></summary>
<ul>

```

```

</ul>
</details>

<br>

### *★　Tier 4 : Storage*

<details>
<summary><b><i>　PVC Persistence </i></b></summary>
<ul>

```

```

</ul>
</details>

<details>
<summary><b><i>　StatefulSet Recovery </i></b></summary>
<ul>

```

```

</ul>
</details>


<br>

### *★　Tier 5 : Autoscaling*

<details>
<summary><b><i>　HPA Out </i></b></summary>
<ul>

```

```

</ul>
</details>

<details>
<summary><b><i>　HPA In </i></b></summary>
<ul>

```

```

</ul>
</details>

<br>

### *★　Tier 6 : Control Plane*

<details>
<summary><b><i>　Single Master Failure </i></b></summary>
<ul>

```

```

</ul>
</details>

<details>
<summary><b><i>　Leader Re-election </i></b></summary>
<ul>

```

```

</ul>
</details>

<br>

### *⭐ B.　Final Statistics*
```
K3s Feature Validation Summary

Cluster:
• 3 Control Plane
• 4 Worker

Validation Result:
--------------------------------

Workload
✓ Pod Crash Recovery
✓ OOMKill Recovery
✓ Liveness Recovery
✓ Rolling Update
✓ Rollback

Node
✓ Node Drain Recovery
✓ Node Failure Recovery

Service
✓ Endpoint Failover
✓ Ingress Failover

Storage
✓ PVC Persistence
✓ StatefulSet Recovery

Autoscaling
✓ HPA Out
✓ HPA In

Control Plane
✓ Single Master Failure
✓ Leader Re-election

--------------------------------

Key Metrics

Pod Recovery Time
Average : xx sec

Node Failure Recovery
Average : xx sec

Rolling Update Downtime
Average : xx sec

PVC Data Loss
None

StatefulSet Recovery
xx sec

HPA Scale Out
xx sec

Control Plane Recovery
xx sec

Overall Result
PASS
```

<br><br><br>