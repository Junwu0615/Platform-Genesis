# terraform/main.tf

terraform {
  # TODO 顯示表達給 Terraform 此模組必須搭配 docker provider 使用
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}
# TODO 僅在此處實例化，模組會自動繼承這個設定
provider "docker" {}


module "monitoring_services" {
  source       = "./modules/monitoring"
  main_name    = var.MAIN_NAME
  network_name = "${var.MAIN_NAME}_monitoring_default"
  service_path = var.SERVICE_PATH
  prometheus_config_path = "${abspath(path.root)}/${var.DOCKER_DIR}/monitoring/prometheus.yaml"
  prometheus_data_name   = "${var.MAIN_NAME}_prometheus_data"
  grafana_data_name      = "${var.MAIN_NAME}_grafana_data"
}

# module "portainer_services" {
#   source       = "./modules/portainer"
#   project_name = var.MAIN_NAME
#   network_name = "${var.MAIN_NAME}_portainer_default"
# }