## *⭐ K8s - Deployment Delivery Baseline ⭐*

### *A.　Delivery Model Comparison*

<br>

<details>
<summary><b><i>　a.1.　Pipeline-Driven Delivery </i></b></summary>
<ul>

<br>

<details>
<summary><b><i>　I.　Explain </i></b></summary>
<ul>

```
# Delivery Model

 • Pipeline-Driven
 • Imperative Deployment Workflow


# Typical Components

 • GitLab CI
 • Jenkins
 • Deployment Scripts
 • Kubernetes API


# Characteristics

 • Suitable for small-to-medium teams
 • Supports VM, Docker, and Kubernetes platforms
 • Deployment logic is maintained within CI pipelines
 • Rollback is typically executed through pipeline workflows
 • Deployment state may be distributed across multiple systems
    - Git Repository
    - CI/CD Pipeline
    - Kubernetes Cluster


# Operational Considerations

 • CI systems require deployment permissions
 • GitLab Runner commonly stores Kubernetes credentials
 • Permission management becomes more complex as environments scale


# Strengths

 • Simple implementation model
 • Flexible deployment customization
 • Mature ecosystem and tooling support


# Limitations

 • Desired state is not continuously enforced
 • Configuration drift is not automatically detected
 • Deployment status visibility may span multiple systems


# Deployment Workflow

    Developer Commit
       ↓
    Git Push
       ↓
    GitLab CI / Jenkins
       ↓
    Container Image Build
       ↓
    Container Registry Push
       ↓
    Manifest Update
       ↓
    kubectl apply
       ↓
    Kubernetes Reconciliation
       ↓
    Application Available
```

</ul>
</details>

<details open>
<summary><b><i>　II.　Showcase </i></b></summary>
<ul>

![PNG](../assets/ci-cd_00.png)
![PNG](../assets/ci-cd_01.png)

</ul>
</details>

</ul>
</details>


<details>
<summary><b><i>　a.2.　GitOps Delivery </i></b></summary>
<ul>

<br>

<details>
<summary><b><i>　I.　Explain </i></b></summary>
<ul>

```
# Delivery Model

 • State-Driven
 • Declarative Deployment Workflow


# Typical Components

 • Git Repository
 • GitLab CI
 • Container Registry
 • Argo CD
 • Kubernetes API


# Characteristics

 • Designed for Kubernetes-native environments
 • Desired state is defined and versioned in Git
 • Deployment reconciliation is performed by controllers
 • Git serves as the Single Source of Truth
 • Deployment state is continuously synchronized with Git
 • Infrastructure and application definitions are fully traceable
 • Build and deployment responsibilities are decoupled


# Operational Considerations

 • Repository structure requires standardized organization
    - Environment
    - Application
    - Helm Chart
    - Version Management
 • Argo CD becomes a critical control-plane component
 • Git repository governance becomes part of platform governance


# Strengths

 • Consistent deployment workflow
 • Continuous drift detection
 • Automated desired-state reconciliation
 • Centralized deployment governance
 • Improved deployment traceability
 • Reduced direct cluster access requirements


# Limitations

 • Kubernetes-focused architecture
 • Initial repository design requires additional planning
 • Operational model may introduce learning overhead
 • Misconfigured Git changes can propagate automatically


# Deployment Workflow

    Developer Commit
       ↓
    Git Push
       ↓
    GitLab CI
       ↓
    Container Image Build
       ↓
    Container Registry Push
       ↓
    Manifest Update
       ↓
    Git Repository
       ↓
    Argo CD Detection
       ↓
    Reconciliation
       ↓
    Kubernetes Apply
       ↓
    Application Available
```

</ul>
</details>

<details open>
<summary><b><i>　II.　Showcase </i></b></summary>
<ul>

![PNG](../assets/argocd_00.png)
![PNG](../assets/argocd_01.png)
![PNG](../assets/argocd_02.png)

</ul>
</details>


</ul>
</details>

<br>

### *B.　Quantitative*
#### *b.1.　Experimental Conditions*
```
[ Validation Scope ]

1. This validation compares only the Deployment Delivery Lifecycle.

   The following activities are excluded from all measurements:
    • Source Code Compilation
    • Container Image Build
    • Container Image Push
    • CI Queue Waiting Time


2. Manual Deployment Scenario

   Deployment is performed through direct host operations,
   including remote access, file transfer, configuration updates,
   and manual deployment execution.

   This scenario represents environments with limited deployment
   automation and serves as the baseline reference model.


3. GitOps Deployment Scenario

   Deployment is performed through a GitOps workflow using
   Argo CD as the deployment reconciliation controller.


[ Test Environment ]
 • Node Count         : 6
 • Application        : pg-python-inst
 • Replica Count      : 1
 • Container Image    : 296 MB

[ Toolchain ]
 • Git Repository     : GitLab
 • Container Registry : Docker Registry
 • GitOps Controller  : Argo CD

[ Measurement Method ]
 • Manual Deployment  : 10 executions
 • GitOps Deployment  : 10 executions
 • Result             : Average value reported
```

<br>

#### *b.2.　Single Deployment Measurement*
```
 [ Scope ]
 This Measurement Only Compares the Deployment Delivery Lifecycle

 [ The following items are not included in the statistics ]
 • Source Code Compilation
 • Container Image Build
 • Container Image Push
 • CI Queue Waiting Time

 [ Measurement Startpoint ]
 • Deployment Change Ready

 [ Measurement Endpoint ]
 • Application Ready

 [ Additional Observation ]
 The following values were observed during testing
 but were excluded from deployment lifecycle measurements.

 • Manual Image Build ............. 85 sec
 • GitLab CI Pipeline Runtime .... 105 sec
```

| Item | Manual ( sec ) | GitOps ( sec ) |
|--:|--:|--:|
| Remote Access | 15 | 0 |
| File Transfer | 20 | 0 |
| Configuration Update | 60 | 0 |
| Deployment Execution | 20 | 0 |
| Health Verification | 30 | 30 |
| Functional Verification | 60 | 60 |
| Service Recovery | 20 | 15 |
| Total Delivery Time | 225 | 105 |

<br>

#### *b.3.　Deployment Scalability Estimation*
```
The following values are estimated projections derived
from ⭐ b.2. Single Deployment Measurement.

These values do not include:
 • Human error
 • Context switching
 • Operational fatigue
 • Concurrent deployment optimization
```

| Node | Manual ( min ) | GitOps ( min ) |
|--:|--:|--:|
| 1 | 3.75 | 1.75 |
| 3 | 11.25 | 1.75 |
| 6 | 22.50 | 1.75 |
| 12 | 45.00 | 1.75 |
| 72 | 270.00 | 1.75 |

<br>

#### *b.4.1.　Post-Adoption Risk Assessment*
| Risk Item | Manual | GitOps |
|--:|:--:|:--:|
| Configuration Consistency Risk | High | Reduced |
| Deployment Error Risk | High | Reduced |
| Version Traceability Risk | High | Reduced |
| Unauthorized Change Risk | Medium | Reduced |
| Key-Person Dependency Risk | High | Reduced |

<br>

#### *b.4.2.　Post-Adoption Operational Comparison*
| Item | Manual | GitOps |
|--:|:--:|:--:|
| Git Push | Y | Y |
| Docker Build on Local | Y | N |
| Manually Push Image<br>to Repository | Y | N |
| Remote Access | Y | N |
| Pull File | Y | N |
| Configuration Update | Y | N |
| Deployment Execution | Y | N |
| Health Verification | Y | Y |
| Functional Verification | Y | Y |
| Update Infrastructure<br>Version History | Y | N |
| Number of Operation Steps | 10 | 3 |
| Reduction ( % ) | 0 | 70 |

<br>

#### *⭐ b.4.3.　Industry Delivery Model Comparison*
| Item | SSH | CI/CD | GitOps |
|--:|:--:|:--:|:--:|
| Build | Manual | Automated | Automated |
| Deployment | Manual | GitLab CI | Argo CD |
| Rollback | Manual | Pipeline-Driven | Git-Based Reconciliation |
| Drift Detection | N | N | Y |
| Audit Trail | Partial | Partial | Complete |
| Desired-State Recovery | Manual | Manual | Automated |

<br>

#### *⭐ b.4.4.　Capability Comparison Matrix*
| Capability | SSH | CI/CD | GitOps |
|--:|:--:|:--:|:--:|
| Automated Deployment | N | Y | Y |
| Git Traceability | N | Partial | Y |
| Drift Detection | N | N | Y |
| Self Healing | N | N | Y |
| Disaster Recovery | Partial | Partial | Y |
| RBAC Centralization | N | Partial | Y |

<br>

### *⭐ Baseline Findings*
| Item | Manual → GitOps |
|--:|:--|
| Measured Deployment<br>Time Reduction | 53.3%<br>( 225 sec → 105 sec ) |
| Estimated Multi-Node Operational Scaling Benefit | Derived from single-deployment measurements<br>and linear operational effort assumptions |
| Post-Adoption<br>Operational Comparison | 70% ( Steps: 10 → 3 ) |
| Deployment<br>Access Centralization | 移除個人 KubeConfig / 直接 Cluster 存取權限<br>/ 部署操作統一經由 Argo CD RBAC 控管<br><br>• 補充 GitLab 尚有權限 ( Registry / Repo / Pipeline ) |
| Rollback<br>Process Simplification | Manual rollback procedures replaced<br>by Git-based version reversion workflow |
| Multi-node Deployment<br>Efficiency Improvement | Linear → Near-constant |

<br>

```
==================================================================================
                  Deployment Delivery Baseline Validation Report
==================================================================================

[ Measured Results ]
 • Deployment delivery time decreased from 225 sec to 105 sec
   under the defined validation scope.
 • Manual operational activities were reduced from 10 steps to 3 steps.
 • Deployment execution became independent of direct cluster access 
   and manual host operations.

[ Observed Benefits ]
 • Reduced operational overhead during application deployment.
 • Improved deployment traceability through Git-based workflows.
 • Centralized deployment permissions through Argo CD RBAC.
 • Consistent deployment process across multiple Kubernetes nodes.

[ Scope Limitation ]
 • Measurements were collected from a single homelab environment.
 • Multi-node scalability results are estimated projections,
   not directly measured observations.
 • Build time, image push time, and CI queue latency were excluded
   from deployment lifecycle measurements.
 • Disaster recovery capability was not validated in this report.

[ Conclusion ]
 • The evaluated GitOps workflow reduced manual deployment effort
   and improved deployment consistency within the defined validation scope.

 • Results indicate operational efficiency improvements compared
   with the manually executed deployment workflow, while providing
   additional governance capabilities that will be evaluated in
   the GitOps Deployment Governance validation report.
   
==================================================================================

```

<br><br><br>