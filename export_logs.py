#!/usr/bin/env python3
"""
Exports logs from SQLite database to CSV and XLSX.

Usage:
    python export_logs.py --db logs.db --csv logs.csv --xlsx logs.xlsx
"""

import sqlite3
import pandas as pd
import argparse
import os

def export_logs(db_path, csv_path=None, xlsx_path=None):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")

    # Read logs table into DataFrame
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY id ASC;", conn)
    conn.close()

    if df.empty:
        print("⚠️ No records found in the logs table.")
        return

    # Export to CSV
    if csv_path:
        df.to_csv(csv_path, index=False)
        print(f"✅ Exported {len(df)} rows to {csv_path}")

    # Export to XLSX
    if xlsx_path:
        df.to_excel(xlsx_path, index=False, engine="openpyxl")
        print(f"✅ Exported {len(df)} rows to {xlsx_path}")

def main():
    parser = argparse.ArgumentParser(description="Export SQLite logs to CSV/XLSX")
    parser.add_argument("--db", default="logs.db", help="Path to SQLite database")
    parser.add_argument("--csv", default="logs.csv", help="Path to output CSV file")
    parser.add_argument("--xlsx", default="logs.xlsx", help="Path to output Excel file")
    args = parser.parse_args()

    export_logs(args.db, args.csv, args.xlsx)

if __name__ == "__main__":
    main()
