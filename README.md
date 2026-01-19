# Simple Database for Streamlit Apps

A lightweight database system that can be shared across multiple Streamlit applications. Supports both CSV (local) and Google Sheets (persistent cloud storage).

## Files

- **`csv_db.py`** - CSV database module with CRUD operations
- **`gsheets_db.py`** - Google Sheets database module with CRUD operations
- **`config.py`** - Database configuration (switch between CSV and Google Sheets)
- **`database_manager.py`** - Main Streamlit app for managing the database
- **`example_app.py`** - Example client app showing how to connect
- **`shared_data.csv`** - CSV database file (created automatically if using CSV mode)
- **`GOOGLE_SHEETS_SETUP.md`** - Complete guide for setting up Google Sheets storage

## Installation

Install the required dependencies:

```bash
pip install streamlit pandas
```

## Usage

### 1. Run the Database Manager

```bash
streamlit run database_manager.py
```

This app allows you to:
- View all records
- Upload CSV files (including Cin7 product exports)
- Add new records
- Update existing records
- Delete records
- Search for records

### 2. Run the Example Client App (in a separate terminal)

```bash
streamlit run example_app.py
```

This demonstrates how other apps can connect to the same database.

### 3. Create Your Own App

To connect any Streamlit app to the database, simply import and use the CSVDatabase class:

```python
from csv_db import CSVDatabase

# Connect to the database
db = CSVDatabase("shared_data.csv")

# Read all data
df = db.read_all()

# Add a record
db.add_record({"name": "John", "age": "30", "email": "john@example.com"})

# Update a record
db.update_record(record_id=1, data={"name": "Jane"})

# Delete a record
db.delete_record(record_id=1)

# Search records
results = db.search(column="name", value="John")
```

## Features

- **Auto-generated IDs** - Each record gets a unique ID automatically
- **Timestamps** - Automatic timestamp tracking for create/update operations
- **Dynamic Schema** - Add any columns you want, schema evolves with your data
- **Multiple App Support** - Multiple Streamlit apps can read/write to the same CSV
- **Simple API** - Easy-to-use CRUD operations

## Storage Options

### CSV Mode (Local Development)
- Fast and simple
- No setup required
- Data stored in `shared_data.csv`
- **Not persistent** on Streamlit Cloud (resets on app restart)

### Google Sheets Mode (Production/Cloud)
- **Persistent** cloud storage
- Data survives app restarts
- Can view/edit directly in Google Sheets
- Free for reasonable usage
- Requires Google Cloud setup (see `GOOGLE_SHEETS_SETUP.md`)

To switch between modes, edit `config.py`:
```python
DATABASE_TYPE = "gsheets"  # or "csv"
```

## Notes

- Data is shared across all apps using the same database
- Google Sheets mode is recommended for Streamlit Cloud deployment
- Suitable for small to medium datasets (< 100K records)
- For larger datasets, consider PostgreSQL (Supabase, etc.)

## Uploading Cin7 Product Exports

1. Export products from Cin7 as CSV
2. Run the Database Manager app
3. Select "Upload CSV (Cin7)" from the operations menu
4. Drag and drop or browse to select your CSV file
5. Preview the data and choose import mode:
   - **Append**: Add records to existing data
   - **Replace**: Clear database and import only new data
6. Click "Import Data"

The system automatically:
- Assigns unique IDs to each record
- Adds timestamps for tracking
- Preserves all columns from your Cin7 export
- Makes data available to all connected apps

## Example Use Cases

- Cin7 product inventory management
- Simple inventory management
- Contact management system
- Task tracking across multiple apps
- Data collection from multiple forms
- Shared configuration storage
