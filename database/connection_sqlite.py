"""
SQLite database connection for local testing.
Use this instead of connection.py for quick testing without PostgreSQL.

To use: Temporarily rename connection.py and rename this file to connection.py
Or modify imports in app.py and other files to use connection_sqlite
"""
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
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
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


def get_database_url() -> str:
    """Get SQLite database URL."""
    return "sqlite:///test_database.db"

