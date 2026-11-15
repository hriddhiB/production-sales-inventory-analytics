"""
config.py
---------
Configuration file storing MySQL database credentials.
Beginners can update their MySQL password and host here in one single place.
"""

import mysql.connector
from mysql.connector import Error

# Database connection parameters
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Hbnit_05",   # Update with your MySQL root password if different
    "database": "inventory_analytics"
}

def get_db_connection(include_database=True):
    """
    Creates and returns a MySQL database connection.
    
    Parameters:
        include_database (bool): If True, connects directly to 'inventory_analytics'.
                                If False, connects to MySQL server without selecting a DB
                                (useful when creating the database for the first time).
    
    Returns:
        mysql.connector.connection_cext.CMySQLConnection: An active database connection object,
        or None if connection fails.
    """
    config = DB_CONFIG.copy()
    if not include_database:
        config.pop("database", None)

    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print(f"\n[ERROR] Could not connect to MySQL server: {e}")
        print("Please check:")
        print(" 1. Is your MySQL server running? (e.g. MySQL Service / XAMPP / MySQL Workbench)")
        print(f" 2. Are credentials correct? (User: {config.get('user')}, Host: {config.get('host')})")
        print(" 3. Update 'config.py' if your password is different.")
        return None
