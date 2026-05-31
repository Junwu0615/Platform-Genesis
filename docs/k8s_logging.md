## *K8s - 日誌統一收集與發送*


### *A.　流程說明*
```
Node1
├── Kubelet
├── Pods
└── Promtail ( *DaemonSet ) # /var/log/containers/*

Node2
├── Kubelet
├── Pods
└── Promtail ( *DaemonSet ) # /var/log/containers/*

Node3
├── Kubelet
├── Pods
└── Promtail ( *DaemonSet ) # /var/log/containers/*

    ↓
  Loki
    ↓
 Grafana
```

<br><br><br>