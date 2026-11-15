-- ========================================================
-- Database Schema: inventory_analytics
-- Purpose: Production, Sales & Inventory Analytics
-- ========================================================

-- Step 1: Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS inventory_analytics;
USE inventory_analytics;

-- Step 2: Create 'products' table
-- Stores master information about each item manufactured/sold
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);

-- Step 3: Create 'production' table
-- Tracks daily manufacturing batches for each product
CREATE TABLE IF NOT EXISTS production (
    production_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    units_produced INT NOT NULL,
    production_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- Step 4: Create 'sales' table
-- Tracks outbound sales transactions for each product
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    units_sold INT NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- Step 5: Create 'inventory' table
-- Tracks current stock levels for each product
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL UNIQUE,
    stock_level INT NOT NULL DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);
