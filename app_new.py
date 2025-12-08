"""
CareerLens - AI Career Intelligence Platform
Main application file with modular imports

WebSocket Stability Notes:
- This application includes multiple mechanisms to prevent WebSocket disconnections:
  1. Chunked sleep operations to send periodic UI updates
  2. Keepalive pings during long-running operations
  3. Progress tracking with automatic connection maintenance
  4. Optimized server configuration in .streamlit/config.toml
"""
import warnings
import os
import gc
import sys
warnings.filterwarnings('ignore')

# Streamlit Cloud optimization - set before importing streamlit
os.environ['STREAMLIT_LOG_LEVEL'] = 'error'
os.environ['SQLITE_TMPDIR'] = '/tmp'

# Disable ALL Streamlit telemetry/analytics to prevent tracking script loads
# Note: Browser may still show "Tracking Prevention" console messages - this is
# the browser blocking residual analytics attempts, not an app error
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = 'false'

# Increase recursion limit for complex operations (prevents stack overflow)
sys.setrecursionlimit(3000)

import streamlit as st

# Set page config FIRST (must be first Streamlit command)
st.set_page_config(
    page_title="CareerLens - AI Career Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "CareerLens - AI-powered career intelligence platform"
    }
)

# Import all modules - UI imports are lightweight, heavy deps are lazy-loaded
from modules.utils import _cleanup_session_state, validate_secrets
from modules.ui.styles import render_styles
from modules.ui import (
    render_sidebar,
    render_hero_banner,
    display_resume_generator,
    display_market_positioning_profile,
    display_refine_results_section,
    display_ranked_matches_table,
    display_match_breakdown
)

# Render CSS styles (lightweight - no heavy imports)
render_styles()

# Note: gc.collect() and websocket keepalive moved to after user interaction
# to speed up initial page load

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'jobs_cache' not in st.session_state:
    st.session_state.jobs_cache = {}
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'generated_resume' not in st.session_state:
    st.session_state.generated_resume = None
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None
if 'show_resume_generator' not in st.session_state:
    st.session_state.show_resume_generator = False
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'resume_embedding' not in st.session_state:
    st.session_state.resume_embedding = None
if 'matched_jobs' not in st.session_state:
    st.session_state.matched_jobs = []
if 'match_score' not in st.session_state:
    st.session_state.match_score = None
if 'missing_keywords' not in st.session_state:
    st.session_state.missing_keywords = None
if 'show_profile_editor' not in st.session_state:
    st.session_state.show_profile_editor = False
if 'use_auto_match' not in st.session_state:
    st.session_state.use_auto_match = False
if 'expanded_job_index' not in st.session_state:
    st.session_state.expanded_job_index = None
if 'industry_filter' not in st.session_state:
    st.session_state.industry_filter = None
if 'salary_min' not in st.session_state:
    st.session_state.salary_min = None
if 'salary_max' not in st.session_state:
    st.session_state.salary_max = None
if 'selected_job_index' not in st.session_state:
    st.session_state.selected_job_index = None
if 'dashboard_ready' not in st.session_state:
    st.session_state.dashboard_ready = False
if 'user_skills_embeddings_cache' not in st.session_state:
    st.session_state.user_skills_embeddings_cache = {}
if 'skill_embeddings_cache' not in st.session_state:
    st.session_state.skill_embeddings_cache = {}

# Limit search history size
MAX_SEARCH_HISTORY = 20
if len(st.session_state.search_history) > MAX_SEARCH_HISTORY:
    st.session_state.search_history = st.session_state.search_history[-MAX_SEARCH_HISTORY:]

# Run memory cleanup after session state is initialized
try:
    _cleanup_session_state()
except Exception:
    pass


def main():
    """Main application function"""
    try:
        # Check if resume generator should be shown
        if st.session_state.get('show_resume_generator', False):
            display_resume_generator()
            return
        
        # Render sidebar with controls
        render_sidebar()
        
        # Render hero banner at the top of main content
        render_hero_banner(
            st.session_state.user_profile if st.session_state.user_profile else {},
            st.session_state.matched_jobs if st.session_state.get('dashboard_ready', False) else None
        )
        
        # Main dashboard area - only show after analysis
        if not st.session_state.get('dashboard_ready', False) or not st.session_state.matched_jobs:
            st.info("👆 Upload your CV in the sidebar and click 'Analyze Profile & Find Matches' to see your market positioning and ranked opportunities.")
            return
        
        # Display Market Positioning Profile (Top Section)
        display_market_positioning_profile(
            st.session_state.matched_jobs,
            st.session_state.user_profile
        )
        
        # Display Refine Results Section
        display_refine_results_section(
            st.session_state.matched_jobs,
            st.session_state.user_profile
        )
        
        # Display Smart Ranked Matches Table (Middle Section)
        display_ranked_matches_table(
            st.session_state.matched_jobs,
            st.session_state.user_profile
        )
        
        # Display Match Breakdown & Application Copilot (Bottom Section)
        display_match_breakdown(
            st.session_state.matched_jobs,
            st.session_state.user_profile
        )
    except Exception as e:
        st.error(f"""
        ❌ **Application Error**
        
        An unexpected error occurred: {e}
        
        Please check:
        1. All required secrets are configured
        2. All dependencies are installed
        3. The application logs for more details
        """)
        st.exception(e)


if __name__ == "__main__":
    # Wrap main() in error handling to prevent crashes
    try:
        main()
    except Exception as e:
        st.error(f"""
        ❌ **Startup Error**
        
        The application failed to start: {e}
        
        This is likely due to:
        1. Missing or incorrect secrets configuration
        2. Missing dependencies
        3. A code error in the application
        
        Please check your Streamlit Cloud logs for more details.
        """)
        st.exception(e)
