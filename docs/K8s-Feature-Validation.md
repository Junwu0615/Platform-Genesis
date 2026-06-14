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
    - Recovery Time
    - Downtime
    - Failed Requests
    - Data Loss
    ...
    - Availability
 • Result: 實際量測結果
 • Validation: Pass/Fail
 • Observation:
    - kubectl get pods
    - Grafana Screenshot
    - Prometheus Metrics
    - Application Screenshot
```

</ul>
</details>

<details>
<summary><b><i>　II.　Quantitative List </i></b></summary>
<ul>

```
Tier 1 : Workload
 • Pod 崩潰恢復 : Pod Crash Recovery
 • OOMKill 恢復 : OOMKill Recovery
    - Out of Memory Killer: 記憶體耗盡時，為了保護系統核心不崩潰，
      自動挑選並強制終止（Kill）佔用過多記憶體之程序（Process）的機制
 • 活力恢復 : Liveness Recovery
 • 滾動更新 : Rolling Update
 • 回滾 : Rollback


Tier 2 : Node
 • Node Drain
 • Node Reboot
 • Node Failure


Tier 3 : Service
 • Endpoint Failover
 • Ingress Failover


Tier 4 : Storage
 • PVC Persistence
 • StatefulSet Recovery


Tier 5 : Autoscaling
 • HPA Out
 • HPA In


Tier 6 : Control Plane
 • Single Master Failure
 • Leader Re-election
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
 • [Total Recovery Time] : 5 sec

Observation:
 • kubectl get pods -n pg-apps-homelab-test -w
 
Validation: PASS
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

```

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
<summary><b><i>　Node Drain </i></b></summary>
<ul>

```

```

</ul>
</details>

<details>
<summary><b><i>　Node Reboot </i></b></summary>
<ul>

```
```

</ul>
</details>

<details>
<summary><b><i>　Node Failure </i></b></summary>
<ul>

![GIF](../assets/gif/Node%20Failure.gif)

```
Objective:
 • 驗證 Scheduler 重新調度能力
 • 驗證 Worker Node 發生故障後，K8s 是否能自動重新調度 Workload 並恢復服務可用性

Situation:
 • Workload Running on Agent-3
 • Application can run on [ Agent-2, Agent-3 ]
 • Application Running
 • Replica = 1
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
 • Container Startup Time : 7 sec
 • [Total Recovery Time] : 72 sec

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
    

Validation: PASS
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
- 3 Control Plane
- 3 Worker

Validation Result:
--------------------------------

Workload
✓ Pod Crash Recovery
✓ OOMKill Recovery
✓ Liveness Recovery
✓ Rolling Update
✓ Rollback

Node
✓ Node Drain
✓ Node Reboot
✓ Node Failure

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