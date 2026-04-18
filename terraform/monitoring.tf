# terraform/monitoring.tf

terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

data "docker_network" "monitoring_network" {
  name = "ooud-cluster_monitoring_default" # 引用原本 Compose 建立的網路 (不自己創)
}

resource "docker_container" "prometheus" {
  name  = "ooud-cluster-prometheus-1"
  image = "prom/prometheus:latest"
  restart = "unless-stopped"
  networks_advanced {
    aliases = ["prometheus"] # 關鍵：增加藝名卡，使網域內可用別名被找到
    name = data.docker_network.monitoring_network.name # 回歸原先集群
  }
  ports {
    internal = 9090
    external = 9090
  }
  volumes {
    host_path      = "${abspath(path.root)}/../docker/monitoring/prometheus.yaml"
    container_path = "/etc/prometheus/prometheus.yml"
  }
  volumes {
    volume_name    = "ooud-cluster_prometheus_data"
    container_path = "/prometheus"
  }

  # [失敗] 補上 Compose 的標籤，讓它出現在 make ps 的清單中
  labels {
    label = "com.docker.compose.project"
    value = "ooud-cluster"
  }
  labels {
    label = "com.docker.compose.service"
    value = "prometheus"
  }
}

resource "docker_container" "grafana" {
  name  = "ooud-cluster-grafana-1"
  image = "grafana/grafana:latest"
  restart = "unless-stopped"
  networks_advanced {
    aliases = ["grafana"]
    name = data.docker_network.monitoring_network.name
  }
  ports {
    internal = 3000
    external = 3000
  }
  env = [
    "GF_SECURITY_ADMIN_PASSWORD=admin"
  ]
  volumes {
    volume_name    = "ooud-cluster_grafana_data"
    container_path = "/var/lib/grafana"
  }

  labels {
    label = "com.docker.compose.project"
    value = "ooud-cluster"
  }
  labels {
    label = "com.docker.compose.service"
    value = "grafana"
  }
}

resource "docker_container" "postgres_exporter" {
  name  = "ooud-cluster-postgres_exporter-1"
  image = "prometheuscommunity/postgres-exporter:latest"
  restart = "unless-stopped"
  networks_advanced {
    aliases = ["postgres_exporter"]
    name = data.docker_network.monitoring_network.name
  }
  ports {
    internal = 9187
    external = 9187
  }
  env = [
    "DATA_SOURCE_NAME=postgresql://postgres_exporter:exporter@host.docker.internal:5432/postgres?sslmode=disable"
  ]
  command = [
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
  host {
    host = "host.docker.internal"
    ip   = "172.19.0.1" # 欲監控 postgres 的主閘道位置
  }
  labels {
    label = "com.docker.compose.project"
    value = "ooud-cluster"
  }
  labels {
    label = "com.docker.compose.service"
    value = "postgres_exporter"
  }
}

resource "docker_container" "node_exporter" {
  name  = "ooud-cluster-node_exporter-1"
  image = "prom/node-exporter:latest"
  restart = "unless-stopped"
  networks_advanced {
    name    = data.docker_network.monitoring_network.name
    aliases = ["node_exporter"]
  }
  ports {
    internal = 9100
    external = 9100
  }

  pid_mode = "host" # 關鍵：對應 pid: host，讓容器能看到宿主機的 Process

  # 掛載宿主機系統檔案來讀取硬體指標
  volumes {
    host_path      = "/proc"
    container_path = "/host/proc"
    read_only      = true
  }
  volumes {
    host_path      = "/sys"
    container_path = "/host/sys"
    read_only      = true
  }
  volumes {
    host_path      = "/"
    container_path = "/rootfs"
    read_only      = true
  }

  # 啟動參數：注意 $ 符號在 Terraform 模板中需要雙寫 $$ 來進行轉義
  command = [
    "--path.procfs=/host/proc",
    "--path.sysfs=/host/sys",
    "--path.rootfs=/rootfs",
    # 避免 pseudo filesystem
    "--collector.filesystem.fs-types-exclude=^(autofs|binfmt_misc|bpf|cgroup2?|configfs|debugfs|devpts|devtmpfs|fusectl|hugetlbfs|mqueue|overlay|proc|pstore|rpc_pipefs|securityfs|sysfs|tracefs)$$",
    # 避免抓 container mount + C、D、E drive mount ( Node Exporter 掃描這些路徑會極度緩慢且容易報錯 )
    "--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc|mnt/c|mnt/d|mnt/e)($$|/)"
  ]

  labels {
    label = "com.docker.compose.project"
    value = "ooud-cluster"
  }
  labels {
    label = "com.docker.compose.service"
    value = "node_exporter"
  }
}