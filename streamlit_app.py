"""
CareerLens - AI Career Intelligence Platform
Combined application with multi-page navigation and modular dashboard

WebSocket Stability Notes:
- This application includes multiple mechanisms to prevent WebSocket disconnections:
  1. Chunked sleep operations to send periodic UI updates
  2. Keepalive pings during long-running operations
  3. Progress tracking with automatic connection maintenance
  4. Optimized server configuration in .streamlit/config.toml
  5. Connection state tracking and recovery mechanisms
  6. Automatic reconnection handling via session state preservation
"""
import warnings
import os
import gc
import sys
import time
warnings.filterwarnings('ignore')

# Streamlit Cloud optimization - set before importing streamlit
os.environ['STREAMLIT_LOG_LEVEL'] = 'error'
os.environ['SQLITE_TMPDIR'] = '/tmp'

# Disable ALL Streamlit telemetry/analytics to prevent tracking script loads
# Note: Browser may still show "Tracking Prevention" console messages - this is
# the browser blocking residual analytics attempts, not an app error
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = 'false'

# WebSocket connection timeout settings (affects Streamlit Cloud behavior)
# Lower values = more frequent keepalive pings but more network overhead
os.environ['STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION'] = 'true'
os.environ['STREAMLIT_SERVER_MAX_MESSAGE_SIZE'] = '200'

# Increase recursion limit for complex operations (prevents stack overflow)
sys.setrecursionlimit(3000)

import streamlit as st
import sqlite3
from typing import List, Dict

# Import backend utilities
from core.rate_limiting import TokenUsageTracker

# Import How It Works page
from how_it_works import render_how_it_works_page

# Import database initialization
from database import init_database, init_head_hunter_database

# Import configuration
from config import Config

# Page config
st.set_page_config(
    page_title="CareerLens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "CareerLens - AI Career Intelligence Platform • Hong Kong"
    }
)

# ============================================================================
# IMPORTS FOR PAGE MODULES AND UTILITIES
# ============================================================================
try:
    from utils import _cleanup_session_state, validate_secrets
    from utils.helpers import (
        _chunked_sleep,
        _websocket_keepalive,
        _ensure_websocket_alive,
        ProgressTracker
    )
    from ui.components.styles import render_styles
    
    # Inject global styles immediately
    render_styles()

    from ui import (
        # Page modules
        main_analyzer_page,
        job_recommendations_page,
        enhanced_head_hunter_page,
        recruitment_match_dashboard,
        ai_interview_dashboard,
        tailored_resume_page,
        market_dashboard_page,
        # UI components (for compatibility)
        render_hero_banner,
        display_resume_generator as modular_display_resume_generator,
        display_market_positioning_profile,
        display_skill_matching_matrix,
    )
    MODULES_AVAILABLE = True
    WEBSOCKET_UTILS_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    WEBSOCKET_UTILS_AVAILABLE = False
    
    # Provide fallback implementations for WebSocket utilities
    def _websocket_keepalive(message=None, force=False):
        """Fallback no-op implementation"""
        pass
    
    def _ensure_websocket_alive():
        """Fallback no-op implementation"""
        pass
    
    def _chunked_sleep(delay, message_prefix=""):
        """Fallback implementation using regular sleep"""
        time.sleep(delay)
    
    class ProgressTracker:
        """Fallback implementation without WebSocket keepalive"""
        def __init__(self, description="Processing", total_steps=100, show_progress=True):
            self.description = description
            self.total_steps = total_steps
            self.show_progress = show_progress
            self.current_step = 0
            self.progress_bar = None
        
        def __enter__(self):
            if self.show_progress:
                self.progress_bar = st.progress(0, text=f"⏳ {self.description}...")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.progress_bar:
                self.progress_bar.empty()
            return False
        
        def update(self, step=None, message=None):
            if step is not None:
                self.current_step = step
            else:
                self.current_step += 1
            progress = min(self.current_step / self.total_steps, 1.0)
            if self.show_progress and self.progress_bar:
                display_message = message or f"⏳ {self.description}... ({int(progress * 100)}%)"
                self.progress_bar.progress(progress, text=display_message)
        
        def set_message(self, message):
            if self.show_progress and self.progress_bar:
                progress = self.current_step / self.total_steps
                self.progress_bar.progress(progress, text=f"⏳ {message}")
    
    # Import page modules directly if modular UI failed
    try:
        from ui import (
            main_analyzer_page,
            job_recommendations_page,
            enhanced_head_hunter_page,
            recruitment_match_dashboard,
            ai_interview_dashboard,
            tailored_resume_page,
            market_dashboard_page,
        )
        MODULES_AVAILABLE = True
    except ImportError:
        MODULES_AVAILABLE = False


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================
@st.cache_resource
def initialize_databases():
    init_database()
    init_head_hunter_database()
    return True

_db_initialized = initialize_databases()


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
# Initialize token tracker in session state
if 'token_tracker' not in st.session_state:
    st.session_state.token_tracker = TokenUsageTracker()

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"

# Additional session state for modular dashboard
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

# WebSocket connection tracking for recovery
if 'ws_connection_time' not in st.session_state:
    st.session_state.ws_connection_time = time.time()
if 'ws_last_activity' not in st.session_state:
    st.session_state.ws_last_activity = time.time()
if 'ws_reconnect_count' not in st.session_state:
    st.session_state.ws_reconnect_count = 0

# Update last activity timestamp on each rerun
st.session_state.ws_last_activity = time.time()

# Check for potential reconnection (session was idle for > 30 seconds)
if time.time() - st.session_state.get('ws_last_activity', time.time()) > 30:
    st.session_state.ws_reconnect_count += 1
    st.session_state.ws_connection_time = time.time()

# Limit search history size
MAX_SEARCH_HISTORY = 5
if len(st.session_state.search_history) > MAX_SEARCH_HISTORY:
    st.session_state.search_history = st.session_state.search_history[:MAX_SEARCH_HISTORY]

# Run memory cleanup after session state is initialized (if modules available)
if MODULES_AVAILABLE and WEBSOCKET_UTILS_AVAILABLE:
    try:
        _cleanup_session_state()
    except Exception:
        pass

# Periodic WebSocket keepalive on app rerun
try:
    _ensure_websocket_alive()
except Exception:
    pass


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def display_token_usage():
    """Display token usage and cost tracking"""
    if 'token_tracker' in st.session_state:
        tracker = st.session_state.token_tracker
        summary = tracker.get_summary()
        
        if summary['total_tokens'] > 0:
            with st.expander("📊 API Usage Stats"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Tokens", f"{summary['total_tokens']:,}")
                with col2:
                    st.metric("Embedding Tokens", f"{summary['embedding_tokens']:,}")
                with col3:
                    st.metric("Est. Cost", f"${summary['estimated_cost_usd']:.4f}")


# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.markdown("""
<style>
    /* CareerLens Logo and Branding */
    .careerlens-logo {
        font-family: 'Montserrat', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .careerlens-logo .brand-span {
        color: var(--brand-core);
    }
    .careerlens-logo .lens-span {
        color: var(--brand-glow);
    }
    .careerlens-tagline {
        font-family: 'Montserrat', sans-serif;
        color: var(--text-secondary-light);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.7rem;
        text-align: center;
        margin-bottom: 2rem;
        margin-top: 0.5rem;
    }

</style>
""", unsafe_allow_html=True)

# Sidebar Logo (centralized)
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "CareerLens_Logo.png")

# Check for custom logo override
custom_logo_path = os.path.join(current_dir, "logo.png")
if os.path.exists(custom_logo_path):
    logo_path = custom_logo_path

logo_displayed = False

# Robust image loading using Base64 to prevent disappearance
# This embeds the image directly in the HTML, bypassing filesystem/serving issues
if os.path.exists(logo_path):
    try:
        import base64
        with open(logo_path, "rb") as f:
            data = f.read()
            logo_base64 = base64.b64encode(data).decode()
        
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{logo_base64}" style="width: 100%; max-width: 100%; margin-bottom: 20px;">',
            unsafe_allow_html=True
        )
        logo_displayed = True
    except Exception as e:
        # Fallback to standard Streamlit image if base64 fails
        print(f"DEBUG: Logo base64 loading failed: {e}")
        try:
            st.sidebar.image(logo_path, use_column_width=True)
            logo_displayed = True
        except Exception as e2:
            print(f"DEBUG: Logo fallback failed: {e2}")
            pass

if not logo_displayed:
    st.sidebar.markdown("""
    <div class="careerlens-logo">
        <span class="brand-span">Career</span><span class="lens-span">Lens</span>
    </div>
    """, unsafe_allow_html=True)
    
st.sidebar.markdown("""
<div class="careerlens-tagline">AI Career Copilot • Hong Kong</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

PAGE_OPTIONS = {
    "👤 Job Seeker": "main",
    "💼 Job Search": "job_recommendations",
    "📝 Tailored Resume": "tailored_resume",
    "🤖 AI Mock Interview": "ai_interview",
    "📊 Market Dashboard": "market_dashboard",
    "🧠 How This App Works": "how_it_works",
    "🎯 Recruiter • Job Posting": "head_hunter",
    "🎯 Recruiter • Recruitment Match": "recruitment_match",
}
if st.session_state.get("current_page") not in PAGE_OPTIONS.values():
    st.session_state.current_page = "main"

def _go_to(page_key: str):
    st.session_state.current_page = page_key
    st.rerun()

# --- SIDEBAR NAV (button-based, grouped) ---
st.sidebar.markdown("### 👤 Job Seeker")

_job_seeker_nav = [
    ("🏠 Job Seeker", "main"),
    ("💼 Job Search", "job_recommendations"),
    ("📄 AI Powered Tailored Resume", "tailored_resume"),
    ("🤖 AI Mock Interview", "ai_interview"),
    ("📊 Market Dashboard", "market_dashboard"),
    ("🧠 How This App Works", "how_it_works"),
]

for label, page_key in _job_seeker_nav:
    is_current = st.session_state.get("current_page") == page_key
    if st.sidebar.button(
        label,
        key=f"nav_btn_{page_key}",
        type="primary",
        disabled=is_current,
        width="stretch",
    ):
        _go_to(page_key)

st.sidebar.divider()

st.sidebar.markdown("### 🎯 Recruiter")

_recruiter_nav = [
    ("📋 Job Posting", "head_hunter"),
    ("🤝 Recruitment Match", "recruitment_match"),
]

for label, page_key in _recruiter_nav:
    is_current = st.session_state.get("current_page") == page_key
    if st.sidebar.button(
        label,
        key=f"nav_btn_{page_key}",
        type="secondary",
        disabled=is_current,
        width="stretch",
    ):
        _go_to(page_key)

active_job = st.session_state.get("selected_job")
if active_job:
    with st.sidebar.expander("Active job focus", expanded=False):
        st.caption("Currently focusing on:")
        st.write(f"**{active_job.get('title', 'Unknown Role')}**")
        company = active_job.get("company")
        if company:
            st.caption(company)

        if st.button("Clear selection", key="clear_selected_job", width="stretch"):
            st.session_state.selected_job = None
            st.session_state.selected_job_for_resume = None
            st.session_state.show_resume_generator = False
            st.session_state.generated_resume = None
            if "interview" in st.session_state:
                del st.session_state.interview
            if "interview_started" in st.session_state:
                del st.session_state.interview_started
            if "_interview_job_key" in st.session_state:
                del st.session_state._interview_job_key
            st.rerun()

current_id = st.session_state.get("job_seeker_id")
if current_id:
    with st.sidebar.expander("Session", expanded=False):
        st.caption(f"Session ID: `{current_id}`")
if not MODULES_AVAILABLE:
    st.error("❌ Page modules not available. Please ensure the modules/ui/pages directory is properly installed.")
    st.info("Falling back to basic functionality...")
    st.stop()

if st.session_state.current_page == "main":
    main_analyzer_page()

elif st.session_state.current_page == "job_recommendations":
    job_seeker_id = st.session_state.get('job_seeker_id')

    # Check if there is saved job seeker data
    if not job_seeker_id:
        st.warning("⚠️ Please first save your personal information on the Job Seeker page")
        st.info("👉 Switch to 'Job Seeker' page to fill in and save your information")
        
        # Provide quick jump
        if st.button("Go to Job Seeker Page"):
            st.session_state.current_page = "main"
            st.rerun()
    else:
        # Call job recommendations page function
        job_recommendations_page(job_seeker_id)

elif st.session_state.current_page == "head_hunter":
    enhanced_head_hunter_page()

elif st.session_state.current_page == "recruitment_match":
    recruitment_match_dashboard()

elif st.session_state.current_page == "ai_interview":
    ai_interview_dashboard()

elif st.session_state.current_page == "tailored_resume":
    tailored_resume_page()

elif st.session_state.current_page == "market_dashboard":
    market_dashboard_page()

elif st.session_state.current_page == "how_it_works":
    render_how_it_works_page()


# ============================================================================
# SIDEBAR HELP AND FOOTER
# ============================================================================
with st.sidebar.expander("Help", expanded=False):
    st.markdown(
        """
**Job seeker flow**
- **Job Seeker**: upload CV + save your profile
- **Job Search**: run matched search + pick an active job
- **Tailored Resume / AI Mock Interview**: use the active job for context

**Recruiter flow**
- **Job Posting**: publish/manage roles
- **Recruitment Match**: match candidates to roles
"""
    )
                    
# Footer
st.markdown("---")
st.caption("🤖 Powered by Azure OpenAI, Pinecone Vector Search, RapidAPI LinkedIn Jobs, and CareerLens AI")

# Application startup
if __name__ == "__main__":
    # Ensure application runs normally
    pass
