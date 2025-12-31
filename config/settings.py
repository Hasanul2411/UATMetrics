"""
Application configuration and settings management.
"""
import os
import streamlit as st
from typing import Dict, Any


def get_db_config() -> Dict[str, Any]:
    """Get database configuration from Streamlit secrets."""
    try:
        return {
            "host": st.secrets["db"]["host"],
            "port": st.secrets["db"]["port"],
            "database": st.secrets["db"]["database"],
            "user": st.secrets["db"]["user"],
            "password": st.secrets["db"]["password"],
        }
    except KeyError as e:
        st.error(f"Missing database configuration: {e}")
        st.stop()


def get_secret_key() -> str:
    """Get application secret key."""
    try:
        return st.secrets["app"]["secret_key"]
    except KeyError:
        return "default-secret-key-change-in-production"


def get_users_config() -> Dict[str, Dict[str, str]]:
    """Get users configuration from Streamlit secrets."""
    users = {}
    try:
        for key in st.secrets["users"].keys():
            user_config = st.secrets["users"][key]
            users[user_config["username"]] = {
                "password": user_config["password"],
                "role": user_config["role"]
            }
    except KeyError:
        pass
    return users



