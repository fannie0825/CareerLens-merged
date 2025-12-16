"""Sidebar UI component"""
import streamlit as st
import time
import sqlite3
from core.resume_parser import extract_text_from_resume, extract_profile_from_resume
from core.semantic_search import generate_and_store_resume_embedding
from ui.components.dashboard import display_skill_matching_matrix

def display_token_usage_sidebar():
    """Display token usage and cost tracking in sidebar"""
    if 'token_tracker' in st.session_state:
        tracker = st.session_state.token_tracker
        summary = tracker.get_summary()
        
        if summary['total_tokens'] > 0:
            with st.expander("📊 API Usage Stats"):
                col1, col2 = st.columns(2)
                with col1:
                    st.caption("Tokens")
                    st.write(f"{summary['total_tokens']:,}")
                with col2:
                    st.caption("Cost (USD)")
                    st.write(f"${summary['estimated_cost_usd']:.4f}")

def render_sidebar():
    """Render CareerLens sidebar with navigation, resume upload and tools."""
    
    with st.sidebar:
        # 1. Logo and Branding
        st.image("CareerLens_Logo.png", use_container_width=True)
        
        st.markdown("""
        <style>
            /* CareerLens Logo and Branding */
            .careerlens-logo {
                font-family: 'Montserrat', sans-serif;
                font-size: 2rem;
                font-weight: 700;
                text-align: center;
                margin-bottom: 0.5rem;
                letter-spacing: -1px;
            }
            .careerlens-logo .brand-span {
                color: var(--brand-core);
            }
            .careerlens-logo .lens-span {
                color: var(--brand-glow);
            }
            .careerlens-tagline {
                font-family: 'Montserrat', sans-serif;
                color: var(--text-secondary-light);
                text-transform: uppercase;
                letter-spacing: 2px;
                font-size: 0.7rem;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            /* Navigation Section Headers */
            .nav-section-header {
                font-family: 'Montserrat', sans-serif;
                font-weight: 700;
                font-size: 1.1rem;
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
                padding-left: 0.5rem;
                border-left: 3px solid var(--brand-glow);
                color: black !important;
            }
        </style>
        
        <div class="careerlens-logo">
            <span class="brand-span">Career</span><span class="lens-span">Lens</span>
        </div>
        <div class="careerlens-tagline">AI Career Copilot • Hong Kong</div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 2. Navigation
        # Job Seeker Section
        st.markdown('<div class="nav-section-header">👤 Job Seeker</div>', unsafe_allow_html=True)
        if st.button("🏠 Job Seeker", use_container_width=True, key="main_btn"):
            st.session_state.current_page = "main"
        if st.button("💼 Job Matching", use_container_width=True, key="job_matching_btn"):
            st.session_state.current_page = "job_recommendations"
        if st.button("📝 AI Powered Tailored Resume", use_container_width=True, key="tailored_resume_btn"):
            st.session_state.current_page = "tailored_resume"
        if st.button("🤖 AI Mock Interview", use_container_width=True, key="ai_interview_btn"):
            st.session_state.current_page = "ai_interview"
        if st.button("📊 Market Dashboard", use_container_width=True, key="market_dashboard_btn"):
            st.session_state.current_page = "market_dashboard"
        if st.button("🧠 How This App Works", use_container_width=True, key="how_it_works_btn"):
            st.session_state.current_page = "how_it_works"
        
        st.markdown("---")
        
        # Recruiter Section
        st.markdown('<div class="nav-section-header">🎯 Recruiter</div>', unsafe_allow_html=True)
        if st.button("📋 Job Posting", use_container_width=True, key="job_posting_btn"):
            st.session_state.current_page = "head_hunter"
        if st.button("🔍 Recruitment Match", use_container_width=True, key="recruitment_match_btn"):
            st.session_state.current_page = "recruitment_match"
            
        st.markdown("---")

        # 3. CareerLens Tools (Resume Upload + Filters)
        st.subheader("🔍 CareerLens Tools")
        
        with st.expander("📄 Resume Upload", expanded=False):
            st.caption("Upload your CV to enable AI features")
            uploaded_file = st.file_uploader(
                "Upload your resume",
                type=['pdf', 'docx'],
                help="We parse your skills and experience to benchmark you against the market.",
                key="sidebar_resume_upload",
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
                            st.warning("⚠️ Could not extract profile.")
                    else:
                        progress_bar.empty()
                        st.error("❌ Could not read file.")
                else:
                    if st.session_state.user_profile.get('name'):
                        st.success(f"✅ Active: {st.session_state.user_profile.get('name')}")

        # Filters - Always show or conditional?
        # Replicating logic from streamlit_app.py: show only on job_recommendations
        if st.session_state.get('current_page') == "job_recommendations":
            with st.expander("🏭 Industry Filters", expanded=True):
                target_domains = st.multiselect(
                    "Target Domains",
                    options=["FinTech", "ESG & Sustainability", "Data Analytics", "Digital Transformation", 
                            "Investment Banking", "Consulting", "Technology", "Healthcare", "Education"],
                    default=st.session_state.get('target_domains', []),
                    key="sidebar_domain_filter"
                )
                st.session_state.target_domains = target_domains
                
                salary_exp = st.slider(
                    "Min. Salary (HKD)",
                    min_value=0,
                    max_value=150000,
                    value=st.session_state.get('salary_expectation', 0),
                    step=5000,
                    key="sidebar_salary_filter"
                )
                st.session_state.salary_expectation = salary_exp

        # Token Usage
        display_token_usage_sidebar()
        
        st.markdown("---")
        
        # Database Debug
        with st.expander("🔧 Database Debug"):
            if st.button("View All Job Seeker Records"):
                try:
                    conn = sqlite3.connect('job_seeker.db')
                    c = conn.cursor()
                    c.execute("SELECT job_seeker_id, timestamp, education_level, primary_role FROM job_seekers ORDER BY id DESC")
                    results = c.fetchall()
                    conn.close()
                    
                    if results:
                        st.write("📋 All Job Seeker Records:")
                        for record in results:
                            st.write(f"- ID: {record[0]}\n  Time: {record[1]}\n  Edu: {record[2]}\n  Role: {record[3]}")
                    else:
                        st.write("No job seeker records yet")
                except Exception as e:
                    st.error(f"Query failed: {e}")
            
            # Display current session state ID
            current_id = st.session_state.get('job_seeker_id')
            if current_id:
                st.info(f"Session ID: {current_id}")

        # Usage Instructions
        st.markdown("---")
        with st.expander("💡 Usage Instructions"):
            st.markdown("""
            **For Job Seekers:**
            - **Job Seeker**: Upload CV & fill profile
            - **Job Matching**: AI-matched positions
            - **AI Powered Tailored Resume**: Generate resumes
            - **AI Mock Interview**: Practice interviews
            - **Market Dashboard**: Market insights
            
            **For Recruiters:**
            - **Job Posting**: Publish jobs
            - **Recruitment Match**: Smart matching
            """)
            
        # Footer
        st.markdown("---")
        st.caption("🤖 Powered by Azure OpenAI, Pinecone Vector Search, RapidAPI LinkedIn Jobs, and CareerLens AI")
