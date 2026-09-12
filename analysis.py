import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password= "Hbnit_05",
    database="manufacturing_analytics"
)

products = pd.read_sql("SELECT * FROM products", conn)
production = pd.read_sql("SELECT * FROM production", conn)
sales = pd.read_sql("SELECT * FROM sales", conn)

production_summary = production.groupby("product_id")["quantity_produced"].sum().reset_index()

production_summary = production_summary.merge(
    products[["product_id", "product_name"]],
    on="product_id"
)

sales_summary = sales.groupby("product_id")["quantity_sold"].sum().reset_index()

sales_summary = sales_summary.merge(
    products[["product_id", "product_name"]],
    on="product_id"
)

inventory = production.groupby("product_id")["quantity_produced"].sum().reset_index()
inventory = inventory.merge(
    sales.groupby("product_id")["quantity_sold"].sum().reset_index(),
    on="product_id"
)

inventory["inventory"] = (
    inventory["quantity_produced"] - inventory["quantity_sold"]
)

inventory = inventory.merge(
    products[["product_id", "product_name"]],
    on="product_id"
)



x = np.arange(len(inventory))
width = 0.35

plt.figure(figsize=(10, 5))

plt.bar(
    x - width/2,
    inventory["quantity_produced"],
    width,
    label="Produced"
)

plt.bar(
    x + width/2,
    inventory["quantity_sold"],
    width,
    label="Sold"
)

plt.xlabel("Product")
plt.ylabel("Quantity")
plt.title("Production vs Sales by Product")
plt.xticks(x, inventory["product_name"], rotation=30)
plt.legend()
plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 5))

plt.bar(
    inventory["product_name"],
    inventory["inventory"]
)

plt.xlabel("Product")
plt.ylabel("Inventory")
plt.title("Inventory by Product")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

revenue = sales.merge(
    products[["product_id", "product_name", "unit_price"]],
    on="product_id"
)

revenue["revenue"] = revenue["quantity_sold"] * revenue["unit_price"]

revenue_summary = (
    revenue.groupby("product_name")["revenue"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(10, 5))

plt.bar(
    revenue_summary["product_name"],
    revenue_summary["revenue"]
)

plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.title("Revenue by Product")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()