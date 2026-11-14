"""
Airbyte API Ingestion Trigger Script
Triggers an Airbyte sync job via REST API or executes direct ingestion into the warehouse.
Used directly by Apache Airflow DAG task 'trigger_airbyte_ingestion'.
"""
import os
import sys
import time
import requests
import duckdb
import pandas as pd

AIRBYTE_URL = os.getenv("AIRBYTE_URL", "http://localhost:8000/api/v1")
AIRBYTE_CONNECTION_ID = os.getenv("AIRBYTE_CONNECTION_ID", "mock-connection-id-12345")
DUCKDB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "warehouse", "retail_dw.duckdb")
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "retail_sales_raw.csv")

def trigger_airbyte_api_sync():
    """Attempts to trigger an active Airbyte server connection."""
    print(f"[*] Contacting Airbyte API at: {AIRBYTE_URL}")
    print(f"[*] Connection ID: {AIRBYTE_CONNECTION_ID}")
    
    endpoint = f"{AIRBYTE_URL}/connections/sync"
    try:
        response = requests.post(
            endpoint,
            json={"connectionId": AIRBYTE_CONNECTION_ID},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        if response.status_code == 200:
            job_info = response.json()
            job_id = job_info.get("job", {}).get("id", "N/A")
            print(f"[+] Airbyte sync job successfully triggered! Job ID: {job_id}")
            return True
        else:
            print(f"[-] Airbyte API responded with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[-] Airbyte server not reachable ({e}). Falling back to direct warehouse loader.")
        return False

def load_data_to_warehouse():
    """Loads CSV directly into Raw layer of target warehouse (DuckDB/Snowflake/BigQuery)."""
    os.makedirs(os.path.dirname(DUCKDB_PATH), exist_ok=True)
    print(f"[*] Loading raw dataset into warehouse: {DUCKDB_PATH}")
    
    con = duckdb.connect(DUCKDB_PATH)
    con.execute("CREATE SCHEMA IF NOT EXISTS retail_raw;")
    
    # Ingest CSV into retail_raw.raw_retail_sales table
    con.execute(f"""
        CREATE OR REPLACE TABLE retail_raw.raw_retail_sales AS 
        SELECT 
            order_id,
            order_date,
            customer_id,
            product,
            category,
            region,
            quantity,
            unit_price,
            payment_status,
            CURRENT_TIMESTAMP AS _ingested_at
        FROM read_csv_auto('{CSV_PATH.replace(os.sep, "/")}');
    """)
    
    count = con.execute("SELECT COUNT(*) FROM retail_raw.raw_retail_sales;").fetchone()[0]
    con.close()
    
    print(f"[+] Ingestion completed successfully! Total rows in retail_raw.raw_retail_sales: {count}")
    return count

def run_ingestion():
    print("=" * 60)
    print("STEP 4: DATA INGESTION EXECUTION (Airbyte / Automated Sync)")
    print("=" * 60)
    
    success = trigger_airbyte_api_sync()
    if not success:
        print("[*] Executing automated ingestion pipeline...")
    
    count = load_data_to_warehouse()
    print("=" * 60)
    return count > 0

if __name__ == "__main__":
    if not run_ingestion():
        sys.exit(1)
