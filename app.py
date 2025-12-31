"""
Main Streamlit application entry point.
Digital Service Analytics & UAT Readiness Platform
"""
import streamlit as st
import traceback
from pages.login import show_login_page
from pages.dashboard import show_dashboard_page
from pages.analytics import show_analytics_page
from pages.uat_tracker import show_uat_tracker_page
from pages.reports import show_reports_page
from utils.auth import init_session_state, check_role_access
from database.connection import init_database
from utils.data_generator import generate_sample_data
from utils.logger import logger

# Page configuration
st.set_page_config(
    page_title="Digital Service Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
try:
    init_session_state()
except Exception as e:
    st.error(f"Error initializing session: {e}")
    logger.error(f"Error initializing session: {e}")

# Initialize database (non-blocking)
_db_initialized = False
try:
    init_database()
    _db_initialized = True
except Exception as e:
    logger.error(f"Database initialization error: {e}")
    # Don't stop the app - allow login page to show
    # Database will be initialized when first accessed


def main():
    """Main application logic."""
    # Check authentication
    if not st.session_state.get("authenticated", False):
        show_login_page()
        return

    # Sidebar navigation
    user = st.session_state.get("user", {})
    st.sidebar.title("📊 Digital Service Analytics")
    st.sidebar.markdown(f"**User:** {user.get('username', 'Unknown')}")
    st.sidebar.markdown(f"**Role:** {user.get('role', 'Unknown')}")

    st.sidebar.markdown("---")

    # Navigation menu
    pages = {
        "Dashboard": show_dashboard_page,
        "Analytics": show_analytics_page,
        "UAT Tracker": show_uat_tracker_page,
    }

    # Add Reports page only for Analyst and Viewer
    if check_role_access(["Analyst", "Viewer"]):
        pages["Reports"] = show_reports_page

    # Admin section (only for Analyst)
    if check_role_access(["Analyst"]):
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔧 Admin Tools")
        if st.sidebar.button("Generate Sample Data"):
            try:
                with st.spinner("Generating sample data..."):
                    result = generate_sample_data()
                    st.sidebar.success(result)
                    st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

    # Page selection - default to Dashboard
    page_keys = list(pages.keys())
    default_index = 0  # Dashboard is first
    
    if "selected_page" in st.session_state and st.session_state["selected_page"] in page_keys:
        try:
            default_index = page_keys.index(st.session_state["selected_page"])
        except ValueError:
            default_index = 0
    
    selected_page = st.sidebar.radio(
        "Navigation",
        options=page_keys,
        index=default_index,
        label_visibility="collapsed",
        key="page_selector"
    )
    st.session_state["selected_page"] = selected_page

    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.rerun()

    # Display selected page
    try:
        pages[selected_page]()
    except Exception as e:
        st.error(f"Error loading page: {e}")
        logger.error(f"Error loading page {selected_page}: {e}")
        st.exception(e)


# Always call main() in Streamlit
if __name__ == "__main__" or True:  # Always run in Streamlit
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {e}")
        logger.error(f"Application error: {e}")
        st.exception(e)
        # Still show login page if possible
        try:
            if not st.session_state.get("authenticated", False):
                show_login_page()
        except:
            pass



