# Google Sheets Setup Guide

This guide will help you set up Google Sheets as your database backend for persistent storage.

## Why Google Sheets?

- **Persistent Storage**: Data survives app restarts on Streamlit Cloud
- **Free**: No cost for reasonable usage
- **Easy to View**: Can open and edit directly in Google Sheets
- **Shareable**: Easy to share with team members
- **No Database Management**: No server setup required

## Setup Steps

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click **"New Project"**
4. Enter project name: `SDATA Database` (or your choice)
5. Click **"Create"**

### Step 2: Enable Google Sheets API

1. In your project, go to **"APIs & Services"** > **"Library"**
2. Search for **"Google Sheets API"**
3. Click on it and click **"Enable"**
4. Also search for **"Google Drive API"** and enable it

### Step 3: Create Service Account

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** > **"Service Account"**
3. Enter details:
   - **Service account name**: `sdata-service-account`
   - **Service account ID**: (auto-generated)
4. Click **"Create and Continue"**
5. Skip optional steps, click **"Done"**

### Step 4: Create and Download Service Account Key

1. Click on the service account you just created
2. Go to the **"Keys"** tab
3. Click **"Add Key"** > **"Create new key"**
4. Choose **JSON** format
5. Click **"Create"**
6. A JSON file will download - **SAVE THIS FILE SECURELY**

### Step 5: Share Google Sheet with Service Account

1. Open the downloaded JSON file
2. Find the `client_email` field (looks like `sdata-service-account@project-name.iam.gserviceaccount.com`)
3. Copy this email address
4. The app will create a Google Sheet automatically, but you'll need to share it:
   - Go to [Google Sheets](https://sheets.google.com)
   - Find the sheet named "SDATA Database" (created by the app)
   - Click **Share**
   - Paste the service account email
   - Give it **Editor** access
   - Click **Send**

## For Local Development

### Option 1: Using credentials.json file

1. Rename the downloaded JSON file to `credentials.json`
2. Place it in your project root directory:
   ```
   C:\Users\selwy\OneDrive\Desktop\PROJECTS HDL\SDATA\credentials.json
   ```

3. Make sure `.gitignore` includes `credentials.json` (already configured)

### Option 2: Update .gitignore

The `.gitignore` file should already include:
```
credentials.json
*.json
```

## For Streamlit Cloud Deployment

### Step 1: Prepare Credentials for Streamlit Secrets

1. Open your `credentials.json` file
2. Copy the entire contents

### Step 2: Add to Streamlit Cloud Secrets

1. Go to your app on [Streamlit Cloud](https://share.streamlit.io)
2. Click on your app
3. Click **"Settings"** (gear icon) > **"Secrets"**
4. Add the following (paste your credentials in TOML format):

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

**Important Notes:**
- Replace all values with your actual credentials from `credentials.json`
- For `private_key`, make sure to keep the `\n` characters and quotes
- Don't add extra quotes around the values

### Step 3: Save and Redeploy

1. Click **"Save"**
2. Your app will automatically redeploy
3. It should now connect to Google Sheets!

## Verification

To verify everything is working:

1. Run your app locally or on Streamlit Cloud
2. You should see "Connected to Google Sheets" or similar message
3. Try adding a record
4. Check your Google Sheets - you should see the data appear!
5. The app will show a link to open the spreadsheet directly

## Troubleshooting

### Error: "SpreadsheetNotFound"
- The app will create the spreadsheet automatically
- Make sure to share it with your service account email after it's created

### Error: "Insufficient Permission"
- Make sure you shared the spreadsheet with the service account email
- Make sure you gave **Editor** access (not just Viewer)

### Error: "Invalid Credentials"
- Double-check your secrets formatting in Streamlit Cloud
- Make sure all fields are copied correctly from credentials.json
- Verify the private_key has proper line breaks (\\n)

### Local Development Not Working
- Make sure `credentials.json` is in the project root directory
- Verify the file name is exactly `credentials.json`
- Check that the JSON file is valid (no syntax errors)

## Switching Between CSV and Google Sheets

Edit `config.py`:

```python
# For Google Sheets
DATABASE_TYPE = "gsheets"

# For CSV (local only)
DATABASE_TYPE = "csv"
```

## Security Best Practices

1. **Never commit credentials.json to Git** - Already in .gitignore
2. **Use Streamlit Secrets for deployment** - Never hardcode credentials
3. **Limit service account permissions** - Only enable required APIs
4. **Rotate keys periodically** - Create new keys and delete old ones

## Benefits of Google Sheets Backend

✅ **Persistent**: Data survives app restarts
✅ **Collaborative**: Multiple apps can share the same sheet
✅ **Viewable**: Open directly in Google Sheets to view/edit
✅ **Free**: Google Sheets API is free for reasonable usage
✅ **Backup**: Google handles backups automatically
✅ **History**: Google Sheets has version history

## Next Steps

1. Complete the setup above
2. Run your app locally to test
3. Deploy to Streamlit Cloud
4. Add secrets to Streamlit Cloud
5. Upload your Cin7 data!

---

**Need Help?**
- Check the [gspread documentation](https://docs.gspread.org/)
- Visit [Google Cloud Console](https://console.cloud.google.com/)
