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
 • Evidence:
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
 • Drain
 • Reboot
 • Failure

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
 • kubectl delete pod inst-homelab-test-xxx-xxx
 • K9s : ctrl + k

Metric:
 • Pod Recovery Time

Result:
 • New Pod Created : 2 sec
 • Ready State : 5 sec

Validation:
 • PASS

Evidence:
 • kubectl get pods -n pg-apps-homelab-test -w
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
<summary><b><i>　Drain </i></b></summary>
<ul>

```

```

</ul>
</details>

<details>
<summary><b><i>　Reboot </i></b></summary>
<ul>

```
```

</ul>
</details>

<details>
<summary><b><i>　Failure </i></b></summary>
<ul>

```

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
✓ Drain
✓ Reboot
✓ Failure

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