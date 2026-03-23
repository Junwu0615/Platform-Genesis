FROM postgres:15

# 安裝 PoWA 及監控插件
RUN apt-get update && apt-get install -y \
    postgresql-15-powa \
    postgresql-15-pg-stat-kcache \
    postgresql-15-pg-qualstats \
    && rm -rf /var/lib/apt/lists/*

# 啟動 PostgreSQL 時 preload 所需 extension
CMD ["postgres", "-c", "shared_preload_libraries=pg_stat_statements,powa,pg_stat_kcache,pg_qualstats"]