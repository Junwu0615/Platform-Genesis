# terraform/modules/monitoring/main.tf

terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

locals {
  apps = {
    "prometheus" = {
      image    = "prom/prometheus:latest"
      ports    = [{ internal = 9090, external = 9090 }]
      restart  = "unless-stopped"
      pid_mode = null
      envs     = null
      command  = null
      host     = [] # TODO 補齊以維持結構一致
      volumes  = [
        { host = var.prometheus_config_path, container = "/etc/prometheus/prometheus.yml", ro = false },
        { volume_name = var.prometheus_data_name, container = "/prometheus", ro = false }
      ]
    },
    "grafana" = {
      image    = "grafana/grafana:latest"
      ports    = [{ internal = 3000, external = 3000 }]
      restart  = "unless-stopped"
      pid_mode = null
      envs     = [
        "GF_SECURITY_ADMIN_PASSWORD=admin",
      ]
      command  = null
      host     = []
      volumes  = [
        { volume_name = var.grafana_data_name, container = "/var/lib/grafana", ro = false },
      ]
    },
    "postgres_exporter" = {
      image    = "prometheuscommunity/postgres-exporter:latest"
      ports    = [{ internal = 9187, external = 9187 }]
      restart  = "unless-stopped"
      pid_mode = null
      envs     = [
        "DATA_SOURCE_NAME=postgresql://postgres_exporter:exporter@host.docker.internal:5432/postgres?sslmode=disable"
      ]
      command  = [
        "--collector.stat_bgwriter", # TPS / IO / tuples
        "--collector.stat_database", # checkpoint / write
        "--collector.stat_user_tables", # table activity
        "--collector.wal", # WAL throughput
        "--collector.locks", # lock contention 貌似預設即開
        "--collector.database", # DB size
        "--auto-discover-databases", # 自動抓所有 database 的 metrics
        "--collector.postmaster", # Table size / index size
        # "--collector.replication", # Replication status 若未來做 HTAP replica
      ]
      host     = [
        { host = "host.docker.internal", ip = "172.19.0.1" },
      ]
      volumes = []
    },
    "node_exporter" = {
      image    = "prom/node-exporter:latest"
      ports    = [{ internal = 9100, external = 9100 }]
      restart  = "unless-stopped"
      pid_mode = "host" # TODO 特例：需要主機 PID 模式
      envs     = null
      command  = [
        "--path.procfs=/host/proc",
        "--path.sysfs=/host/sys",
        "--path.rootfs=/rootfs",
        # 避免 pseudo filesystem
        "--collector.filesystem.fs-types-exclude=^(autofs|binfmt_misc|bpf|cgroup2?|configfs|debugfs|devpts|devtmpfs|fusectl|hugetlbfs|mqueue|overlay|proc|pstore|rpc_pipefs|securityfs|sysfs|tracefs)$$",
        # 避免抓 container mount + C、D、E drive mount ( Node Exporter 掃描這些路徑會極度緩慢且容易報錯 )
        "--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc|mnt/c|mnt/d|mnt/e)($$|/)"
      ]
      host     = []
      volumes  = [
        { host = "/proc", container = "/host/proc", ro = true },
        { host = "/sys", container = "/host/sys", ro = true },
        { host = "/", container = "/rootfs", ro = true }
      ]
    }
  }
}

resource "docker_container" "apps" {
  for_each = local.apps

  # TODO 基礎設置
  name     = "${var.main_name}-${each.key}-1"
  image    = each.value.image

  # TODO 針對性處理共性與非共性的
  dynamic "volumes" {
    for_each = each.value.volumes
    content {
      host_path      = lookup(volumes.value, "host", null)
      volume_name    = lookup(volumes.value, "volume_name", null)
      container_path = volumes.value.container
      read_only      = volumes.value.ro
    }
  }
  dynamic "host" {
    for_each = each.value.host
    content {
      host  = lookup(host.value, "host", null)
      ip    = lookup(host.value, "ip", null) # 欲監控目標的主閘道
    }
  }
  dynamic "ports" {
    for_each = each.value.ports
    content {
      internal  = lookup(ports.value, "internal", null)
      external  = lookup(ports.value, "external", null)
    }
  }

  # TODO 其餘共性標籤 ( 含 ports, lifecycle ... )
  pid_mode = each.value.pid_mode # TODO 若是 null 則自動忽略
  restart  = each.value.restart
  env      = each.value.envs

  labels {
    label = "com.docker.compose.project"
    value = var.main_name
  }
  labels {
    label = "com.docker.compose.service"
    value = each.key
  }
  networks_advanced {
    aliases = [each.key] # TODO 增加藝名卡，使網域內可用別名被找到
    name = var.network_name
  }
  lifecycle {
    ignore_changes = [
      image,         # 忽略 sha256 與 latest 的字串差異
      network_mode,  # 忽略 Docker 自動補上的 bridge 模式
      user,          # 忽略映像檔內建的 user ID
      working_dir,   # 忽略映像檔內建的工作目錄
      command,       # 忽略啟動指令的格式微差
      entrypoint,    # 忽略入口點的微差
    ]
  }
}