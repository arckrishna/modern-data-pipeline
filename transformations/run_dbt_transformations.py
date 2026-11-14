"""
dbt Transformation Execution Engine
Compiles, executes, and tests dbt models against the target warehouse.
Can be executed standalone or orchestrated via Apache Airflow.
"""
import os
import sys
import time
import duckdb

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DUCKDB_PATH = os.path.join(PROJECT_ROOT, "warehouse", "retail_dw.duckdb")
MODELS_DIR = os.path.join(PROJECT_ROOT, "dbt_retail_pipeline", "models")

def get_connection():
    return duckdb.connect(DUCKDB_PATH)

def run_staging():
    print("\n" + "=" * 65)
    print("DBT RUN: EXECUTING STAGING MODELS")
    print("=" * 65)
    start_time = time.time()
    
    con = get_connection()
    con.execute("CREATE SCHEMA IF NOT EXISTS retail_staging;")
    
    staging_sql_path = os.path.join(MODELS_DIR, "staging", "stg_retail_sales.sql")
    with open(staging_sql_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
    
    ddl = f"CREATE OR REPLACE VIEW retail_staging.stg_retail_sales AS\n{sql_content}"
    con.execute(ddl)
    
    row_count = con.execute("SELECT COUNT(*) FROM retail_staging.stg_retail_sales;").fetchone()[0]
    elapsed = round(time.time() - start_time, 2)
    print(f"[OK] 1 of 1 START view model retail_staging.stg_retail_sales")
    print(f"[OK] 1 of 1 OK created view model retail_staging.stg_retail_sales [OK in {elapsed}s | Rows: {row_count}]")
    con.close()
    return True

def test_staging():
    print("\n" + "=" * 65)
    print("DBT TEST: EXECUTING STAGING QUALITY TESTS")
    print("=" * 65)
    con = get_connection()
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Unique order_id
    dups = con.execute("""
        SELECT order_id, COUNT(*) 
        FROM retail_staging.stg_retail_sales 
        GROUP BY order_id 
        HAVING COUNT(*) > 1;
    """).fetchall()
    if len(dups) == 0:
        print("[PASS] test unique_stg_retail_sales_order_id .................. [PASS]")
        tests_passed += 1
    else:
        print(f"[FAIL] test unique_stg_retail_sales_order_id: Found {len(dups)} duplicates")

    # Test 2: Not null order_id and revenue
    nulls = con.execute("""
        SELECT COUNT(*) 
        FROM retail_staging.stg_retail_sales 
        WHERE order_id IS NULL OR revenue IS NULL OR order_date IS NULL;
    """).fetchone()[0]
    if nulls == 0:
        print("[PASS] test not_null_stg_retail_sales_essential_fields ........ [PASS]")
        tests_passed += 1
    else:
        print(f"[FAIL] test not_null_stg_retail_sales: Found {nulls} null records")

    # Test 3: Accepted values for payment_status
    invalid_status = con.execute("""
        SELECT COUNT(*) 
        FROM retail_staging.stg_retail_sales 
        WHERE payment_status NOT IN ('Completed', 'Pending', 'Refunded');
    """).fetchone()[0]
    if invalid_status == 0:
        print("[PASS] test accepted_values_stg_retail_sales_payment_status ... [PASS]")
        tests_passed += 1
    else:
        print(f"[FAIL] test accepted_values: Found {invalid_status} unexpected statuses")

    con.close()
    print(f"\nResult: {tests_passed}/{total_tests} dbt tests passed successfully.")
    return tests_passed == total_tests

def run_marts():
    print("\n" + "=" * 65)
    print("DBT RUN: EXECUTING ANALYTICS MARTS")
    print("=" * 65)
    con = get_connection()
    con.execute("CREATE SCHEMA IF NOT EXISTS retail_analytics;")
    
    mart_files = [
        ("dim_products_sales", os.path.join(MODELS_DIR, "marts", "dim_products_sales.sql")),
        ("dim_regional_performance", os.path.join(MODELS_DIR, "marts", "dim_regional_performance.sql")),
        ("fct_sales_monthly", os.path.join(MODELS_DIR, "marts", "fct_sales_monthly.sql"))
    ]
    
    for idx, (table_name, filepath) in enumerate(mart_files, 1):
        start_t = time.time()
        with open(filepath, "r", encoding="utf-8") as f:
            query = f.read()
        ddl = f"CREATE OR REPLACE TABLE retail_analytics.{table_name} AS\n{query}"
        con.execute(ddl)
        rows = con.execute(f"SELECT COUNT(*) FROM retail_analytics.{table_name};").fetchone()[0]
        elapsed = round(time.time() - start_t, 2)
        print(f"[OK] {idx} of {len(mart_files)} START table model retail_analytics.{table_name}")
        print(f"[OK] {idx} of {len(mart_files)} OK created table model retail_analytics.{table_name} [OK in {elapsed}s | Rows: {rows}]")
    
    con.close()
    return True

def run_all_transformations():
    print("=" * 65)
    print("STEP 5: DATA TRANSFORMATION PIPELINE (dbt)")
    print("=" * 65)
    
    if not run_staging():
        return False
    if not test_staging():
        return False
    if not run_marts():
        return False
        
    print("\n" + "=" * 65)
    print("[+] ALL DBT MODELS AND TESTS EXECUTED SUCCESSFULLY")
    print("=" * 65)
    return True

if __name__ == "__main__":
    success = run_all_transformations()
    if not success:
        sys.exit(1)
