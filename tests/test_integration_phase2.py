# tests/test_integration_phase2.py

import pytest
from backend import JobSeekerBackend, JobMatcherBackend

def test_job_seeker_backend_initializes():
    """Test JobSeekerBackend orchestrator initializes correctly"""
    
    backend = JobSeekerBackend()
    
    # Verify it has the expected components
    assert hasattr(backend, 'resume_parser')
    assert hasattr(backend, 'gpt4_detector')
    assert hasattr(backend, 'process_resume')
    assert hasattr(backend, 'search_and_match_jobs')
    
    # Verify lazy-loaded properties exist
    assert hasattr(backend, 'matcher')
    assert hasattr(backend, 'job_searcher')


def test_job_matcher_backend_works():
    """Test JobMatcherBackend orchestrator still works"""
    
    backend = JobMatcherBackend()
    
    # Test matching (uses calculate_job_match_score from core/)
    job_seeker_data = {
        'hard_skills': 'Python, SQL, Data Analysis',
        'work_experience': 'senior',
        'location_preference': 'Hong Kong',
        'primary_role': 'Data Analyst',
        'simple_search_terms': 'data, analyst, python'
    }
    
    job_data = {
        'job_title': 'Senior Data Analyst',
        'job_description': 'Looking for Python expert with SQL knowledge and data analysis skills',
        'job_city': 'Hong Kong'
    }
    
    match = backend.calculate_job_match_score(job_seeker_data, job_data)
    assert match is not None
    assert 'overall_score' in match
    assert 'matched_skills' in match
    assert match['overall_score'] >= 0
    assert match['overall_score'] <= 100


def test_job_matcher_backend_mock_jobs():
    """Test JobMatcherBackend can generate mock jobs"""
    
    backend = JobMatcherBackend()
    
    mock_jobs = backend.get_mock_jobs("Software Engineer", "Hong Kong")
    
    assert mock_jobs is not None
    assert len(mock_jobs) > 0
    assert 'job_title' in mock_jobs[0]
    assert 'job_description' in mock_jobs[0]
