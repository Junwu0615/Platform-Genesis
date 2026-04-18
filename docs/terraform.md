## *Terraform*

### *A.　安裝 Terraform*
```
sudo snap install terraform --classic

# return: terraform 1.14.8 from Snapcrafters✪ installed
# 確認安裝成功否: terraform -v
```

<br>

### *~~[ Some Problem ] B.　接管既有服務~~*
```
# 語法：terraform import <資源類型>.<資源名稱> <Docker容器ID或名稱>

docker ps --filter "name=ooud-cluster-prometheus-1" --format "{{.ID}}"
terraform import docker_container.prometheus 4468de5345db

terraform import docker_container.grafana ooud-cluster-grafana-1
```

<br>

### *C.　確認 Compose 產生的容器標籤，讓 Terraform 欺騙 Docker Compose 的管理機制！*
```
# sudo snap install jq
docker inspect ooud-cluster-dev-db-1 --format '{{json .Config.Labels}}' | jq
```