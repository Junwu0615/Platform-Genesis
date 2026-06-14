## *⭐ K8s - 原生能力驗證 ( Feature Validation ) ⭐*

### *A.　Quantitative Format*
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

<br>

### *B.　Quantitative List*
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
 • 
Tier 5 : Autoscaling
 • HPA Out
 • HPA In

Tier 6 : Control Plane
 • Single Master Failure
 • Leader Re-election
```

<br>

### *C.　Final Statistics*
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