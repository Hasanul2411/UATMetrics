"""
Login page for user authentication.
"""
import streamlit as st
from utils.auth import authenticate_user, init_session_state, register_user
from database.models import User
from database.connection import get_session
from utils.logger import logger

init_session_state()


def show_login_page():
    """Display login page and handle authentication."""
    try:
        from utils.ui import render_page_header
        render_page_header("Digital Service", "Analytics Platform", icon="login")
    except Exception as e:
        st.error(f"Error displaying login page: {e}")
        return

    # Create tabs for Login and Sign Up
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
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

    with tab2:
        st.markdown("Create a new account (default role: Viewer)")
        with st.form("register_form"):
            new_username = st.text_input("Choose Username", key="reg_username")
            new_password = st.text_input("Choose Password", type="password", help="Minimum 8 characters", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
            
            # Default role is Viewer for security, admin can upgrade later if needed
            # Or we could allow selection if this is an internal internal tool, but let's stick to secure default
            
            register_button = st.form_submit_button("Create Account", use_container_width=True)

            if register_button:
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message = register_user(new_username, new_password, role="Viewer")
                    if success:
                        st.success(message)
                        st.info("Please switch to the Login tab to sign in.")
                    else:
                        st.error(message)



