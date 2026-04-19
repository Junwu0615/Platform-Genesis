# terraform/modules/generic_docker_container/main.tf


terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

resource "docker_container" "this" {
  for_each = var.app_configs # TODO 接收外部傳入變數清單
  # for_each = local.apps # 原先: 接收本地清單

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
  pid_mode      = each.value.pid_mode # TODO 若是 null 則自動忽略
  restart       = each.value.restart
  env           = each.value.envs
  security_opts = each.value.security_opts

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