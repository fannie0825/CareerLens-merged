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
        from utils.config import get_num_jobs_to_search
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

        # Page header (fast)
        st.title("📊 Your Market Position")

        # =========================================================
        # Smart entry: show focused context if arriving from Job Search
        # =========================================================
        job_context = st.session_state.get("selected_job")
        if job_context:
            target_title = job_context.get("title") or job_context.get("job_title") or "Selected role"
            target_company = job_context.get("company") or job_context.get("company_name") or ""
            subtitle = f"{target_title} @ {target_company}" if target_company else target_title
            st.subheader(f"Focus role: {subtitle}")
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

        # ---------------------------------------------------------------------
        # State drift guard: make sure matched jobs exist before analysis runs
        # ---------------------------------------------------------------------
        # Job Search stores the selected speed under this key.
        # Fall back to older keys if they still exist in a user's session.
        search_mode_label = (
            st.session_state.get("job_search_speed")
            or st.session_state.get("search_mode")
            or st.session_state.get("job_search_mode")
        )
        expected_jobs = get_num_jobs_to_search(search_mode_label, default=15) if search_mode_label else None

        # If the user refreshed/navigated directly here, session state may have
        # been re-initialized (matched_jobs=[]). Try to rehydrate from the DB.
        if not st.session_state.get("matched_jobs"):
            job_seeker_id = st.session_state.get("job_seeker_id")
            if job_seeker_id:
                try:
                    from database import get_matched_jobs_for_seeker

                    # Fetch at least the expected count (or a reasonable default).
                    limit = max(int(expected_jobs or 0), 25)
                    saved_jobs = get_matched_jobs_for_seeker(job_seeker_id, min_score=0.0, limit=limit)

                    processed_matches = []
                    for job in saved_jobs or []:
                        if not isinstance(job, dict):
                            continue

                        def _split_csv(value):
                            if value is None:
                                return []
                            if isinstance(value, list):
                                return [str(s).strip() for s in value if str(s).strip()]
                            if isinstance(value, str):
                                return [s.strip() for s in value.split(",") if s.strip()]
                            return []

                        processed_matches.append({
                            "job": {
                                "title": job.get("job_title", ""),
                                "company": job.get("company_name", ""),
                                "location": job.get("location", ""),
                                "description": job.get("job_description", ""),
                                "skills": _split_csv(job.get("required_skills")),
                                "url": job.get("application_url", ""),
                                "posted_date": job.get("posted_date", ""),
                                "employment_type": job.get("employment_type", ""),
                                "industry": job.get("industry", ""),
                                "salary_min": job.get("salary_min"),
                                "salary_max": job.get("salary_max"),
                            },
                            # Normalize DB fields to in-app visualization fields
                            "combined_score": job.get("match_percentage", 0) or 0,
                            "semantic_score": job.get("cosine_similarity_score", 0) or 0,
                            "skill_match_percentage": job.get("skill_match_score", 0) or 0,
                            "experience_match_score": job.get("experience_match_score", 0) or 0,
                            "matched_skills": _split_csv(job.get("matched_skills")),
                            "missing_skills": _split_csv(job.get("missing_skills")),
                        })

                    if processed_matches:
                        st.session_state.matched_jobs = processed_matches
                except Exception:
                    # If DB rehydration fails, fall back to the standard empty-state UI.
                    pass

        if not st.session_state.get('matched_jobs'):
            st.info(
                "To see your market positioning, first upload your CV on **Job Seeker** and generate job matches on **Job Search**. "
                "Then come back here to review your positioning, skill gaps, and match breakdown."
            )
            if expected_jobs:
                st.caption(f"Tip: your current Search Mode is set to fetch about **{expected_jobs}** jobs per run.")
            return

        matched_jobs = st.session_state.matched_jobs
        if not isinstance(matched_jobs, list):
            st.warning("Your job matches are not in the expected format. Please rerun Job Search to regenerate matched roles.")
            return

        st.caption(f"Using **{len(matched_jobs)}** matched roles to estimate your positioning and skill gaps.")

        # Quick skill-gap summary (fast, no charts)
        try:
            from collections import Counter

            missing_counter: Counter[str] = Counter()
            for result in matched_jobs:
                if not isinstance(result, dict):
                    continue

                job_data = result.get("job", result)
                missing = (
                    result.get("missing_skills")
                    or job_data.get("missing_skills")
                    or job_data.get("missing_keywords")
                    or []
                )

                if isinstance(missing, str):
                    missing = [s.strip() for s in missing.split(",") if s.strip()]

                if isinstance(missing, list):
                    missing_counter.update([s.strip() for s in missing if isinstance(s, str) and s.strip()])

            top_missing = missing_counter.most_common(10)
            if top_missing:
                st.markdown("### 🧩 Most Common Missing Skills (across your matched roles)")
                st.write(", ".join([f"**{skill}** ({count})" for skill, count in top_missing]))
        except Exception:
            # Don't block the page if summary parsing fails
            pass
        
        # Display Market Positioning Profile (Top Section)
        display_market_positioning_profile(
            matched_jobs,
            st.session_state.get('user_profile', {})
        )
        
        # Keep landing fast: heavy charts and deep dive are opt-in.
        with st.expander("📈 Charts & Visualizations", expanded=False):
            create_enhanced_visualizations(
                matched_jobs,
                st.session_state.get('user_profile', {})
            )
        
        # Additional detailed analysis
        with st.expander("🔍 Deep Dive Analysis", expanded=False):
            # Industry distribution of matched jobs
            industries = {}
            for job in matched_jobs:
                # Handle both nested 'job' structure and direct job properties
                job_data = job.get('job', job) if isinstance(job, dict) else {}
                
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
            st.markdown("#### 🏆 Ranked Matches")
            display_ranked_matches_table(
                matched_jobs,
                st.session_state.get('user_profile', {})
            )
            
            # Display Match Breakdown & Application Copilot (Bottom Section)
            st.markdown("#### 🧠 Match Breakdown & Skill Gaps")
            display_match_breakdown(
                matched_jobs,
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
