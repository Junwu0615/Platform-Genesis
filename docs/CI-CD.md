## *K8s - CI/CD*


### *A.　說明*
```
```

<br>

### *B.　Tradition*
```
Git Push
  ↓
GitLab CI
  ↓
Build Image
  ↓
Push Registry
  ↓
Update values.yaml
  ↓
K8s Apply
  ↓
Pod Service Running
```

<br>

### *C.　GitOps*
![PNG](../assets/argocd_00.png)
![PNG](../assets/argocd_01.png)
```
Git Push
  ↓
GitLab CI
  ↓
Build Image
  ↓
Push Registry
  ↓
Update values.yaml
  ↓
ArgoCD Detect Drift
  ↓
Sync
  ↓
K8s Apply
  ↓
Pod Service Running
```

<br>

### *D.　Manual vs. GitOps*
```
```

<br><br><br>