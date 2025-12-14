"""Page modules for the CareerLens Streamlit application - DEPRECATED.

NOTE: This module is maintained for backward compatibility.
New code should import directly from the `ui` package:

    from ui import main_analyzer_page, job_recommendations_page, ...

This module re-exports all page symbols from the new `ui` package.
"""

# Re-export everything from the new ui package
from ui import (
    main_analyzer_page,
    job_recommendations_page,
    enhanced_head_hunter_page,
    publish_new_job,
    view_published_jobs,
    show_job_statistics,
    recruitment_match_dashboard,
    recruitment_match_page,
    ai_interview_dashboard,
    show_interview_guidance,
    show_interview_instructions,
    tailored_resume_page,
    market_dashboard_page,
    create_enhanced_visualizations,
    create_job_comparison_radar,
    resume_upload_page,
    process_resume_text,
)

__all__ = [
    # Job Seeker Dashboard
    'main_analyzer_page',
    
    # Job Search Page
    'job_recommendations_page',
    
    # Headhunter Dashboard
    'enhanced_head_hunter_page',
    'publish_new_job',
    'view_published_jobs',
    'show_job_statistics',
    
    # Recruitment Match
    'recruitment_match_dashboard',
    'recruitment_match_page',
    
    # AI Interview
    'ai_interview_dashboard',
    'show_interview_guidance',
    'show_interview_instructions',
    
    # Resume Tailor
    'tailored_resume_page',
    
    # Market Dashboard
    'market_dashboard_page',
    
    # Visualizations
    'create_enhanced_visualizations',
    'create_job_comparison_radar',
    
    # Resume Upload
    'resume_upload_page',
    'process_resume_text',
]
