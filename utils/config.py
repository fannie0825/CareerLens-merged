"""Configuration and environment setup"""
import os
import streamlit as st

def _coerce_positive_int(value, default, minimum=1):
    """Ensure configuration values are positive integers."""
    try:
        if value is None:
            raise ValueError
        coerced = int(value)
        return max(minimum, coerced)
    except (ValueError, TypeError):
        return default


def _coerce_positive_float(value, default, minimum=0.0):
    """Ensure configuration values are positive floats."""
    try:
        if value is None:
            raise ValueError
        coerced = float(value)
        return max(minimum, coerced)
    except (ValueError, TypeError):
        return default


def _get_config_int(key, default, minimum=1):
    """Look up configuration values from Streamlit secrets or environment."""
    try:
        secrets_value = st.secrets.get(key)
    except (AttributeError, RuntimeError, KeyError, Exception):
        secrets_value = None
    env_value = os.getenv(key)
    candidate = secrets_value if secrets_value not in (None, "") else env_value
    return _coerce_positive_int(candidate, default, minimum)


def _get_config_float(key, default, minimum=0.0):
    """Look up float configuration values from Streamlit secrets or environment."""
    try:
        secrets_value = st.secrets.get(key)
    except (AttributeError, RuntimeError, KeyError, Exception):
        secrets_value = None
    env_value = os.getenv(key)
    candidate = secrets_value if secrets_value not in (None, "") else env_value
    return _coerce_positive_float(candidate, default, minimum)


# Configuration constants - Optimized for performance
# Batch size increased from 15 to 20 for fewer API calls
DEFAULT_EMBEDDING_BATCH_SIZE = _get_config_int("EMBEDDING_BATCH_SIZE", 20, minimum=5)
# Max jobs reduced from 25 to 15 for faster default searches
DEFAULT_MAX_JOBS_TO_INDEX = _get_config_int("MAX_JOBS_TO_INDEX", 15, minimum=10)
# Batch delay reduced from 0.5s to 0.2s for faster processing
EMBEDDING_BATCH_DELAY = _get_config_float("EMBEDDING_BATCH_DELAY", 0.2, minimum=0.0)
RAPIDAPI_MAX_REQUESTS_PER_MINUTE = _get_config_int("RAPIDAPI_MAX_REQUESTS_PER_MINUTE", 3, minimum=1)
# Pass 2 disabled by default - will be run lazily before resume generation
ENABLE_PROFILE_PASS2 = os.getenv("ENABLE_PROFILE_PASS2", "false").lower() in ("true", "1", "yes")
USE_FAST_SKILL_MATCHING = os.getenv("USE_FAST_SKILL_MATCHING", "true").lower() in ("true", "1", "yes")

# ============================================================================
# Job Search UI constants (shared across pages)
# ============================================================================

# Labels are used directly in Streamlit radio controls.
JOB_SEARCH_MODE_TO_COUNT = {
    "⚡ Quick Search (15 jobs)": 15,
    "🔍 Standard Search (25 jobs)": 25,
    "🔬 Deep Search (40 jobs)": 40,
}

JOB_SEARCH_MODE_OPTIONS = list(JOB_SEARCH_MODE_TO_COUNT.keys())

JOB_SEARCH_MODE_TIME_ESTIMATES = {
    "⚡ Quick Search (15 jobs)": "~30-60 seconds",
    "🔍 Standard Search (25 jobs)": "~60-90 seconds",
    "🔬 Deep Search (40 jobs)": "~90-120 seconds",
}


def get_num_jobs_to_search(search_mode_label: str, default: int = 15) -> int:
    """Map a UI search-mode label to how many jobs to fetch."""
    return int(JOB_SEARCH_MODE_TO_COUNT.get(search_mode_label, default))


def get_search_time_estimate(search_mode_label: str, default: str = "~60 seconds") -> str:
    """Map a UI search-mode label to the time estimate string."""
    return str(JOB_SEARCH_MODE_TIME_ESTIMATES.get(search_mode_label, default))


def _determine_index_limit(total_jobs, desired_top_matches):
    """Cap how many jobs we embed per search to avoid unnecessary API calls."""
    baseline = max(desired_top_matches + 10, 15)
    limit = min(DEFAULT_MAX_JOBS_TO_INDEX, baseline)
    return min(total_jobs, limit)
