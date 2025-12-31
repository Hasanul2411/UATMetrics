"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from typing import Generator
from urllib.parse import quote_plus
import streamlit as st
from config.settings import get_db_config
from database.models import Base


def get_database_url() -> str:
    """Construct database URL from configuration with proper encoding."""
    config = get_db_config()
    # URL-encode username and password to handle special characters
    user = quote_plus(config['user'])
    password = quote_plus(config['password'])
    host = config['host']
    port = config['port']
    database = config['database']
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


@st.cache_resource
def get_engine():
    """Create and cache database engine."""
    try:
        database_url = get_database_url()
        # Supabase requires SSL connections
        engine = create_engine(
            database_url,
            poolclass=NullPool,
            echo=False,
            connect_args={
                "connect_timeout": 10,
                "sslmode": "require"
            }
        )
        return engine
    except KeyError as e:
        # Database config not set up yet
        st.warning("⚠️ Database not configured. Please set up Supabase credentials in `.streamlit/secrets.toml`")
        st.info("See `SUPABASE_SETUP.md` for instructions.")
        logger.error(f"Database configuration missing: {e}")
        st.stop()
    except Exception as e:
        error_msg = str(e)
        st.error(f"Failed to connect to database: {error_msg}")
        st.info("Please check your Supabase credentials in `.streamlit/secrets.toml`")
        logger.error(f"Database connection error: {e}")
        # Don't stop - allow user to see the error and fix it
        st.info("💡 **Tip**: If using Supabase, make sure you're using the **Session Pooler** connection string for IPv4 compatibility.")
        st.stop()


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



