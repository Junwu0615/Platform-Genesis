## *K8s - Observability Platform*


### *A.　Architecture*
```
Application
    │
    ├──  Metrics
    │       ↓
    │  Prometheus
    │       ↓
    │ AlertManager
    │       ↓
    │    Grafana
    │
    ├──   Logs
    │       ↓
    │    Promtail
    │       ↓
    │      Loki
    │       ↓
    │    Grafana
    │
    └──   Traces
            ↓
          Tempo
            ↓
         Grafana
```

![PNG](../assets/logging_00.png)
![PNG](../assets/observability_00.png)

<br>

### *B.　Components*
| Item | Purpose |
|:--:|:--:|
| Prometheus | Metrics Collection |
| AlertManager | Alert Routing |
| Grafana | Visualization |
| Promtail | Log Collection |
| Loki | Log Storage |
| Tempo | Distributed Tracing |

<br>

### *C.　Logging Validation*
```
k3s-master-0
├── Kubelet
├── Pods
└── Promtail ( *DaemonSet ) # /var/log/containers/*

k3s-master-1
├── Kubelet
├── Pods
└── Promtail ( *DaemonSet ) # /var/log/containers/*

  ...
  
k3s-agent-2
├── Kubelet
├── Pods
└── Promtail ( *DaemonSet ) # /var/log/containers/*
    ↓
  Loki
    ↓
 Grafana
```

<br>

### *D.　Metrics Validation*
```
[ 
  Node Exporter, 
  Kube State Metrics,
]
       ↓
    Prometheus
       ↓
    Grafana
```

<br>

### *E.　Tracing Validation*
```
    TraceID
    
    Frontend
      ↓
    Backend
      ↓
    Kafka
      ↓
    PostgreSQL


❌ 只有 Loki 的痛苦 →> Only Logging → 線索斷開
每個 Pod 都是獨立印 Log，當並發量很高、一秒鐘有幾千筆 Log 湧入時，
根本沒辦法把「前端 A 使用者的這一次點擊」、「Kafka 的某個事件」，
以及「PostgreSQL 的某一條 SQL」精準綁在一起。
                 ↓
不知道這 5 秒鐘到底是被卡在 Kafka 還是卡在資料庫。


Tempo 引入了一個概念 → TraceID
當 A 使用者點擊的瞬間，系統會產生一個獨一無二的 TraceID=abc123xyz。
當這個請求流經所有服務時，這個 ID 會像接力棒一樣一直傳下去。
在 Tempo (Grafana) 畫面上會看到一張完美的時間瀑布圖（Flame Graph）：

[Gateway: /order] ────────────────────────────────────────── (總共 5.0s)
  ├── [Auth-Service: Check Token] ── (0.1s)
  ├── [Backend-API: Create Order] ────────────────────────── (4.9s)
  │     ├── [PostgreSQL: INSERT Order] ─ (0.02s)  <-- 看到了吧！ DB 其實超快
  │     └── [Kafka: Produce Message] ────────────────────── (4.8s) 🔥 兇手抓到了！
```

<br>

### *F.　Alert Manager Validation*
```
* Test 1: CPU High Usage
    - Action: stress-ng --cpu 4
    - Alert Rule: CPU > 80%


* Test 2: Pod Crash
    - Action: kubectl delete pod
    - Alert Rule: Pod Restart Count


* Test 3: Node Down
    - Action: shutdown now
    - Alert Rule: Node Not Ready
```

<br>

### *G.　Failure Correlation Demo*
```
Observability Platform 主目的是為了【 定位問題 】

 * Scenario: User API Timeout
     ↓
 * Metrics: CPU Usage Spike
     ↓
 * Logs: Kafka Connection Timeout
     ↓
 * Trace: Kafka Span = 4.8 sec
     ↓
 * Root Cause: Kafka Latency
```

<br><br><br>