-- =====================================================================
-- Production, Sales & Inventory Analytics
-- Relational Database Schema & Analytical Queries
-- =====================================================================

-- Step 1: Database Initialization
CREATE DATABASE IF NOT EXISTS inventory_analytics;
USE inventory_analytics;

-- Step 2: Create Tables
-- 1. Products Catalog Table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);

-- 2. Production Batches Table
CREATE TABLE IF NOT EXISTS production (
    production_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    units_produced INT NOT NULL,
    production_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- 3. Sales Transactions Table
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    units_sold INT NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- 4. Inventory Stock Table
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL UNIQUE,
    stock_level INT NOT NULL DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- =====================================================================
-- Step 3: Populate Sample Data
-- =====================================================================

INSERT INTO products (product_id, product_name, category, unit_price) VALUES
(1, 'Gear Assembly', 'Mechanical', 1200.00),
(2, 'Shaft', 'Mechanical', 800.00),
(3, 'Bearing Housing', 'Component', 1500.00),
(4, 'Coupling', 'Mechanical', 950.00),
(5, 'Pulley', 'Mechanical', 700.00),
(6, 'Bracket', 'Component', 450.00),
(7, 'Hydraulic Valve', 'Hydraulics', 2100.00),
(8, 'Industrial Sensor', 'Electronics', 1850.00)
ON DUPLICATE KEY UPDATE 
    product_name = VALUES(product_name),
    category = VALUES(category),
    unit_price = VALUES(unit_price);

INSERT INTO production (production_id, product_id, units_produced, production_date) VALUES
(1,  1, 500, '2026-09-01'),
(2,  2, 700, '2026-09-01'),
(3,  3, 300, '2026-09-01'),
(4,  4, 450, '2026-09-02'),
(5,  5, 600, '2026-09-02'),
(6,  6, 800, '2026-09-02'),
(7,  1, 550, '2026-09-03'),
(8,  2, 750, '2026-09-03'),
(9,  3, 350, '2026-09-03'),
(10, 4, 500, '2026-09-04'),
(11, 5, 650, '2026-09-04'),
(12, 6, 900, '2026-09-04'),
(13, 7, 200, '2026-09-05'),
(14, 8, 400, '2026-09-05'),
(15, 7, 250, '2026-09-06'),
(16, 8, 450, '2026-09-06')
ON DUPLICATE KEY UPDATE units_produced = VALUES(units_produced);

INSERT INTO sales (sale_id, product_id, units_sold, sale_date) VALUES
(1,  1, 420, '2026-09-02'),
(2,  2, 600, '2026-09-02'),
(3,  3, 250, '2026-09-02'),
(4,  4, 380, '2026-09-03'),
(5,  5, 500, '2026-09-03'),
(6,  6, 650, '2026-09-03'),
(7,  1, 450, '2026-09-04'),
(8,  2, 620, '2026-09-04'),
(9,  3, 280, '2026-09-04'),
(10, 4, 420, '2026-09-05'),
(11, 5, 550, '2026-09-05'),
(12, 6, 700, '2026-09-05'),
(13, 7, 240, '2026-09-07'),
(14, 8, 390, '2026-09-07'),
(15, 7, 200, '2026-09-08'),
(16, 8, 410, '2026-09-08')
ON DUPLICATE KEY UPDATE units_sold = VALUES(units_sold);

-- Sync initial inventory (Stock = Produced - Sold)
INSERT INTO inventory (product_id, stock_level)
SELECT 
    p.product_id,
    COALESCE(prod.total_produced, 0) - COALESCE(s.total_sold, 0) AS stock_level
FROM products p
LEFT JOIN (
    SELECT product_id, SUM(units_produced) AS total_produced
    FROM production GROUP BY product_id
) prod ON p.product_id = prod.product_id
LEFT JOIN (
    SELECT product_id, SUM(units_sold) AS total_sold
    FROM sales GROUP BY product_id
) s ON p.product_id = s.product_id
ON DUPLICATE KEY UPDATE stock_level = VALUES(stock_level);

-- =====================================================================
-- Step 4: Analytical Queries
-- =====================================================================

-- 1. High-Demand Products (Ranked by Total Units Sold)
SELECT
    p.product_name,
    p.category,
    p.unit_price,
    SUM(s.units_sold) AS total_units_sold,
    SUM(s.units_sold * p.unit_price) AS total_revenue
FROM products p
JOIN sales s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.category, p.unit_price
ORDER BY total_units_sold DESC;

-- 2. Production vs. Sales Gap Analysis (Spotting Excess Stock & Shortages)
SELECT
    p.product_name,
    pr.total_produced,
    s.total_sold,
    (pr.total_produced - s.total_sold) AS net_inventory_gap,
    ROUND((s.total_sold / pr.total_produced) * 100, 1) AS sell_through_pct,
    CASE 
        WHEN (pr.total_produced - s.total_sold) > 150 THEN 'Excess Surplus'
        WHEN (pr.total_produced - s.total_sold) >= 50 THEN 'Balanced Buffer'
        ELSE 'Tight Inventory'
    END AS status
FROM products p
JOIN (
    SELECT product_id, SUM(units_produced) AS total_produced
    FROM production
    GROUP BY product_id
) pr ON p.product_id = pr.product_id
JOIN (
    SELECT product_id, SUM(units_sold) AS total_sold
    FROM sales
    GROUP BY product_id
) s ON p.product_id = s.product_id
ORDER BY net_inventory_gap DESC;

-- 3. Top Best-Selling Product (Limit 1)
SELECT
    p.product_name,
    SUM(s.units_sold) AS total_sold
FROM products p
JOIN sales s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_sold DESC
LIMIT 1;

-- 4. Highest Revenue Generating Product
SELECT
    p.product_name,
    p.unit_price,
    SUM(s.units_sold) AS total_sold,
    SUM(s.units_sold * p.unit_price) AS total_revenue
FROM products p
JOIN sales s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.unit_price
ORDER BY total_revenue DESC
LIMIT 1;

-- 5. Products with Excess Inventory (> 150 Units)
SELECT
    p.product_name,
    (pr.total_produced - s.total_sold) AS excess_units
FROM products p
JOIN (
    SELECT product_id, SUM(units_produced) AS total_produced FROM production GROUP BY product_id
) pr ON p.product_id = pr.product_id
JOIN (
    SELECT product_id, SUM(units_sold) AS total_sold FROM sales GROUP BY product_id
) s ON p.product_id = s.product_id
WHERE (pr.total_produced - s.total_sold) > 150;

-- 6. Total Overall Revenue
SELECT
    SUM(s.units_sold * p.unit_price) AS total_portfolio_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id;

-- 7. Daily Production Trend
SELECT
    production_date,
    SUM(units_produced) AS total_produced_on_date
FROM production
GROUP BY production_date
ORDER BY production_date ASC;
