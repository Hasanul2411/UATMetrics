# Data Entry Guide - How to Add Data for Reports & Analysis

This guide explains how to add data to generate meaningful reports and analytics in the Digital Service Analytics Platform.

## Quick Start: Generate Sample Data

**Fastest way to get started:**

1. **Login as Analyst** (username: `admin`, password: `admin123`)
2. **Click "Generate Sample Data"** in the sidebar (under Admin Tools)
3. This creates:
   - 5 sample services
   - 1000 sample events (last 30 days)
   - 7 sample test cases
   - 7 sample defects

**That's it!** You can now view dashboards, analytics, and generate reports.

---

## Manual Data Entry

### 1. Adding Digital Services

**Services** are the foundation - all events, test cases, and defects are linked to services.

**Currently:** Services are created automatically when you generate sample data, or you can add them via the database.

**To add a service manually:**
- Use the database directly, or
- Modify the sample data generator to include your services

**Example Service:**
- Name: "Customer Portal"
- Channel: "web"
- Description: "Main customer-facing web application"

---

### 2. Adding Events (Digital Journey Data)

**Events** represent user actions and interactions with your digital services.

**How Events Work:**
- Each event is linked to a service
- Events have: action, status, timestamp, journey time
- Status can be: `success`, `error`, or `pending`

**Ways to Add Events:**

#### Option A: Through Application Integration (Recommended for Production)

Add events programmatically from your application:

```python
from database.connection import get_session
from database.models import Event, Service
from datetime import datetime

# Example: Log a user login event
with get_session() as session:
    # Find your service
    service = session.query(Service).filter(Service.name == "Customer Portal").first()
    
    # Create event
    event = Event(
        service_id=service.id,
        action="user_login",
        status="success",
        timestamp=datetime.now(),
        journey_time=2.5  # seconds
    )
    session.add(event)
    session.commit()
```

#### Option B: Bulk Import via Script

Create a Python script to import events from CSV or API:

```python
import pandas as pd
from database.connection import get_session
from database.models import Event, Service
from datetime import datetime

def import_events_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    
    with get_session() as session:
        service = session.query(Service).first()  # Get first service
        
        for _, row in df.iterrows():
            event = Event(
                service_id=service.id,
                action=row['action'],
                status=row['status'],
                timestamp=pd.to_datetime(row['timestamp']),
                journey_time=row.get('journey_time'),
                error_message=row.get('error_message')
            )
            session.add(event)
        
        session.commit()
```

#### Option C: Real-time Event Logging

If you have a web application, add an API endpoint to log events:

```python
# Example Flask endpoint
@app.route('/api/log-event', methods=['POST'])
def log_event():
    data = request.json
    with get_session() as session:
        service = session.query(Service).filter(Service.name == data['service']).first()
        event = Event(
            service_id=service.id,
            action=data['action'],
            status=data['status'],
            timestamp=datetime.now(),
            journey_time=data.get('journey_time')
        )
        session.add(event)
        session.commit()
    return {'status': 'success'}
```

---

### 3. Adding Test Cases

**Test Cases** are managed through the UAT Tracker page.

**Steps:**
1. Go to **UAT Tracker** page
2. Click on **"Test Cases"** tab
3. Expand **"➕ Create New Test Case"**
4. Fill in:
   - **Service**: Select the service to test
   - **Title**: e.g., "User Login Flow"
   - **Description**: What you're testing
   - **Expected Result**: What should happen
   - **Test Steps**: Step-by-step instructions
   - **Status**: Not Started, Passed, Failed, or Blocked
5. Click **"Create Test Case"**

**Example Test Case:**
- Title: "Payment Processing"
- Description: "Verify payment transaction completes successfully"
- Expected Result: "Payment processed and confirmation shown"
- Status: "Passed"

---

### 4. Adding Defects

**Defects** (bugs/issues) are also managed through UAT Tracker.

**Steps:**
1. Go to **UAT Tracker** page
2. Click on **"Defects"** tab
3. Expand **"🐛 Create New Defect"**
4. Fill in:
   - **Service**: Which service has the defect
   - **Title**: Brief description
   - **Description**: Detailed explanation
   - **Severity**: Critical, High, Medium, or Low
   - **Status**: Open, In Progress, Resolved, or Closed
   - **Steps to Reproduce**: How to trigger the issue
   - **Expected Behavior**: What should happen
   - **Actual Behavior**: What actually happens
5. Click **"Create Defect"**

**Example Defect:**
- Title: "Login timeout error"
- Severity: "High"
- Status: "Open"
- Description: "Users experiencing timeout during login process"

---

## Data Structure Overview

### Services
- **Purpose**: Digital services you're monitoring (web apps, mobile apps, APIs)
- **Fields**: name, channel, description
- **Required**: Yes - all other data links to services

### Events
- **Purpose**: User actions and system events
- **Fields**: service_id, action, status, timestamp, journey_time, error_message
- **Volume**: Can be thousands per day
- **Use**: Analytics, KPIs, performance monitoring

### Test Cases
- **Purpose**: UAT and regression test scenarios
- **Fields**: service_id, title, description, expected_result, status
- **Use**: Test coverage tracking, quality metrics

### Defects
- **Purpose**: Bugs and issues tracking
- **Fields**: service_id, title, severity, status, description
- **Use**: Quality metrics, defect tracking, prioritization

---

## Best Practices

### 1. Service Naming
- Use clear, descriptive names
- Group related services logically
- Examples: "Mobile Banking App", "Payment Gateway API", "Customer Portal"

### 2. Event Actions
- Use consistent naming: `user_login`, `payment_submit`, `checkout_complete`
- Follow a pattern: `[entity]_[action]` or `[feature]_[action]`
- Document your action names for consistency

### 3. Event Status
- **success**: Operation completed successfully
- **error**: Operation failed
- **pending**: Operation in progress (use sparingly)

### 4. Journey Time
- Measure in seconds
- Include for successful operations
- Helps identify performance issues

### 5. Test Case Status
- **Not Started**: Test not yet executed
- **Passed**: Test executed and passed
- **Failed**: Test executed and failed
- **Blocked**: Test cannot be executed (dependency issue)

### 6. Defect Severity
- **Critical**: System down, data loss, security breach
- **High**: Major feature broken, significant impact
- **Medium**: Feature partially broken, moderate impact
- **Low**: Minor issue, cosmetic problem

---

## Generating Reports

Once you have data:

### Analytics Reports
1. Go to **Reports** page
2. Select **"Analytics Report"**
3. Choose date range and service filter
4. Click **"Generate Analytics Report"**
5. Download the PDF

### UAT Reports
1. Go to **Reports** page
2. Select **"UAT & Testing Report"**
3. Choose service filter
4. Click **"Generate UAT Report"**
5. Download the PDF

---

## Data Volume Recommendations

### For Meaningful Analytics:
- **Minimum**: 100+ events per service
- **Recommended**: 1000+ events for better insights
- **Time Range**: At least 7 days of data

### For Testing Reports:
- **Minimum**: 5-10 test cases per service
- **Recommended**: 20+ test cases
- **Defects**: Track all defects, regardless of volume

---

## Troubleshooting

### "No data available" messages
- **Solution**: Generate sample data or add your own data
- Check date filters aren't too restrictive
- Verify services exist

### Charts not showing
- **Solution**: Ensure you have events with the required fields
- Check that status values are: success, error, or pending
- Verify journey_time is numeric

### Reports are empty
- **Solution**: Add data first, then generate reports
- Check date ranges include data
- Verify service filters match your data

---

## Next Steps

1. ✅ Generate sample data to see the platform in action
2. ✅ Explore the dashboards and analytics
3. ✅ Generate sample reports
4. ✅ Plan your real data integration
5. ✅ Set up event logging from your applications
6. ✅ Start tracking test cases and defects

**Need help?** Check the main README.md or create an issue in the repository.

