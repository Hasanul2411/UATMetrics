"""
Basic test script to verify application setup and imports.
Run this before starting the Streamlit app to catch common issues.
"""
import sys
import importlib


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    required_modules = [
        "streamlit",
        "pandas",
        "sqlalchemy",
        "plotly",
        "reportlab",
        "bcrypt",
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"[OK] {module}")
        except ImportError as e:
            print(f"[FAIL] {module} - {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n[OK] All imports successful!")
    return True


def test_project_structure():
    """Test that project structure is correct."""
    print("\nTesting project structure...")
    
    import os
    
    required_files = [
        "app.py",
        "requirements.txt",
        "config/settings.py",
        "database/models.py",
        "database/connection.py",
        "pages/login.py",
        "pages/dashboard.py",
        "pages/analytics.py",
        "pages/uat_tracker.py",
        "pages/reports.py",
        "utils/auth.py",
        "utils/logger.py",
        "reports/pdf_generator.py",
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"[OK] {file_path}")
        else:
            print(f"[FAIL] {file_path} - NOT FOUND")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n[ERROR] Missing files: {', '.join(missing_files)}")
        return False
    
    print("\n[OK] Project structure is correct!")
    return True


def test_secrets_file():
    """Check if secrets file exists."""
    print("\nTesting configuration...")
    
    import os
    
    secrets_file = ".streamlit/secrets.toml"
    secrets_example = ".streamlit/secrets.toml.example"
    
    if os.path.exists(secrets_file):
        print(f"[OK] {secrets_file} exists")
        return True
    elif os.path.exists(secrets_example):
        print(f"[WARN] {secrets_file} not found, but example exists")
        print(f"  Copy {secrets_example} to {secrets_file} and configure it")
        return False
    else:
        print(f"[ERROR] Neither {secrets_file} nor {secrets_example} found")
        return False


def test_database_models():
    """Test that database models can be imported and are valid."""
    print("\nTesting database models...")
    
    try:
        from database.models import (
            User, Service, Event, TestCase, Defect,
            UserRole, EventStatus, DefectSeverity, DefectStatus
        )
        print("[OK] All models imported successfully")
        
        # Test that models have required attributes
        assert hasattr(User, 'username')
        assert hasattr(Service, 'name')
        assert hasattr(Event, 'service_id')
        assert hasattr(TestCase, 'title')
        assert hasattr(Defect, 'severity')
        print("[OK] Model attributes verified")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error testing models: {e}")
        return False


def test_auth_utilities():
    """Test authentication utilities."""
    print("\nTesting authentication utilities...")
    
    try:
        from utils.auth import hash_password, verify_password
        
        # Test password hashing
        test_password = "test123"
        hashed = hash_password(test_password)
        
        if not hashed or len(hashed) < 10:
            print("[ERROR] Password hashing failed")
            return False
        
        # Test password verification
        if not verify_password(test_password, hashed):
            print("[ERROR] Password verification failed")
            return False
        
        # Test wrong password
        if verify_password("wrong", hashed):
            print("[ERROR] Password verification incorrectly passed")
            return False
        
        print("[OK] Authentication utilities working correctly")
        return True
    except Exception as e:
        print(f"[ERROR] Error testing auth: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Digital Service Analytics Platform - Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Project Structure", test_project_structure()))
    results.append(("Secrets File", test_secrets_file()))
    results.append(("Database Models", test_database_models()))
    results.append(("Auth Utilities", test_auth_utilities()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] All tests passed! You're ready to run the app.")
        print("\nNext steps:")
        print("1. Configure .streamlit/secrets.toml with your database credentials")
        print("2. Run: streamlit run app.py")
    else:
        print("[ERROR] Some tests failed. Please fix the issues above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

