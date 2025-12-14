# tests/test_no_duplicates.py

def test_no_duplicate_linkedin_searcher():
    """Ensure LinkedInJobSearcher only exists in services/linkedin_api.py"""
    
    import backend
    import services.linkedin_api
    
    # backend should NOT have the class definition, only import
    # Check if backend.py has a duplicate definition by inspecting source
    import inspect
    
    backend_source = inspect.getsource(backend)
    
    # Should NOT find "class LinkedInJobSearcher" in backend.py
    assert "class LinkedInJobSearcher" not in backend_source, \
        "LinkedInJobSearcher is duplicated in backend.py!"


def test_no_duplicate_job_matcher():
    """Ensure JobMatcher only exists in core/job_matcher.py"""
    
    import backend
    import inspect
    import re
    
    backend_source = inspect.getsource(backend)
    
    # Check for exact "class JobMatcher:" or "class JobMatcher(" to avoid matching JobMatcherBackend
    # JobMatcherBackend is a DIFFERENT class that should remain in backend.py
    assert not re.search(r"class JobMatcher[\(:]", backend_source), \
        "JobMatcher is duplicated in backend.py!"
    
    assert "def analyze_match_simple" not in backend_source, \
        "analyze_match_simple is duplicated in backend.py!"


def test_backend_is_facade():
    """Verify backend.py is now just a facade (imports + orchestrators)"""
    
    import backend
    import inspect
    
    backend_source = inspect.getsource(backend)
    lines = backend_source.split('\n')
    
    # Count lines (excluding blanks and comments)
    code_lines = [
        line for line in lines 
        if line.strip() and not line.strip().startswith('#')
    ]
    
    # backend.py should be < 500 lines now
    assert len(code_lines) < 500, \
        f"backend.py still has {len(code_lines)} lines of code!"
