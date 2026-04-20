MAIN_NAME = ooud-cluster

COMPOSE_DIR = ./docker-compose.yaml
TERRAFORM_DIR = ./terraform
ANSIBLE_DIR = ./ansible
AIRFLOW_DIR = ./docker/airflow

ALL_COMPOSE := $(wildcard ./docker/*/docker-compose.yaml)

SUB_SERVICES = ./docker/airflow/docker-compose.yaml \
			   ./docker/monitoring/docker-compose.yaml \
			   ./docker/portainer/docker-compose.yaml \
			   ./docker/postgresql/docker-compose.yaml

BUILD_SERVICES =./docker/postgresql/docker-compose.yaml

AIRFLOW_CONTENT = airflow-webserver airflow-scheduler airflow-worker airflow-triggerer redis
MONITORING_CONTENT = grafana prometheus node_exporter postgres_exporter
POSTGRESQL_CONTENT = dev-db pgadmin
PORTAINER_CONTENT = portainer

.PHONY: build up down down-v ps rm \
fix-sock db-wait list-configs clear-force get-chown-all dev-mode prod-mode \
airflow monitoring portainer postgresql \
setup config infra all destroy graph

init:
	@echo "* 針對子服務進行必要性 init"
	@echo "1. 正在建立 Airflow 必要目錄 ..."
	mkdir -p $(AIRFLOW_DIR)/config $(AIRFLOW_DIR)/dags $(AIRFLOW_DIR)/logs $(AIRFLOW_DIR)/plugins
	@echo "2. 修正 Airflow 目錄權限, 讓目錄及其子目錄歸屬給 UID 50000 + 確保權限足夠 (rwxr-xr-x)"
	@make prod-mode
	@echo "3. 執行 Airflow 資料庫初始化 ..."
	docker compose -f $(COMPOSE_DIR) up airflow-init
	@echo "4. 環境預熱完成 ..."

build:
	@echo "* 針對子服務進行必要性 build (no-cache)..."
	docker compose -f $(BUILD_SERVICES) build --no-cache

up: fix-sock db-wait copy-dag
	@echo "* Notice | 指定單一服務指令 | ex: docker compose -f ./docker-compose.yaml up -d grafana"
	@echo "* Notice | 只針對 Airflow Webserver 更新設定 | ex: docker compose -f ./docker-compose.yaml up -d --no-deps airflow-webserver"
	docker compose -p $(MAIN_NAME) -f $(COMPOSE_DIR) up -d --no-recreate
	@echo "* 啟動完成 ..."

down:
	# 使用 -p 指定專案名稱，或者使用 -f 指定總控檔案
	docker compose -p $(MAIN_NAME) down --remove-orphans

down-v:
	# 使用 -p 指定專案名稱，或者使用 -f 指定總控檔案
	docker compose -p $(MAIN_NAME) down --remove-orphans -v

ps:
	# ! 不使用 | docker compose -p $(MAIN_NAME) ps | -p 指定專案名稱，或 -f 指定總控檔案
	@echo "* 正在搜尋名稱包含 $(MAIN_NAME) 的容器..."
	docker ps -a --filter "name=$(MAIN_NAME)"

fix-sock:
	sudo chmod 666 /var/run/docker.sock

db-wait:
	@echo "1. 正在啟動資料庫 ..."
	docker compose -f $(COMPOSE_DIR) up -d dev-db --no-recreate
	@echo "2. 等待資料庫就緒 ..."
	sleep 10

list-configs:
	@echo "偵測到的子服務設定檔如下："
	@echo "$(ALL_COMPOSE)" | tr ' ' '\n'

clear-force:
	@echo "清理 build cache + container + image + network + volume"
	docker compose -f $(COMPOSE_DIR) down -v --remove-orphans
	docker system prune -a --volumes -f

get-chown-all:
	@echo "回收所有專案權至 $$(whoami)..."
	sudo chown -R $$(whoami):$$(whoami) .

dev-mode:
	@echo "開發模式：IDE 編輯時把權限拿回來"
	sudo chown -R $$(whoami):$$(whoami) $(AIRFLOW_DIR)

prod-mode:
	@echo "運行模式：把權限交還給 Airflow"
	sudo chown -R 50000:0 $(AIRFLOW_DIR)
	sudo chmod -R 775 $(AIRFLOW_DIR)

copy-dag:
	@echo "將開發 DAGs 複製到 Airflow 容器中的 DAGs 對應資料夾 | 先刪除目錄下所有內容 | 執行複製"
	@make dev-mode
	sudo rm -rf $(AIRFLOW_DIR)/dags/*
	cp -ra ../src/scripts/dags $(AIRFLOW_DIR)
	@make prod-mode
	@echo "DAGs 同步完成並已校正權限 ..."

airflow: fix-sock copy-dag
	@echo "重新啟動 Airflow 相關服務"
	docker compose -f $(COMPOSE_DIR) down $(AIRFLOW_CONTENT)
	docker compose -f $(COMPOSE_DIR) up -d $(AIRFLOW_CONTENT)

monitoring: fix-sock
	@echo "重新啟動 Monitoring 相關服務"
	docker compose -f $(COMPOSE_DIR) down $(MONITORING_CONTENT)
	docker compose -f $(COMPOSE_DIR) up -d $(MONITORING_CONTENT)

postgresql: fix-sock
	@echo "重新啟動 Postgresql 相關服務"
	docker compose -f $(COMPOSE_DIR) down $(POSTGRESQL_CONTENT)
	docker compose -f $(COMPOSE_DIR) up -d $(POSTGRESQL_CONTENT)

portainer: fix-sock
	@echo "重新啟動 Portainer 相關服務"
	docker compose -f $(COMPOSE_DIR) down $(PORTAINER_CONTENT)
	docker compose -f $(COMPOSE_DIR) up -d $(PORTAINER_CONTENT)

refresh: fix-sock
	@echo "1. 檢查是否有定義 container 且不為空"
	@if [ -z "$(container)" ]; then \
		echo "Error: 必須指定服務名稱，ex: make refresh container=airflow-webserver"; \
		exit 1; \
	fi
	@echo "2. 更新單一服務 $(container) | 強制砍並重開 | 完全不動其他關聯服務"
	docker compose -f $(COMPOSE_DIR) up -d --force-recreate --no-deps $(container)

rm:
	@echo "* 正在檢查並清理指定的容器..."
	@echo "1. 檢查是否有定義 container 且不為空"
	@if [ -z "$(container)" ]; then \
		echo "Error: 必須指定服務名稱，ex: make rm container=airflow-webserver"; \
		exit 1; \
	fi
	@if [ $$(docker ps -a -q -f name=$(container)) ]; then \
		echo "2.1 偵測到容器，正在執行強制刪除..."; \
		docker rm -f $(container); \
	else \
		echo "2.2 容器不存在，跳過刪除動作"; \
	fi
	@echo "3. 當前集群狀態"
	@make ps

setup:
	@echo "* Initializing Infrastructure ..."
	cd $(TERRAFORM_DIR) && terraform init
	ansible-galaxy collection install community.docker

infra:
	@echo "* Terraform: Deploying Infrastructure ..."
	cd $(TERRAFORM_DIR) && terraform apply -auto-approve

config:
	@echo "* Ansible: Applying Configurations ..."
	cd $(ANSIBLE_DIR) && ansible-playbook -i inventory.ini playbook.yml

reload:
	@echo "* Ansible: Applying Configurations ..."
	cd $(ANSIBLE_DIR) && ansible-playbook -i inventory.ini playbook.yml --tags reload

all: infra config
	@echo "* 依賴 Terraform + Ansible 服務全部啟動 ..."

destroy:
	@echo "* Terraform: Destroy Infrastructure ..."
	cd $(TERRAFORM_DIR) && terraform destroy -auto-approve

graph:
	@echo "* 顯示 Terraform 如何理清模組間依賴關係 ..."
	cd $(TERRAFORM_DIR) && terraform graph