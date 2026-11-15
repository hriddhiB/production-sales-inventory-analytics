"""
seed_data.py
------------
Sample Data Generator:
Populates 'inventory_analytics' database with clean, realistic manufacturing,
sales, and inventory numbers for analytics.
"""

from mysql.connector import Error
from config import get_db_connection

# 1. Master Products List
SAMPLE_PRODUCTS = [
    # (product_id, product_name, category, unit_price)
    (1, "Gear Assembly", "Mechanical", 1200.00),
    (2, "Shaft", "Mechanical", 800.00),
    (3, "Bearing Housing", "Component", 1500.00),
    (4, "Coupling", "Mechanical", 950.00),
    (5, "Pulley", "Mechanical", 700.00),
    (6, "Bracket", "Component", 450.00),
    (7, "Hydraulic Valve", "Hydraulics", 2100.00),
    (8, "Industrial Sensor", "Electronics", 1850.00),
]

# 2. Production Batches
SAMPLE_PRODUCTION = [
    # (production_id, product_id, units_produced, production_date)
    (1,  1, 500, "2026-09-01"),
    (2,  2, 700, "2026-09-01"),
    (3,  3, 300, "2026-09-01"),
    (4,  4, 450, "2026-09-02"),
    (5,  5, 600, "2026-09-02"),
    (6,  6, 800, "2026-09-02"),
    (7,  1, 550, "2026-09-03"),
    (8,  2, 750, "2026-09-03"),
    (9,  3, 350, "2026-09-03"),
    (10, 4, 500, "2026-09-04"),
    (11, 5, 650, "2026-09-04"),
    (12, 6, 900, "2026-09-04"),
    (13, 7, 200, "2026-09-05"),
    (14, 8, 400, "2026-09-05"),
    (15, 7, 250, "2026-09-06"),
    (16, 8, 450, "2026-09-06"),
]

# 3. Sales Transactions
SAMPLE_SALES = [
    # (sale_id, product_id, units_sold, sale_date)
    (1,  1, 420, "2026-09-02"),
    (2,  2, 600, "2026-09-02"),
    (3,  3, 250, "2026-09-02"),
    (4,  4, 380, "2026-09-03"),
    (5,  5, 500, "2026-09-03"),
    (6,  6, 650, "2026-09-03"),
    (7,  1, 450, "2026-09-04"),
    (8,  2, 620, "2026-09-04"),
    (9,  3, 280, "2026-09-04"),
    (10, 4, 420, "2026-09-05"),
    (11, 5, 550, "2026-09-05"),
    (12, 6, 700, "2026-09-05"),
    (13, 7, 240, "2026-09-07"),
    (14, 8, 390, "2026-09-07"),
    (15, 7, 200, "2026-09-08"),
    (16, 8, 410, "2026-09-08"),
]

def populate_sample_data():
    """
    Cleans existing records and inserts clean dummy data into all 4 tables.
    Also synchronizes the 'inventory' table based on (total produced - total sold).
    """
    print("=" * 60)
    print(" STEP 2: POPULATING SAMPLE DATA")
    print("=" * 60)

    conn = get_db_connection(include_database=True)
    if not conn:
        print("[FAILED] Cannot connect to database. Make sure setup has been run first.")
        return False

    cursor = conn.cursor()

    try:
        # Disable foreign key checks for safe truncation
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE inventory;")
        cursor.execute("TRUNCATE TABLE sales;")
        cursor.execute("TRUNCATE TABLE production;")
        cursor.execute("TRUNCATE TABLE products;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        # 1. Insert Products
        product_insert_query = """
            INSERT INTO products (product_id, product_name, category, unit_price)
            VALUES (%s, %s, %s, %s);
        """
        cursor.executemany(product_insert_query, SAMPLE_PRODUCTS)
        print(f"[OK] Inserted {cursor.rowcount} products into 'products' table.")

        # 2. Insert Production Records
        production_insert_query = """
            INSERT INTO production (production_id, product_id, units_produced, production_date)
            VALUES (%s, %s, %s, %s);
        """
        cursor.executemany(production_insert_query, SAMPLE_PRODUCTION)
        print(f"[OK] Inserted {cursor.rowcount} production batches into 'production' table.")

        # 3. Insert Sales Records
        sales_insert_query = """
            INSERT INTO sales (sale_id, product_id, units_sold, sale_date)
            VALUES (%s, %s, %s, %s);
        """
        cursor.executemany(sales_insert_query, SAMPLE_SALES)
        print(f"[OK] Inserted {cursor.rowcount} sales transactions into 'sales' table.")

        # 4. Populate Inventory Table
        # Current Stock Level = (Total Units Produced) - (Total Units Sold)
        inventory_sync_query = """
            INSERT INTO inventory (product_id, stock_level)
            SELECT 
                p.product_id,
                COALESCE(prod.total_produced, 0) - COALESCE(s.total_sold, 0) AS stock_level
            FROM products p
            LEFT JOIN (
                SELECT product_id, SUM(units_produced) AS total_produced
                FROM production
                GROUP BY product_id
            ) prod ON p.product_id = prod.product_id
            LEFT JOIN (
                SELECT product_id, SUM(units_sold) AS total_sold
                FROM sales
                GROUP BY product_id
            ) s ON p.product_id = s.product_id;
        """
        cursor.execute(inventory_sync_query)
        print(f"[OK] Computed and initialized stock levels for {cursor.rowcount} items in 'inventory' table.")

        conn.commit()
        print("\n" + "-" * 60)
        print("[SUCCESS] All sample data loaded successfully!")
        print("-" * 60)
        return True

    except Error as e:
        conn.rollback()
        print(f"[ERROR] Failed to populate sample data: {e}")
        return False

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    populate_sample_data()
