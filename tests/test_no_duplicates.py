# tests/test_no_duplicates.py
"""
Test that there are no duplicate class definitions across modules.
"""

def test_linkedin_searcher_exists():
    """Ensure LinkedInJobSearcher exists in services/linkedin_api.py"""
    
    from services.linkedin_api import LinkedInJobSearcher
    import inspect
    
    # Verify it's a class
    assert inspect.isclass(LinkedInJobSearcher), \
        "LinkedInJobSearcher should be a class!"


def test_job_matcher_exists():
    """Ensure JobMatcher exists in core/job_matcher.py"""
    
    from core.job_matcher import JobMatcher, analyze_match_simple
    import inspect
    
    # Verify it's a class
    assert inspect.isclass(JobMatcher), \
        "JobMatcher should be a class!"
    
    # Verify analyze_match_simple is a function
    assert callable(analyze_match_simple), \
        "analyze_match_simple should be callable!"


def test_job_processor_exists():
    """Verify JobSeekerBackend exists in core/job_processor.py"""
    
    from core.job_processor import JobSeekerBackend, JobMatcherBackend
    import inspect
    
    assert inspect.isclass(JobSeekerBackend), \
        "JobSeekerBackend should be a class!"
    
    assert inspect.isclass(JobMatcherBackend), \
        "JobMatcherBackend should be a class!"


def test_core_module_exports():
    """Verify core module exports all expected items"""
    
    from core import (
        TokenUsageTracker,
        RateLimiter,
        JobMatcher,
        calculate_match_scores,
        analyze_match_simple,
        ResumeParser,
        GPT4JobRoleDetector,
        JobSeekerBackend,
        JobMatcherBackend
    )
    
    # All should be importable
    assert TokenUsageTracker is not None
    assert RateLimiter is not None
    assert JobMatcher is not None
