# tests/test_backward_compatibility.py

def test_streamlit_imports_work():
    """Ensure streamlit_app.py imports don't break"""
    
    # Old imports should still work (thanks to backend.py re-exports)
    from backend import (
        analyze_match_simple,
        JobSeekerBackend,
        JobMatcherBackend,
        extract_structured_profile,
        generate_tailored_resume
    )
    
    assert analyze_match_simple is not None
    assert JobSeekerBackend is not None


def test_imports_are_same_object():
    """Verify re-exports point to same objects (not copies)"""
    
    from services.linkedin_api import LinkedInJobSearcher as DirectImport
    from backend import LinkedInJobSearcher as ReExport
    
    # Should be the SAME class object
    assert DirectImport is ReExport
    
    from core.job_matcher import JobMatcher as DirectMatcher
    from backend import JobMatcher as ReExportMatcher
    
    assert DirectMatcher is ReExportMatcher
