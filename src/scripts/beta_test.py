"""
Update Date: 2026-03-24
"""
import logging, random, psycopg2
from datetime import datetime, timedelta


# ===============================
# DB Connection
# ===============================
conn = psycopg2.connect(
    host="localhost",
    database="pgdatabase",
    user="oltp_user",
    password="oltp_pwd"
)
cursor = conn.cursor()


# ===============================
# Config
# ===============================
NUM_PRODUCTS = 5
NUM_MACHINES = 20
NUM_ORDERS = 30
SIMULATION_HOURS = 24

STATUSES = ["RUNNING", "IDLE", "DOWN"]
EVENT_TYPES = ["ERROR", "MAINTENANCE", "ALARM"]


# ===============================
# Generate Products
# ===============================
def generate_products():
    for i in range(NUM_PRODUCTS):
        cursor.execute("""
            INSERT INTO oltp.products (product_name, product_type)
            VALUES (%s,%s)
        """, (
            f"Product-{i}",
            random.choice(["A","B","C"])
        ))
    conn.commit()
    logging.warning("products generated")


# ===============================
# Generate Machines
# ===============================
def generate_machines():
    for i in range(NUM_MACHINES):
        cursor.execute("""
            INSERT INTO oltp.machines (machine_name, machine_type, line_no)
            VALUES (%s,%s,%s)
        """, (
            f"Machine-{i}",
            random.choice(["CNC","DRILL","LATHE"]),
            f"L{random.randint(1,3)}"
        ))
    conn.commit()
    logging.warning("machines generated")


# ===============================
# Generate Orders
# ===============================
def generate_orders():
    for i in range(NUM_ORDERS):
        start_time = datetime.now() - timedelta(hours=random.randint(1,48))
        end_time = start_time + timedelta(hours=random.randint(1,5))

        cursor.execute("""
            INSERT INTO oltp.production_orders
            (product_id, planned_quantity, start_time, end_time)
            VALUES (%s,%s,%s,%s)
        """, (
            random.randint(1,NUM_PRODUCTS),
            random.randint(100,500),
            start_time,
            end_time
        ))
    conn.commit()
    logging.warning("orders generated")


# ===============================
# Generate Machine Status Logs
# ===============================
def generate_machine_status():
    start_time = datetime.now() - timedelta(hours=SIMULATION_HOURS)
    for machine_id in range(1, NUM_MACHINES + 1):
        current_time = start_time
        while current_time < datetime.now():
            status = random.choices(
                STATUSES,
                weights=[0.7,0.2,0.1]
            )[0]

            cursor.execute("""
                INSERT INTO oltp.machine_status_logs
                (machine_id, status, event_time)
                VALUES (%s,%s,%s)
            """, (
                machine_id,
                status,
                current_time
            ))
            current_time += timedelta(minutes=random.randint(1,5))

    conn.commit()
    logging.warning("machine status generated")


# ===============================
# Generate Production Records
# ===============================

def generate_production_records():
    for _ in range(500):
        event_time = datetime.now() - timedelta(
            minutes=random.randint(0,1440)
        )

        cursor.execute("""
            INSERT INTO oltp.production_records
            (order_id, machine_id, product_id, quantity, event_time)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            random.randint(1,NUM_ORDERS),
            random.randint(1,NUM_MACHINES),
            random.randint(1,NUM_PRODUCTS),
            random.randint(1,10),
            event_time
        ))
    conn.commit()
    logging.warning("production records generated")


# ===============================
# Generate Machine Events
# ===============================
def generate_machine_events():
    for _ in range(100):
        event_time = datetime.now() - timedelta(
            minutes=random.randint(0,1440)
        )

        cursor.execute("""
            INSERT INTO oltp.machine_events
            (machine_id, event_type, description, event_time)
            VALUES (%s,%s,%s,%s)
        """, (
            random.randint(1,NUM_MACHINES),
            random.choice(EVENT_TYPES),
            "auto generated event",
            event_time
        ))
    conn.commit()
    logging.warning("machine events generated")


def main():
    try:
        generate_products()
        generate_machines()
        generate_orders()
        generate_machine_status()
        generate_production_records()
        generate_machine_events()
        logging.warning("simulation completed")

    except Exception as e:
        logging.error("Exception", exc_info=True)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()