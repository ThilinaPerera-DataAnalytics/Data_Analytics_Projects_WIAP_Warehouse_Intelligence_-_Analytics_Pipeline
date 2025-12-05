import os
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# ----------------------------
# CONFIG
# ----------------------------
CSV_DIR = "../data_generator/"
DB_URL = "postgresql://postgres:password@localhost:5432/warehouse_db"

LOG_FILE = "loader.log"

engine = create_engine(DB_URL)


# ----------------------------
# LOGGING
# ----------------------------
def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)


# ----------------------------
# GENERIC LOAD FUNCTION
# ----------------------------
def load_table(csv_name, table_name, conflict_key):
    csv_path = os.path.join(CSV_DIR, csv_name)

    if not os.path.exists(csv_path):
        log(f"❌ CSV not found: {csv_name}")
        return

    df = pd.read_csv(csv_path)

    if df.empty:
        log(f"⚠️ Skipped {table_name} — CSV is empty.")
        return

    log(f"➡️ Loading {table_name} ({len(df)} rows)")

    cols = list(df.columns)
    insert_cols = ", ".join(cols)
    values_cols = ", ".join([f":{c}" for c in cols])
    update_cols = ", ".join([f"{c} = EXCLUDED.{c}" for c in cols if c != conflict_key])

    query = text(f"""
        INSERT INTO {table_name} ({insert_cols})
        VALUES ({values_cols})
        ON CONFLICT ({conflict_key})
        DO UPDATE SET {update_cols};
    """)

    try:
        with engine.begin() as conn:
            conn.execute(query, df.to_dict(orient="records"))
        log(f"✅ Loaded: {table_name}")
    except Exception as e:
        log(f"❌ FAILED loading {table_name}: {e}")


# ----------------------------
# LOAD ORDER (FK-SAFE)
# ----------------------------
LOAD_SEQUENCE = [
    ("vehicle_details.csv", "vehicle_details", "vehicle_no"),
    ("supplier_details.csv", "supplier_details", "supplier_id"),
    ("customer_details.csv", "customer_details", "customer_id"),
    ("employee_details.csv", "employee_details", "employee_id"),
    ("product_details.csv", "product_details", "product_id"),

    ("inbound_log.csv", "inbound_log", "inbound_id"),
    ("outbound_log.csv", "outbound_log", "outbound_id"),
    ("return_handling_log.csv", "return_handling_log", "return_id"),

    ("vehicle_ncr_log.csv", "vehicle_ncr_log", "ncr_id"),
    ("vehicle_hygiene_log.csv", "vehicle_hygiene_log", "hygiene_id"),
    ("inbound_inspection_log.csv", "inbound_inspection_log", "inspection_id"),
    ("complaint_handling_log.csv", "complaint_handling_log", "complaint_id"),

    ("cycle_count_log.csv", "cycle_count_log", "cycle_id"),
    ("product_disposal_log.csv", "product_disposal_log", "disposal_id"),
    ("warehouse_incident_reporting_log.csv", "warehouse_incident_reporting_log", "incident_id"),
]


# ----------------------------
# MAIN EXECUTION
# ----------------------------
def main():
    log("-------------------------------------------------")
    log("🚀 DATA LOAD STARTED")

    for csv_name, table_name, key in LOAD_SEQUENCE:
        load_table(csv_name, table_name, key)

    log("🎉 DATA LOAD COMPLETED SUCCESSFULLY")
    log("-------------------------------------------------")


if __name__ == "__main__":
    main()
