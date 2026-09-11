CREATE DATABASE manufacturing_analytics;
USE manufacturing_analytics;
CREATE TABLE products(
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    unit_price DECIMAL(10,2)
);
CREATE TABLE production(
    production_id INT PRIMARY KEY,
    product_id INT,
    production_date DATE,
    quantity_produced INT,
    FOREIGN KEY (product_id) REFERENCES products(product_id) -- foreign key connects the product id with other tables
);
CREATE TABLE sales(
    sale_id INT PRIMARY KEY,
    product_id INT,
    sale_date DATE,
    quantity_sold INT,
    FOREIGN KEY (product_id) REFERENCES products(product_id) -- foreign key connects the product id with other tables
);
SHOW TABLES;
INSERT INTO products VALUES
(1, 'Gear Assembly', 'Mechanical', 1200.00),
(2, 'Shaft', 'Mechanical', 800.00),
(3, 'Bearing Housing', 'Component', 1500.00),
(4, 'Coupling', 'Mechanical', 950.00),
(5, 'Pulley', 'Mechanical', 700.00),
(6, 'Bracket', 'Component', 450.00);

SELECT*FROM products;

INSERT INTO production VALUES
(1, 1, '2026-09-01', 500),
(2, 2, '2026-09-01', 700),
(3, 3, '2026-09-01', 300),
(4, 4, '2026-09-02', 450),
(5, 5, '2026-09-02', 600),
(6, 6, '2026-09-02', 800),
(7, 1, '2026-09-03', 550),
(8, 2, '2026-09-03', 750),
(9, 3, '2026-09-03', 350),
(10, 4, '2026-09-04', 500),
(11, 5, '2026-09-04', 650),
(12, 6, '2026-09-04', 900);

SELECT*FROM production;

INSERT INTO sales VALUES
(1, 1, '2026-09-02', 420),
(2, 2, '2026-09-02', 600),
(3, 3, '2026-09-02', 250),
(4, 4, '2026-09-03', 380),
(5, 5, '2026-09-03', 500),
(6, 6, '2026-09-03', 650),
(7, 1, '2026-09-04', 450),
(8, 2, '2026-09-04', 620),
(9, 3, '2026-09-04', 280),
(10, 4, '2026-09-05', 420),
(11, 5, '2026-09-05', 550),
(12, 6, '2026-09-05', 700);

SELECT*FROM sales;

SELECT 
    product_id,
    SUM(quantity_produced) AS total_produced
FROM production
GROUP BY product_id;

SELECT
    product_id,
    SUM(quantity_sold) AS total_sold
FROM sales
GROUP BY product_id;

SELECT
    p.product_name,
    SUM(s.quantity_sold) AS total_sold
FROM products p
JOIN sales s
ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name;

SELECT
    p.product_name,                                  
    p.unit_price,                                    -- show the unit price
    SUM(s.quantity_sold) AS total_sold,              -- SUM = add all sold quantities
    p.unit_price * SUM(s.quantity_sold) AS total_revenue -- * = multiplication
FROM products p                                      -- FROM = take data from products
JOIN sales s                                          -- JOIN = connect another table
ON p.product_id = s.product_id                        -- ON = tell SQL how to connect them
GROUP BY p.product_id, p.product_name, p.unit_price; -- GROUP BY = make a group for each product

SELECT
    p.product_name,
    pr.total_produced,
    s.total_sold,
    pr.total_produced - s.total_sold AS inventory
FROM products p

JOIN (
    SELECT
        product_id,
        SUM(quantity_produced) AS total_produced
    FROM production
    GROUP BY product_id
) pr
ON p.product_id = pr.product_id

JOIN (
    SELECT
        product_id,
        SUM(quantity_sold) AS total_sold
    FROM sales
    GROUP BY product_id
) s
ON p.product_id = s.product_id;

SELECT
    p.product_name,
    SUM(s.quantity_sold) AS total_sold
FROM products p
JOIN sales s
ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_sold DESC
LIMIT 1;

SELECT
    p.product_name,
    SUM(s.quantity_sold) AS total_sold,
    p.unit_price * SUM(s.quantity_sold) AS total_revenue
FROM products p
JOIN sales s
ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.unit_price
ORDER BY total_revenue DESC
LIMIT 1;

SELECT
    p.product_name,
    pr.total_produced,
    s.total_sold,
    pr.total_produced - s.total_sold AS inventory
FROM products p
JOIN (
    SELECT
        product_id,
        SUM(quantity_produced) AS total_produced
    FROM production
    GROUP BY product_id
) pr
ON p.product_id = pr.product_id
JOIN (
    SELECT
        product_id,
        SUM(quantity_sold) AS total_sold
    FROM sales
    GROUP BY product_id
) s
ON p.product_id = s.product_id
WHERE pr.total_produced - s.total_sold > 200;

SELECT
    SUM(s.quantity_sold * p.unit_price) AS total_revenue
FROM sales s
JOIN products p
ON s.product_id = p.product_id;

SELECT
    AVG(quantity_sold) AS average_units_sold
FROM sales;

SELECT
    COUNT(*) AS total_sales_records
FROM sales;

SELECT
    MAX(quantity_produced) AS highest_production,
    MIN(quantity_produced) AS lowest_production
FROM production;

SELECT
    production_date,
    SUM(quantity_produced) AS total_produced
FROM production
GROUP BY production_date
ORDER BY production_date;