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

![PNG](../assets/logging_00.png)

```
$ kubectl get pods -n promtail-homelab-test -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
promtail-homelab-test-5grsh   1/1     Running   0          63m   10.42.1.4    k3s-master-1   <none>           <none>
promtail-homelab-test-bqt59   1/1     Running   0          63m   10.42.0.5    k3s-master-0   <none>           <none>
promtail-homelab-test-cfr8l   1/1     Running   0          63m   10.42.5.11   k3s-agent-2    <none>           <none>
promtail-homelab-test-ldh6c   1/1     Running   0          63m   10.42.4.9    k3s-agent-1    <none>           <none>
promtail-homelab-test-rplhr   1/1     Running   0          63m   10.42.6.9    k3s-agent-0    <none>           <none>
promtail-homelab-test-wqt5l   1/1     Running   0          63m   10.42.3.4    k3s-master-2   <none>           <none>


$ kubectl get pods -n loki-homelab-test -o wide
NAME                                                        READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
loki-canary-8676d                                           1/1     Running   0          55m   10.42.1.5    k3s-master-1   <none>           <none>
loki-canary-9vjp9                                           1/1     Running   0          55m   10.42.6.12   k3s-agent-0    <none>           <none>
loki-canary-fbdkh                                           1/1     Running   0          55m   10.42.4.11   k3s-agent-1    <none>           <none>
loki-canary-rt5t9                                           1/1     Running   0          55m   10.42.0.6    k3s-master-0   <none>           <none>
loki-canary-xnc5s                                           1/1     Running   0          55m   10.42.5.12   k3s-agent-2    <none>           <none>
loki-canary-zn2rz                                           1/1     Running   0          54m   10.42.3.5    k3s-master-2   <none>           <none>
loki-gateway-6d5fc56d7-bxvq5                                1/1     Running   0          54m   10.42.3.6    k3s-master-2   <none>           <none>
loki-homelab-test-0                                         1/1     Running   0          54m   10.42.5.14   k3s-agent-2    <none>           <none>
loki-homelab-test-grafana-agent-operator-599f47b676-ccw9m   1/1     Running   0          55m   10.42.4.12   k3s-agent-1    <none>           <none>
loki-homelab-test-logs-6qjxq                                2/2     Running   0          54m   10.42.1.6    k3s-master-1   <none>           <none>
loki-homelab-test-logs-8l7vd                                2/2     Running   0          54m   10.42.5.15   k3s-agent-2    <none>           <none>
loki-homelab-test-logs-h2wqt                                2/2     Running   0          54m   10.42.3.7    k3s-master-2   <none>           <none>
loki-homelab-test-logs-k985l                                2/2     Running   0          54m   10.42.4.13   k3s-agent-1    <none>           <none>
loki-homelab-test-logs-tnt29                                2/2     Running   0          54m   10.42.6.14   k3s-agent-0    <none>           <none>
loki-homelab-test-logs-wmgc2                                2/2     Running   0          54m   10.42.0.7    k3s-master-0   <none>           <none>


$ kubectl get pods -n tempo-homelab-test -o wide
NAME                                                READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
tempo-homelab-test-compactor-5cc476bcb9-xxwkn       1/1     Running   0          66m   10.42.6.6    k3s-agent-0    <none>           <none>
tempo-homelab-test-distributor-5f4998dcfc-hzsx9     1/1     Running   0          57m   10.42.6.10   k3s-agent-0    <none>           <none>
tempo-homelab-test-ingester-0                       1/1     Running   0          66m   10.42.5.5    k3s-agent-2    <none>           <none>
tempo-homelab-test-memcached-0                      1/1     Running   0          66m   10.42.6.7    k3s-agent-0    <none>           <none>
tempo-homelab-test-querier-84bbb4689d-dmz2x         1/1     Running   0          66m   10.42.1.3    k3s-master-1   <none>           <none>
tempo-homelab-test-query-frontend-88759c5fc-4pkrr   1/1     Running   0          66m   10.42.4.6    k3s-agent-1    <none>           <none>


$ kubectl get pods -n prometheus-stack-homelab-test -o wide
NAME                                                              READY   STATUS    RESTARTS      AGE   IP           NODE           NOMINATED NODE   READINESS GATES
alertmanager-prometheus-stack-homelab-t-alertmanager-0            2/2     Running   0             65m   10.42.5.9    k3s-agent-2    <none>           <none>
prometheus-prometheus-stack-homelab-t-prometheus-0                2/2     Running   0             65m   10.42.5.10   k3s-agent-2    <none>           <none>
prometheus-stack-homelab-t-operator-6d64d57745-pqrz7              1/1     Running   0             65m   10.42.6.8    k3s-agent-0    <none>           <none>
prometheus-stack-homelab-test-kube-state-metrics-6db996d4dz77dz   1/1     Running   0             65m   10.42.4.8    k3s-agent-1    <none>           <none>
prometheus-stack-homelab-test-prometheus-node-exporter-5ntwn      1/1     Running   0             65m   10.88.0.20   k3s-agent-0    <none>           <none>
prometheus-stack-homelab-test-prometheus-node-exporter-8hhmk      1/1     Running   0             65m   10.88.0.22   k3s-agent-2    <none>           <none>
prometheus-stack-homelab-test-prometheus-node-exporter-8rlnm      1/1     Running   0             65m   10.88.0.10   k3s-master-0   <none>           <none>
prometheus-stack-homelab-test-prometheus-node-exporter-bf5s7      1/1     Running   0             65m   10.88.0.11   k3s-master-1   <none>           <none>
prometheus-stack-homelab-test-prometheus-node-exporter-q8x7z      1/1     Running   0             65m   10.88.0.21   k3s-agent-1    <none>           <none>
prometheus-stack-homelab-test-prometheus-node-exporter-tlnwk      1/1     Running   1 (55m ago)   65m   10.88.0.12   k3s-master-2   <none>           <none>
```

<br><br><br>