"""
Helper script to set up Supabase connection.
This will restore the PostgreSQL connection file and help you configure it.
"""
import os
import shutil

def setup_supabase():
    """Set up Supabase connection."""
    print("=" * 60)
    print("Supabase Setup Helper")
    print("=" * 60)
    
    # Check if backup exists
    backup_file = "database/connection_postgresql.py.backup"
    if not os.path.exists(backup_file):
        print("\n[ERROR] PostgreSQL backup file not found!")
        print("Creating PostgreSQL connection file from template...")
        
        # Create PostgreSQL connection file
        pg_content = '''"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from typing import Generator
import streamlit as st
from config.settings import get_db_config
from database.models import Base


def get_database_url() -> str:
    """Construct database URL from configuration."""
    config = get_db_config()
    return (
        f"postgresql://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['database']}"
    )


@st.cache_resource
def get_engine():
    """Create and cache database engine."""
    try:
        database_url = get_database_url()
        engine = create_engine(
            database_url,
            poolclass=NullPool,
            echo=False,
            connect_args={"connect_timeout": 10}
        )
        return engine
    except Exception as e:
        st.error(f"Failed to connect to database: {e}")
        st.stop()


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get database session with automatic cleanup."""
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def init_database():
    """Initialize database tables."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    return engine
'''
        
        with open("database/connection.py", "w") as f:
            f.write(pg_content)
        print("[OK] Created PostgreSQL connection file")
    else:
        # Restore from backup
        print(f"\n[OK] Found backup file: {backup_file}")
        shutil.copy(backup_file, "database/connection.py")
        print("[OK] Restored PostgreSQL connection file")
    
    # Check secrets file
    secrets_file = ".streamlit/secrets.toml"
    if os.path.exists(secrets_file):
        print(f"\n[OK] Secrets file exists: {secrets_file}")
        print("\nNext steps:")
        print("1. Open .streamlit/secrets.toml")
        print("2. Add your Supabase database credentials:")
        print("   [db]")
        print("   host = 'db.xxxxx.supabase.co'")
        print("   port = 5432")
        print("   database = 'postgres'")
        print("   user = 'postgres'")
        print("   password = 'your-password'")
        print("\n3. See SUPABASE_SETUP.md for detailed instructions")
    else:
        print(f"\n[WARN] Secrets file not found: {secrets_file}")
        print("Creating example secrets file...")
        os.makedirs(".streamlit", exist_ok=True)
        example_content = '''[db]
host = "db.xxxxx.supabase.co"
port = 5432
database = "postgres"
user = "postgres"
password = "your-password"

[app]
secret_key = "your-secret-key-change-this"

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
'''
        with open(secrets_file, "w") as f:
            f.write(example_content)
        print(f"[OK] Created {secrets_file}")
        print("Please edit it with your Supabase credentials")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Setup complete!")
    print("=" * 60)
    print("\nNext: Update .streamlit/secrets.toml with your Supabase credentials")
    print("Then restart the app: streamlit run app.py")

if __name__ == "__main__":
    setup_supabase()

