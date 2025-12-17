"""
Market Dashboard Page - Comprehensive Market Insights.

This module contains the modular CareerLens dashboard for viewing:
- Market positioning profile
- Ranked job matches
- Match breakdown and analysis
- Application copilot features
"""

import streamlit as st


def market_dashboard_page():
    """Market Dashboard Page - Modular CareerLens Dashboard"""
    # Check if modules are available
    try:
        from utils import _cleanup_session_state, validate_secrets
        from ui.components.styles import render_styles
        from ui.components import (
            render_sidebar as modular_render_sidebar,
            render_hero_banner,
            display_resume_generator as modular_display_resume_generator,
            display_market_positioning_profile,
            display_refine_results_section,
            display_ranked_matches_table,
            display_match_breakdown
        )
        from ui.visualizations import create_enhanced_visualizations
        MODULES_AVAILABLE = True
    except ImportError as e:
        MODULES_AVAILABLE = False
        import_error = str(e)
    
    if not MODULES_AVAILABLE:
        st.error("❌ Market Dashboard modules are not available. Please ensure the modules/ directory is properly installed.")
        st.info("The Market Dashboard requires the modular UI components from the modules/ directory.")
        return
    
    try:
        # Render CSS styles (Handled globally in streamlit_app.py)
        # render_styles()
        
        # Check if resume generator should be shown
        if st.session_state.get('show_resume_generator', False):
            modular_display_resume_generator()
            return
        
        # Render modular sidebar with controls
        modular_render_sidebar()
        
        # Render hero banner at the top of main content
        render_hero_banner(
            st.session_state.get('user_profile', {}),
            st.session_state.matched_jobs if st.session_state.get('dashboard_ready', False) else None
        )
        
        # Main dashboard area - only show after analysis
        if not st.session_state.get('dashboard_ready', False) or not st.session_state.get('matched_jobs'):
            st.info("👆 Upload your CV in the sidebar to get started. Once uploaded, use the 'Refine Results' section below to search for jobs and see your market positioning.")
            
            # Show the Refine Results section even before search to allow user to initiate search
            display_refine_results_section([], st.session_state.get('user_profile', {}))
            return
        
        # Display Market Positioning Profile (Top Section)
        display_market_positioning_profile(
            st.session_state.matched_jobs,
            st.session_state.get('user_profile', {})
        )
        
        # Display Refine Results Section
        display_refine_results_section(
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
