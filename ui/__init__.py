"""UI module for the CareerLens Streamlit application.

This package contains:
- Page modules (top-level): Individual page implementations
- components/: Reusable UI components

Page modules:
- job_seeker_dashboard: Main CV upload and profile management page
- job_search_page: Job recommendations and semantic search
- headhunter_dashboard: Job publishing and management for recruiters
- recruitment_match_page: Smart talent matching
- ai_interview_page: AI-powered mock interviews
- resume_tailor_page: AI-powered tailored resume generation
- market_dashboard_page: Comprehensive market insights
- visualizations: Chart and visualization components
- resume_upload_page: Dedicated resume upload page
"""

# Re-export page modules
from .job_seeker_dashboard import main_analyzer_page
from .job_search_page import job_recommendations_page
from .headhunter_dashboard import (
    enhanced_head_hunter_page,
    publish_new_job,
    view_published_jobs,
    show_job_statistics
)
from .recruitment_match_page import (
    recruitment_match_dashboard,
    recruitment_match_page
)
from .ai_interview_page import (
    ai_interview_dashboard,
    show_interview_guidance,
    show_interview_instructions
)
from .resume_tailor_page import tailored_resume_page
from .market_dashboard_page import market_dashboard_page
from .visualizations import (
    create_enhanced_visualizations,
    create_job_comparison_radar
)
from .resume_upload_page import (
    resume_upload_page,
    process_resume_text
)

# Re-export components for convenience
from .components.hero_banner import render_hero_banner
from .components.job_cards import display_job_card
from .components.user_profile import display_user_profile
from .components.dashboard import (
    display_market_positioning_profile,
    display_ranked_matches_table,
    display_match_breakdown,
    display_skill_matching_matrix,
    calculate_match_scores
)
from .components.resume_editor import display_resume_generator, render_structured_resume_editor
from .components.match_feedback import display_match_score_feedback
from .components.styles import render_styles, get_logo_html

__all__ = [
    # Page modules - Job Seeker
    'main_analyzer_page',
    
    # Page modules - Job Search
    'job_recommendations_page',
    
    # Page modules - Headhunter
    'enhanced_head_hunter_page',
    'publish_new_job',
    'view_published_jobs',
    'show_job_statistics',
    
    # Page modules - Recruitment Match
    'recruitment_match_dashboard',
    'recruitment_match_page',
    
    # Page modules - AI Interview
    'ai_interview_dashboard',
    'show_interview_guidance',
    'show_interview_instructions',
    
    # Page modules - Resume Tailor
    'tailored_resume_page',
    
    # Page modules - Market Dashboard
    'market_dashboard_page',
    
    # Page modules - Visualizations
    'create_enhanced_visualizations',
    'create_job_comparison_radar',
    
    # Page modules - Resume Upload
    'resume_upload_page',
    'process_resume_text',
    
    # Components - Hero Banner
    'render_hero_banner',
    
    # Components - Job Cards
    'display_job_card',
    
    # Components - User Profile
    'display_user_profile',
    
    # Components - Dashboard
    'display_market_positioning_profile',
    'display_ranked_matches_table',
    'display_match_breakdown',
    'display_skill_matching_matrix',
    'calculate_match_scores',
    
    # Components - Resume Editor
    'display_resume_generator',
    'render_structured_resume_editor',
    
    # Components - Match Feedback
    'display_match_score_feedback',
    
    # Components - Styles
    'render_styles',
    'get_logo_html',
]
