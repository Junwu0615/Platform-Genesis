ALL_PROJECT := \
    Junwu0615/Platform-Genesis \
    Junwu0615/PG-Infrastructure \
    Junwu0615/PG-APP-Core \
    Junwu0615/PG-Shared-Lib \
    Junwu0615/PG-Edge-Container \
    Junwu0615/PG-Airflow-DAGs \
    Junwu0615/PG-Core \
    Junwu0615/PG-Synapse \
    Junwu0615/PG-Cortex \
    Junwu0615/PG-Sentinel \
	Junwu0615/PG-Analytics \

FILTER_PROJECT := \
	Junwu0615/Platform-Genesis \

CLONE_PROJECT := $(filter-out $(FILTER_PROJECT), $(ALL_PROJECT))

.PHONY: clone pull assets-size

clone:
	@echo "🚀 正在克隆 Platform Genesis 全模組 ..."
	@for repo in $(CLONE_PROJECT); do \
	   repo_name=$$(basename $$repo); \
	   echo "📥 Cloning $$repo_name ..."; \
	   if [ ! -d "../$$repo_name" ]; then \
	      git clone https://github.com/$$repo ../$$repo_name; \
	      echo "   ✅  Success"; \
	   else \
	      echo "   ⏭️  Skipping ➔ $$repo_name 已存在"; \
	   fi \
	done
	@echo "✅  <make clone> done."

pull:
	@echo "🚀 正在更新 Platform Genesis 全模組 ..."
	@for repo in $(CLONE_PROJECT); do \
	   repo_name=$$(basename $$repo); \
	   target_dir="../$$repo_name"; \
	   if [ ! -d "$$target_dir" ]; then \
	      echo "  ⚠️  $$repo_name ➔ 未存在"; \
	   else \
	      echo "- $$repo_name ..."; \
	      echo "   🔄 Pulling"; \
	      (cd "$$target_dir" && git pull origin $$(git branch --show-current) --quiet) && \
	      echo "   ✅  Success"; \
	   fi \
	done
	@echo "✅  <make pull> done."

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