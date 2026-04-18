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

resource "docker_network" "monitoring" {
  name = "monitoring_default"
}

# Prometheus 容器
resource "docker_container" "prometheus" {
  name  = "ooud-cluster-prometheus-1"
  image = "prom/prometheus:latest"
  restart = "unless-stopped"
  networks_advanced { name = docker_network.monitoring.name }
  ports {
    internal = 9090
    external = 9090
  }
  # 掛載點：指向你本機的資料夾，Ansible 會在那裡產生檔案
  volumes {
    host_path      = "${abspath(path.root)}/../docker/monitoring/prometheus.yaml"
    container_path = "/etc/prometheus/prometheus.yml"
  }
}

# Grafana 容器
resource "docker_container" "grafana" {
  name  = "ooud-cluster-grafana-1"
  image = "grafana/grafana:latest"
  restart = "unless-stopped"
  networks_advanced { name = docker_network.monitoring.name }
  ports {
    internal = 3000
    external = 3000
  }
  env = ["GF_SECURITY_ADMIN_PASSWORD=admin"]
}