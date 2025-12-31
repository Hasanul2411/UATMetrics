"""
Sample data generator for testing and demonstration.
"""
import random
from datetime import datetime, timedelta
from database.connection import get_session
from database.models import Service, Event, TestCase, Defect
from utils.logger import logger


def generate_sample_data():
    """Generate sample data for demonstration."""
    try:
        with get_session() as session:
            # Check if data already exists
            existing_services = session.query(Service).count()
            if existing_services > 0:
                logger.info("Sample data already exists. Skipping generation.")
                return "Sample data already exists."

            # Create Services
            services_data = [
                {"name": "Online Banking Portal", "channel": "web", "description": "Customer banking portal"},
                {"name": "Mobile Banking App", "channel": "mobile", "description": "iOS and Android mobile app"},
                {"name": "Payment Gateway API", "channel": "api", "description": "RESTful payment processing API"},
                {"name": "Customer Support Chat", "channel": "web", "description": "Live chat support system"},
                {"name": "Loan Application System", "channel": "web", "description": "Digital loan application platform"}
            ]

            services = []
            for svc_data in services_data:
                service = Service(**svc_data)
                session.add(service)
                services.append(service)
            session.flush()  # Get IDs

            # Generate Events (last 30 days)
            actions = ["login", "checkout", "payment", "transfer", "view_statement", "apply_loan", "chat_start", "chat_end"]
            statuses = ["success", "error", "pending"]
            status_weights = [0.85, 0.10, 0.05]  # 85% success, 10% error, 5% pending

            events = []
            for _ in range(1000):  # Generate 1000 events
                service = random.choice(services)
                action = random.choice(actions)
                status = random.choices(statuses, weights=status_weights)[0]
                timestamp = datetime.now() - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                journey_time = random.uniform(2.0, 120.0) if status == "success" else None
                error_message = f"Error: {random.choice(['Timeout', 'Validation failed', 'Network error', 'Invalid input'])}" if status == "error" else None

                event = Event(
                    service_id=service.id,
                    action=action,
                    status=status,
                    timestamp=timestamp,
                    journey_time=journey_time,
                    error_message=error_message
                )
                events.append(event)

            session.add_all(events)

            # Generate Test Cases
            test_cases_data = [
                {"title": "User Login Flow", "description": "Verify user can login with valid credentials", "expected_result": "User successfully logged in", "status": "Passed"},
                {"title": "Payment Processing", "description": "Test payment transaction completion", "expected_result": "Payment processed successfully", "status": "Passed"},
                {"title": "Fund Transfer", "description": "Verify fund transfer between accounts", "expected_result": "Transfer completed", "status": "Failed"},
                {"title": "Loan Application Submission", "description": "Test loan application form submission", "expected_result": "Application submitted", "status": "Passed"},
                {"title": "Mobile App Navigation", "description": "Test navigation flow in mobile app", "expected_result": "Navigation works correctly", "status": "Not Started"},
                {"title": "API Authentication", "description": "Verify API token authentication", "expected_result": "Authentication successful", "status": "Passed"},
                {"title": "Chat Session Management", "description": "Test chat session creation and termination", "expected_result": "Sessions managed correctly", "status": "Blocked"},
            ]

            test_cases = []
            for tc_data in test_cases_data:
                service = random.choice(services)
                test_case = TestCase(
                    service_id=service.id,
                    **tc_data
                )
                test_cases.append(test_case)
                session.add(test_case)

            session.flush()

            # Generate Defects
            defects_data = [
                {"title": "Login timeout error", "description": "Users experiencing timeout during login", "severity": "High", "status": "Open"},
                {"title": "Payment gateway connection failure", "description": "Intermittent connection failures to payment gateway", "severity": "Critical", "status": "In Progress"},
                {"title": "Mobile app crashes on iOS 17", "description": "App crashes when opening on iOS 17 devices", "severity": "Critical", "status": "Open"},
                {"title": "Fund transfer validation error", "description": "Incorrect validation message shown during transfer", "severity": "Medium", "status": "Resolved"},
                {"title": "API rate limiting too strict", "description": "API rate limits causing legitimate requests to fail", "severity": "Medium", "status": "Open"},
                {"title": "Chat widget not loading", "description": "Chat widget fails to load on certain browsers", "severity": "High", "status": "In Progress"},
                {"title": "Loan application form validation", "description": "Form accepts invalid input in some fields", "severity": "Low", "status": "Open"},
            ]

            for defect_data in defects_data:
                service = random.choice(services)
                test_case = random.choice(test_cases) if test_cases else None
                defect = Defect(
                    service_id=service.id,
                    test_case_id=test_case.id if test_case else None,
                    **defect_data
                )
                session.add(defect)

            # Context manager will commit automatically
            logger.info("Sample data generated successfully")
            return "Sample data generated successfully!"

    except Exception as e:
        logger.error(f"Error generating sample data: {e}")
        raise


def clear_all_data():
    """Clear all data from database (use with caution)."""
    try:
        with get_session() as session:
            session.query(Defect).delete()
            session.query(TestCase).delete()
            session.query(Event).delete()
            session.query(Service).delete()
            # Context manager will commit automatically
            logger.info("All data cleared")
            return "All data cleared successfully!"
    except Exception as e:
        logger.error(f"Error clearing data: {e}")
        raise

