"""
=============================================================================
MASTER PIPELINE RUNNER & DEMONSTRATION SUITE
DATA ENGINEERING MICROPROJECT
=============================================================================
Executes the full automated modern data pipeline from end to end:
1. Generate and inspect source dataset
2. Ingest raw records into the warehouse (Airbyte simulation)
3. Run dbt staging transformations and data quality tests
4. Build dbt analytical marts (product, regional, monthly)
5. Orchestrate tasks via Airflow DAG dependency graph
6. Execute Conversational BI business queries (answering Q1, Q2, Q3)
=============================================================================
"""
import os
import sys
import duckdb
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from scripts.inspect_data import inspect_dataset
from ingestion.load_raw_data import run_ingestion
from transformations.run_dbt_transformations import run_all_transformations
from orchestration.run_airflow_simulation import execute_dag

def demonstrate_bi_queries():
    print("\n" + "=" * 70)
    print("CONVERSATIONAL BI QUERY DEMONSTRATION (STEP 7 & 8)")
    print("=" * 70)
    
    dw_path = os.path.join(PROJECT_ROOT, "warehouse", "retail_dw.duckdb")
    con = duckdb.connect(dw_path, read_only=True)
    
    # -------------------------------------------------------------
    # Question 1
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print("BUSINESS QUESTION 1: Which product has the highest revenue?")
    print("-" * 70)
    sql_q1 = """
    SELECT 
        product_name,
        category,
        total_revenue,
        total_units_sold,
        total_orders,
        revenue_rank
    FROM retail_analytics.dim_products_sales
    ORDER BY total_revenue DESC
    LIMIT 3;
    """
    print(f"Generated SQL:\n{sql_q1.strip()}\n")
    df1 = con.execute(sql_q1).df()
    print("Query Result (Top 3 Products):")
    print(df1.to_string(index=False))
    print(f"\n>> INSIGHT: '{df1.iloc[0]['product_name']}' generated the highest revenue at ${df1.iloc[0]['total_revenue']:,.2f}.")

    # -------------------------------------------------------------
    # Question 2
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print("BUSINESS QUESTION 2: Which region records the highest sales?")
    print("-" * 70)
    sql_q2 = """
    SELECT 
        region,
        total_revenue,
        total_orders,
        unique_customers,
        avg_order_value,
        completion_rate_pct,
        regional_rank
    FROM retail_analytics.dim_regional_performance
    ORDER BY total_revenue DESC;
    """
    print(f"Generated SQL:\n{sql_q2.strip()}\n")
    df2 = con.execute(sql_q2).df()
    print("Query Result (All Regions):")
    print(df2.to_string(index=False))
    print(f"\n>> INSIGHT: '{df2.iloc[0]['region']}' recorded the highest sales at ${df2.iloc[0]['total_revenue']:,.2f} ({df2.iloc[0]['total_orders']} orders).")

    # -------------------------------------------------------------
    # Question 3
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print("BUSINESS QUESTION 3: How does revenue change month by month?")
    print("-" * 70)
    sql_q3 = """
    SELECT 
        sales_month,
        total_revenue,
        total_orders,
        total_units_sold,
        mom_revenue_growth
    FROM retail_analytics.fct_sales_monthly
    ORDER BY sales_month ASC;
    """
    print(f"Generated SQL:\n{sql_q3.strip()}\n")
    df3 = con.execute(sql_q3).df()
    print("Query Result (Monthly Breakdown):")
    print(df3.to_string(index=False))
    max_idx = df3["total_revenue"].idxmax()
    print(f"\n>> INSIGHT: Revenue peaked in {df3.loc[max_idx, 'sales_month']} at ${df3.loc[max_idx, 'total_revenue']:,.2f}.")
    print("=" * 70)
    con.close()

def main():
    print("=" * 70)
    print("STARTING COMPLETE END-TO-END MODERN DATA PIPELINE DEMONSTRATION")
    print("=" * 70)
    
    # Step 2: Inspect Source Data
    inspect_dataset()
    
    # Step 6: Run Orchestrated DAG (which executes Step 4 Ingestion & Step 5 dbt Transformations)
    success = execute_dag()
    if not success:
        print("[!] Orchestration pipeline execution failed.")
        sys.exit(1)
        
    # Step 7 & 8: Demonstrate Conversational BI Insights
    demonstrate_bi_queries()
    
    print("\n" + "=" * 70)
    print("ALL PIPELINE STAGES, QUALITY TESTS, AND BI DEMONSTRATIONS COMPLETED!")
    print("To launch the Streamlit Conversational BI interface:")
    print("    python -m streamlit run bi_app/app.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
