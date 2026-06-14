## *⭐ K8s - 原生能力驗證 ( Feature Validation ) ⭐*

<br>

### *A.　Quantitative*

<details>
<summary><b><i>　I.　Format </i></b></summary>
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
<summary><b><i>　II.　List </i></b></summary>
<ul>

```
Tier 1 : Workload
 • Pod Crash
 • OOMKill
 • Liveness
 • Rolling Update
 • Rollback

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

#### *★　Tier 1 : Workload*

<details>
<summary><b><i>　Pod Crash </i></b></summary>
<ul>

```

```

</ul>
</details>

<details>
<summary><b><i>　OOMKill </i></b></summary>
<ul>

```
```

</ul>
</details>

<details>
<summary><b><i>　Liveness </i></b></summary>
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

### *B.　Final Statistics*
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