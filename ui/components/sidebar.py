"""Sidebar UI component (modular pages)."""
import streamlit as st
from ui.components.dashboard import display_skill_matching_matrix


def render_sidebar():
    """Render the modular Market Dashboard sidebar content."""
    with st.sidebar:
        # Logo/branding is rendered centrally in streamlit_app.py to avoid duplicate
        # sidebar headers when modular pages add their own sidebar controls.
        st.markdown("---")
        st.subheader("📌 Market Dashboard")
        
        # Display skill matching explanation
        user_profile = st.session_state.get("user_profile") or {}
        if user_profile:
            display_skill_matching_matrix(user_profile)
        else:
            st.info("Upload your CV to see skill matching insights.")
