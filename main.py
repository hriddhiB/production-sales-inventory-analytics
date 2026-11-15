"""
main.py
-------
Interactive Master Console Application for Production, Sales & Inventory Analytics.
Allows beginners to execute each step (setup, seed, analytics, or launch web dashboard).
"""

import sys
import subprocess
from database_setup import setup_database
from seed_data import populate_sample_data
from analytics import run_all_analytics
from config import DB_CONFIG

def show_menu():
    print("\n" + "=" * 60)
    print(" PRODUCTION, SALES & INVENTORY ANALYTICS SYSTEM")
    print(f" Target Database: '{DB_CONFIG['database']}' on '{DB_CONFIG['host']}'")
    print("=" * 60)
    print("  [1] Setup Database & Tables (Create MySQL schema)")
    print("  [2] Populate / Reset Sample Data (Insert dummy records)")
    print("  [3] Run Terminal Analytics & Insights (Text reports)")
    print("  [4] Run Full Database Pipeline (1 -> 2 -> 3)")
    print("  [5] 🚀 Launch Interactive Streamlit Web Dashboard")
    print("  [6] Exit Application")
    print("=" * 60)

def launch_dashboard():
    print("\nLaunching Streamlit Web Dashboard in your browser...")
    print("Press Ctrl+C in terminal when you wish to stop the dashboard server.\n")
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    except FileNotFoundError:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

def main():
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            setup_database()
        elif choice == "2":
            populate_sample_data()
        elif choice == "3":
            run_all_analytics()
        elif choice == "4":
            print("\n>>> Running Full Pipeline...")
            if setup_database():
                if populate_sample_data():
                    run_all_analytics()
        elif choice == "5":
            launch_dashboard()
        elif choice == "6":
            print("\nExiting application. Happy Analyzing!\n")
            sys.exit(0)
        else:
            print("\n[!] Invalid selection. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
