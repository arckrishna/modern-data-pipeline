"""
Architecture Diagram Generator (PNG)
Generates a publication-quality architecture diagram for the Modern Data Pipeline.
Complies with Step 6 & Submission Guidelines of the Microproject.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("docs", exist_ok=True)

fig, ax = plt.subplots(figsize=(18, 10.5), dpi=300)
fig.patch.set_facecolor('#0f172a')  # Dark sleek background
ax.set_facecolor('#0f172a')
ax.set_xlim(0, 18)
ax.set_ylim(0, 10.5)
ax.axis('off')

# Title & Subtitle Banner
ax.text(9, 10.0, "MODERN AUTOMATED DATA PIPELINE ARCHITECTURE", 
        fontsize=22, fontweight='bold', color='#ffffff', ha='center', va='center', fontfamily='sans-serif')
ax.text(9, 9.55, "Data Engineering Microproject | Apache Airflow • Airbyte • dbt • Snowflake / BigQuery • Streamlit Conversational BI", 
        fontsize=12, color='#94a3b8', ha='center', va='center')

def draw_box(x, y, w, h, bg_color, border_color, title, subtitle="", items=[], title_color="#ffffff"):
    # Drop shadow
    shadow = patches.FancyBboxPatch((x+0.08, y-0.08), w, h,
                                    boxstyle="round,pad=0.2,rounding_size=0.15",
                                    facecolor="#000000", edgecolor="none", alpha=0.35, zorder=2)
    ax.add_patch(shadow)
    
    # Main Box
    box = patches.FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.2,rounding_size=0.15",
                                facecolor=bg_color, edgecolor=border_color, linewidth=2, zorder=3)
    ax.add_patch(box)
    
    # Title
    ax.text(x + w/2, y + h - 0.35, title, fontsize=12, fontweight='bold', color=title_color, ha='center', va='center', zorder=4)
    if subtitle:
        ax.text(x + w/2, y + h - 0.70, subtitle, fontsize=9.5, fontstyle='italic', color='#94a3b8', ha='center', va='center', zorder=4)
    
    # Items
    start_y = y + h - (1.1 if subtitle else 0.8)
    for i, item in enumerate(items):
        ax.text(x + 0.25, start_y - (i * 0.38), f"• {item}", fontsize=9, color='#e2e8f0', va='center', zorder=4)

# -------------------------------------------------------------
# 5. ORCHESTRATION LAYER (Apache Airflow) - Top Banner
# -------------------------------------------------------------
draw_box(x=1.0, y=7.6, w=16.0, h=1.45,
         bg_color="#1e1e38", border_color="#f43f5e",
         title="5. ORCHESTRATION LAYER: Apache Airflow (Control Plane)",
         subtitle="Coordinates DAG Dependencies & Triggers Pipeline Steps (Does NOT directly transfer payload data)",
         items=[
             "DAG: retail_modern_data_pipeline  |  Schedule: @daily",
             "Task Flow: start >> trigger_airbyte >> wait_sync >> dbt_staging >> dbt_test >> dbt_marts >> validate_output >> finish"
         ],
         title_color="#fb7185")

# -------------------------------------------------------------
# 1. SOURCE LAYER
# -------------------------------------------------------------
draw_box(x=0.8, y=3.2, w=2.6, h=3.4,
         bg_color="#1e293b", border_color="#475569",
         title="1. DATA SOURCE",
         subtitle="CSV / Relational DB",
         items=[
             "retail_sales_raw.csv",
             "500 Transaction Rows",
             "9 Source Columns",
             "order_id (PK)",
             "order_date, customer",
             "product, category",
             "region, quantity",
             "unit_price, status"
         ])

# -------------------------------------------------------------
# 2. INGESTION LAYER (Airbyte)
# -------------------------------------------------------------
draw_box(x=4.0, y=3.2, w=2.7, h=3.4,
         bg_color="#1e1b4b", border_color="#6366f1",
         title="2. INGESTION",
         subtitle="Airbyte / Fivetran",
         items=[
             "Source: File / CSV",
             "Destination: Cloud DWH",
             "Sync: Full Refresh /",
             "      Append Deduped",
             "Trigger: REST API",
             "Idempotent Loads",
             "Automated Failure",
             "Retry Policies"
         ],
         title_color="#a5b4fc")

# -------------------------------------------------------------
# 3. TARGET DATA WAREHOUSE (BigQuery / Snowflake / DuckDB)
# -------------------------------------------------------------
# Outer Warehouse Container
dwh_outer = patches.FancyBboxPatch((7.3, 1.2), 6.4, 5.4,
                                   boxstyle="round,pad=0.25,rounding_size=0.2",
                                   facecolor="#0c2340", edgecolor="#0284c7", linewidth=2.5, zorder=2)
ax.add_patch(dwh_outer)
ax.text(10.5, 6.35, "3. TARGET DATA WAREHOUSE (Medallion Architecture)", fontsize=12.5, fontweight='bold', color="#38bdf8", ha='center', zorder=4)
ax.text(10.5, 6.05, "Snowflake / Google BigQuery / Local Embedded DuckDB", fontsize=9.5, fontstyle='italic', color="#94a3b8", ha='center', zorder=4)

# Bronze / Raw Layer
draw_box(x=7.6, y=4.4, w=5.8, h=1.35,
         bg_color="#1e293b", border_color="#94a3b8",
         title="Bronze Tier: Raw Ingestion Landing Zone",
         items=["retail_raw.raw_retail_sales (500 untransformed records ingested by Airbyte)"],
         title_color="#cbd5e1")

# Silver / Staging Layer
draw_box(x=7.6, y=2.85, w=5.8, h=1.35,
         bg_color="#134e4a", border_color="#14b8a6",
         title="Silver Tier: Cleaned & Validated Staging View",
         items=["retail_staging.stg_retail_sales (Cleaned data types, revenue = qty * price, 3/3 tests passed)"],
         title_color="#5eead4")

# Gold / Marts Layer
draw_box(x=7.6, y=1.35, w=5.8, h=1.35,
         bg_color="#78350f", border_color="#f59e0b",
         title="Gold Tier: Business-Ready Analytics Marts",
         items=[
             "dim_products_sales (Product Revenue & Rank)  |  dim_regional_performance (Region AOV)",
             "fct_sales_monthly (Chronological Trends & Month-over-Month Revenue Growth)"
         ],
         title_color="#fde68a")

# -------------------------------------------------------------
# 4. TRANSFORMATION LAYER (dbt)
# -------------------------------------------------------------
draw_box(x=7.6, y=0.08, w=5.8, h=0.85,
         bg_color="#064e3b", border_color="#10b981",
         title="4. TRANSFORMATION ENGINE: dbt Core (In-Warehouse ELT)",
         items=["Compiles SQL models into warehouse, executes schema tests (unique, not_null, accepted_values)"],
         title_color="#6ee7b7")

# -------------------------------------------------------------
# 6. CONSUMPTION LAYER (Conversational BI)
# -------------------------------------------------------------
draw_box(x=14.3, y=2.5, w=2.9, h=4.1,
         bg_color="#3b0764", border_color="#a855f7",
         title="6. CONVERSATIONAL BI",
         subtitle="Streamlit + Natural Language",
         items=[
             "Natural Language -> SQL",
             "Safe Read-Only SELECT",
             "Plotly Charts & KPIs",
             "Answers 3 Core Questions:",
             " Q1: Top Product Revenue",
             " Q2: Regional Leaderboard",
             " Q3: Monthly Trend/Growth",
             "Medallion Data Explorer",
             "Airflow DAG Monitor UI"
         ],
         title_color="#d8b4fe")

# -------------------------------------------------------------
# ARROWS: DATA MOVEMENT (Solid Teal Arrows)
# -------------------------------------------------------------
arrow_data_style = dict(arrowstyle="->,head_width=0.4,head_length=0.6", color="#38bdf8", lw=3.0, zorder=5)

# Source -> Airbyte
ax.annotate("", xy=(4.0, 4.9), xytext=(3.4, 4.9), arrowprops=arrow_data_style)
ax.text(3.7, 5.15, "Extract", fontsize=8.5, color="#38bdf8", fontweight='bold', ha='center')

# Airbyte -> Raw DWH
ax.annotate("", xy=(7.6, 5.0), xytext=(6.7, 5.0), arrowprops=arrow_data_style)
ax.text(7.15, 5.25, "Load Raw", fontsize=8.5, color="#38bdf8", fontweight='bold', ha='center')

# Raw -> Silver Staging (inside DWH)
ax.annotate("", xy=(10.5, 4.2), xytext=(10.5, 4.4), arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.5", color="#14b8a6", lw=2.5, zorder=5))

# Silver -> Gold Marts (inside DWH)
ax.annotate("", xy=(10.5, 2.7), xytext=(10.5, 2.85), arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.5", color="#f59e0b", lw=2.5, zorder=5))

# Gold Marts -> Conversational BI
ax.annotate("", xy=(14.3, 4.2), xytext=(13.7, 2.0),
            arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color="#c084fc", lw=3.0, connectionstyle="arc3,rad=-0.2", zorder=5))
ax.text(14.05, 3.1, "Query Marts", fontsize=8.5, color="#c084fc", fontweight='bold', ha='center')

# -------------------------------------------------------------
# ARROWS: ORCHESTRATION CONTROL (Dashed Pink/Red Arrows)
# -------------------------------------------------------------
arrow_ctrl_style = dict(arrowstyle="->,head_width=0.35,head_length=0.55", color="#f43f5e", lw=2.2, linestyle="dashed", zorder=5)

# Airflow -> Airbyte (Trigger Ingestion)
ax.annotate("", xy=(5.35, 6.6), xytext=(5.35, 7.6), arrowprops=arrow_ctrl_style)
ax.text(5.4, 7.1, "1. Trigger Sync", fontsize=8, color="#fb7185", fontweight='bold', ha='center', backgroundcolor="#0f172a")

# Airflow -> dbt (Trigger Staging & Marts)
ax.annotate("", xy=(10.5, 6.6), xytext=(10.5, 7.6), arrowprops=arrow_ctrl_style)
ax.text(10.5, 7.1, "2. Trigger dbt run / test", fontsize=8, color="#fb7185", fontweight='bold', ha='center', backgroundcolor="#0f172a")

# Airflow -> Validation
ax.annotate("", xy=(13.2, 6.6), xytext=(13.2, 7.6), arrowprops=arrow_ctrl_style)
ax.text(13.2, 7.1, "3. Assert Quality", fontsize=8, color="#fb7185", fontweight='bold', ha='center', backgroundcolor="#0f172a")

# -------------------------------------------------------------
# LEGEND BOX (Bottom Left)
# -------------------------------------------------------------
legend_box = patches.FancyBboxPatch((0.8, 0.4), 6.0, 1.4,
                                   boxstyle="round,pad=0.15",
                                   facecolor="#1e293b", edgecolor="#475569", linewidth=1.5, zorder=3)
ax.add_patch(legend_box)
ax.text(1.0, 1.5, "DIAGRAM LEGEND & CLARITY", fontsize=10, fontweight='bold', color="#ffffff")

# Solid teal line for Data Flow
ax.plot([1.1, 2.0], [1.1, 1.1], color="#38bdf8", lw=3.0, zorder=4)
ax.text(2.2, 1.1, "Data Movement Flow (Airbyte loads raw, dbt transforms in DWH)", fontsize=8.5, color="#e2e8f0", va='center')

# Dashed red line for Orchestration Control
ax.plot([1.1, 2.0], [0.7, 0.7], color="#f43f5e", lw=2.2, linestyle="dashed", zorder=4)
ax.text(2.2, 0.7, "Orchestration Control Flow (Airflow coordinates dependencies & triggers)", fontsize=8.5, color="#e2e8f0", va='center')

plt.tight_layout()
png_path = "docs/architecture_diagram.png"
plt.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig("architecture_diagram.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()

print(f"Successfully generated architecture diagram PNG at: {png_path} and architecture_diagram.png")
