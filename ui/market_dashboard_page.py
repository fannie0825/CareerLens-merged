"""
Your Market Position Page - Comprehensive Market Insights.

This module contains the modular CareerLens dashboard for viewing:
- Market positioning profile
- Ranked job matches
- Match breakdown and analysis
- Application copilot features
"""

import streamlit as st


def market_dashboard_page():
    """Your Market Position Page - Modular CareerLens Dashboard"""
    # Check if modules are available
    try:
        from utils import _cleanup_session_state, validate_secrets
        from ui.components.styles import render_styles
        from ui.components import (
            render_hero_banner,
            display_resume_generator as modular_display_resume_generator,
            display_market_positioning_profile,
            display_ranked_matches_table,
            display_match_breakdown
        )
        from ui.visualizations import create_enhanced_visualizations
        MODULES_AVAILABLE = True
    except ImportError as e:
        MODULES_AVAILABLE = False
        import_error = str(e)
    
    if not MODULES_AVAILABLE:
        st.error("❌ Your Market Position modules are not available. Please ensure the modules/ directory is properly installed.")
        st.info("This page requires the modular UI components from the modules/ directory.")
        return
    
    try:
        # Render CSS styles (Handled globally in streamlit_app.py)
        # render_styles()

        # =========================================================
        # Smart entry: show focused context if arriving from Job Search
        # =========================================================
        job_context = st.session_state.get("selected_job")
        if job_context:
            target_title = job_context.get("title") or job_context.get("job_title") or "Selected role"
            target_company = job_context.get("company") or job_context.get("company_name") or ""
            subtitle = f"{target_title} @ {target_company}" if target_company else target_title
            st.subheader(f"📊 Your Market Position for: {subtitle}")
            st.caption("Tip: run a Job Search first to generate matched roles, then review your positioning here.")
        
        # Check if resume generator should be shown
        if st.session_state.get('show_resume_generator', False):
            modular_display_resume_generator()
            return
        
        # Render hero banner at the top of main content
        render_hero_banner(
            st.session_state.get('user_profile', {}),
            st.session_state.get('matched_jobs')
        )
        
        if not st.session_state.get('matched_jobs'):
            st.info(
                "To see your market positioning, first upload your CV on **Job Seeker** and generate job matches on **Job Search**. "
                "Then come back here to review your positioning, skill gaps, and match breakdown."
            )
            return
        
        # Display Market Positioning Profile (Top Section)
        display_market_positioning_profile(
            st.session_state.matched_jobs,
            st.session_state.get('user_profile', {})
        )
        
        # Create enhanced visualizations
        create_enhanced_visualizations(
            st.session_state.matched_jobs, 
            st.session_state.get('user_profile', {})
        )
        
        # Additional detailed analysis
        st.markdown("---")
        st.subheader("🔍 Deep Dive Analysis")
        
        # Industry distribution of matched jobs
        matched_jobs = st.session_state.matched_jobs
        industries = {}
        for job in matched_jobs:
            # Handle both nested 'job' structure and direct job properties
            job_data = job.get('job', job)
            
            # Extract industry from company or description
            company = job_data.get('company', '').lower()
            if any(tech in company for tech in ['tech', 'software', 'ai', 'data']):
                industry = 'Technology'
            elif any(finance in company for finance in ['bank', 'finance', 'investment', 'capital']):
                industry = 'Finance'
            elif any(consult in company for consult in ['consulting', 'consultancy']):
                industry = 'Consulting'
            else:
                industry = 'Other'
            
            industries[industry] = industries.get(industry, 0) + 1
        
        if industries:
            st.markdown("#### 🏭 Industries in Your Matches")
            for industry, count in industries.items():
                percentage = (count / len(matched_jobs)) * 100
                st.write(f"- **{industry}**: {count} jobs ({percentage:.1f}%)")
        
        # Display Smart Ranked Matches Table (Middle Section)
        display_ranked_matches_table(
            st.session_state.matched_jobs,
            st.session_state.get('user_profile', {})
        )
        
        # Display Match Breakdown & Application Copilot (Bottom Section)
        display_match_breakdown(
            st.session_state.matched_jobs,
            st.session_state.get('user_profile', {})
        )
    except Exception as e:
        st.error(f"""
        ❌ **Dashboard Error**
        
        An unexpected error occurred: {e}
        
        Please check:
        1. All required secrets are configured
        2. All dependencies are installed
        3. The application logs for more details
        """)
