"""
Example script to add events to the database programmatically.
Use this as a template for integrating event logging into your applications.
"""
from database.connection import get_session
from database.models import Event, Service
from datetime import datetime, timedelta
import random

def add_sample_events(service_name: str, num_events: int = 100):
    """
    Add sample events for a service.
    
    Args:
        service_name: Name of the service
        num_events: Number of events to add
    """
    try:
        with get_session() as session:
            # Find the service
            service = session.query(Service).filter(Service.name == service_name).first()
            
            if not service:
                print(f"Service '{service_name}' not found. Please create it first.")
                return
            
            # Sample actions
            actions = ["login", "checkout", "payment", "transfer", "view_statement", 
                      "apply_loan", "chat_start", "chat_end", "search", "filter"]
            
            # Generate events
            events = []
            for i in range(num_events):
                # Random timestamp in last 30 days
                days_ago = random.randint(0, 30)
                hours_ago = random.randint(0, 23)
                timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
                
                # Random action and status
                action = random.choice(actions)
                status = random.choices(
                    ["success", "error", "pending"],
                    weights=[0.85, 0.10, 0.05]
                )[0]
                
                # Journey time for successful events
                journey_time = random.uniform(1.0, 60.0) if status == "success" else None
                
                # Error message for failed events
                error_message = None
                if status == "error":
                    error_message = random.choice([
                        "Timeout error",
                        "Validation failed",
                        "Network error",
                        "Invalid input"
                    ])
                
                event = Event(
                    service_id=service.id,
                    action=action,
                    status=status,
                    timestamp=timestamp,
                    journey_time=journey_time,
                    error_message=error_message
                )
                events.append(event)
            
            # Bulk insert
            session.add_all(events)
            session.commit()
            
            print(f"✅ Successfully added {num_events} events for service '{service_name}'")
            
    except Exception as e:
        print(f"❌ Error adding events: {e}")
        import traceback
        traceback.print_exc()


def add_single_event(service_name: str, action: str, status: str = "success", 
                     journey_time: float = None, error_message: str = None):
    """
    Add a single event.
    
    Args:
        service_name: Name of the service
        action: Action name (e.g., "user_login", "payment_submit")
        status: "success", "error", or "pending"
        journey_time: Time in seconds (optional)
        error_message: Error message if status is "error" (optional)
    """
    try:
        with get_session() as session:
            service = session.query(Service).filter(Service.name == service_name).first()
            
            if not service:
                print(f"Service '{service_name}' not found.")
                return
            
            event = Event(
                service_id=service.id,
                action=action,
                status=status,
                timestamp=datetime.now(),
                journey_time=journey_time,
                error_message=error_message
            )
            
            session.add(event)
            session.commit()
            
            print(f"✅ Event added: {action} - {status}")
            
    except Exception as e:
        print(f"❌ Error adding event: {e}")


if __name__ == "__main__":
    # Example usage:
    
    # Add 100 sample events for a service
    # add_sample_events("Online Banking Portal", num_events=100)
    
    # Add a single event
    # add_single_event(
    #     service_name="Online Banking Portal",
    #     action="user_login",
    #     status="success",
    #     journey_time=2.5
    # )
    
    print("Event logging script ready.")
    print("Uncomment the examples above to add events, or use the functions in your own code.")

