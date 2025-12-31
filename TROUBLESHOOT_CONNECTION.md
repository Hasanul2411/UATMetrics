# Troubleshooting Supabase Connection

## Current Issue
The hostname `db.uoyhfsjmtsbtnijjmmtl.supabase.co` is not resolving properly.

## Possible Causes & Solutions

### 1. Check Project Status
- Go to https://supabase.com/dashboard
- Verify your project is **Active** (not paused)
- Paused projects won't accept connections

### 2. Try Connection Pooling
Supabase provides connection pooling URLs that might work better:

1. In Supabase Dashboard → Project Settings → Database
2. Look for **"Connection pooling"** section
3. Use the **"Session" mode** connection string
4. The hostname will be different (like `aws-0-[region].pooler.supabase.com`)

### 3. Check Network/DNS
- Try accessing: https://uoyhfsjmtsbtnijjmmtl.supabase.co in your browser
- If that works, the project is active
- The database hostname should resolve

### 4. Verify Connection String Format
Make sure in `.streamlit/secrets.toml`:
```toml
[db]
host = "db.uoyhfsjmtsbtnijjmmtl.supabase.co"  # Exact hostname from Supabase
port = 5432
database = "postgres"
user = "postgres"
password = "Duat2026@mohd"
```

### 5. Alternative: Use Direct Connection String
If the above doesn't work, we can modify the code to accept a full connection string instead of individual parameters.

## Next Steps
1. Check if project is active in Supabase dashboard
2. Try the connection pooling URL if available
3. Share the connection pooling string if you find it

