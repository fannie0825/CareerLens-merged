"""Sidebar UI component"""
import streamlit as st
import os
import time
from core.resume_parser import extract_text_from_resume, extract_profile_from_resume
from core.semantic_search import generate_and_store_resume_embedding
from ui.components.dashboard import display_skill_matching_matrix


def render_sidebar():
    """Render CareerLens sidebar with resume upload and search criteria settings.
    
    Note: Job fetching/filtering is handled in the Job Search page.
    The sidebar is simplified to only handle profile upload and guidance.
    """
    with st.sidebar:
        # Logo/branding is rendered centrally in streamlit_app.py to avoid duplicate
        # sidebar headers when modular pages add their own sidebar controls.
        st.markdown("---")
        st.subheader("📌 Your Market Position")
        
        # Display skill matching explanation
        display_skill_matching_matrix(st.session_state.user_profile)
