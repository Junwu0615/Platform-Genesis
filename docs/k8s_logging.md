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
```
$ kubectl get pods -n promtail -o wide
NAME             READY   STATUS    RESTARTS   AGE   IP           NODE         NOMINATED NODE   READINESS GATES
promtail-4nkxv   1/1     Running   0          12m   10.42.0.29   k3s-node-0   <none>           <none>
promtail-b89dw   1/1     Running   0          12m   10.42.1.66   k3s-node-2   <none>           <none>
promtail-sj8w7   1/1     Running   0          12m   10.42.3.75   k3s-node-1   <none>           <none>
```

<br><br><br>