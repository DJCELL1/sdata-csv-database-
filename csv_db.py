"""
Simple CSV Database Module
Provides basic CRUD operations for CSV files that can be shared across multiple Streamlit apps.
"""

import pandas as pd
import os
from typing import Optional, List, Dict
from datetime import datetime


class CSVDatabase:
    """A simple CSV-based database with basic CRUD operations."""

    def __init__(self, db_path: str = "data.csv"):
        """
        Initialize the CSV database.

        Args:
            db_path: Path to the CSV file
        """
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Create the CSV file if it doesn't exist."""
        if not os.path.exists(self.db_path):
            # Create empty dataframe with default columns
            df = pd.DataFrame(columns=["id", "timestamp"])
            df.to_csv(self.db_path, index=False)

    def read_all(self) -> pd.DataFrame:
        """Read all data from the CSV file."""
        try:
            df = pd.read_csv(self.db_path)
            return df
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return pd.DataFrame()

    def add_record(self, data: Dict) -> bool:
        """
        Add a new record to the database.

        Args:
            data: Dictionary containing the record data

        Returns:
            True if successful, False otherwise
        """
        try:
            df = self.read_all()

            # Auto-generate ID
            if len(df) == 0:
                new_id = 1
            else:
                new_id = df["id"].max() + 1

            # Add timestamp
            data["id"] = new_id
            data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Append new record
            new_df = pd.DataFrame([data])
            df = pd.concat([df, new_df], ignore_index=True)

            df.to_csv(self.db_path, index=False)
            return True
        except Exception as e:
            print(f"Error adding record: {e}")
            return False

    def update_record(self, record_id: int, data: Dict) -> bool:
        """
        Update an existing record.

        Args:
            record_id: ID of the record to update
            data: Dictionary containing the updated data

        Returns:
            True if successful, False otherwise
        """
        try:
            df = self.read_all()

            if record_id not in df["id"].values:
                print(f"Record with ID {record_id} not found")
                return False

            # Update the record
            for key, value in data.items():
                if key != "id":  # Don't allow ID updates
                    df.loc[df["id"] == record_id, key] = value

            # Update timestamp
            df.loc[df["id"] == record_id, "timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            df.to_csv(self.db_path, index=False)
            return True
        except Exception as e:
            print(f"Error updating record: {e}")
            return False

    def delete_record(self, record_id: int) -> bool:
        """
        Delete a record from the database.

        Args:
            record_id: ID of the record to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            df = self.read_all()

            if record_id not in df["id"].values:
                print(f"Record with ID {record_id} not found")
                return False

            df = df[df["id"] != record_id]
            df.to_csv(self.db_path, index=False)
            return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False

    def search(self, column: str, value) -> pd.DataFrame:
        """
        Search for records matching a specific value in a column.

        Args:
            column: Column name to search in
            value: Value to search for

        Returns:
            DataFrame containing matching records
        """
        try:
            df = self.read_all()
            if column not in df.columns:
                print(f"Column {column} not found")
                return pd.DataFrame()

            return df[df[column] == value]
        except Exception as e:
            print(f"Error searching: {e}")
            return pd.DataFrame()

    def get_columns(self) -> List[str]:
        """Get list of all columns in the database."""
        df = self.read_all()
        return list(df.columns)

    def bulk_import(self, df_import: pd.DataFrame, mode: str = "append") -> bool:
        """
        Import data from a DataFrame in bulk.

        Args:
            df_import: DataFrame to import
            mode: 'append' to add to existing data, 'replace' to overwrite

        Returns:
            True if successful, False otherwise
        """
        try:
            if mode == "replace":
                # Add id and timestamp columns
                df_import = df_import.reset_index(drop=True)
                df_import.insert(0, "id", range(1, len(df_import) + 1))
                df_import["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df_import.to_csv(self.db_path, index=False)
            elif mode == "append":
                df_existing = self.read_all()

                # Get the next ID
                if len(df_existing) == 0:
                    next_id = 1
                else:
                    next_id = df_existing["id"].max() + 1

                # Add id and timestamp to imported data
                df_import = df_import.reset_index(drop=True)
                df_import.insert(0, "id", range(next_id, next_id + len(df_import)))
                df_import["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Combine with existing data
                df_combined = pd.concat([df_existing, df_import], ignore_index=True)
                df_combined.to_csv(self.db_path, index=False)

            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
