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

        def _split_csv(value):
            if value is None:
                return []
            if isinstance(value, list):
                return [str(s).strip() for s in value if str(s).strip()]
            if isinstance(value, str):
                return [s.strip() for s in value.split(",") if s.strip()]
            return []

        def _normalize_job_for_session(job: dict, *, fallback_id: str | None = None) -> dict:
            """Normalize a job dict so downstream renderers don't KeyError/AttributeError."""
            if not isinstance(job, dict):
                job = {}

            title = job.get("title") or job.get("job_title") or "Unknown Role"
            company = job.get("company") or job.get("company_name") or "Unknown Company"
            location = job.get("location") or "Unknown Location"
            description = job.get("description") or job.get("job_description") or ""
            url = job.get("url") or job.get("application_url") or job.get("job_url") or "#"

            skills = job.get("skills") or job.get("required_skills") or []
            if isinstance(skills, str):
                skills = _split_csv(skills)
            elif not isinstance(skills, list):
                skills = []

            salary = job.get("salary") or job.get("salary_range") or ""
            salary_min = job.get("salary_min")
            salary_max = job.get("salary_max")
            if not salary and (salary_min is not None or salary_max is not None):
                try:
                    if salary_min is not None and salary_max is not None:
                        salary = f"{float(salary_min):.0f}-{float(salary_max):.0f}"
                    elif salary_min is not None:
                        salary = f"{float(salary_min):.0f}"
                    elif salary_max is not None:
                        salary = f"{float(salary_max):.0f}"
                except Exception:
                    salary = ""

            normalized = dict(job)
            normalized.update(
                {
                    "id": job.get("id") or job.get("job_id") or fallback_id,
                    "title": title,
                    "company": company,
                    "location": location,
                    "description": description,
                    "url": url,
                    "skills": skills,
                    "salary": salary,
                    "salary_min": salary_min,
                    "salary_max": salary_max,
                    "posted_date": job.get("posted_date") or job.get("date_posted") or "",
                    "employment_type": job.get("employment_type") or job.get("job_type") or "",
                    "industry": job.get("industry") or "",
                }
            )
            return normalized

        def _normalize_match_result(result: dict, *, fallback_id: str) -> dict:
            """Normalize one match result (top-level scores + nested job dict)."""
            if not isinstance(result, dict):
                return {"job": _normalize_job_for_session({}, fallback_id=fallback_id)}

            job = result.get("job", result)
            normalized_job = _normalize_job_for_session(job if isinstance(job, dict) else {}, fallback_id=fallback_id)

            combined_score = (
                result.get("combined_score")
                if result.get("combined_score") is not None
                else result.get("combined_match_score")
            )
            if combined_score is None:
                combined_score = result.get("match_percentage", 0) or 0

            semantic_score = result.get("semantic_score")
            if semantic_score is None:
                semantic_score = result.get("cosine_similarity_score", result.get("similarity_score", 0)) or 0

            skill_match_percentage = result.get("skill_match_percentage")
            if skill_match_percentage is None:
                skill_match_percentage = result.get("skill_match_score", 0) or 0

            missing_skills = result.get("missing_skills", [])
            matched_skills = result.get("matched_skills", [])
            if isinstance(missing_skills, str):
                missing_skills = _split_csv(missing_skills)
            if isinstance(matched_skills, str):
                matched_skills = _split_csv(matched_skills)
            if not isinstance(missing_skills, list):
                missing_skills = []
            if not isinstance(matched_skills, list):
                matched_skills = []

            normalized = dict(result)
            normalized.update(
                {
                    "job": normalized_job,
                    "combined_score": combined_score,
                    "semantic_score": semantic_score,
                    "skill_match_percentage": skill_match_percentage,
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                }
            )
            return normalized

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

        # Safeguard: ensure analyzer/renderers don't crash on missing data.
        jobs = st.session_state.get("matched_jobs", [])
        if not jobs:
            st.warning("No jobs found to analyze. Please run a search first!")
            return

        if not isinstance(jobs, list):
            st.warning("Your job matches are not in the expected format. Please rerun Job Search to regenerate matched roles.")
            return

        matched_jobs = []
        for i, result in enumerate(jobs):
            if not isinstance(result, dict):
                continue
            matched_jobs.append(_normalize_match_result(result, fallback_id=str(result.get("id", i))))

        if not matched_jobs:
            st.warning("No jobs found to analyze. Please run a search first!")
            return

        st.session_state.matched_jobs = matched_jobs
        selected_idx = st.session_state.get("selected_job_index")
        if isinstance(selected_idx, int) and (selected_idx < 0 or selected_idx >= len(matched_jobs)):
            st.session_state.selected_job_index = None

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
