# terraform/outputs.tf

output "monitoring_summary" {
  value = {
    container_ids               = module.monitoring_services.container_ids
    container_names             = module.monitoring_services.container_names
    network_used                = module.monitoring_services.network_used
    url_path_grafana            = module.monitoring_services.url_path_grafana
    url_path_prometheus         = module.monitoring_services.url_path_prometheus
    url_path_postgres_exporter  = module.monitoring_services.url_path_postgres_exporter
    url_path_node_exporter      = module.monitoring_services.url_path_node_exporter
    all_service_urls            = module.monitoring_services.all_service_urls
  }
}