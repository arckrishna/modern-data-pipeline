"""
Source Data Inspection and Profiling Script (Step 2 of Microproject Guidelines)
Analyzes column names, data types, missing values, duplicates, and summary statistics.
"""
import pandas as pd
import numpy as np

def inspect_dataset(csv_path="data/raw/retail_sales_raw.csv"):
    df = pd.read_csv(csv_path)
    
    print("=" * 65)
    print("DATA ENGINEERING MICROPROJECT - DATASET INSPECTION REPORT")
    print("=" * 65)
    print(f"Dataset Path: {csv_path}")
    print(f"Total Records: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    print("-" * 65)
    
    print("\n1. SCHEMA & DATA TYPES:")
    schema_info = pd.DataFrame({
        "Column": df.columns,
        "Non-Null Count": df.notnull().sum().values,
        "Null Count": df.isnull().sum().values,
        "Data Type": df.dtypes.values,
        "Unique Values": [df[col].nunique() for col in df.columns]
    })
    print(schema_info.to_string(index=False))
    
    print("\n2. DUPLICATE CHECK:")
    duplicates = df.duplicated().sum()
    id_duplicates = df["order_id"].duplicated().sum()
    print(f"Full Row Duplicates: {duplicates}")
    print(f"Primary Key (order_id) Duplicates: {id_duplicates}")
    
    print("\n3. SAMPLE RECORDS (FIRST 5 ROWS):")
    print(df.head(5).to_string(index=False))
    
    print("\n4. NUMERICAL METRICS SUMMARY:")
    print(df[["quantity", "unit_price"]].describe().to_string())
    
    print("\n5. CATEGORICAL DISTRIBUTION:")
    print("\nRegion Breakdown:")
    print(df["region"].value_counts().to_string())
    print("\nCategory Breakdown:")
    print(df["category"].value_counts().to_string())
    print("\nPayment Status Breakdown:")
    print(df["payment_status"].value_counts().to_string())
    print("=" * 65)

if __name__ == "__main__":
    inspect_dataset()
