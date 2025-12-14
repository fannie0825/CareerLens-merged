# tests/test_phase2_complete.py

def test_import_linkedin_api():
    """Verify LinkedIn API imports work"""
    from services.linkedin_api import LinkedInJobSearcher, get_linkedin_job_searcher
    assert LinkedInJobSearcher is not None
    assert get_linkedin_job_searcher is not None


def test_import_job_matcher():
    """Verify job matching imports work"""
    from core.job_matcher import (
        JobMatcher,
        analyze_match_simple,
        calculate_match_scores,
        calculate_job_match_score
    )
    assert JobMatcher is not None
    assert analyze_match_simple is not None


def test_import_resume_parser():
    """Verify resume parser imports work"""
    from core.resume_parser import (
        ResumeParser,
        GPT4JobRoleDetector,
        extract_structured_profile,
        generate_tailored_resume
    )
    assert ResumeParser is not None
    assert GPT4JobRoleDetector is not None


def test_import_interview():
    """Verify interview imports work"""
    from core.interview import (
        initialize_interview_session,
        generate_interview_question,
        evaluate_answer,
        generate_final_summary
    )
    assert initialize_interview_session is not None
    assert generate_interview_question is not None


def test_import_resume_formatters():
    """Verify resume formatters imports work"""
    from services.azure_openai import (
        generate_docx_from_json,
        generate_pdf_from_json,
        format_resume_as_text
    )
    assert generate_docx_from_json is not None
    assert generate_pdf_from_json is not None


def test_backend_imports():
    """Verify backend.py re-exports everything"""
    from backend import (
        LinkedInJobSearcher,
        JobMatcher,
        ResumeParser,
        analyze_match_simple,
        extract_structured_profile,
        generate_tailored_resume,
        JobSeekerBackend,
        JobMatcherBackend
    )
    # All should be importable
    assert LinkedInJobSearcher is not None
    assert JobMatcher is not None
