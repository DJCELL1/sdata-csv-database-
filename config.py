"""
Configuration file for database selection
"""

import streamlit as st
import os

# Database configuration
# Options: "csv" or "gsheets"
DATABASE_TYPE = "gsheets"  # Change to "csv" for local CSV storage

# CSV settings
CSV_PATH = "shared_data.csv"

# Google Sheets settings
GSHEETS_SPREADSHEET_NAME = "SDATA Database"
GSHEETS_WORKSHEET_NAME = "data"


def check_gsheets_credentials():
    """Check if Google Sheets credentials are available."""
    # Check for Streamlit secrets (Cloud deployment)
    if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
        return True
    # Check for local credentials file
    if os.path.exists('credentials.json'):
        return True
    return False


def get_database():
    """
    Get the configured database instance.

    Returns:
        Database instance (CSVDatabase or GoogleSheetsDatabase)
    """
    if DATABASE_TYPE == "gsheets":
        # Check if credentials are available
        if not check_gsheets_credentials():
            st.warning("⚠️ Google Sheets credentials not found. Falling back to CSV mode.")
            st.info("To use Google Sheets, please follow the setup guide in GOOGLE_SHEETS_SETUP.md")
            from csv_db import CSVDatabase
            return CSVDatabase(db_path=CSV_PATH)

        try:
            from gsheets_db import GoogleSheetsDatabase
            return GoogleSheetsDatabase(
                spreadsheet_name=GSHEETS_SPREADSHEET_NAME,
                worksheet_name=GSHEETS_WORKSHEET_NAME
            )
        except Exception as e:
            st.error(f"Failed to connect to Google Sheets: {str(e)}")
            st.warning("Falling back to CSV mode.")
            from csv_db import CSVDatabase
            return CSVDatabase(db_path=CSV_PATH)
    else:
        from csv_db import CSVDatabase
        return CSVDatabase(db_path=CSV_PATH)
