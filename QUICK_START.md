# Quick Start Guide

## For Local Development (CSV Mode - Easiest)

Want to test the app right away without setting up Google Sheets? Just use CSV mode:

1. **Edit `config.py`** and change:
   ```python
   DATABASE_TYPE = "csv"  # Change from "gsheets" to "csv"
   ```

2. **Run the app:**
   ```bash
   pip install streamlit pandas
   streamlit run database_manager.py
   ```

That's it! Your data will be stored in `shared_data.csv`

## For Google Sheets (Persistent Cloud Storage)

If you want your data to persist on Streamlit Cloud, follow these steps:

### Step 1: Get Google Cloud Credentials (15 minutes)

1. **Go to Google Cloud Console:** https://console.cloud.google.com/
2. **Create a new project** (or select existing)
3. **Enable APIs:**
   - Search for "Google Sheets API" → Enable
   - Search for "Google Drive API" → Enable

4. **Create Service Account:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Name it: `sdata-service-account`
   - Click "Create and Continue" → Skip optional steps → Done

5. **Create Key:**
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose JSON format
   - Click "Create" → **Save this file!**

### Step 2: Setup Locally

1. **Rename the downloaded file** to `credentials.json`
2. **Move it to your project folder:**
   ```
   C:\Users\selwy\OneDrive\Desktop\PROJECTS HDL\SDATA\credentials.json
   ```

3. **Run the app:**
   ```bash
   pip install -r requirements.txt
   streamlit run database_manager.py
   ```

4. **Share the spreadsheet:**
   - Open the JSON file and find `client_email` (looks like `name@project.iam.gserviceaccount.com`)
   - When the app creates the Google Sheet, share it with this email
   - Give it "Editor" access

### Step 3: Deploy to Streamlit Cloud

1. **Go to:** https://share.streamlit.io
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure:**
   - Repository: `DJCELL1/sdata-csv-database-`
   - Branch: `main`
   - Main file: `database_manager.py`

5. **Add Secrets:**
   - Click "Advanced settings" → "Secrets"
   - Copy your `credentials.json` content
   - Format it as TOML (see below)
   - Click "Deploy"

**Secrets format (TOML):**
```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

**Important:** Replace all values with your actual credentials from `credentials.json`

## Current Status

Right now, your app is configured to use **Google Sheets mode** but will automatically fall back to **CSV mode** if credentials aren't found.

**To check which mode you're using:**
- Run the app
- Look at the title - it will say either "Database Manager (Google Sheets)" or "Database Manager (CSV)"
- If you see a warning about credentials, you're in fallback CSV mode

## Troubleshooting

### "Google Sheets credentials not found"
→ Either add `credentials.json` or change `DATABASE_TYPE = "csv"` in `config.py`

### "Failed to connect to Google Sheets"
→ Check that your `credentials.json` is valid JSON
→ Make sure you enabled both Google Sheets API and Google Drive API

### App works but data disappears on Streamlit Cloud
→ You're in CSV mode - CSV data doesn't persist on Streamlit Cloud
→ Follow the Google Sheets setup above for persistent storage

## Which Mode Should I Use?

**Use CSV if:**
- Testing locally
- Quick prototype
- Don't need data to persist online

**Use Google Sheets if:**
- Deploying to Streamlit Cloud
- Need data to persist between app restarts
- Want to view/edit data in Google Sheets
- Sharing with others

## Need More Help?

- Full Google Sheets guide: See `GOOGLE_SHEETS_SETUP.md`
- Deployment guide: See `DEPLOYMENT.md`
- General usage: See `README.md`
