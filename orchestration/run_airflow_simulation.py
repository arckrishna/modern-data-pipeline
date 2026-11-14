"""
Standalone Airflow Orchestration Execution Runner
Executes the defined DAG tasks according to their dependency graph,
logs state transitions, and creates an execution summary.
"""
import os
import sys
import time
from datetime import datetime

# Add root directory to sys.path so modules can be imported directly
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from airflow.dags.retail_etl_orchestration_dag import (
    task_trigger_ingestion,
    task_wait_for_ingestion,
    task_run_dbt_staging,
    task_test_dbt_staging,
    task_run_dbt_marts,
    task_validate_warehouse
)

def execute_dag():
    print("=" * 70)
    print("APACHE AIRFLOW ORCHESTRATOR - DAG RUN: retail_modern_data_pipeline")
    print("=" * 70)
    run_id = f"manual__{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"
    print(f"Run ID: {run_id}")
    print(f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"DAG State: RUNNING")
    print("-" * 70)
    
    tasks = [
        ("start", lambda: print("[Airflow] Dummy start task triggered.")),
        ("trigger_airbyte_ingestion", task_trigger_ingestion),
        ("wait_for_ingestion_sync", task_wait_for_ingestion),
        ("run_dbt_staging", task_run_dbt_staging),
        ("test_dbt_staging", task_test_dbt_staging),
        ("run_dbt_analytics_marts", task_run_dbt_marts),
        ("validate_warehouse_output", task_validate_warehouse),
        ("finish", lambda: print("[Airflow] Pipeline execution completed successfully."))
    ]
    
    task_results = []
    dag_start = time.time()
    
    for idx, (task_name, task_fn) in enumerate(tasks, 1):
        print(f"\n[Task {idx}/{len(tasks)}] QUEUED -> RUNNING: {task_name}")
        t_start = time.time()
        try:
            task_fn()
            duration = round(time.time() - t_start, 2)
            print(f"[Task {idx}/{len(tasks)}] SUCCESS: {task_name} (Duration: {duration}s)")
            task_results.append((task_name, "SUCCESS", f"{duration}s"))
        except Exception as e:
            duration = round(time.time() - t_start, 2)
            print(f"[Task {idx}/{len(tasks)}] FAILED: {task_name} Error: {e}")
            task_results.append((task_name, "FAILED", f"{duration}s"))
            print(f"\nDAG Run FAILED at task '{task_name}'")
            return False
            
    total_duration = round(time.time() - dag_start, 2)
    print("\n" + "=" * 70)
    print("AIRFLOW DAG EXECUTION SUMMARY")
    print("=" * 70)
    print(f"{'Task Name':<32} | {'State':<10} | {'Duration'}")
    print("-" * 70)
    for t_name, state, dur in task_results:
        print(f"{t_name:<32} | {state:<10} | {dur}")
    print("-" * 70)
    print(f"Overall DAG Status: SUCCESS | Total Elapsed Time: {total_duration}s")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = execute_dag()
    if not success:
        sys.exit(1)
