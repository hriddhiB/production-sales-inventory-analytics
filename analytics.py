"""
analytics.py
------------
Analytics & Insights Script:
Connects to MySQL database using only 'mysql-connector-python' and standard Python.
Generates structured, easy-to-read business insights:
  1. High-Demand Products (Ranked by Total Units Sold & Revenue)
  2. Production vs. Sales Gap Analysis (Spotting Excess Stock vs Shortages)
  3. Current Inventory Stock Levels & Reorder Alerts
  4. Category-Wise Performance Summary
"""

from mysql.connector import Error
from config import get_db_connection

def format_currency(amount):
    """Formats numeric values into standard currency string representation."""
    if amount is None:
        return "₹0.00"
    return f"₹{amount:,.2f}"

def print_section_header(title):
    """Prints a styled banner for terminal readability."""
    print("\n" + "=" * 80)
    print(f" {title.upper()}")
    print("=" * 80)

def print_table(headers, rows, alignments=None):
    """
    Prints a clean ASCII table using only standard Python string formatting.
    No third-party libraries (like pandas or tabulate) required!
    
    Parameters:
        headers (list of str): Column header titles.
        rows (list of list): Rows of data to print.
        alignments (list of str): 'L' for left-aligned, 'R' for right-aligned.
    """
    if not rows:
        print("  [No data available to display]")
        return

    num_cols = len(headers)
    if alignments is None:
        alignments = ["L"] * num_cols

    # Calculate required width for each column based on content
    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, val in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(val)))

    # Add padding
    col_widths = [w + 2 for w in col_widths]

    # Build separator lines
    sep_line = "+" + "+".join("-" * w for w in col_widths) + "+"

    # Build header row
    header_cells = []
    for h, w, align in zip(headers, col_widths, alignments):
        if align == "R":
            header_cells.append(h.rjust(w - 1) + " ")
        else:
            header_cells.append(" " + h.ljust(w - 1))
    header_str = "|" + "|".join(header_cells) + "|"

    print(sep_line)
    print(header_str)
    print(sep_line)

    # Build data rows
    for row in rows:
        row_cells = []
        for val, w, align in zip(row, col_widths, alignments):
            s_val = str(val)
            if align == "R":
                row_cells.append(s_val.rjust(w - 1) + " ")
            else:
                row_cells.append(" " + s_val.ljust(w - 1))
        print("|" + "|".join(row_cells) + "|")

    print(sep_line)

# -------------------------------------------------------------------------
# Insight 1: High-Demand Products (Ranking by Units Sold & Revenue)
# -------------------------------------------------------------------------
def analyze_high_demand_products(conn):
    """
    Ranks products by total units sold to identify high-performing inventory.
    Also calculates total sales revenue for each product.
    """
    print_section_header("1. High-Demand Products (Ranked by Sales Volume)")

    query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.category,
            p.unit_price,
            COALESCE(SUM(s.units_sold), 0) AS total_units_sold,
            COALESCE(SUM(s.units_sold * p.unit_price), 0) AS total_revenue
        FROM products p
        LEFT JOIN sales s ON p.product_id = s.product_id
        GROUP BY p.product_id, p.product_name, p.category, p.unit_price
        ORDER BY total_units_sold DESC, total_revenue DESC;
    """

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    headers = ["Rank", "Product Name", "Category", "Unit Price", "Units Sold", "Total Revenue"]
    table_rows = []
    total_sales_units = 0
    total_sales_val = 0.0

    for rank, row in enumerate(results, start=1):
        units = row["total_units_sold"]
        rev = float(row["total_revenue"])
        total_sales_units += units
        total_sales_val += rev

        table_rows.append([
            f"#{rank}",
            row["product_name"],
            row["category"],
            format_currency(float(row["unit_price"])),
            f"{units:,}",
            format_currency(rev)
        ])

    print_table(headers, table_rows, alignments=["L", "L", "L", "R", "R", "R"])

    if results:
        top_product = results[0]
        print(f"\n  [KEY TAKEAWAY]")
        print(f"  * Best Seller: '{top_product['product_name']}' with {top_product['total_units_sold']:,} units sold.")
        print(f"  * Total Portfolio Sales Volume : {total_sales_units:,} units")
        print(f"  * Total Portfolio Sales Revenue: {format_currency(total_sales_val)}")

# -------------------------------------------------------------------------
# Insight 2: Production-Sales Gap Analysis (Surplus vs. Shortage)
# -------------------------------------------------------------------------
def analyze_production_sales_gap(conn):
    """
    Compares total units produced vs total units sold.
    Identifies production gaps:
      - Gap > 150 : Excess Surplus (Risk of holding costs / capital lockup)
      - Gap 50-150: Balanced Buffer
      - Gap < 50  : Tight Inventory (Potential stockout risk if sales spike)
      - Gap < 0   : Shortage (Demand exceeded production)
    """
    print_section_header("2. Production vs. Sales Gap Analysis")

    query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.category,
            COALESCE(prod.total_produced, 0) AS units_produced,
            COALESCE(sales.total_sold, 0) AS units_sold,
            (COALESCE(prod.total_produced, 0) - COALESCE(sales.total_sold, 0)) AS net_gap
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
        ) sales ON p.product_id = sales.product_id
        ORDER BY net_gap DESC;
    """

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    headers = ["Product Name", "Produced", "Sold", "Gap (Prod - Sold)", "Sell-Through", "Inventory Status"]
    table_rows = []

    excess_items = []
    tight_items = []

    for row in results:
        produced = row["units_produced"]
        sold = row["units_sold"]
        gap = row["net_gap"]

        # Calculate Sell-Through Rate (% of produced goods that were sold)
        sell_through = (sold / produced * 100) if produced > 0 else 0.0

        # Determine actionable status
        if gap > 150:
            status = "Excess Surplus"
            excess_items.append(row["product_name"])
        elif gap >= 50:
            status = "Balanced Buffer"
        elif gap >= 0:
            status = "Tight Stock"
            tight_items.append(row["product_name"])
        else:
            status = "SHORTAGE (Deficit)"
            tight_items.append(row["product_name"])

        table_rows.append([
            row["product_name"],
            f"{produced:,}",
            f"{sold:,}",
            f"{gap:+,}",
            f"{sell_through:.1f}%",
            status
        ])

    print_table(headers, table_rows, alignments=["L", "R", "R", "R", "R", "L"])

    print("\n  [MANAGEMENT INSIGHTS]")
    if excess_items:
        print(f"  * High Excess Inventory Items : {', '.join(excess_items)}")
        print("    -> Recommendation: Slow down upcoming manufacturing batches to prevent overstocking.")
    if tight_items:
        print(f"  * Tight / At-Risk Items       : {', '.join(tight_items)}")
        print("    -> Recommendation: Increase production batch size to prevent impending stockouts.")

# -------------------------------------------------------------------------
# Insight 3: Current Inventory Stock Levels & Health
# -------------------------------------------------------------------------
def analyze_inventory_stock_levels(conn):
    """
    Queries the 'inventory' table and flags items falling below safety threshold.
    """
    print_section_header("3. Warehouse Inventory Health & Reorder Check")

    query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.category,
            i.stock_level
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        ORDER BY i.stock_level ASC;
    """

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    headers = ["Product ID", "Product Name", "Category", "Current Stock", "Health Status"]
    table_rows = []

    REORDER_THRESHOLD = 75  # Safety threshold

    for row in results:
        stock = row["stock_level"]
        if stock <= 50:
            status = "CRITICAL LOW (Reorder Immediately)"
        elif stock <= REORDER_THRESHOLD:
            status = "MODERATE (Monitor Closely)"
        else:
            status = "HEALTHY"

        table_rows.append([
            f"PRD-{row['product_id']:03d}",
            row["product_name"],
            row["category"],
            f"{stock:,} units",
            status
        ])

    print_table(headers, table_rows, alignments=["L", "L", "L", "R", "L"])

# -------------------------------------------------------------------------
# Insight 4: Category-Wise Performance Summary
# -------------------------------------------------------------------------
def analyze_category_summary(conn):
    """
    Aggregates performance by category (Total Produced, Total Sold, Revenue).
    """
    print_section_header("4. Category-Wise Performance Summary")

    query = """
        SELECT 
            p.category,
            COUNT(DISTINCT p.product_id) AS product_count,
            COALESCE(SUM(prod.units_produced), 0) AS total_produced,
            COALESCE(SUM(sales.units_sold), 0) AS total_sold,
            COALESCE(SUM(sales.units_sold * p.unit_price), 0) AS total_revenue
        FROM products p
        LEFT JOIN production prod ON p.product_id = prod.product_id
        LEFT JOIN sales ON p.product_id = sales.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC;
    """

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    headers = ["Category", "Products", "Total Produced", "Total Sold", "Total Revenue"]
    table_rows = []

    for row in results:
        table_rows.append([
            row["category"],
            str(row["product_count"]),
            f"{int(row['total_produced']):,}",
            f"{int(row['total_sold']):,}",
            format_currency(float(row["total_revenue"]))
        ])

    print_table(headers, table_rows, alignments=["L", "R", "R", "R", "R"])

# -------------------------------------------------------------------------
# Main Execution Entry Point
# -------------------------------------------------------------------------
def run_all_analytics():
    """Connects to MySQL and executes all analytics reports."""
    conn = get_db_connection(include_database=True)
    if not conn:
        print("[FAILED] Could not run analytics: Database connection failed.")
        return False

    try:
        analyze_high_demand_products(conn)
        analyze_production_sales_gap(conn)
        analyze_inventory_stock_levels(conn)
        analyze_category_summary(conn)
        print("\n" + "=" * 80)
        print(" [COMPLETED] All analytics reports generated successfully.")
        print("=" * 80 + "\n")
        return True
    finally:
        conn.close()

if __name__ == "__main__":
    run_all_analytics()
