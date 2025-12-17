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
        # Display logo image at the top
        # Try to resolve logo path relative to workspace root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, "../.."))
        logo_path = os.path.join(root_dir, "CareerLens_Logo.png")
        
        # Check if custom logo exists
        custom_logo = os.path.join(root_dir, "logo.png")
        if os.path.exists(custom_logo):
            logo_path = custom_logo
            
        logo_displayed = False
        try:
            # Use Base64 embedding for robustness (same as streamlit_app.py)
            if os.path.exists(logo_path):
                import base64
                with open(logo_path, "rb") as f:
                    data = f.read()
                    logo_base64 = base64.b64encode(data).decode()
                
                st.markdown(
                    f'<img src="data:image/png;base64,{logo_base64}" style="width: 100%; max-width: 100%; margin-bottom: 20px;">',
                    unsafe_allow_html=True
                )
                logo_displayed = True
        except Exception as e:
            # Fallback
            print(f"DEBUG: Sidebar logo base64 loading failed: {e}")
            if os.path.exists(logo_path):
                st.image(logo_path, use_column_width=True)
                logo_displayed = True
        
        st.markdown("""
        <style>
            .sidebar-logo {
                color: white !important;
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-family: 'Montserrat', sans-serif;
                font-size: 2rem;
                font-weight: 700;
                letter-spacing: -1px;
                text-align: center;
                justify-content: center;
            }
            .sidebar-logo .brand-span {
                color: var(--brand-core);
            }
            .sidebar-logo .lens-span {
                color: var(--brand-glow);
            }
            .sidebar-tagline {
                color: var(--text-secondary-light);
                font-size: 0.7rem;
                margin: 0;
                font-family: 'Montserrat', sans-serif;
                text-transform: uppercase;
                letter-spacing: 2px;
                text-align: center;
            }
        </style>
        """, unsafe_allow_html=True)
        
        if not logo_displayed:
            st.markdown("""
            <div style="margin-bottom: 2rem;">
                <h2 class="sidebar-logo">
                    <span class="brand-span">Career</span><span class="lens-span">Lens</span>
                </h2>
                <p class="sidebar-tagline">AI Career Copilot • Hong Kong</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="margin-bottom: 2rem;">
                <p class="sidebar-tagline" style="margin-top: 0.5rem;">AI Career Copilot • Hong Kong</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display skill matching explanation
        display_skill_matching_matrix(st.session_state.user_profile)
