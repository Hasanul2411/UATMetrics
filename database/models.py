"""
SQLAlchemy database models for the Digital Service Analytics platform.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(enum.Enum):
    """User role enumeration."""
    ANALYST = "Analyst"
    TESTER = "Tester"
    VIEWER = "Viewer"


class EventStatus(enum.Enum):
    """Event status enumeration."""
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"


class DefectSeverity(enum.Enum):
    """Defect severity enumeration."""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class DefectStatus(enum.Enum):
    """Defect status enumeration."""
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="Viewer")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"


class Service(Base):
    """Digital service model."""
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    channel = Column(String(100), nullable=False)  # web, mobile, api, etc.
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    events = relationship("Event", back_populates="service", cascade="all, delete-orphan")
    test_cases = relationship("TestCase", back_populates="service", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Service(name='{self.name}', channel='{self.channel}')>"


class Event(Base):
    """Digital journey event model."""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    action = Column(String(200), nullable=False)  # login, checkout, payment, etc.
    status = Column(String(50), nullable=False, default="success")
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    journey_time = Column(Float, nullable=True)  # Time in seconds
    error_message = Column(Text, nullable=True)
    event_metadata = Column(Text, nullable=True)  # JSON string for additional data

    # Relationships
    service = relationship("Service", back_populates="events")

    def __repr__(self):
        return f"<Event(service_id={self.service_id}, action='{self.action}', status='{self.status}')>"


class TestCase(Base):
    """UAT test case model."""
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    expected_result = Column(Text, nullable=False)
    test_steps = Column(Text, nullable=True)
    status = Column(String(50), default="Not Started")  # Not Started, Passed, Failed, Blocked
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    service = relationship("Service", back_populates="test_cases")
    defects = relationship("Defect", back_populates="test_case", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TestCase(id={self.id}, title='{self.title[:50]}...')>"


class Defect(Base):
    """Defect/bug model."""
    __tablename__ = "defects"

    id = Column(Integer, primary_key=True, index=True)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False, default="Medium")
    status = Column(String(50), nullable=False, default="Open")
    steps_to_reproduce = Column(Text, nullable=True)
    expected_behavior = Column(Text, nullable=True)
    actual_behavior = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # Relationships
    test_case = relationship("TestCase", back_populates="defects")

    def __repr__(self):
        return f"<Defect(id={self.id}, title='{self.title[:50]}...', severity='{self.severity}')>"



