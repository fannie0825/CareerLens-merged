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
        st.markdown("### 1. Upload your CV to begin")
        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=['pdf', 'docx'],
            help="We parse your skills and experience to benchmark you against the market.",
            key="careerlens_resume_upload",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            file_key = f"{uploaded_file.name}_{uploaded_file.size}"
            current_cached_key = st.session_state.get('_last_uploaded_file_key')
            
            if current_cached_key != file_key:
                progress_bar = st.progress(0, text="📖 Reading resume...")
                resume_text = extract_text_from_resume(uploaded_file)
                
                if resume_text:
                    progress_bar.progress(30, text="✅ Resume read successfully")
                    st.session_state.resume_text = resume_text
                    st.session_state._last_uploaded_file_key = file_key
                    
                    progress_bar.progress(40, text="🤖 Extracting profile with AI...")
                    profile_data = extract_profile_from_resume(resume_text)
                    
                    if profile_data:
                        progress_bar.progress(80, text="📊 Finalizing profile...")
                        st.session_state.user_profile = {
                            'name': profile_data.get('name', ''),
                            'email': profile_data.get('email', ''),
                            'phone': profile_data.get('phone', ''),
                            'location': profile_data.get('location', ''),
                            'linkedin': profile_data.get('linkedin', ''),
                            'portfolio': profile_data.get('portfolio', ''),
                            'summary': profile_data.get('summary', ''),
                            'experience': profile_data.get('experience', ''),
                            'education': profile_data.get('education', ''),
                            'skills': profile_data.get('skills', ''),
                            'hard_skills': profile_data.get('skills', ''),  # Alias for compatibility
                            'certifications': profile_data.get('certifications', '')
                        }
                        
                        progress_bar.progress(90, text="🔗 Creating search embedding...")
                        generate_and_store_resume_embedding(resume_text, st.session_state.user_profile)
                        
                        progress_bar.progress(100, text="✅ Profile ready!")
                        time.sleep(0.3)
                        progress_bar.empty()
                        st.success("✅ Profile extracted!")
                    else:
                        progress_bar.empty()
                        st.warning("⚠️ Could not extract profile. Please try again.")
                else:
                    progress_bar.empty()
                    st.error("❌ Could not read the resume file.")
            else:
                if st.session_state.user_profile.get('name'):
                    st.success(f"✅ Using profile for: {st.session_state.user_profile.get('name', 'Unknown')}")
        
        st.markdown("---")
        
        # Display skill matching explanation
        display_skill_matching_matrix(st.session_state.user_profile)
        
        # Session Management
        if st.session_state.get('job_seeker_id'):
            st.markdown("---")
            st.caption("Session Management")
            current_id = st.session_state.get('job_seeker_id')
            st.info(f"Current Session ID: **{current_id}**")
            
            if st.button("🔄 Reset Session", key="sidebar_reset_btn", use_container_width=True, help="Clear current session and start over"):
                # Clear specific session state keys
                keys_to_clear = [
                    'job_seeker_id', 'user_profile', 'resume_text', 
                    'matched_jobs', 'autofill_data', 'analysis_complete',
                    'ai_analysis', 'generated_resume'
                ]
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.success("Session reset!")
                time.sleep(1)
                st.rerun()
