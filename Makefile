MAIN_NAME = ooud-cluster

MAIN_COMPOSE = ./docker/docker-compose.yaml

ALL_COMPOSE := $(wildcard ./docker/*/docker-compose.yaml)

SUB_SERVICES = ./docker/airflow/docker-compose.yaml \
			   ./docker/monitoring/docker-compose.yaml \
			   ./docker/portainer/docker-compose.yaml \
			   ./docker/postgresql/docker-compose.yaml

BUILD_SERVICES =./docker/postgresql/docker-compose.yaml

MAIN_DIR = ./docker
AIRFLOW_DIR = ./docker/airflow

AIRFLOW_CONTENT = airflow-webserver airflow-scheduler airflow-worker airflow-triggerer redis
MONITORING_CONTENT = grafana prometheus node_exporter postgres_exporter
POSTGRESQL_CONTENT = dev-db pgadmin
PORTAINER_CONTENT = portainer

.PHONY: build up down down-v ps \
fix-sock db-wait list-configs clear-force get-chown-all dev-mode prod-mode \
airflow monitoring portainer postgresql

init:
	@echo "* 針對子服務進行必要性 init"
	@echo "1. 正在建立 Airflow 必要目錄 ..."
	mkdir -p $(AIRFLOW_DIR)/config $(AIRFLOW_DIR)/dags $(AIRFLOW_DIR)/logs $(AIRFLOW_DIR)/plugins
	@echo "2. 修正 Airflow 目錄權限, 讓目錄及其子目錄歸屬給 UID 50000 + 確保權限足夠 (rwxr-xr-x)"
	make prod-mode
	@echo "3. 執行 Airflow 資料庫初始化 ..."
	docker compose -f $(MAIN_COMPOSE) up airflow-init
	@echo "4. 環境預熱完成 ..."

build:
	@echo "* 針對子服務進行必要性 build (no-cache)..."
	docker compose -f $(BUILD_SERVICES) build --no-cache

up: fix-sock db-wait copy-dag
	@echo "* Notice | 指定單一服務指令 | ex: docker compose -f ./docker/docker-compose.yaml up -d grafana"
	@echo "* Notice | 只針對 Airflow Webserver 更新設定 | ex: docker compose -f ./docker/docker-compose.yaml up -d --no-deps airflow-webserver"
	@echo "* 正在一次性啟動集群服務 ..."
	docker compose -f $(MAIN_COMPOSE) up -d
	@echo "* 啟動完成 ..."

down:
	# 使用 -p 指定專案名稱，或者使用 -f 指定總控檔案
	docker compose -p $(MAIN_NAME) down

down-v:
	# 使用 -p 指定專案名稱，或者使用 -f 指定總控檔案
	docker compose -p $(MAIN_NAME) down --remove-orphans

ps:
	# 使用 -p 指定專案名稱，或者使用 -f 指定總控檔案
	docker compose -p $(MAIN_NAME) ps

fix-sock:
	sudo chmod 666 /var/run/docker.sock

db-wait:
	@echo "1. 正在啟動資料庫 ..."
	docker compose -f $(MAIN_COMPOSE) up -d dev-db
	@echo "2. 等待資料庫就緒 ..."
	sleep 10

list-configs:
	@echo "偵測到的子服務設定檔如下："
	@echo "$(ALL_COMPOSE)" | tr ' ' '\n'

clear-force:
	@echo "清理 build cache + container + image + network + volume"
	docker compose -f $(MAIN_COMPOSE) down -v --remove-orphans
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
	make dev-mode
	sudo rm -rf $(AIRFLOW_DIR)/dags/*
	cp -ra src/scripts/dags $(AIRFLOW_DIR)
	make prod-mode
	@echo "DAGs 同步完成並已校正權限 ..."

airflow: fix-sock copy-dag
	@echo "重新啟動 Airflow 相關服務"
	docker compose -f $(MAIN_COMPOSE) down $(AIRFLOW_CONTENT)
	docker compose -f $(MAIN_COMPOSE) up -d $(AIRFLOW_CONTENT)

monitoring: fix-sock
	@echo "重新啟動 Monitoring 相關服務"
	docker compose -f $(MAIN_COMPOSE) down $(MONITORING_CONTENT)
	docker compose -f $(MAIN_COMPOSE) up -d $(MONITORING_CONTENT)

postgresql: fix-sock
	@echo "重新啟動 Postgresql 相關服務"
	docker compose -f $(MAIN_COMPOSE) down $(POSTGRESQL_CONTENT)
	docker compose -f $(MAIN_COMPOSE) up -d $(POSTGRESQL_CONTENT)

portainer: fix-sock
	@echo "重新啟動 Portainer 相關服務"
	docker compose -f $(MAIN_COMPOSE) down $(PORTAINER_CONTENT)
	docker compose -f $(MAIN_COMPOSE) up -d $(PORTAINER_CONTENT)

refresh: fix-sock
	@echo "1. 檢查是否有定義 container 且不為空"
	@if [ -z "$(container)" ]; then \
		echo "Error: 必須指定服務名稱，ex: make refresh container=airflow-webserver"; \
		exit 1; \
	fi
	@echo "2. 更新單一服務 $(container) | 強制砍並重開 | 完全不動其他關聯服務"
	docker compose -f $(MAIN_COMPOSE) up -d --force-recreate --no-deps $(container)