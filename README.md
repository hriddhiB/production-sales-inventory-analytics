# Production, Sales & Inventory Analytics Dashboard

A modern, interactive Python & MySQL application for tracking manufacturing output, sales demand, and warehouse stock levels.

Features both an **Interactive Streamlit Web Dashboard** and a **Lightweight Terminal CLI System**. It comes pre-loaded with sample data so you can run and explore the web dashboard immediately without needing MySQL configured first!

---

## 📁 Project Structure

```text
inventory_analytics/
│
├── app.py                 # 🚀 Interactive Streamlit Web Dashboard (Pre-loaded data)
├── main.py                # Interactive CLI menu with one-click launcher
├── config.py              # Central MySQL connection credentials & helper
├── schema.sql             # Pure SQL DDL queries for database and table creation
├── database_setup.py      # Automated database and table creation script
├── seed_data.py           # Populates clean sample records in MySQL
├── analytics.py           # Core business analytics & formatted terminal reports
└── README.md              # Project documentation and guide
```

---

## 🚀 How to Launch the Streamlit Web Dashboard

### 1. Open Terminal (PowerShell or Command Prompt)
Navigate to the project folder:
```powershell
cd "C:\Users\RAJIB KUMAR BARUA\.gemini\antigravity\scratch\inventory_analytics"
```

### 2. Start Streamlit
Run:
```powershell
streamlit run app.py
```
*(Or run `python main.py` and select option `5`!)*

Your browser will automatically open to **`http://localhost:8501`**.

---

## ✨ Dashboard Highlights

- **Pre-loaded Sample Data (Instant Mode)**:
  - Works out-of-the-box on first launch with 8 manufacturing products, 16 production batches, and 16 sales orders.
  - No database setup required to start exploring visual charts!
- **Optional Live MySQL Switch**:
  - In the sidebar, toggle between *Pre-loaded Sample Data* and *Live MySQL Database (`inventory_analytics`)*.
- **Top Executive KPIs**:
  - Total Units Produced, Total Units Sold, Total Revenue (₹), Current Stock, and Average Sell-Through Rate.
- **Interactive Tabs**:
  1. **📊 Production vs. Sales Gap**: Grouped bar charts comparing production against sales volume, net gap calculation, and automated surplus/shortage recommendations.
  2. **🏆 High-Demand Products**: Demand rankings by volume, revenue contribution donut chart, and bestseller breakdown.
  3. **📦 Inventory Health & Alerts**: Warehouse stock level bars with a 50-unit safety threshold line and critical low-stock warnings.
  4. **🏷️ Category Breakdown & Raw Data**: Revenue by category and inspection tables for products, production, and sales.
