# Digital Service Analytics & UAT Readiness Platform

A production-ready Streamlit application for analyzing digital service performance, managing UAT & regression testing, and generating business-ready insights.

## Features

### 🔐 Authentication & Roles
- Simple login system using Streamlit secrets
- Role-based access control (Analyst, Tester, Viewer)
- Secure password hashing with bcrypt

### 📊 Digital Journey Analytics
- Event logging and tracking
- KPI calculations:
  - Completion rate
  - Error rate
  - Average journey time
- Advanced filtering by date, service, and channel
- Interactive visualizations with Plotly

### 🧪 UAT & Regression Tracker
- Create, read, and update test cases
- Defect management with severity and status tracking
- Link defects to digital services and test cases
- Comprehensive test case and defect dashboards

### 📈 Executive Dashboards
- High-level performance overview
- Interactive charts and visualizations
- Service performance metrics
- Executive summary with recommendations

### 📄 Automated Reporting
- Generate PDF reports using ReportLab
- Analytics reports with KPIs and charts
- UAT reports with test case and defect summaries
- Business-ready insights and recommendations

## Tech Stack

- **Python 3.8+**
- **Streamlit** - Web application framework
- **PostgreSQL** - Database (Supabase/Neon compatible)
- **SQLAlchemy** - ORM for database operations
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations
- **ReportLab** - PDF generation
- **bcrypt** - Password hashing

## Project Structure

```
UATMetrics/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml.example   # Example secrets file
├── config/
│   └── settings.py            # Application settings
├── database/
│   ├── models.py              # SQLAlchemy models
│   └── connection.py          # Database connection management
├── pages/
│   ├── login.py               # Authentication page
│   ├── dashboard.py           # Executive dashboard
│   ├── analytics.py           # Digital journey analytics
│   ├── uat_tracker.py         # UAT & testing tracker
│   └── reports.py             # PDF report generation
├── utils/
│   ├── auth.py                # Authentication utilities
│   ├── validators.py          # Input validation
│   ├── logger.py              # Logging configuration
│   └── data_generator.py      # Sample data generator
└── reports/
    └── pdf_generator.py        # PDF report generation
```

## Quick Start Testing

**Want to test quickly without setting up PostgreSQL?**

1. Run the test script to verify setup:
```bash
python test_app.py
```

2. Set up SQLite for quick testing:
```bash
python quick_test.py
```

3. Run the app:
```bash
streamlit run app.py
```

4. Login with test credentials:
   - Username: `admin`, Password: `admin123` (Analyst)
   - Username: `tester`, Password: `test123` (Tester)
   - Username: `viewer`, Password: `view123` (Viewer)

See [TESTING.md](TESTING.md) for detailed testing instructions.

## Setup & Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd UATMetrics
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Tests (Optional but Recommended)

```bash
python test_app.py
```

### 4. Database Setup

#### Option A: Using Supabase
1. Create a new project on [Supabase](https://supabase.com)
2. Get your database connection details from Project Settings > Database

#### Option B: Using Neon
1. Create a new project on [Neon](https://neon.tech)
2. Copy your connection string

#### Option C: Local PostgreSQL
1. Install PostgreSQL locally
2. Create a new database:
```sql
CREATE DATABASE digital_analytics;
```

### 5. Configure Secrets

1. Copy the example secrets file:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

2. Edit `.streamlit/secrets.toml` with your database credentials:

```toml
[db]
host = "your-db-host"
port = 5432
database = "your-database-name"
user = "your-username"
password = "your-password"

[app]
secret_key = "your-secret-key-change-this-in-production"

[users.admin]
username = "admin"
password = "admin123"  # Change this!
role = "Analyst"
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Database Schema

The application automatically creates the following tables:

### users
- `id` (Primary Key)
- `username` (Unique)
- `password_hash`
- `role` (Analyst, Tester, Viewer)
- `created_at`

### services
- `id` (Primary Key)
- `name`
- `channel` (web, mobile, api, etc.)
- `description`
- `created_at`

### events
- `id` (Primary Key)
- `service_id` (Foreign Key)
- `action`
- `status` (success, error, pending)
- `timestamp`
- `journey_time`
- `error_message`
- `metadata`

### test_cases
- `id` (Primary Key)
- `service_id` (Foreign Key)
- `title`
- `description`
- `expected_result`
- `test_steps`
- `status` (Not Started, Passed, Failed, Blocked)
- `created_at`
- `updated_at`

### defects
- `id` (Primary Key)
- `test_case_id` (Foreign Key, nullable)
- `service_id` (Foreign Key)
- `title`
- `description`
- `severity` (Critical, High, Medium, Low)
- `status` (Open, In Progress, Resolved, Closed)
- `steps_to_reproduce`
- `expected_behavior`
- `actual_behavior`
- `created_at`
- `updated_at`
- `resolved_at`

## Sample Data

After logging in as an Analyst, you can generate sample data using the "Generate Sample Data" button in the sidebar. This will create:
- 5 sample services
- 1000 sample events (last 30 days)
- 7 sample test cases
- 7 sample defects

## Deployment to Streamlit Cloud

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Connect your GitHub repository
4. Select the repository and branch
5. Set the main file path to `app.py`

### 3. Configure Secrets

In Streamlit Cloud, go to your app settings and add secrets:

```
[db]
host = "your-db-host"
port = 5432
database = "your-database-name"
user = "your-username"
password = "your-password"

[app]
secret_key = "your-secret-key"

[users.admin]
username = "admin"
password = "your-secure-password"
role = "Analyst"
```

### 4. Deploy

Click "Deploy" and your app will be live!

## Usage Guide

### For Analysts
- Full access to all features
- Can create test cases and defects
- Can generate PDF reports
- Can generate sample data

### For Testers
- Can view analytics and dashboards
- Can create and manage test cases
- Can create and manage defects
- Cannot generate reports

### For Viewers
- Read-only access to dashboards and analytics
- Can view test cases and defects
- Can generate reports (read-only)

## Security Best Practices

1. **Change Default Passwords**: Always change default passwords in production
2. **Secure Secret Key**: Use a strong, random secret key
3. **Database Security**: Use connection pooling and SSL for database connections
4. **Environment Variables**: Never commit secrets to version control
5. **Role-Based Access**: Regularly review user roles and permissions

## Troubleshooting

### Database Connection Issues
- Verify database credentials in `.streamlit/secrets.toml`
- Check if database is accessible from your network
- Ensure PostgreSQL is running (for local setup)

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### PDF Generation Issues
- Ensure ReportLab is properly installed
- Check file permissions for PDF output

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.

## Roadmap

- [ ] Advanced filtering and search
- [ ] Email notifications for critical defects
- [ ] Integration with CI/CD pipelines
- [ ] Real-time event streaming
- [ ] Advanced analytics and ML insights
- [ ] Multi-tenant support
- [ ] API endpoints for external integrations



