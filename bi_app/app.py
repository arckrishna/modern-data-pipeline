"""
=============================================================================
Conversational BI Interface (Streamlit)
Step 7 of Data Engineering Microproject
Allows stakeholders to ask natural language business questions against
the modern data warehouse (retail_analytics dimensional & fact models).
=============================================================================
"""
import os
import re
import duckdb
import pandas as pd
import streamlit as st

# Configure page
st.set_page_config(
    page_title="Retail Insights - Conversational BI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WAREHOUSE_PATH = os.path.join(PROJECT_ROOT, "warehouse", "retail_dw.duckdb")

def get_warehouse_connection():
    return duckdb.connect(WAREHOUSE_PATH, read_only=True)

def execute_query(sql: str):
    """Executes a sanitized SELECT query on the target warehouse."""
    # Security safeguard
    forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
    for kw in forbidden_keywords:
        if re.search(r'\b' + kw + r'\b', sql, re.IGNORECASE):
            raise ValueError(f"Execution blocked: query contains forbidden keyword '{kw}'. Only SELECT queries are permitted.")
    
    con = get_warehouse_connection()
    try:
        df = con.execute(sql).df()
    finally:
        con.close()
    return df

def nl_to_sql_intent(prompt: str):
    """
    Translates Natural Language queries into verified SQL queries
    targeting the dbt transformed marts in retail_analytics.
    """
    p = prompt.lower().strip()
    
    # Question 1: Which product generated the highest revenue?
    if any(k in p for k in ["product", "item"]) and any(k in p for k in ["highest revenue", "top revenue", "most revenue", "best product", "max revenue", "sales rank"]):
        sql = """
        SELECT 
            product_name,
            category,
            total_revenue,
            total_units_sold,
            total_orders,
            revenue_rank
        FROM retail_analytics.dim_products_sales
        ORDER BY total_revenue DESC;
        """
        chart_type = "bar_product_revenue"
        summary = "Querying `dim_products_sales` to identify top performing products by total revenue."
        return sql, chart_type, summary

    # Question 2: Which region records the highest sales / performance?
    elif any(k in p for k in ["region", "geography", "country", "territory", "area"]) or ("highest sales" in p and "month" not in p and "product" not in p):
        sql = """
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
        chart_type = "bar_regional_revenue"
        summary = "Querying `dim_regional_performance` to rank geographical sales regions by total revenue."
        return sql, chart_type, summary

    # Question 3: How does revenue change month by month?
    elif any(k in p for k in ["month", "trend", "monthly", "over time", "change month", "seasonality", "mom"]):
        sql = """
        SELECT 
            sales_month,
            total_revenue,
            total_orders,
            total_units_sold,
            mom_revenue_growth
        FROM retail_analytics.fct_sales_monthly
        ORDER BY sales_month ASC;
        """
        chart_type = "line_monthly_trend"
        summary = "Querying `fct_sales_monthly` to examine chronological revenue changes and month-over-month growth."
        return sql, chart_type, summary

    # Bonus: Units sold by product
    elif any(k in p for k in ["units", "quantity", "volume", "most sold"]):
        sql = """
        SELECT 
            product_name,
            category,
            total_units_sold,
            total_revenue
        FROM retail_analytics.dim_products_sales
        ORDER BY total_units_sold DESC;
        """
        chart_type = "bar_product_units"
        summary = "Querying `dim_products_sales` ranked by total units sold."
        return sql, chart_type, summary

    # Bonus: Payment status breakdown
    elif any(k in p for k in ["payment", "status", "refund", "pending", "completed"]):
        sql = """
        SELECT 
            payment_status,
            COUNT(*) AS total_transactions,
            ROUND(SUM(revenue), 2) AS total_amount,
            ROUND(AVG(revenue), 2) AS avg_transaction_value
        FROM retail_staging.stg_retail_sales
        GROUP BY payment_status
        ORDER BY total_amount DESC;
        """
        chart_type = "pie_payment_status"
        summary = "Querying `stg_retail_sales` to examine order counts and dollar volumes by payment status."
        return sql, chart_type, summary

    # Default fallback: Show overview
    else:
        sql = """
        SELECT 
            product_name,
            category,
            total_revenue,
            total_orders,
            revenue_rank
        FROM retail_analytics.dim_products_sales
        ORDER BY total_revenue DESC
        LIMIT 5;
        """
        chart_type = "bar_product_revenue"
        summary = "Showing top 5 products by revenue as a general overview."
        return sql, chart_type, summary

# ----------------- UI LAYOUT -----------------

st.title("🛒 Modern Data Pipeline: Conversational BI")
st.markdown("""
**Subject: Data Engineering Microproject** | Architecture: **Airflow + Airbyte + dbt + Cloud DW (BigQuery / Snowflake / DuckDB)**  
Ask natural-language business questions below to query transformed analytical marts in real time.
""")

# Sidebar Navigation & Details
with st.sidebar:
    st.header("⚙️ Pipeline Architecture")
    st.info("""
    **1. Ingestion:** Airbyte / Source CSV  
    **2. Warehouse:** Medallion Architecture  
       - `retail_raw` (Raw Landing)  
       - `retail_staging` (dbt Staging View)  
       - `retail_analytics` (dbt Marts)  
    **3. Transformations:** dbt (SQL Models & Tests)  
    **4. Orchestration:** Apache Airflow DAG  
    **5. Consumption:** Streamlit Conversational BI  
    """)
    
    st.subheader("💡 Recommended Sample Questions")
    sample_q1 = st.button("1️⃣ Which product has the highest revenue?")
    sample_q2 = st.button("2️⃣ Which region records the highest sales?")
    sample_q3 = st.button("3️⃣ How does revenue change month by month?")
    sample_q4 = st.button("4️⃣ What is the breakdown by payment status?")

# Tabs for Application Views
tab_chat, tab_explorer, tab_arch = st.tabs(["💬 Conversational BI Chat", "🔍 Warehouse Data Explorer", "📐 Architecture & Lineage"])

# Process sample question button clicks
selected_prompt = None
if sample_q1:
    selected_prompt = "Which product has the highest revenue?"
elif sample_q2:
    selected_prompt = "Which region records the highest sales?"
elif sample_q3:
    selected_prompt = "How does revenue change month by month?"
elif sample_q4:
    selected_prompt = "What is the breakdown by payment status?"

with tab_chat:
    st.markdown("### 💬 Ask a Business Question")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Hello! I am your Conversational BI Assistant connected to the retail warehouse. You can ask me questions like:\n- *Which product generated the highest revenue?*\n- *Which region records the highest sales performance?*\n- *How does revenue change month-by-month over the year?*"
            }
        ]

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "df" in msg:
                st.dataframe(msg["df"], width='stretch')

    # Chat input
    user_query = st.chat_input("Enter your business question here...")
    active_query = selected_prompt or user_query

    if active_query:
        # Add user prompt to chat
        st.session_state.messages.append({"role": "user", "content": active_query})
        with st.chat_message("user"):
            st.markdown(active_query)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing schema, generating SQL, and querying warehouse..."):
                sql, chart_type, summary = nl_to_sql_intent(active_query)
                df = execute_query(sql)

                # Formulate natural language answer
                response_text = f"**Intent:** {summary}\n\n```sql\n{sql.strip()}\n```"
                
                # Context-specific answers
                if chart_type == "bar_product_revenue":
                    top_prod = df.iloc[0]["product_name"]
                    top_rev = df.iloc[0]["total_revenue"]
                    response_text += f"\n\n🏆 **Key Finding:** The product with the highest revenue is **{top_prod}**, generating **${top_rev:,.2f}** in total sales across {df.iloc[0]['total_orders']} orders."
                elif chart_type == "bar_regional_revenue":
                    top_reg = df.iloc[0]["region"]
                    top_rev = df.iloc[0]["total_revenue"]
                    response_text += f"\n\n🌍 **Key Finding:** The top performing sales region is **{top_reg}**, recording **${top_rev:,.2f}** in gross sales ({df.iloc[0]['total_orders']} orders)."
                elif chart_type == "line_monthly_trend":
                    max_month_idx = df["total_revenue"].idxmax()
                    best_month = df.loc[max_month_idx, "sales_month"]
                    best_month_rev = df.loc[max_month_idx, "total_revenue"]
                    response_text += f"\n\n📈 **Key Finding:** Revenue peaked in **{best_month}** at **${best_month_rev:,.2f}**."

                st.markdown(response_text)

                # Visualizations
                if chart_type == "bar_product_revenue":
                    st.subheader("📊 Revenue by Product")
                    st.bar_chart(df.set_index("product_name")["total_revenue"])
                elif chart_type == "bar_regional_revenue":
                    st.subheader("🌍 Regional Revenue Comparison")
                    st.bar_chart(df.set_index("region")["total_revenue"])
                elif chart_type == "line_monthly_trend":
                    st.subheader("📈 Monthly Revenue Trend")
                    st.line_chart(df.set_index("sales_month")["total_revenue"])
                elif chart_type == "pie_payment_status":
                    st.subheader("💳 Breakdown by Payment Status")
                    st.bar_chart(df.set_index("payment_status")["total_amount"])

                st.subheader("📋 Query Results Table")
                st.dataframe(df, width='stretch')

                # Save assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "df": df
                })

with tab_explorer:
    st.subheader("🔍 Target Data Warehouse Layer Explorer")
    st.markdown("Inspect data across the three layers of the Medallion Architecture:")
    
    con = get_warehouse_connection()
    layer = st.radio("Select Warehouse Layer:", [
        "1. Raw Ingestion Layer (retail_raw.raw_retail_sales)",
        "2. Staging Layer (retail_staging.stg_retail_sales)",
        "3. Products Mart (retail_analytics.dim_products_sales)",
        "4. Regional Mart (retail_analytics.dim_regional_performance)",
        "5. Monthly Fact Mart (retail_analytics.fct_sales_monthly)"
    ])
    
    if "1. Raw" in layer:
        res = con.execute("SELECT * FROM retail_raw.raw_retail_sales LIMIT 50;").df()
    elif "2. Staging" in layer:
        res = con.execute("SELECT * FROM retail_staging.stg_retail_sales LIMIT 50;").df()
    elif "3. Products" in layer:
        res = con.execute("SELECT * FROM retail_analytics.dim_products_sales;").df()
    elif "4. Regional" in layer:
        res = con.execute("SELECT * FROM retail_analytics.dim_regional_performance;").df()
    else:
        res = con.execute("SELECT * FROM retail_analytics.fct_sales_monthly;").df()
    con.close()
    
    st.dataframe(res, width='stretch')
    st.caption(f"Showing up to 50 rows. Total retrieved: {len(res)} records.")

with tab_arch:
    st.subheader("📐 Architecture & Data Flow Lineage")
    st.markdown("""
    ```
    +-------------------------+
    | Source CSV Dataset      | (data/raw/retail_sales_raw.csv, 500 records)
    +-------------------------+
                 |
                 v [Step 4: Airbyte Ingestion / Automated Sync]
    +-------------------------+
    | RAW LAYER               | retail_raw.raw_retail_sales (Untransformed landing zone)
    +-------------------------+
                 |
                 v [Step 5: dbt run --select stg_retail_sales + dbt test]
    +-------------------------+
    | STAGING LAYER           | retail_staging.stg_retail_sales (Casting, cleaning, calculated revenue)
    +-------------------------+
                 |
                 v [Step 5: dbt run --select marts + validation tests]
    +-------------------------+
    | ANALYTICS MARTS LAYER   | - dim_products_sales (Product rankings)
    |                         | - dim_regional_performance (Geographic breakdown)
    |                         | - fct_sales_monthly (Monthly revenue & MoM growth)
    +-------------------------+
                 |
                 v [Step 7: Natural Language to SQL]
    +-------------------------+
    | CONVERSATIONAL BI APP   | Streamlit Web UI -> Natural Language Queries -> Insights & Charts
    +-------------------------+
    
    * Apache Airflow Orchestrates the entire DAG:
      start >> trigger_airbyte >> wait_sync >> dbt_staging >> dbt_test >> dbt_marts >> validation >> finish
    ```
    """)
