### *A.　Event Description*
```
工廠情境：
  - 多台機台
  - 生產訂單
  - 機台狀態 ( 運轉 / 停機 / 故障 )
  - 生產產出 ( 良品 / 不良品 )
```

<br>

### *B.　Table Features*
- #### *OLTP*
|**Name**|**Type**|*Streaming*|**Description**|**Remark**|
|--:|:--:|:--:|:--:|:--:|
| machines | 靜態 | - | 儲存機台基本資訊 | 須預處理 |
| products | 靜態 | - | 儲存產品基本資訊 | 須預處理 |
| machine_events | 動態 | 中頻 | 記錄機台運行過程中的各類事件 | - |
| machine_status_logs | 動態 | 高頻 | 持續記錄機台狀態變化， | - |
| production_orders | 動態 | 低頻 | 記錄生產訂單資訊 | - |
| production_records | 動態 | 高頻 | 記錄實際生產結果 | - |

- #### *OLAP*
|**Name**|**Description**|**Remark**|
|--:|:--:|:--:|
| dim_machine | 機台維度表 | - |
| dim_product | 產品維度表 | - |
| dim_time | 時間維度表 | - |
| fact_machine_status | 機台狀態事實表 | - |
| fact_production | 生產事實表 | - |

<br>

### *C.　Simulation Data volume*
```
Products:            5
Machines:            20
Orders:              30
Status logs:         ~5000+
Production records:  500
Machine events:      100
```

<br>

### *D.　Benchmark*

<br>

### *E.　Metrics*

<br>