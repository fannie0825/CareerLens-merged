"""UI module for Streamlit components - DEPRECATED.

NOTE: This module is maintained for backward compatibility.
New code should import directly from the `ui` package:

    from ui import main_analyzer_page, render_sidebar, ...
    from ui.components import display_job_card, display_market_positioning_profile, ...

This module re-exports all symbols from the new `ui` package.
"""

# Re-export everything from the new ui package
from ui import (
    # Page modules
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
    
    # Components
    render_sidebar,
    render_hero_banner,
    display_job_card,
    display_user_profile,
    display_market_positioning_profile,
    display_refine_results_section,
    display_ranked_matches_table,
    display_match_breakdown,
    display_skill_matching_matrix,
    calculate_match_scores,
    display_resume_generator,
    render_structured_resume_editor,
    display_match_score_feedback,
    render_styles,
    get_logo_html,
)

__all__ = [
    # Core UI components
    'render_sidebar',
    'render_hero_banner',
    'display_job_card',
    'display_user_profile',
    'display_market_positioning_profile',
    'display_refine_results_section',
    'display_ranked_matches_table',
    'display_match_breakdown',
    'display_resume_generator',
    'display_skill_matching_matrix',
    'display_match_score_feedback',
    'render_structured_resume_editor',
    'calculate_match_scores',
    'render_styles',
    'get_logo_html',
    
    # Page modules
    'main_analyzer_page',
    'job_recommendations_page',
    'enhanced_head_hunter_page',
    'publish_new_job',
    'view_published_jobs',
    'show_job_statistics',
    'recruitment_match_dashboard',
    'recruitment_match_page',
    'ai_interview_dashboard',
    'show_interview_guidance',
    'show_interview_instructions',
    'tailored_resume_page',
    'market_dashboard_page',
    'create_enhanced_visualizations',
    'create_job_comparison_radar',
    'resume_upload_page',
    'process_resume_text',
]
