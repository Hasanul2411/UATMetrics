# Supabase Setup Guide

This guide will help you connect the Digital Service Analytics Platform to your Supabase PostgreSQL database.

## Step 1: Get Your Supabase Credentials

1. **Log in to Supabase**: Go to https://supabase.com and sign in to your account

2. **Select or Create a Project**:
   - If you have an existing project, select it
   - If not, click "New Project" and create one
   - Wait for the project to finish setting up (takes a few minutes)

3. **Get Database Connection Details**:
   - Go to **Project Settings** (gear icon in the left sidebar)
   - Click on **Database** in the settings menu
   - Scroll down to find **Connection string** section
   - You'll see two options:
     - **URI** (recommended) - Full connection string
     - **Parameters** - Individual connection details

## Step 2: Extract Connection Information

You need the following information:

### Option A: Using Connection String (URI)
If you see a connection string like:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

Extract:
- **Host**: `db.xxxxx.supabase.co` (the part after `@` and before `:5432`)
- **Port**: `5432` (usually this)
- **Database**: `postgres` (usually this)
- **User**: `postgres` (usually this)
- **Password**: The password you set when creating the project (or reset it if needed)

### Option B: Using Individual Parameters
Look for:
- **Host**: Something like `db.xxxxx.supabase.co`
- **Port**: `5432`
- **Database name**: Usually `postgres`
- **User**: Usually `postgres`
- **Password**: Your database password

**Note**: If you forgot your password, you can reset it in Project Settings > Database > Database password

## Step 3: Update Your Secrets File

1. **Open** `.streamlit/secrets.toml` in your project

2. **Replace the database section** with your Supabase credentials:

```toml
[db]
host = "db.xxxxx.supabase.co"  # Replace with your Supabase host
port = 5432
database = "postgres"  # Usually "postgres"
user = "postgres"  # Usually "postgres"
password = "your-supabase-password"  # Your database password

[app]
secret_key = "your-secret-key-change-this-in-production"

[users.admin]
username = "admin"
password = "admin123"
role = "Analyst"

[users.tester]
username = "tester"
password = "test123"
role = "Tester"

[users.viewer]
username = "viewer"
password = "view123"
role = "Viewer"
```

3. **Save the file**

## Step 4: Switch Back to PostgreSQL Connection

The app is currently using SQLite. You need to restore the PostgreSQL connection:

1. **Check if backup exists**:
   ```bash
   ls database/connection_postgresql.py.backup
   ```

2. **Restore PostgreSQL connection**:
   ```bash
   # On Windows PowerShell:
   Copy-Item database\connection_postgresql.py.backup database\connection.py -Force
   ```

   Or manually:
   - Delete or rename `database/connection.py`
   - Rename `database/connection_postgresql.py.backup` to `database/connection.py`

## Step 5: Test the Connection

1. **Restart the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Check for errors**: The app should connect to Supabase without errors

3. **Login and test**: 
   - Login with `admin` / `admin123`
   - The database tables will be created automatically on first run
   - Try generating sample data to verify everything works

## Troubleshooting

### Connection Timeout
- **Issue**: "Connection timeout" or "Could not connect"
- **Solution**: 
  - Check your Supabase project is active (not paused)
  - Verify the host, port, and password are correct
  - Check if your IP needs to be whitelisted (usually not needed for Supabase)

### Authentication Failed
- **Issue**: "Authentication failed" or "Password incorrect"
- **Solution**:
  - Reset your database password in Supabase: Project Settings > Database > Database password
  - Update the password in `.streamlit/secrets.toml`

### SSL Connection Required
- **Issue**: "SSL connection required"
- **Solution**: Supabase requires SSL. The connection should handle this automatically, but if you see this error, add SSL parameters to the connection string.

### Tables Not Created
- **Issue**: App runs but tables don't exist
- **Solution**: 
  - The app auto-creates tables on first run
  - Check Supabase SQL Editor to see if tables were created
  - You can manually run the schema if needed (see database/models.py)

## Security Best Practices

1. **Never commit secrets.toml**: It's already in `.gitignore`
2. **Use strong passwords**: For both Supabase and app users
3. **Rotate passwords regularly**: Especially in production
4. **Use connection pooling**: For production (Supabase provides this)

## Next Steps

Once connected:
1. ✅ Login to the app
2. ✅ Generate sample data (as Analyst)
3. ✅ Explore all features
4. ✅ Deploy to Streamlit Cloud (add secrets there too)

## Need Help?

- Supabase Docs: https://supabase.com/docs
- Check the app logs for specific error messages
- Verify your Supabase project is active and not paused

