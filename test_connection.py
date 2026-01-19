"""
Quick test script to verify Google Sheets connection
"""

import json

print("=" * 60)
print("Google Sheets Connection Test")
print("=" * 60)

# Load credentials
try:
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
    print("✅ credentials.json found and loaded")
    print(f"\nYour service account email:")
    print(f"   {creds['client_email']}")
    print(f"\nProject ID: {creds['project_id']}")
except Exception as e:
    print(f"❌ Error loading credentials: {e}")
    exit(1)

# Test Google Sheets connection
print("\n" + "=" * 60)
print("Testing Google Sheets API connection...")
print("=" * 60)

try:
    from gsheets_db import GoogleSheetsDatabase

    print("\n📝 Attempting to connect to Google Sheets...")
    db = GoogleSheetsDatabase(
        spreadsheet_name="SDATA Database Test",
        worksheet_name="data"
    )

    print("✅ Successfully connected to Google Sheets!")

    # Get spreadsheet URL
    url = db.get_spreadsheet_url()
    if url:
        print(f"\n📊 Spreadsheet URL:")
        print(f"   {url}")
        print(f"\n⚠️ IMPORTANT: Share this spreadsheet with:")
        print(f"   {creds['client_email']}")
        print(f"   Give it 'Editor' access!")

    # Try to read data
    print("\n📖 Testing read operation...")
    df = db.read_all()
    print(f"✅ Successfully read data: {len(df)} rows")

    print("\n" + "=" * 60)
    print("🎉 All tests passed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Go to the spreadsheet URL above")
    print("2. Click 'Share' button")
    print(f"3. Add: {creds['client_email']}")
    print("4. Give it 'Editor' permissions")
    print("5. Run: streamlit run database_manager.py")

except Exception as e:
    print(f"\n❌ Connection failed: {str(e)}")
    print("\nPossible issues:")
    print("1. Google Sheets API not enabled")
    print("2. Google Drive API not enabled")
    print("3. Spreadsheet not shared with service account")
    print("\nSee GOOGLE_SHEETS_SETUP.md for detailed setup instructions")
