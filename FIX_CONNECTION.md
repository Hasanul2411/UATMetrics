# Fix Supabase Connection

The error suggests the hostname format might be incorrect. Let's verify your Supabase connection details.

## Get the Correct Connection String

1. **Go to Supabase Dashboard**: https://supabase.com/dashboard
2. **Select your project** (uoyhfsjmtsbtnijjmmtl)
3. **Go to**: Project Settings → Database
4. **Scroll to**: Connection string section
5. **Select**: "URI" tab (not "JDBC" or "Golang")

You should see something like:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

## Check These Details:

1. **Host format**: Should be `db.[project-ref].supabase.co`
   - Your project ref appears to be: `uoyhfsjmtsbtnijjmmtl`
   - So host should be: `db.uoyhfsjmtsbtnijjmmtl.supabase.co`

2. **Alternative**: Some Supabase projects use connection pooling
   - Check if there's a "Connection pooling" section
   - It might show a different hostname like `aws-0-[region].pooler.supabase.com`

3. **Verify project is active**: 
   - Make sure your Supabase project is not paused
   - Paused projects won't resolve hostnames

## Update Your Secrets

Once you have the correct hostname, update `.streamlit/secrets.toml`:

```toml
[db]
host = "db.uoyhfsjmtsbtnijjmmtl.supabase.co"  # Or the correct host from Supabase
port = 5432
database = "postgres"
user = "postgres"
password = "Duat2026@mohd"
```

## Test Connection

After updating, the app should connect. If it still doesn't work, try:
- Using the connection pooling URL if available
- Checking if your project needs IP whitelisting (usually not needed)
- Verifying the project is active in Supabase dashboard

