"""
Example Client App - Demonstrates how to connect to the shared CSV database
"""

import streamlit as st
import pandas as pd
from csv_db import CSVDatabase

# Page configuration
st.set_page_config(
    page_title="Example Client App",
    page_icon="📱",
    layout="wide"
)

# Connect to the same database
db = CSVDatabase("shared_data.csv")

st.title("📱 Example Client App")
st.markdown("This app demonstrates connecting to the shared CSV database")

# Show that we're connected to the same database
st.info("🔗 Connected to: `shared_data.csv`")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📊 View Data", "➕ Quick Add", "📈 Statistics"])

with tab1:
    st.header("Current Database Contents")

    df = db.read_all()

    if len(df) > 0:
        st.dataframe(df, use_container_width=True)

        # Refresh button
        if st.button("🔄 Refresh Data"):
            st.rerun()
    else:
        st.warning("No data in database yet. Add some records using the Database Manager!")

with tab2:
    st.header("Quick Add Record")

    df = db.read_all()
    existing_cols = db.get_columns()
    data_cols = [col for col in existing_cols if col not in ["id", "timestamp"]]

    if len(data_cols) > 0:
        with st.form("quick_add"):
            st.write("Fill in the fields:")

            record_data = {}
            for col in data_cols:
                record_data[col] = st.text_input(f"{col}:")

            submitted = st.form_submit_button("Add Record")

            if submitted:
                if any(record_data.values()):
                    if db.add_record(record_data):
                        st.success("✅ Record added!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to add record")
                else:
                    st.warning("⚠️ Please fill in at least one field")
    else:
        st.info("No schema defined yet. Use the Database Manager to create your first record and define the schema.")

with tab3:
    st.header("Database Statistics")

    df = db.read_all()

    if len(df) > 0:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Records", len(df))

        with col2:
            st.metric("Total Columns", len(df.columns))

        with col3:
            # Get most recent timestamp
            if "timestamp" in df.columns:
                latest = df["timestamp"].max()
                st.metric("Last Updated", latest)

        st.subheader("Column Information")
        col_info = pd.DataFrame({
            "Column": df.columns,
            "Non-Null Count": [df[col].notna().sum() for col in df.columns],
            "Data Type": [str(df[col].dtype) for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)

        # Sample data
        st.subheader("Sample Data (First 5 Records)")
        st.dataframe(df.head(), use_container_width=True)
    else:
        st.warning("No data available for statistics.")

# Sidebar
st.sidebar.header("About")
st.sidebar.markdown("""
This is an example app showing how to connect to the shared CSV database.

**Features:**
- View all records
- Quick add functionality
- Database statistics

**To use:**
1. Run the Database Manager app to add/edit records
2. This app will automatically see those changes
3. You can also add records directly from this app
""")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh All Data"):
    st.rerun()
