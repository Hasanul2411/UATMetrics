# How to Get Your Supabase Password

Your Supabase URL: `https://uoyhfsjmtsbtnijjmmtl.supabase.co`

## Steps to Get Your Database Password:

1. **Go to Supabase Dashboard**: https://supabase.com/dashboard
2. **Select your project** (the one with URL ending in `uoyhfsjmtsbtnijjmmtl.supabase.co`)
3. **Click**: Project Settings (gear icon in left sidebar)
4. **Click**: Database (in the settings menu)
5. **Scroll down** to find your database password

### If You Don't See the Password:

You can **reset it**:
1. In the Database settings page
2. Look for "Database password" section
3. Click "Reset database password"
4. Copy the new password immediately (you won't see it again!)

## Update Your Secrets File:

1. Open `.streamlit/secrets.toml`
2. Find the line: `password = "YOUR_PASSWORD_HERE"`
3. Replace `YOUR_PASSWORD_HERE` with your actual Supabase database password
4. Save the file

## Example:

```toml
[db]
host = "db.uoyhfsjmtsbtnijjmmtl.supabase.co"
port = 5432
database = "postgres"
user = "postgres"
password = "your-actual-password-here"  # ← Replace this
```

## After Updating:

Restart the Streamlit app (or refresh the browser) and it should connect to Supabase!

