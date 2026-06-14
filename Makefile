ALL_PROJECT := \
    Junwu0615/Platform-Genesis \
    Junwu0615/PG-Infrastructure \
    Junwu0615/PG-APP-Core \
    Junwu0615/PG-Shared-Lib \
    Junwu0615/PG-Edge-Container \
    Junwu0615/PG-Airflow-DAGs \

FILTER_PROJECT := \
	Junwu0615/Platform-Genesis \

CLONE_PROJECT := $(filter-out $(FILTER_PROJECT), $(ALL_PROJECT))

.PHONY: clone assets-size

clone:
	@echo "* 將子專案克隆至上一層"
	@for repo in $(CLONE_PROJECT); do \
		repo_name=$$(basename $$repo); \
		if [ ! -d "../$$repo_name" ]; then \
			echo "Cloning $$repo_name ..."; \
			git clone https://github.com/$$repo ../$$repo_name; \
		else \
			echo "- $$repo_name 已存在，跳過 ..."; \
		fi \
	done
	@echo "✅  <make clone> done."

assets-size:
	@echo "* 計算總體資源佔用(MB)..."
	@total_kb=0; \
	for repo in $(ALL_PROJECT); do \
		size=$$(curl -s https://api.github.com/repos/$$repo | grep '"size":' | awk '{print $$2}' | tr -d ','); \
		if [ -n "$$size" ]; then \
			total_kb=$$(($$total_kb + $$size)); \
			echo "  - $$repo: $$(($$size / 1024)) MB ($$size KB)"; \
		fi \
	done; \
	echo "----------------------------------------"; \
	echo "⭐ 所有專案總計: $$(($$total_kb / 1024)) MB"
	@echo "✅  <make assets-size> done."