"""
Database Manager - Main Streamlit app for managing the CSV database
"""

import streamlit as st
import pandas as pd
from csv_db import CSVDatabase

# Page configuration
st.set_page_config(
    page_title="CSV Database Manager",
    page_icon="🗄️",
    layout="wide"
)

# Initialize database
db = CSVDatabase("shared_data.csv")

# Title
st.title("🗄️ CSV Database Manager")
st.markdown("Manage your shared CSV database with CRUD operations")

# Sidebar for operations
st.sidebar.header("Operations")
operation = st.sidebar.radio(
    "Choose an operation:",
    ["View All", "Upload CSV (Cin7)", "Add Record", "Update Record", "Delete Record", "Search"]
)

# VIEW ALL RECORDS
if operation == "View All":
    st.header("📊 All Records")
    df = db.read_all()

    if len(df) > 0:
        st.dataframe(df, use_container_width=True)
        st.info(f"Total records: {len(df)}")

        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="database_export.csv",
            mime="text/csv"
        )
    else:
        st.warning("No records found in the database.")

# UPLOAD CSV (CIN7)
elif operation == "Upload CSV (Cin7)":
    st.header("📤 Upload CSV File")
    st.markdown("Upload a product export from Cin7 or any CSV file to import data into the database.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

    if uploaded_file is not None:
        try:
            # Read the uploaded CSV
            df_upload = pd.read_csv(uploaded_file)

            st.success(f"✅ File loaded successfully: {uploaded_file.name}")
            st.info(f"Found {len(df_upload)} records with {len(df_upload.columns)} columns")

            # Preview the data
            st.subheader("Preview of uploaded data:")
            st.dataframe(df_upload.head(10), use_container_width=True)

            # Show column information
            with st.expander("📋 Column Details"):
                col_info = pd.DataFrame({
                    "Column Name": df_upload.columns,
                    "Data Type": [str(df_upload[col].dtype) for col in df_upload.columns],
                    "Non-Null Count": [df_upload[col].notna().sum() for col in df_upload.columns],
                    "Sample Value": [str(df_upload[col].iloc[0]) if len(df_upload) > 0 else "" for col in df_upload.columns]
                })
                st.dataframe(col_info, use_container_width=True)

            # Import options
            st.subheader("Import Options:")

            col1, col2 = st.columns(2)

            with col1:
                import_mode = st.radio(
                    "Select import mode:",
                    ["Append to existing data", "Replace all existing data"],
                    help="Append: Add new records to existing database\nReplace: Delete all existing records and import only new data"
                )

            with col2:
                st.info(
                    "**Append Mode:**\n"
                    "- Keeps existing records\n"
                    "- Adds new records\n\n"
                    "**Replace Mode:**\n"
                    "- Deletes all existing data\n"
                    "- Imports only uploaded data"
                )

            # Confirmation and import
            if import_mode == "Replace all existing data":
                st.warning("⚠️ **Warning**: This will delete all existing records in the database!")

            # Show what will happen
            current_df = db.read_all()
            current_count = len(current_df)

            if import_mode == "Append to existing data":
                st.info(f"Current records: {current_count} → After import: {current_count + len(df_upload)}")
            else:
                st.info(f"Current records: {current_count} → After import: {len(df_upload)}")

            # Import button
            col_a, col_b, col_c = st.columns([1, 1, 2])

            with col_a:
                if st.button("📥 Import Data", type="primary"):
                    mode = "append" if import_mode == "Append to existing data" else "replace"

                    with st.spinner("Importing data..."):
                        if db.bulk_import(df_upload, mode=mode):
                            st.success(f"✅ Successfully imported {len(df_upload)} records!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Failed to import data. Please check the file format.")

            with col_b:
                if st.button("Cancel"):
                    st.rerun()

        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("Please make sure the file is a valid CSV format.")

    else:
        st.info("👆 Upload a CSV file to get started")

        # Instructions
        with st.expander("ℹ️ How to export from Cin7"):
            st.markdown("""
            ### Exporting Products from Cin7:

            1. Log into your Cin7 account
            2. Navigate to **Products** section
            3. Click on **Export** button
            4. Select the fields you want to export
            5. Choose **CSV** format
            6. Download the exported file
            7. Upload the file here using the file uploader above

            ### Supported formats:
            - CSV files (.csv)
            - Any standard CSV export from Cin7
            - Custom CSV files with product data
            """)

# ADD RECORD
elif operation == "Add Record":
    st.header("➕ Add New Record")

    # Get existing columns (excluding id and timestamp)
    existing_cols = db.get_columns()
    data_cols = [col for col in existing_cols if col not in ["id", "timestamp"]]

    with st.form("add_record_form"):
        st.subheader("Enter record data:")

        # Dynamic form based on existing columns or create new
        if len(data_cols) > 0:
            use_existing = st.checkbox("Use existing columns", value=True)

            if use_existing:
                record_data = {}
                for col in data_cols:
                    record_data[col] = st.text_input(f"{col}:")
            else:
                st.info("Add custom fields (one per line in format: column_name)")
                custom_fields = st.text_area("Custom fields:", placeholder="name\nage\nemail")
                record_data = {}
                if custom_fields:
                    fields = [f.strip() for f in custom_fields.split("\n") if f.strip()]
                    for field in fields:
                        record_data[field] = st.text_input(f"{field}:")
        else:
            st.info("Define your database schema by adding fields")
            num_fields = st.number_input("Number of fields:", min_value=1, max_value=20, value=3)
            record_data = {}
            for i in range(num_fields):
                col1, col2 = st.columns(2)
                with col1:
                    field_name = st.text_input(f"Field {i+1} name:", key=f"field_name_{i}")
                with col2:
                    if field_name:
                        field_value = st.text_input(f"Field {i+1} value:", key=f"field_value_{i}")
                        if field_name and field_value:
                            record_data[field_name] = field_value

        submitted = st.form_submit_button("Add Record")

        if submitted:
            if record_data and any(record_data.values()):
                if db.add_record(record_data):
                    st.success("✅ Record added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add record")
            else:
                st.warning("⚠️ Please enter at least one field with data")

# UPDATE RECORD
elif operation == "Update Record":
    st.header("✏️ Update Record")

    df = db.read_all()

    if len(df) > 0:
        # Select record to update
        record_id = st.selectbox("Select Record ID to update:", df["id"].tolist())

        # Get current record data
        current_record = df[df["id"] == record_id].iloc[0]

        st.subheader(f"Current data for Record ID: {record_id}")
        st.json(current_record.to_dict())

        with st.form("update_record_form"):
            st.subheader("Enter new values:")

            updated_data = {}
            data_cols = [col for col in df.columns if col not in ["id", "timestamp"]]

            for col in data_cols:
                current_value = str(current_record[col]) if pd.notna(current_record[col]) else ""
                updated_data[col] = st.text_input(f"{col}:", value=current_value)

            submitted = st.form_submit_button("Update Record")

            if submitted:
                if db.update_record(record_id, updated_data):
                    st.success("✅ Record updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update record")
    else:
        st.warning("No records available to update.")

# DELETE RECORD
elif operation == "Delete Record":
    st.header("🗑️ Delete Record")

    df = db.read_all()

    if len(df) > 0:
        # Show all records
        st.dataframe(df, use_container_width=True)

        # Select record to delete
        record_id = st.selectbox("Select Record ID to delete:", df["id"].tolist())

        # Show record details
        record_to_delete = df[df["id"] == record_id].iloc[0]
        st.subheader("Record to be deleted:")
        st.json(record_to_delete.to_dict())

        # Confirmation
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🗑️ Delete", type="primary"):
                if db.delete_record(record_id):
                    st.success("✅ Record deleted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete record")
        with col2:
            st.button("Cancel")
    else:
        st.warning("No records available to delete.")

# SEARCH
elif operation == "Search":
    st.header("🔍 Search Records")

    df = db.read_all()

    if len(df) > 0:
        col1, col2 = st.columns(2)

        with col1:
            search_column = st.selectbox("Select column to search:", df.columns.tolist())

        with col2:
            search_value = st.text_input("Enter search value:")

        if st.button("Search"):
            if search_value:
                results = db.search(search_column, search_value)

                if len(results) > 0:
                    st.success(f"Found {len(results)} matching record(s)")
                    st.dataframe(results, use_container_width=True)
                else:
                    st.warning("No matching records found")
            else:
                st.warning("Please enter a search value")
    else:
        st.warning("No records available to search.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 This database can be accessed by multiple Streamlit apps using the CSVDatabase class.")
