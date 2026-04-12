MAIN_NAME = oltp-olap-unified-db-cluster
MAIN_COMPOSE = ./docker/docker-compose.yaml

ALL_COMPOSE := $(wildcard ./docker/*/docker-compose.yaml)

SUB_SERVICES = ./docker/airflow/docker-compose.yaml \
			   ./docker/monitoring/docker-compose.yaml \
			   ./docker/portainer/docker-compose.yaml \
			   ./docker/postgresql/docker-compose.yaml

BUILD_SERVICES =./docker/postgresql/docker-compose.yaml

AIRFLOW_DIR = ./docker/airflow

.PHONY: build up down down-v ps fix-sock db-wait list-configs clear-force get-chown-all dev-mode prod-mode

init:
	@echo "* 針對子服務進行必要性 init"
	@echo "1. 正在建立 Airflow 必要目錄..."
	mkdir -p $(AIRFLOW_DIR)/config $(AIRFLOW_DIR)/dags $(AIRFLOW_DIR)/logs $(AIRFLOW_DIR)/plugins
	@echo "2. 修正 Airflow 目錄權限, 讓目錄及其子目錄歸屬給 UID 50000"
	sudo chown -R 50000:0 $(AIRFLOW_DIR)
	@echo "3. 確保權限足夠 (rwxr-xr-x)"
	sudo chmod -R 775 $(AIRFLOW_DIR)
	@echo "4. 執行 Airflow 資料庫初始化 (airflow-init)..."
	docker compose -f $(MAIN_COMPOSE) up airflow-init
	@echo "5. 環境預熱完成 ..."

build:
	@echo "* 針對子服務進行必要性 build (no-cache)..."
	docker compose -f $(BUILD_SERVICES) build --no-cache

up: fix-sock db-wait prod-mode
	@echo "* 正在啟動集群版服務..."
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
	@echo "1. 正在啟動資料庫..."
	docker compose -f $(MAIN_COMPOSE) up -d dev-db
	@echo "2. 等待資料庫就緒..."
	sleep 10
	@echo "3. Continue..."

list-configs:
	@echo "偵測到的子服務設定檔如下："
	@echo "$(ALL_COMPOSE)" | tr ' ' '\n'

clear-force:
	@echo "清理 container + image + network + volume"
	docker system prune -a --volumes

get-chown-all:
	@echo "正在回收專案所有權至 $$(whoami)..."
	sudo chown -R $$(whoami):$$(whoami) .

dev-mode:
	@echo "開發模式：IDE 編輯時把權限拿回來"
	sudo chown -R $$(whoami):$$(whoami) $(AIRFLOW_DIR)

prod-mode:
	@echo "運行模式：把權限交還給 Airflow (容器啟動用)"
	sudo chown -R 50000:0 $(AIRFLOW_DIR)

copy-dag: dev-mode
	@echo "將開發 DAGs 複製到 Airflow 容器中的 DAGs 對應資料夾"
	cp -ra src/scripts/dags $(AIRFLOW_DIR)
	sudo chown -R 50000:0 $(AIRFLOW_DIR)
	sudo chmod -R 775 $(AIRFLOW_DIR)
	@echo "DAGs 同步完成並已校正權限 !"