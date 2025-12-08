"""User profile display and editing"""
import streamlit as st
import time
from modules.resume_upload import extract_text_from_resume, extract_profile_from_resume
from modules.semantic_search import generate_and_store_resume_embedding


def display_user_profile():
    """Display and edit user profile"""
    st.header("👤 Your Profile")
    st.caption("Fill in your information to generate tailored resumes")
    
    st.markdown("---")
    st.subheader("📄 Upload Your Resume (Optional)")
    st.caption("Upload your resume to automatically extract your information")
    
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    if uploaded_file is not None:
        if st.button("🔍 Extract Information from Resume", type="primary", use_container_width=True):
            progress_bar = st.progress(0, text="📖 Reading resume...")
            
            resume_text = extract_text_from_resume(uploaded_file)
            
            if resume_text:
                progress_bar.progress(25, text=f"✅ Read {len(resume_text)} characters")
                st.session_state.resume_text = resume_text
                
                with st.expander("📝 Preview Extracted Text"):
                    st.text(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)
                
                progress_bar.progress(35, text="🤖 Extracting profile with AI...")
                profile_data = extract_profile_from_resume(resume_text)
                
                if profile_data:
                    progress_bar.progress(75, text="📊 Finalizing profile...")
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
                        'certifications': profile_data.get('certifications', '')
                    }
                    
                    progress_bar.progress(90, text="🔗 Creating search embedding...")
                    generate_and_store_resume_embedding(resume_text, st.session_state.user_profile)
                    
                    progress_bar.progress(100, text="✅ Complete!")
                    time.sleep(0.3)
                    progress_bar.empty()
                    
                    st.success("✅ Profile information extracted successfully! Review and edit below.")
                    st.balloons()
                    time.sleep(0.5)
                    st.rerun()
                else:
                    progress_bar.empty()
                    st.warning("⚠️ Could not extract structured information. Please fill in manually.")
            else:
                progress_bar.empty()
                st.error("❌ Could not read the resume file. Please try a different file.")
    
    st.markdown("---")
    
    with st.form("user_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=st.session_state.user_profile.get('name', ''))
            email = st.text_input("Email", value=st.session_state.user_profile.get('email', ''))
            phone = st.text_input("Phone", value=st.session_state.user_profile.get('phone', ''))
        
        with col2:
            location = st.text_input("Location", value=st.session_state.user_profile.get('location', ''))
            linkedin = st.text_input("LinkedIn URL", value=st.session_state.user_profile.get('linkedin', ''))
            portfolio = st.text_input("Portfolio/Website", value=st.session_state.user_profile.get('portfolio', ''))
        
        summary = st.text_area(
            "Professional Summary",
            value=st.session_state.user_profile.get('summary', ''),
            height=100,
            placeholder="Brief overview of your professional background..."
        )
        
        experience = st.text_area(
            "Work Experience",
            value=st.session_state.user_profile.get('experience', ''),
            height=150,
            placeholder="List your work experience with job titles, companies, dates, and key achievements..."
        )
        
        education = st.text_area(
            "Education",
            value=st.session_state.user_profile.get('education', ''),
            height=100,
            placeholder="Degrees, institutions, graduation dates..."
        )
        
        skills = st.text_area(
            "Skills",
            value=st.session_state.user_profile.get('skills', ''),
            height=80,
            placeholder="List your technical and soft skills (comma-separated)..."
        )
        
        certifications = st.text_area(
            "Certifications & Awards",
            value=st.session_state.user_profile.get('certifications', ''),
            height=80,
            placeholder="Professional certifications, awards, publications..."
        )
        
        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")
        
        if submitted:
            st.session_state.user_profile = {
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'linkedin': linkedin,
                'portfolio': portfolio,
                'summary': summary,
                'experience': experience,
                'education': education,
                'skills': skills,
                'certifications': certifications
            }
            st.success("✅ Profile saved successfully!")
            time.sleep(1)
            st.rerun()
