"""
Login page for user authentication.
"""
import streamlit as st
from utils.auth import authenticate_user, init_session_state, hash_password
from database.models import User
from database.connection import get_session
from utils.logger import logger

init_session_state()


def show_login_page():
    """Display login page and handle authentication."""
    try:
        st.title("🔐 Digital Service Analytics Platform")
        st.markdown("### Login to continue")
    except Exception as e:
        st.error(f"Error displaying login page: {e}")
        return

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Login", use_container_width=True)

        if submit_button:
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                user_info = authenticate_user(username, password)
                if user_info:
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = user_info
                    logger.info(f"User {username} logged in successfully")
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
                    logger.warning(f"Failed login attempt for username: {username}")

    # Registration section (for initial admin setup)
    with st.expander("🔧 Admin: Create Database User"):
        st.markdown("**Note:** This creates a user in the database. For production, use proper user management.")
        with st.form("register_form"):
            new_username = st.text_input("New Username", key="reg_username")
            new_password = st.text_input("New Password", type="password", key="reg_password")
            new_role = st.selectbox("Role", ["Analyst", "Tester", "Viewer"], key="reg_role")
            register_button = st.form_submit_button("Create User", use_container_width=True)

            if register_button:
                if not new_username or not new_password:
                    st.error("Username and password are required.")
                else:
                    try:
                        with get_session() as session:
                            # Check if user exists
                            existing = session.query(User).filter(User.username == new_username).first()
                            if existing:
                                st.error("Username already exists.")
                            else:
                                new_user = User(
                                    username=new_username,
                                    password_hash=hash_password(new_password),
                                    role=new_role
                                )
                                session.add(new_user)
                                session.commit()
                                st.success(f"User '{new_username}' created successfully!")
                                logger.info(f"New user created: {new_username} with role {new_role}")
                    except Exception as e:
                        st.error(f"Error creating user: {e}")
                        logger.error(f"Error creating user: {e}")



