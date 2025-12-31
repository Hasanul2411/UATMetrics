"""
Quick test script to run the app with SQLite (no PostgreSQL required).
This is a temporary setup for testing purposes.
"""
import sys
import os
import shutil

def setup_sqlite_testing():
    """Set up SQLite connection for testing."""
    print("Setting up SQLite for testing...")
    
    # Backup original connection file
    if os.path.exists("database/connection.py"):
        if not os.path.exists("database/connection_postgresql.py.backup"):
            shutil.copy("database/connection.py", "database/connection_postgresql.py.backup")
            print("[OK] Backed up PostgreSQL connection file")
    
    # Copy SQLite connection
    if os.path.exists("database/connection_sqlite.py"):
        shutil.copy("database/connection_sqlite.py", "database/connection.py")
        print("[OK] Switched to SQLite connection")
    
    # Create minimal secrets if it doesn't exist
    secrets_dir = ".streamlit"
    secrets_file = os.path.join(secrets_dir, "secrets.toml")
    secrets_example = os.path.join(secrets_dir, "secrets.toml.example")
    
    if not os.path.exists(secrets_file):
        os.makedirs(secrets_dir, exist_ok=True)
        if os.path.exists(secrets_example):
            shutil.copy(secrets_example, secrets_file)
            print("[OK] Created secrets.toml from example")
        else:
            # Create minimal secrets
            with open(secrets_file, "w") as f:
                f.write("""[app]
secret_key = "test-secret-key"

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
""")
            print("[OK] Created minimal secrets.toml")
    
    print("\n[OK] Setup complete! You can now run: streamlit run app.py")
    print("\nNote: This uses SQLite for testing. For production, restore connection_postgresql.py.backup")


def restore_postgresql():
    """Restore PostgreSQL connection."""
    print("Restoring PostgreSQL connection...")
    
    backup_file = "database/connection_postgresql.py.backup"
    if os.path.exists(backup_file):
        shutil.copy(backup_file, "database/connection.py")
        print("[OK] Restored PostgreSQL connection")
    else:
        print("[WARN] No backup found. You'll need to restore connection.py manually")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        restore_postgresql()
    else:
        setup_sqlite_testing()

