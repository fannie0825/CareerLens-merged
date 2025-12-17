"""Sidebar UI component"""
import streamlit as st
import os
import time
from core.resume_parser import extract_text_from_resume, extract_profile_from_resume
from core.semantic_search import generate_and_store_resume_embedding
from ui.components.dashboard import display_skill_matching_matrix


def render_sidebar():
    """Render CareerLens sidebar with resume upload and search criteria settings.
    
    Note: Search functionality is now handled only in the dashboard (display_refine_results_section).
    The sidebar is simplified to only handle profile upload and filter settings.
    """
    with st.sidebar:
        # Branding/logo is rendered once by the main app (`streamlit_app.py`).
        # This modular sidebar must not re-render the global logo to avoid duplicates.
        display_skill_matching_matrix(st.session_state.user_profile)
