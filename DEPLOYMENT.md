# Deployment Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Fill in the repository details:
   - **Repository name**: `sdata-csv-database` (or your preferred name)
   - **Description**: `Simple CSV database for Streamlit apps with Cin7 integration`
   - **Visibility**: Public (required for free Streamlit Cloud hosting)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click **Create repository**

## Step 2: Push Code to GitHub

After creating the repository, run these commands in your terminal:

```bash
cd "C:\Users\selwy\OneDrive\Desktop\PROJECTS HDL\SDATA"

# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/sdata-csv-database.git

# Push the code
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Streamlit Cloud (FREE)

### 3.1 Sign up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Authorize Streamlit Cloud to access your repositories

### 3.2 Deploy the App

1. Click **New app** button
2. Fill in the deployment settings:
   - **Repository**: Select your repository (e.g., `YOUR_USERNAME/sdata-csv-database`)
   - **Branch**: `main`
   - **Main file path**: `database_manager.py`
   - **App URL**: Choose a custom URL (e.g., `your-app-name.streamlit.app`)

3. Click **Deploy**

### 3.3 Deploy the Example App (Optional)

Repeat the process for the example app:
- **Main file path**: `example_app.py`
- **App URL**: Choose a different URL (e.g., `your-app-name-client.streamlit.app`)

## Step 4: Your Apps are Live! 🎉

After deployment (usually takes 2-3 minutes), you'll get URLs like:

- **Database Manager**: `https://your-app-name.streamlit.app`
- **Example Client**: `https://your-app-name-client.streamlit.app`

## Important Notes

### Data Persistence

⚠️ **Important**: Streamlit Cloud apps restart periodically, which means:
- Your CSV data will be lost on restart
- For production use, consider these options:
  1. **GitHub Storage**: Store `shared_data.csv` in the repo and commit changes
  2. **External Storage**: Use Google Drive, Dropbox, or AWS S3
  3. **Database**: Migrate to a real database (Supabase, PlanetScale, etc.)

### Recommended: Use External Storage

For persistent data, I recommend adding one of these:

#### Option A: Google Drive (via PyDrive2)
```python
pip install PyDrive2
# Store CSV in Google Drive
```

#### Option B: Supabase (Free PostgreSQL)
```python
pip install supabase
# Migrate from CSV to PostgreSQL
```

#### Option C: AWS S3
```python
pip install boto3
# Store CSV in S3 bucket
```

## Updating Your App

Whenever you make changes:

```bash
cd "C:\Users\selwy\OneDrive\Desktop\PROJECTS HDL\SDATA"
git add .
git commit -m "Your commit message"
git push
```

Streamlit Cloud will automatically redeploy your app!

## Managing Multiple Apps

All apps that import `csv_db.py` and point to `shared_data.csv` will share the same data:

```python
from csv_db import CSVDatabase
db = CSVDatabase("shared_data.csv")
```

## Troubleshooting

### App won't start?
- Check the logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Make sure Python version is compatible (3.8+)

### Data not persisting?
- This is expected with CSV storage on Streamlit Cloud
- See "Data Persistence" section above

### Need help?
- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- GitHub Issues: Create an issue in your repository

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy to Streamlit Cloud
3. 🔄 Consider adding persistent storage
4. 📱 Share your app URL with others!

---

**Your app is ready to go live! Follow the steps above to deploy.** 🚀
