"""Quick test to verify all imports work."""
import sys

try:
    print("Testing imports...")
    import streamlit as st
    print("[OK] streamlit")
    
    from pages.login import show_login_page
    print("[OK] pages.login")
    
    from database.connection import init_database, get_session
    print("[OK] database.connection")
    
    from database.models import Base, User, Service, Event, TestCase, Defect
    print("[OK] database.models")
    
    from utils.auth import authenticate_user, init_session_state
    print("[OK] utils.auth")
    
    from config.settings import get_users_config
    print("[OK] config.settings")
    
    print("\n[SUCCESS] All imports successful!")
    
    # Test database initialization
    print("\nTesting database initialization...")
    try:
        init_database()
        print("[OK] Database initialized successfully")
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
    
except Exception as e:
    print(f"\n[ERROR] Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

