"""Test Supabase connection directly."""
import psycopg2
from urllib.parse import quote_plus
import streamlit as st

# Read secrets
try:
    host = st.secrets["db"]["host"]
    port = st.secrets["db"]["port"]
    database = st.secrets["db"]["database"]
    user = st.secrets["db"]["user"]
    password = st.secrets["db"]["password"]
    
    print(f"Testing connection to: {host}:{port}")
    print(f"Database: {database}, User: {user}")
    
    # Test connection
    conn_string = f"host={host} port={port} dbname={database} user={user} password={password} sslmode=require"
    
    print("\nAttempting connection...")
    conn = psycopg2.connect(conn_string)
    print("[SUCCESS] Connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"PostgreSQL version: {version[0]}")
    
    conn.close()
    print("[SUCCESS] Connection closed successfully")
    
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
    import traceback
    traceback.print_exc()

