"""
app.py
------
Production, Sales & Inventory Analytics Dashboard
Built with Streamlit & Plotly.

Features:
- Comes pre-loaded with rich sample data out of the box (works instantly!).
- Optional toggle to connect to live MySQL ('inventory_analytics').
- Real-time KPI summary cards.
- Interactive Production vs. Sales Gap comparison.
- High-demand product rankings and revenue analysis.
- Warehouse stock levels with low-stock alerts.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Production, Sales & Inventory Analytics",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 1. PRE-LOADED SAMPLE DATASETS (Instant Out-of-the-Box Mode)
# -----------------------------------------------------------------------------
DEFAULT_PRODUCTS = [
    {"product_id": 1, "product_name": "Gear Assembly", "category": "Mechanical", "unit_price": 1200.00},
    {"product_id": 2, "product_name": "Shaft", "category": "Mechanical", "unit_price": 800.00},
    {"product_id": 3, "product_name": "Bearing Housing", "category": "Component", "unit_price": 1500.00},
    {"product_id": 4, "product_name": "Coupling", "category": "Mechanical", "unit_price": 950.00},
    {"product_id": 5, "product_name": "Pulley", "category": "Mechanical", "unit_price": 700.00},
    {"product_id": 6, "product_name": "Bracket", "category": "Component", "unit_price": 450.00},
    {"product_id": 7, "product_name": "Hydraulic Valve", "category": "Hydraulics", "unit_price": 2100.00},
    {"product_id": 8, "product_name": "Industrial Sensor", "category": "Electronics", "unit_price": 1850.00},
]

DEFAULT_PRODUCTION = [
    {"production_id": 1,  "product_id": 1, "units_produced": 500, "production_date": "2026-09-01"},
    {"production_id": 2,  "product_id": 2, "units_produced": 700, "production_date": "2026-09-01"},
    {"production_id": 3,  "product_id": 3, "units_produced": 300, "production_date": "2026-09-01"},
    {"production_id": 4,  "product_id": 4, "units_produced": 450, "production_date": "2026-09-02"},
    {"production_id": 5,  "product_id": 5, "units_produced": 600, "production_date": "2026-09-02"},
    {"production_id": 6,  "product_id": 6, "units_produced": 800, "production_date": "2026-09-02"},
    {"production_id": 7,  "product_id": 1, "units_produced": 550, "production_date": "2026-09-03"},
    {"production_id": 8,  "product_id": 2, "units_produced": 750, "production_date": "2026-09-03"},
    {"production_id": 9,  "product_id": 3, "units_produced": 350, "production_date": "2026-09-03"},
    {"production_id": 10, "product_id": 4, "units_produced": 500, "production_date": "2026-09-04"},
    {"production_id": 11, "product_id": 5, "units_produced": 650, "production_date": "2026-09-04"},
    {"production_id": 12, "product_id": 6, "units_produced": 900, "production_date": "2026-09-04"},
    {"production_id": 13, "product_id": 7, "units_produced": 200, "production_date": "2026-09-05"},
    {"production_id": 14, "product_id": 8, "units_produced": 400, "production_date": "2026-09-05"},
    {"production_id": 15, "product_id": 7, "units_produced": 250, "production_date": "2026-09-06"},
    {"production_id": 16, "product_id": 8, "units_produced": 450, "production_date": "2026-09-06"},
]

DEFAULT_SALES = [
    {"sale_id": 1,  "product_id": 1, "units_sold": 420, "sale_date": "2026-09-02"},
    {"sale_id": 2,  "product_id": 2, "units_sold": 600, "sale_date": "2026-09-02"},
    {"sale_id": 3,  "product_id": 3, "units_sold": 250, "sale_date": "2026-09-02"},
    {"sale_id": 4,  "product_id": 4, "units_sold": 380, "sale_date": "2026-09-03"},
    {"sale_id": 5,  "product_id": 5, "units_sold": 500, "sale_date": "2026-09-03"},
    {"sale_id": 6,  "product_id": 6, "units_sold": 650, "sale_date": "2026-09-03"},
    {"sale_id": 7,  "product_id": 1, "units_sold": 450, "sale_date": "2026-09-04"},
    {"sale_id": 8,  "product_id": 2, "units_sold": 620, "sale_date": "2026-09-04"},
    {"sale_id": 9,  "product_id": 3, "units_sold": 280, "sale_date": "2026-09-04"},
    {"sale_id": 10, "product_id": 4, "units_sold": 420, "sale_date": "2026-09-05"},
    {"sale_id": 11, "product_id": 5, "units_sold": 550, "sale_date": "2026-09-05"},
    {"sale_id": 12, "product_id": 6, "units_sold": 700, "sale_date": "2026-09-05"},
    {"sale_id": 13, "product_id": 7, "units_sold": 240, "sale_date": "2026-09-07"},
    {"sale_id": 14, "product_id": 8, "units_sold": 390, "sale_date": "2026-09-07"},
    {"sale_id": 15, "product_id": 7, "units_sold": 200, "sale_date": "2026-09-08"},
    {"sale_id": 16, "product_id": 8, "units_sold": 410, "sale_date": "2026-09-08"},
]

def load_sample_dataframe():
    """Builds pre-computed analytical dataframes from sample data."""
    df_products = pd.DataFrame(DEFAULT_PRODUCTS)
    df_production = pd.DataFrame(DEFAULT_PRODUCTION)
    df_sales = pd.DataFrame(DEFAULT_SALES)

    # Compute production totals
    prod_summary = df_production.groupby("product_id")["units_produced"].sum().reset_index()
    # Compute sales totals
    sales_summary = df_sales.groupby("product_id")["units_sold"].sum().reset_index()

    # Merge everything
    df_master = df_products.merge(prod_summary, on="product_id", how="left").fillna(0)
    df_master = df_master.merge(sales_summary, on="product_id", how="left").fillna(0)

    df_master["units_produced"] = df_master["units_produced"].astype(int)
    df_master["units_sold"] = df_master["units_sold"].astype(int)
    df_master["stock_level"] = df_master["units_produced"] - df_master["units_sold"]
    df_master["gap"] = df_master["stock_level"]
    df_master["revenue"] = df_master["units_sold"] * df_master["unit_price"]
    df_master["sell_through_rate"] = (
        (df_master["units_sold"] / df_master["units_produced"]) * 100
    ).round(1)

    return df_master, df_products, df_production, df_sales

# -----------------------------------------------------------------------------
# 2. OPTIONAL MYSQL LIVE CONNECTOR
# -----------------------------------------------------------------------------
def load_mysql_data(host, user, password, database):
    """Attempts to connect to live MySQL database."""
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        df_products = pd.read_sql("SELECT * FROM products", conn)
        df_production = pd.read_sql("SELECT * FROM production", conn)
        df_sales = pd.read_sql("SELECT * FROM sales", conn)
        conn.close()

        prod_summary = df_production.groupby("product_id")["units_produced"].sum().reset_index()
        sales_summary = df_sales.groupby("product_id")["units_sold"].sum().reset_index()

        df_master = df_products.merge(prod_summary, on="product_id", how="left").fillna(0)
        df_master = df_master.merge(sales_summary, on="product_id", how="left").fillna(0)

        df_master["units_produced"] = df_master["units_produced"].astype(int)
        df_master["units_sold"] = df_master["units_sold"].astype(int)
        df_master["stock_level"] = df_master["units_produced"] - df_master["units_sold"]
        df_master["gap"] = df_master["stock_level"]
        df_master["revenue"] = df_master["units_sold"] * df_master["unit_price"]
        df_master["sell_through_rate"] = (
            (df_master["units_sold"] / df_master["units_produced"]) * 100
        ).round(1)

        return df_master, df_products, df_production, df_sales, None
    except Exception as e:
        return None, None, None, None, str(e)

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2897/2897785.png", width=64)
    st.title("Settings & Filter")

    data_source = st.radio(
        "Data Source",
        ["🚀 Pre-loaded Sample Data (Instant)", "🗄️ Live MySQL Database"],
        help="Use pre-loaded sample data to run immediately, or connect to your local MySQL instance."
    )

    if data_source == "🗄️ Live MySQL Database":
        st.subheader("MySQL Credentials")
        db_host = st.text_input("Host", value="localhost")
        db_user = st.text_input("User", value="root")
        db_pass = st.text_input("Password", value="Hbnit_05", type="password")
        db_name = st.text_input("Database", value="inventory_analytics")

        df_master, df_products, df_production, df_sales, err = load_mysql_data(db_host, db_user, db_pass, db_name)
        if err:
            st.error(f"MySQL Error: {err}")
            st.info("Falling back to pre-loaded sample data so you can continue exploring.")
            df_master, df_products, df_production, df_sales = load_sample_dataframe()
        else:
            st.success("Connected to live MySQL!")
    else:
        df_master, df_products, df_production, df_sales = load_sample_dataframe()
        st.success("Loaded pre-populated sample dataset.")

    st.markdown("---")
    # Category Filter
    all_categories = sorted(df_master["category"].unique().tolist())
    selected_categories = st.multiselect(
        "Filter by Category",
        options=all_categories,
        default=all_categories
    )

    st.markdown("---")
    st.caption("Inventory Analytics Dashboard • Built with Python & Streamlit")

# Filter data
if not selected_categories:
    st.warning("Please select at least one category from the sidebar.")
    st.stop()

df_filtered = df_master[df_master["category"].isin(selected_categories)].copy()

# Status tagging
def tag_gap_status(gap):
    if gap > 150:
        return "Excess Surplus 📦"
    elif gap >= 50:
        return "Balanced Buffer 🟢"
    elif gap >= 0:
        return "Tight Stock ⚠️"
    else:
        return "Shortage Alert 🚨"

df_filtered["Status"] = df_filtered["gap"].apply(tag_gap_status)

# -----------------------------------------------------------------------------
# 4. MAIN DASHBOARD CONTENT
# -----------------------------------------------------------------------------
st.title("🏭 Production, Sales & Inventory Analytics")
st.markdown("Monitor real-time manufacturing batch production, sales demand, and warehouse inventory health.")

# Top KPIs
col1, col2, col3, col4, col5 = st.columns(5)

total_produced = int(df_filtered["units_produced"].sum())
total_sold = int(df_filtered["units_sold"].sum())
total_revenue = float(df_filtered["revenue"].sum())
total_stock = int(df_filtered["stock_level"].sum())
avg_sell_through = (total_sold / total_produced * 100) if total_produced > 0 else 0.0

col1.metric("Units Produced", f"{total_produced:,}")
col2.metric("Units Sold", f"{total_sold:,}")
col3.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col4.metric("Current Stock", f"{total_stock:,}")
col5.metric("Avg Sell-Through", f"{avg_sell_through:.1f}%")

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Production vs Sales Gap",
    "🏆 High-Demand Products",
    "📦 Inventory Health & Alerts",
    "🏷️ Category Breakdown & Raw Data"
])

# -----------------------------------------------------------------------------
# TAB 1: PRODUCTION VS SALES GAP
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Production vs. Sales Volume by Product")
    
    # Dual Bar Chart
    fig_gap = go.Figure()
    fig_gap.add_trace(go.Bar(
        x=df_filtered["product_name"],
        y=df_filtered["units_produced"],
        name="Units Produced",
        marker_color="#1E88E5"
    ))
    fig_gap.add_trace(go.Bar(
        x=df_filtered["product_name"],
        y=df_filtered["units_sold"],
        name="Units Sold",
        marker_color="#43A047"
    ))

    fig_gap.update_layout(
        barmode="group",
        xaxis_title="Product Name",
        yaxis_title="Units",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_gap, use_container_width=True)

    # Detailed Gap Table
    st.markdown("#### Production-Sales Gap Analysis Table")
    gap_display = df_filtered[[
        "product_name", "category", "units_produced", "units_sold", "gap", "sell_through_rate", "Status"
    ]].rename(columns={
        "product_name": "Product Name",
        "category": "Category",
        "units_produced": "Produced",
        "units_sold": "Sold",
        "gap": "Net Gap (Produced - Sold)",
        "sell_through_rate": "Sell-Through %",
        "Status": "Inventory Status"
    })
    st.dataframe(gap_display.sort_values(by="Net Gap (Produced - Sold)", ascending=False), use_container_width=True, hide_index=True)

    # Management Insights Callout
    excess_items = df_filtered[df_filtered["gap"] > 150]["product_name"].tolist()
    tight_items = df_filtered[df_filtered["gap"] <= 50]["product_name"].tolist()

    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**📦 Excess Surplus Items:** {', '.join(excess_items) if excess_items else 'None'}\n\n*Action: Consider pacing production down to avoid warehouse holding costs.*")
    with c2:
        st.warning(f"**⚠️ Low Buffer / Tight Items:** {', '.join(tight_items) if tight_items else 'None'}\n\n*Action: Prioritize manufacturing for these products to prevent stockouts.*")

# -----------------------------------------------------------------------------
# TAB 2: HIGH-DEMAND PRODUCTS
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Top Performing Products (Ranked by Demand)")

    c_left, c_right = st.columns([3, 2])

    with c_left:
        # Horizontal Bar Chart for Sales Volume
        df_sorted_sales = df_filtered.sort_values(by="units_sold", ascending=True)
        fig_demand = px.bar(
            df_sorted_sales,
            x="units_sold",
            y="product_name",
            orientation="h",
            color="units_sold",
            color_continuous_scale="Viridis",
            labels={"units_sold": "Units Sold", "product_name": "Product"},
            title="Sales Volume by Product"
        )
        fig_demand.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_demand, use_container_width=True)

    with c_right:
        # Revenue by Product Donut Chart
        fig_rev = px.pie(
            df_filtered,
            names="product_name",
            values="revenue",
            hole=0.45,
            title="Revenue Contribution Share",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_rev.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_rev, use_container_width=True)

    # Ranked Summary Table
    st.markdown("#### High-Demand Ranking Summary")
    high_demand_df = df_filtered[[
        "product_name", "category", "unit_price", "units_sold", "revenue"
    ]].sort_values(by="units_sold", ascending=False).reset_index(drop=True)
    high_demand_df.index += 1
    high_demand_df["unit_price"] = high_demand_df["unit_price"].apply(lambda x: f"₹{x:,.2f}")
    high_demand_df["revenue"] = high_demand_df["revenue"].apply(lambda x: f"₹{x:,.2f}")
    high_demand_df.columns = ["Product Name", "Category", "Unit Price", "Total Units Sold", "Total Revenue"]
    st.dataframe(high_demand_df, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 3: INVENTORY HEALTH & REORDER ALERTS
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Current Warehouse Stock Levels")

    fig_stock = px.bar(
        df_filtered.sort_values(by="stock_level", ascending=False),
        x="product_name",
        y="stock_level",
        color="stock_level",
        color_continuous_scale=["#E53935", "#FDD835", "#43A047"],
        labels={"stock_level": "Stock Level (Units)", "product_name": "Product"},
        title="Stock Level by Product"
    )
    # Add a horizontal line for threshold
    fig_stock.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="Safety Buffer (50 Units)")
    fig_stock.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_stock, use_container_width=True)

    st.markdown("#### Inventory Reorder Assessment")
    stock_df = df_filtered[["product_id", "product_name", "category", "stock_level"]].copy()
    stock_df["Reorder Status"] = stock_df["stock_level"].apply(
        lambda x: "🚨 CRITICAL LOW (Order Now)" if x <= 50 else ("⚠️ MODERATE" if x <= 100 else "🟢 HEALTHY")
    )
    stock_df.columns = ["Product ID", "Product Name", "Category", "Current Stock (Units)", "Reorder Status"]
    st.dataframe(stock_df.sort_values(by="Current Stock (Units)", ascending=True), use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 4: CATEGORY BREAKDOWN & RAW DATA
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Category-Wise Performance Overview")

    cat_summary = df_filtered.groupby("category").agg(
        Total_Products=("product_id", "count"),
        Total_Produced=("units_produced", "sum"),
        Total_Sold=("units_sold", "sum"),
        Total_Revenue=("revenue", "sum")
    ).reset_index()

    c_cat1, c_cat2 = st.columns(2)
    with c_cat1:
        fig_cat_rev = px.bar(
            cat_summary,
            x="category",
            y="Total_Revenue",
            color="category",
            labels={"Total_Revenue": "Total Revenue (₹)", "category": "Category"},
            title="Revenue by Category"
        )
        fig_cat_rev.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig_cat_rev, use_container_width=True)

    with c_cat2:
        cat_summary_display = cat_summary.copy()
        cat_summary_display["Total_Revenue"] = cat_summary_display["Total_Revenue"].apply(lambda x: f"₹{x:,.2f}")
        st.markdown("#### Category Metrics")
        st.dataframe(cat_summary_display, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Raw Data Tables")
    raw_tab1, raw_tab2, raw_tab3 = st.tabs(["Products", "Production Batches", "Sales Transactions"])
    with raw_tab1:
        st.dataframe(df_products, use_container_width=True, hide_index=True)
    with raw_tab2:
        st.dataframe(df_production, use_container_width=True, hide_index=True)
    with raw_tab3:
        st.dataframe(df_sales, use_container_width=True, hide_index=True)
