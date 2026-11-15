"""
analysis.py
-----------
Upgraded analysis script supporting both formatted terminal insights
and optional Matplotlib visualizations.
"""

import mysql.connector
from config import DB_CONFIG, get_db_connection
from analytics import run_all_analytics

def run_visual_charts():
    """Generates visual charts if pandas/matplotlib are installed."""
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import numpy as np

        conn = get_db_connection(include_database=True)
        if not conn:
            print("[INFO] MySQL connection unavailable for matplotlib charts. Run 'streamlit run app.py' for interactive charts.")
            return

        print("\n[*] Fetching data for Matplotlib charts...")
        products = pd.read_sql("SELECT * FROM products", conn)
        production = pd.read_sql("SELECT * FROM production", conn)
        sales = pd.read_sql("SELECT * FROM sales", conn)
        conn.close()

        # Merge summaries
        prod_sum = production.groupby("product_id")["units_produced"].sum().reset_index()
        sales_sum = sales.groupby("product_id")["units_sold"].sum().reset_index()

        df = products.merge(prod_sum, on="product_id", how="left").fillna(0)
        df = df.merge(sales_sum, on="product_id", how="left").fillna(0)
        df["inventory"] = df["units_produced"] - df["units_sold"]
        df["revenue"] = df["units_sold"] * df["unit_price"]

        # Chart 1: Production vs Sales
        x = np.arange(len(df))
        width = 0.35
        plt.figure(figsize=(10, 5))
        plt.bar(x - width/2, df["units_produced"], width, label="Produced", color="#1E88E5")
        plt.bar(x + width/2, df["units_sold"], width, label="Sold", color="#43A047")
        plt.xlabel("Product")
        plt.ylabel("Quantity (Units)")
        plt.title("Production vs Sales by Product")
        plt.xticks(x, df["product_name"], rotation=30)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # Chart 2: Inventory Gap
        plt.figure(figsize=(10, 5))
        plt.bar(df["product_name"], df["inventory"], color="#FB8C00")
        plt.xlabel("Product")
        plt.ylabel("Net Stock Level (Units)")
        plt.title("Warehouse Stock Level by Product")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

        # Chart 3: Revenue by Product
        plt.figure(figsize=(10, 5))
        plt.bar(df["product_name"], df["revenue"], color="#8E24AA")
        plt.xlabel("Product")
        plt.ylabel("Revenue (₹)")
        plt.title("Revenue by Product")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

    except ImportError:
        print("[INFO] Matplotlib not found. Run 'streamlit run app.py' to view interactive web charts!")

if __name__ == "__main__":
    print("=" * 60)
    print(" RUNNING ANALYTICS PIPELINE")
    print("=" * 60)
    # 1. Run standard library terminal reports
    run_all_analytics()
    # 2. Optionally trigger visual charts
    run_visual_charts()
