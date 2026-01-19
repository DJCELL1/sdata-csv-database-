"""
Configuration file for database selection
"""

import streamlit as st

# Database configuration
# Options: "csv" or "gsheets"
DATABASE_TYPE = "gsheets"  # Change to "csv" for local CSV storage

# CSV settings
CSV_PATH = "shared_data.csv"

# Google Sheets settings
GSHEETS_SPREADSHEET_NAME = "SDATA Database"
GSHEETS_WORKSHEET_NAME = "data"


def get_database():
    """
    Get the configured database instance.

    Returns:
        Database instance (CSVDatabase or GoogleSheetsDatabase)
    """
    if DATABASE_TYPE == "gsheets":
        from gsheets_db import GoogleSheetsDatabase
        return GoogleSheetsDatabase(
            spreadsheet_name=GSHEETS_SPREADSHEET_NAME,
            worksheet_name=GSHEETS_WORKSHEET_NAME
        )
    else:
        from csv_db import CSVDatabase
        return CSVDatabase(db_path=CSV_PATH)
