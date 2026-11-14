"""
Dataset Generator for Retail Sales Analytics Microproject
Generates ~500 clean yet realistic retail transaction records.
Columns: order_id, order_date, customer_id, product, category, region, quantity, unit_price, payment_status
"""
import os
import random
import csv
from datetime import datetime, timedelta

os.makedirs("data/raw", exist_ok=True)

# Seed for reproducibility
random.seed(42)

products_data = [
    ("Laptop Pro 15", "Electronics", 1199.99),
    ("UltraHD 4K Monitor", "Electronics", 379.50),
    ("Wireless Noise-Canceling Headphones", "Accessories", 189.99),
    ("Mechanical Gaming Keyboard", "Peripherals", 129.00),
    ("Ergonomic Office Chair", "Furniture", 249.99),
    ("USB-C Multi-Port Hub", "Accessories", 49.99),
    ("Wireless Ergonomic Mouse", "Peripherals", 59.95),
    ("Height-Adjustable Standing Desk", "Furniture", 449.00),
    ("HD Webcam 1080p", "Accessories", 79.99),
    ("Portable SSD 1TB", "Electronics", 109.99)
]

regions = ["North America", "Europe", "Asia Pacific", "Latin America"]
payment_statuses = ["Completed", "Completed", "Completed", "Completed", "Pending", "Refunded"]

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
date_range_days = (end_date - start_date).days

records = []
num_records = 500

for i in range(1, num_records + 1):
    order_id = f"ORD-{1000 + i}"
    cust_num = random.randint(101, 250)
    customer_id = f"CUST-{cust_num}"
    
    prod_name, category, base_price = random.choice(products_data)
    # Slight price fluctuation (promotions/discounts)
    unit_price = round(base_price * random.uniform(0.92, 1.05), 2)
    quantity = random.choices([1, 2, 3, 4, 5, 8], weights=[45, 25, 15, 8, 5, 2])[0]
    
    # Seasonality weights: slightly higher towards Q4 (Nov, Dec)
    random_days = random.randint(0, date_range_days)
    order_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
    
    region = random.choices(regions, weights=[38, 28, 24, 10])[0]
    status = random.choice(payment_statuses)
    
    records.append({
        "order_id": order_id,
        "order_date": order_date,
        "customer_id": customer_id,
        "product": prod_name,
        "category": category,
        "region": region,
        "quantity": quantity,
        "unit_price": unit_price,
        "payment_status": status
    })

csv_file_path = "data/raw/retail_sales_raw.csv"
fieldnames = ["order_id", "order_date", "customer_id", "product", "category", "region", "quantity", "unit_price", "payment_status"]

with open(csv_file_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"Successfully generated {len(records)} records in {csv_file_path}")
