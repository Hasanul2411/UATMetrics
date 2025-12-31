# Quick Start: Connect to Supabase

## Get Your Supabase Credentials (2 minutes)

1. **Go to Supabase**: https://supabase.com/dashboard
2. **Select your project** (or create one)
3. **Go to**: Project Settings → Database
4. **Find**: Connection string or Connection parameters

You need:
- **Host**: `db.xxxxx.supabase.co`
- **Port**: `5432`
- **Database**: `postgres`
- **User**: `postgres`
- **Password**: Your database password (reset if needed)

## Update Secrets File

Open `.streamlit/secrets.toml` and add/update the `[db]` section:

```toml
[db]
host = "db.xxxxx.supabase.co"  # Your Supabase host
port = 5432
database = "postgres"
user = "postgres"
password = "your-actual-password"  # Your Supabase database password
```

**Keep the rest of the file as is** (users, app config, etc.)

## Restart the App

```bash
streamlit run app.py
```

The app will:
- ✅ Connect to Supabase
- ✅ Create all tables automatically
- ✅ Be ready to use!

## That's It!

Login with:
- Username: `admin`
- Password: `admin123`

Then click "Generate Sample Data" in the sidebar to populate the database.

---

**Need more help?** See `SUPABASE_SETUP.md` for detailed instructions.

