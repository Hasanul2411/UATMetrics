# Use Session Pooler for IPv4 Compatibility

Your Supabase project shows "Not IPv4 compatible" - this is why the direct connection isn't working.

## Solution: Use Session Pooler

1. **In the Supabase connection dialog**, click **"Pooler settings"** button
2. **Or go to**: Project Settings → Database → Connection pooling
3. **Select**: "Session mode" (not Transaction mode)
4. **Copy the connection string** - it will look like:
   ```
   postgresql://postgres.uoyhfsjmtsbtnijjmmtl:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

## Key Differences:
- **Host**: `aws-0-[region].pooler.supabase.com` (not `db.xxx.supabase.co`)
- **Port**: `6543` (not `5432`)
- **User**: `postgres.uoyhfsjmtsbtnijjmmtl` (includes project ref)

## Update Your Secrets

Once you have the pooler connection string, update `.streamlit/secrets.toml`:

```toml
[db]
host = "aws-0-us-east-1.pooler.supabase.com"  # From pooler connection string
port = 6543  # Pooler port
database = "postgres"
user = "postgres.uoyhfsjmtsbtnijjmmtl"  # Includes project ref
password = "Duat2026@mohd"
```

**Please share the Session Pooler connection string from Supabase** and I'll update the configuration!

