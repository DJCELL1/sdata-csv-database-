"""
Simple test app to verify everything works
"""

import streamlit as st
import sys
import os

st.title("🔧 Database Test")

# Show current directory
st.write(f"**Current directory:** {os.getcwd()}")

# Test config import
try:
    from config import DATABASE_TYPE
    st.success(f"✅ Config loaded: DATABASE_TYPE = {DATABASE_TYPE}")
except Exception as e:
    st.error(f"❌ Failed to load config: {e}")
    st.stop()

# Test database connection
try:
    from config import get_database
    db = get_database()
    st.success(f"✅ Database connected: {type(db).__name__}")
except Exception as e:
    st.error(f"❌ Failed to connect to database: {e}")
    st.write("**Error details:**")
    st.code(str(e))
    st.stop()

# Test reading data
try:
    df = db.read_all()
    st.success(f"✅ Data read successfully: {len(df)} records")
    if len(df) > 0:
        st.dataframe(df)
    else:
        st.info("No data yet - database is empty")
except Exception as e:
    st.error(f"❌ Failed to read data: {e}")

st.success("🎉 All tests passed! Your database is working correctly.")
st.info("Now you can run: streamlit run database_manager.py")
