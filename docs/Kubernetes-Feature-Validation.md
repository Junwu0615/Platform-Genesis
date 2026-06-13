## *⭐ K8s - 原生能力驗證 ( Feature Validation ) ⭐*

### *A.　測試內容*
```
A. Workload Resilience: 驗證 Pod 與 Deployment 自癒能力
    * 指標:
        - Pod Recovery Time (s)
        - Service Recovery Time (s)
        - Request Failure Count

    * 測試項目:
    👁️ Test 1 : Pod Crash Recovery
    👁️ Test 2 : Container Crash Recovery
    👁️ Test 3 : OOMKilled Recovery
    👁️ Test 4 : Liveness Probe Failure
    👁️ Test 5 : Readiness Probe Failure
    👁️ Test 6 : Rolling Update
    👁️ Test 7 : Rollback


B. Scheduling Resilience: 驗證 Scheduler
    * 指標:
        - Reschedule Time
        - Pod Migration Time
        - Unavailable Pod Count

    * 測試項目:
    👁️ Test 8 : Anti-Affinity
    👁️ Test 9 : Node Affinity
    👁️ Test 10 : Taints & Tolerations
    👁️ Test 11 : Node Drain
    👁️ Test 12 : Node Failure


C. Service Resilience: 驗證網路與流量
    * 指標:
        - Success Rate
        - Error Rate
        - Response Time

    * 測試項目:
    👁️ Test 13 : Service Connectivity
    👁️ Test 14 : Load Balancing
    👁️ Test 15 : Endpoint Removal
    👁️ Test 16 : Ingress Routing


D. Scalability: 驗證可擴展性
    * 指標:
        - Scale Trigger Time
        - Scale Completion Time

    * 測試項目:
    👁️ Test 17 : HPA Scale Out
    👁️ Test 18 : HPA Scale In


E. Storage Resilience: 驗證儲存彈性
    * 指標:
        - Data Loss
        - Recovery Time
        - Volume Reattach Time

    * 測試項目:
    👁️ Test 19 : PVC Persistence
    👁️ Test 20 : Pod Recreate with PVC
    👁️ Test 21 : Node Failure with PVC


F. GitOps Resilience: 驗證 GitOps 彈性
    * 指標:
        - Drift Detection Time
        - Sync Time
        - Rollback Time

    * 測試項目:
    👁️ Test 22 : Drift Detection
    👁️ Test 23 : Auto Sync Recovery
    👁️ Test 24 : Git Rollback


G. Control Plane: 驗證 Master 多節點高可用
    * 指標:
        - API Availability
        - Workload Availability
        - Recovery Time

    * 測試項目:
    👁️ Test 25 : Control Plane Failure
    
    
------
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

Tier 6 : GitOps Recovery
 • Drift Detection
 • Auto Heal
 • Git Rollback

Tier 7 : Control Plane
 • Single Master Failure
 • Leader Re-election
```

<br>

### *B.　測試紀錄*
```
* 定義測試內容格式

# Test 1

Pod Crash Recovery

Action:
kubectl delete pod

Metric:
Pod Recovery Time

Pass:
< ? sec

------

# Test 12

Node Failure

Action:
shutdown node

Metric:
Pod Migration Time

Pass:
< ? sec

------

# Test 22

Drift Detection

Action:
kubectl scale deployment xxx --replicas=10

Metric:
Drift Detection Time

Pass:
< ? sec
```

<br>

### *C.　最終統計*
```
K3s HA Validation Result

* Node Count : 6

* Pod Recovery Time
    Average : - sec

* Node Failure Recovery
    Average : - sec

* Rolling Update Downtime
    - sec

* Rollback Time
    - sec

* HPA Scale Out
    - sec

* PVC Data Loss
    -

ArgoCD Drift Recovery
    - sec
```

<br><br><br>