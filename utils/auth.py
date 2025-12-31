"""
Authentication and authorization utilities.
"""
import bcrypt
import streamlit as st
from typing import Optional, Dict
from config.settings import get_users_config
from database.models import User
from database.connection import get_session


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False


def authenticate_user(username: str, password: str) -> Optional[Dict[str, str]]:
    """
    Authenticate user against database or secrets configuration.
    Returns user info dict if authenticated, None otherwise.
    """
    # First, try database
    try:
        with get_session() as session:
            user = session.query(User).filter(User.username == username).first()
            if user and verify_password(password, user.password_hash):
                return {
                    "username": user.username,
                    "role": user.role
                }
    except Exception:
        pass  # Fall back to secrets config

    # Fall back to secrets configuration
    users_config = get_users_config()
    if username in users_config:
        user_config = users_config[username]
        if password == user_config["password"]:  # Simple comparison for secrets-based auth
            return {
                "username": username,
                "role": user_config["role"]
            }

    return None


def check_role_access(required_roles: list) -> bool:
    """Check if current user has access based on role."""
    if "user" not in st.session_state:
        return False
    
    user = st.session_state.get("user")
    if user is None:
        return False
    
    user_role = user.get("role") if isinstance(user, dict) else None
    if user_role is None:
        return False
    
    return user_role in required_roles


def require_role(required_roles: list):
    """Decorator/function to require specific roles for page access."""
    # Check if user is authenticated first
    if not st.session_state.get("authenticated", False):
        st.error("Please log in to access this page.")
        st.stop()
        return
    
    if not check_role_access(required_roles):
        st.error("You don't have permission to access this page.")
        st.stop()


def init_session_state():
    """Initialize session state variables."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None



