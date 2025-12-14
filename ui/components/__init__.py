"""UI components for the CareerLens application.

This package contains reusable UI components:
- sidebar: Sidebar navigation and controls
- hero_banner: Hero banner display
- dashboard: Dashboard metric cards and widgets
- job_cards: Job listing card displays
- resume_editor: Resume editing and generation UI
- styles: CSS styles and JavaScript
- match_feedback: Match score feedback display
- user_profile: User profile display and editing
"""

from .sidebar import render_sidebar
from .hero_banner import render_hero_banner
from .job_cards import display_job_card
from .user_profile import display_user_profile
from .dashboard import (
    display_market_positioning_profile,
    display_refine_results_section,
    display_ranked_matches_table,
    display_match_breakdown,
    display_skill_matching_matrix,
    calculate_match_scores
)
from .resume_editor import display_resume_generator, render_structured_resume_editor
from .match_feedback import display_match_score_feedback
from .styles import render_styles, get_logo_html

__all__ = [
    # Sidebar
    'render_sidebar',
    
    # Hero Banner
    'render_hero_banner',
    
    # Job Cards
    'display_job_card',
    
    # User Profile
    'display_user_profile',
    
    # Dashboard components
    'display_market_positioning_profile',
    'display_refine_results_section',
    'display_ranked_matches_table',
    'display_match_breakdown',
    'display_skill_matching_matrix',
    'calculate_match_scores',
    
    # Resume Editor
    'display_resume_generator',
    'render_structured_resume_editor',
    
    # Match Feedback
    'display_match_score_feedback',
    
    # Styles
    'render_styles',
    'get_logo_html',
]
