"""
database_setup.py
-----------------
Automated setup script to create the 'inventory_analytics' database
and all required tables (products, production, sales, inventory).

Run this script once to initialize your MySQL database.
"""

from mysql.connector import Error
from config import get_db_connection, DB_CONFIG

# SQL DDL statements for creating tables
TABLE_DEFINITIONS = {
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00
        ) ENGINE=InnoDB;
    """,
    "production": """
        CREATE TABLE IF NOT EXISTS production (
            production_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            units_produced INT NOT NULL,
            production_date DATE NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
    """,
    "sales": """
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            units_sold INT NOT NULL,
            sale_date DATE NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
    """,
    "inventory": """
        CREATE TABLE IF NOT EXISTS inventory (
            inventory_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL UNIQUE,
            stock_level INT NOT NULL DEFAULT 0,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
    """
}

def setup_database():
    """
    Connects to MySQL server, creates the 'inventory_analytics' database,
    and creates the 4 core tables.
    """
    print("=" * 60)
    print(" STEP 1: INITIALIZING DATABASE & SCHEMA")
    print("=" * 60)

    # 1. Connect to MySQL without specifying a database yet
    conn = get_db_connection(include_database=False)
    if not conn:
        print("[FAILED] Could not connect to MySQL server. Please verify credentials in config.py.")
        return False

    cursor = conn.cursor()
    db_name = DB_CONFIG["database"]

    try:
        # 2. Create database
        print(f"[*] Creating database '{db_name}' (if not exists)...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4;")
        print(f"[OK] Database '{db_name}' ready.")

        # 3. Switch to the newly created database
        cursor.execute(f"USE `{db_name}`;")

        # 4. Create each table
        for table_name, ddl_query in TABLE_DEFINITIONS.items():
            print(f"[*] Creating table '{table_name}'...")
            cursor.execute(ddl_query)
            print(f"[OK] Table '{table_name}' is ready.")

        conn.commit()
        print("\n" + "-" * 60)
        print("[SUCCESS] Database & all tables created successfully!")
        print("-" * 60)
        return True

    except Error as e:
        print(f"[ERROR] Database setup failed: {e}")
        return False

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    setup_database()
