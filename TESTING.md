# Testing Guide

This guide will help you test the Digital Service Analytics & UAT Readiness Platform.

## Quick Start Testing (Without Database Setup)

For quick testing without setting up PostgreSQL, you can use the built-in secrets-based authentication (no database required for initial testing).

### Step 1: Create Secrets File

1. Copy the example secrets file:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

2. For initial testing, you can use minimal configuration. Edit `.streamlit/secrets.toml`:

```toml
# Minimal config for testing (without database)
[app]
secret_key = "test-secret-key-change-in-production"

# Test users (no database needed for these)
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
```

**Note:** Without database configuration, you can still test authentication and UI, but analytics and data features will require a database.

## Full Testing with Database

### Option A: Using SQLite (Easiest for Testing)

For local testing, you can modify the connection to use SQLite instead of PostgreSQL:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Modify `database/connection.py` temporarily to use SQLite (see instructions below)

3. Run the app:
```bash
streamlit run app.py
```

### Option B: Using PostgreSQL (Production-like)

1. **Local PostgreSQL:**
   - Install PostgreSQL
   - Create database: `CREATE DATABASE digital_analytics;`
   - Update `.streamlit/secrets.toml` with credentials

2. **Supabase (Free tier):**
   - Sign up at https://supabase.com
   - Create new project
   - Get connection details from Settings > Database
   - Update `.streamlit/secrets.toml`

3. **Neon (Free tier):**
   - Sign up at https://neon.tech
   - Create new project
   - Copy connection string
   - Update `.streamlit/secrets.toml`

## Step-by-Step Testing Checklist

### 1. Authentication Testing

- [ ] **Login with different roles:**
  - Login as `admin` (Analyst role)
  - Login as `tester` (Tester role)
  - Login as `viewer` (Viewer role)
  - Verify incorrect password is rejected

- [ ] **Role-based access:**
  - As Analyst: Verify access to all pages including Reports
  - As Tester: Verify access to Analytics, UAT Tracker (no Reports)
  - As Viewer: Verify read-only access

- [ ] **Logout:**
  - Click logout button
  - Verify redirected to login page

### 2. Sample Data Generation

- [ ] **Generate sample data (Analyst only):**
  - Login as Analyst
  - Click "Generate Sample Data" in sidebar
  - Verify success message
  - Verify data appears in dashboards

### 3. Dashboard Testing

- [ ] **View Executive Dashboard:**
  - Check all metrics display correctly
  - Verify charts render
  - Check executive summary section

### 4. Analytics Testing

- [ ] **Filter events:**
  - Select different services
  - Change date ranges
  - Verify data updates

- [ ] **KPI calculations:**
  - Verify completion rate calculation
  - Verify error rate calculation
  - Verify average journey time

- [ ] **Visualizations:**
  - Check pie chart for status distribution
  - Check line chart for events over time
  - Check bar chart for service performance

- [ ] **Data export:**
  - Click "Download Data as CSV"
  - Verify CSV file downloads correctly

### 5. UAT Tracker Testing

- [ ] **Test Cases:**
  - View existing test cases
  - Create new test case (Analyst/Tester)
  - Verify test case appears in list
  - Check status filtering

- [ ] **Defects:**
  - View existing defects
  - Create new defect (Analyst/Tester)
  - Verify defect appears in list
  - Check severity and status filtering
  - Verify defect summary by severity/status

### 6. Reports Testing

- [ ] **Analytics Report (Analyst/Viewer):**
  - Select date range
  - Select service filter
  - Click "Generate Analytics Report"
  - Verify PDF downloads
  - Open PDF and verify content

- [ ] **UAT Report (Analyst/Viewer):**
  - Select service filter
  - Click "Generate UAT Report"
  - Verify PDF downloads
  - Open PDF and verify content

### 7. Database User Creation

- [ ] **Create database user:**
  - On login page, expand "Admin: Create Database User"
  - Create new user with different role
  - Login with new user
  - Verify role-based access works

## Testing with SQLite (Quick Setup)

To test without PostgreSQL, create a modified connection file:

1. Create `database/connection_sqlite.py` (temporary):

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
import streamlit as st
from database.models import Base
import os

@st.cache_resource
def get_engine():
    """Create SQLite engine for testing."""
    db_path = "test_database.db"
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    return engine

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
```

2. Temporarily modify imports in files that use `database.connection` to use `database.connection_sqlite`

**Or** use the provided test script below.

## Automated Testing Script

Run the test script to verify basic functionality:

```bash
python test_app.py
```

## Common Issues & Solutions

### Issue: "Failed to connect to database"
**Solution:** 
- Check database credentials in `.streamlit/secrets.toml`
- Verify database is running (for local PostgreSQL)
- Check network connectivity (for cloud databases)

### Issue: "No module named 'X'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Table doesn't exist"
**Solution:**
- The app auto-creates tables on first run
- Check database connection is working
- Verify you have CREATE TABLE permissions

### Issue: "Authentication fails"
**Solution:**
- Check username/password in `.streamlit/secrets.toml`
- Verify secrets file is in `.streamlit/` directory
- Check for typos in username/password

## Performance Testing

- Test with 1000+ events
- Test with multiple services
- Test PDF generation with large datasets
- Verify page load times are acceptable

## Security Testing

- Verify passwords are hashed in database
- Test SQL injection attempts (should be safe with SQLAlchemy)
- Verify role-based access is enforced
- Test session management (logout clears session)

## Browser Testing

Test in multiple browsers:
- Chrome/Edge
- Firefox
- Safari (if on Mac)

## Mobile Testing

- Test responsive design on mobile devices
- Verify charts render correctly on small screens
- Test form inputs on mobile

