# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-03-24
    Description:
        - Supporting Contexts: OFF_PEAK, NORMAL, PEAK
"""
import os, time, yaml, random, psycopg2
from datetime import datetime, timedelta
from src.scripts.factory_load_model import get_load_profile
from src.models.log import Logger


logging = Logger(console_name='.main_console')
YAML_CONFIG_PATH = os.path.join('./src/scripts/factory_config.yaml')

with open(YAML_CONFIG_PATH) as f:
    config = yaml.safe_load(f)

db = config["database"]
simulation = config["simulation"]
load_cfg = config["load_profile"]

STATUSES = simulation["status_types"]
EVENT_TYPES = simulation["event_types"]

conn = psycopg2.connect(**db)
cursor = conn.cursor()

NUM_PRODUCTS = 8
NUM_MACHINES = 18
NUM_ORDERS = 30


def insert_machine_status():
    cursor.execute("""
    INSERT INTO oltp.machine_status_logs
    (machine_id, status, event_time)
    VALUES (%s,%s,%s)
    """,
    (
        random.randint(1, NUM_MACHINES),
        random.choice(STATUSES),
        datetime.now()
    ))


def insert_production_record():
    cursor.execute("""
    INSERT INTO oltp.production_records
    (order_id, machine_id, product_id, quantity, event_time)
    VALUES (%s,%s,%s,%s,%s)
    """,
    (
        random.randint(1, NUM_ORDERS),
        random.randint(1, NUM_MACHINES),
        random.randint(1, NUM_PRODUCTS),
        random.randint(1, 10),
        datetime.now()
    ))


def insert_machine_event():
    cursor.execute("""
    INSERT INTO oltp.machine_events
    (machine_id, event_type, description, event_time)
    VALUES (%s,%s,%s,%s)
    """,
    (
        random.randint(1, NUM_MACHINES),
        random.choice(EVENT_TYPES),
        "auto generated event",
        datetime.now()
    ))


def simulate():
    while True:
        now = datetime.now()
        load = get_load_profile(now.hour)
        load_setting = load_cfg[load]

        status_count = load_setting["status_per_sec"]
        prod_count = load_setting["production_per_sec"]
        event_count = load_setting["event_per_sec"]

        for _ in range(int(status_count)):
            insert_machine_status()

        for _ in range(int(prod_count)):
            insert_production_record()

        if random.random() < event_count:
            insert_machine_event()

        conn.commit()

        logging.info(
            f"{now} | load={load} | "
            f"status={status_count} "
            f"prod={prod_count}"
        )

        time.sleep(1)


def main():
    logging.warning("Starting factory stream simulation...")
    simulate()


if __name__ == "__main__":
    main()