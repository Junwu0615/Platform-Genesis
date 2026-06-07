## *K8s - 基礎設施高可用性測試*

### *A.　測試項目*
```
👁️ 測試 0: 取得需要對外交互的服務位置 確認能訪問服務 ( ex: Portainer )
👁️ 測試 1: Pod 故障自癒 ( 模擬服務崩潰 ) 
👁️ 測試 2: 容器層級故障 ( 容器逃逸測試 )
👁️ 測試 3: 滾動更新 ( Rolling Update )
👁️ 測試 4： 錯誤與回滾 ( Rollback )
👁️ 測試 5： 配置更新自動觸發重啟 ( Reloader )
👁️ 測試 6： 網路層級（ Service 斷線測試 ）
👁️ 測試 7： 資源限制 ( Resource Limit - OOMKilled )
👁️ 測試 8： 親和性與反親和性 ( Anti-Affinity )
👁️ 測試 9： 存活探針故障 ( Liveness Probe Failure )
👁️ 測試 10： Node Affinity ( 指定居所 )
👁️ 測試 11： 多節點自癒與調度演習
👁️ 測試 12： Service 的負載平衡與連通性
👁️ 測試 13： 自動摘除與恢復
👁️ 測試 14： 零停機更新與回滾 ( Rolling Update & Rollback )
👁️ 測試 15： Ingress 流量入口 ( Traefik )
👁️ 測試 16： 高可用單一實例 ( HA Singleton )
👁️ 測試 17： 橫向自動伸縮 ( HPA - Horizontal Pod Autoscaler )
👁️ 測試 18： 持久化儲存與節點漂移 ( PV / PVC / Local Path )
```

<br><br><br>