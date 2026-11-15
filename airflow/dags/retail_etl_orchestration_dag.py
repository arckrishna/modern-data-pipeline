"""
=============================================================================
Apache Airflow DAG: retail_modern_data_pipeline
Platform: RetailPulse AI
=============================================================================
Orchestrates an enterprise Modern Data Stack ETL pipeline:
1. Start Pipeline
2. Trigger Airbyte Ingestion (Source CSV/DB -> Target Data Warehouse Raw Layer)
3. Wait for Ingestion Sync Completion
4. Run dbt Staging Transformations (Cleaning & Type Standardization)
5. Test dbt Staging Models (Data Quality & Uniqueness Checks)
6. Run dbt Analytics Marts (Dimensional & Fact Tables)
7. Validate Data Warehouse Output (Sanity checks, row counts, non-empty tables)
8. Finish Pipeline

Task Dependencies:
start >> trigger_airbyte_ingestion >> wait_for_ingestion_sync >> run_dbt_staging
      >> test_dbt_staging >> run_dbt_analytics_marts >> validate_warehouse_output >> finish
=============================================================================
"""

from datetime import datetime, timedelta
import os
import sys
import subprocess

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Airflow imports with graceful fallback for standalone execution
try:
    from airflow import DAG
    from airflow.operators.empty import EmptyOperator
    from airflow.operators.python import PythonOperator
    AIRFLOW_INSTALLED = True
except ImportError:
    AIRFLOW_INSTALLED = False

# Configuration and Paths
DAG_ID = "retail_modern_data_pipeline"
SCHEDULE_INTERVAL = "@daily"
START_DATE = datetime(2024, 1, 1)

DEFAULT_ARGS = {
    "owner": "data_engineering_team",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

def task_trigger_ingestion(**context):
    """Task: Trigger data ingestion from source into the raw warehouse layer."""
    print("[Airflow Task: trigger_airbyte_ingestion] Initiating raw data ingestion...")
    script_path = os.path.join(PROJECT_ROOT, "ingestion", "load_raw_data.py")
    res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error output:\n{res.stderr}")
        raise RuntimeError(f"Data ingestion failed with exit code {res.returncode}")
    print(res.stdout)
    print("[Airflow Task: trigger_airbyte_ingestion] Ingestion completed successfully.")

def task_wait_for_ingestion(**context):
    """Task: Poll / confirm ingestion status."""
    print("[Airflow Task: wait_for_ingestion_sync] Verifying raw ingestion sync completion status...")
    import duckdb
    dw_path = os.path.join(PROJECT_ROOT, "warehouse", "retail_dw.duckdb")
    con = duckdb.connect(dw_path, read_only=True)
    cnt = con.execute("SELECT COUNT(*) FROM retail_raw.raw_retail_sales").fetchone()[0]
    con.close()
    if cnt == 0:
        raise RuntimeError("Ingestion validation failed: retail_raw.raw_retail_sales is empty!")
    print(f"[Airflow Task: wait_for_ingestion_sync] Raw sync confirmed: {cnt} records present. Status = SUCCESS.")

def task_run_dbt_staging(**context):
    """Task: Run dbt staging models."""
    print("[Airflow Task: run_dbt_staging] Executing dbt run --select staging...")
    from transformations.run_dbt_transformations import run_staging
    if not run_staging():
        raise RuntimeError("dbt staging execution failed!")

def task_test_dbt_staging(**context):
    """Task: Run dbt tests on staging models."""
    print("[Airflow Task: test_dbt_staging] Executing dbt test --select staging...")
    from transformations.run_dbt_transformations import test_staging
    if not test_staging():
        raise RuntimeError("dbt data quality tests failed!")

def task_run_dbt_marts(**context):
    """Task: Run dbt analytics marts."""
    print("[Airflow Task: run_dbt_analytics_marts] Executing dbt run --select marts...")
    from transformations.run_dbt_transformations import run_marts
    if not run_marts():
        raise RuntimeError("dbt marts transformation failed!")

def task_validate_warehouse(**context):
    """Task: Run final data sanity and consistency assertions on target warehouse."""
    import duckdb
    dw_path = os.path.join(PROJECT_ROOT, "warehouse", "retail_dw.duckdb")
    con = duckdb.connect(dw_path, read_only=True)
    
    products_count = con.execute("SELECT COUNT(*) FROM retail_analytics.dim_products_sales").fetchone()[0]
    regional_count = con.execute("SELECT COUNT(*) FROM retail_analytics.dim_regional_performance").fetchone()[0]
    monthly_count = con.execute("SELECT COUNT(*) FROM retail_analytics.fct_sales_monthly").fetchone()[0]
    total_rev = con.execute("SELECT SUM(total_revenue) FROM retail_analytics.dim_products_sales").fetchone()[0]
    
    con.close()
    
    print(f"[Validation Check] Products Mart Rows: {products_count}")
    print(f"[Validation Check] Regional Mart Rows: {regional_count}")
    print(f"[Validation Check] Monthly Mart Rows: {monthly_count}")
    print(f"[Validation Check] Total Warehouse Revenue: ${total_rev:,.2f}")
    
    assert products_count > 0, "Products mart is empty!"
    assert regional_count > 0, "Regional mart is empty!"
    assert monthly_count > 0, "Monthly fact mart is empty!"
    assert total_rev > 0, "Total calculated revenue is non-positive!"
    print("[Airflow Task: validate_warehouse_output] Target warehouse validation checks PASSED 100%.")

# Standard Airflow DAG Declaration
if AIRFLOW_INSTALLED:
    with DAG(
        dag_id=DAG_ID,
        default_args=DEFAULT_ARGS,
        description="End-to-End Modern Data Pipeline Orchestration - RetailPulse AI",
        schedule_interval=SCHEDULE_INTERVAL,
        start_date=START_DATE,
        catchup=False,
        tags=["retail", "airbyte", "dbt", "snowflake", "bigquery", "retailpulse"],
    ) as dag:

        start = EmptyOperator(task_id="start")
        
        trigger_airbyte = PythonOperator(
            task_id="trigger_airbyte_ingestion",
            python_callable=task_trigger_ingestion
        )
        
        wait_for_ingestion = PythonOperator(
            task_id="wait_for_ingestion_sync",
            python_callable=task_wait_for_ingestion
        )
        
        run_staging_model = PythonOperator(
            task_id="run_dbt_staging",
            python_callable=task_run_dbt_staging
        )
        
        test_staging_model = PythonOperator(
            task_id="test_dbt_staging",
            python_callable=task_test_dbt_staging
        )
        
        run_marts_model = PythonOperator(
            task_id="run_dbt_analytics_marts",
            python_callable=task_run_dbt_marts
        )
        
        validate_output = PythonOperator(
            task_id="validate_warehouse_output",
            python_callable=task_validate_warehouse
        )
        
        finish = EmptyOperator(task_id="finish")

        # Dependency chain
        start >> trigger_airbyte >> wait_for_ingestion >> run_staging_model >> test_staging_model >> run_marts_model >> validate_output >> finish
