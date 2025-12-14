"""
Core modules for CareerLens application.

This package contains centralized, reusable components that are shared
across the application.
"""

from .job_processor import JobSeekerBackend, JobMatcherBackend
from .job_matcher import (
    JobMatcher,
    calculate_match_scores,
    analyze_match_simple,
    calculate_job_match_score
)
from .resume_parser import (
    ResumeParser,
    GPT4JobRoleDetector,
    extract_relevant_resume_sections,
    extract_structured_profile,
    generate_tailored_resume,
    # Streamlit-integrated functions (from modules/resume_upload)
    extract_text_from_resume,
    extract_profile_from_resume,
    verify_profile_data_pass2
)
from .rate_limiting import TokenUsageTracker, RateLimiter
from .interview import (
    initialize_interview_session,
    generate_interview_question,
    evaluate_answer,
    generate_final_summary
    # NOTE: ai_interview_page is UI, not business logic
    # UI is in modules/ui/pages/ai_interview_page.py
)
from .salary_analyzer import (
    SalaryAnalyzer,
    extract_salary_from_text,
    extract_salary_from_text_regex,
    filter_jobs_by_salary,
    calculate_salary_band
)
from .domain_filter import (
    DomainFilter,
    filter_jobs_by_domains,
    DOMAIN_KEYWORDS
)
from .resume_generator import (
    ResumeGenerator,
    generate_docx_from_json,
    generate_pdf_from_json,
    format_resume_as_text
)
from .semantic_search import (
    SemanticJobSearch,
    fetch_jobs_with_cache,
    is_cache_valid,
    generate_and_store_resume_embedding
)
from .job_seeker_flow import (
    # Step 1: Resume Upload & Profile Creation
    process_resume_and_create_profile,
    save_job_seeker_profile,
    get_job_seeker_profile,
    # Step 2: Job Matching & API Storage
    search_and_match_jobs,
    get_matched_jobs_for_seeker,
    get_top_matched_jobs,
    # Step 3: AI Resume & Interview
    get_job_for_resume_tailoring,
    generate_tailored_resume_for_job,
    get_job_for_interview,
    get_jobs_for_interview_from_matches,
    convert_matched_job_to_interview_tuple,
    convert_profile_to_interview_tuple,
    # Utilities
    get_current_job_seeker_id,
    set_current_job_seeker_id,
    clear_matched_jobs_for_seeker,
    get_match_statistics,
    MATCH_SCORE_THRESHOLD
)

__all__ = [
    # Job Processing
    'JobSeekerBackend',
    'JobMatcherBackend',
    
    # Job Matching
    'JobMatcher',
    'calculate_match_scores',
    'analyze_match_simple',
    'calculate_job_match_score',
    
    # Resume Processing
    'ResumeParser',
    'GPT4JobRoleDetector',
    'extract_relevant_resume_sections',
    'extract_structured_profile',
    'generate_tailored_resume',
    'extract_text_from_resume',
    'extract_profile_from_resume',
    'verify_profile_data_pass2',
    
    # Rate Limiting
    'TokenUsageTracker',
    'RateLimiter',
    
    # Interview Logic (business logic only)
    'initialize_interview_session',
    'generate_interview_question',
    'evaluate_answer',
    'generate_final_summary',
    
    # Salary Analysis
    'SalaryAnalyzer',
    'extract_salary_from_text',
    'extract_salary_from_text_regex',
    'filter_jobs_by_salary',
    'calculate_salary_band',
    
    # Domain Filtering
    'DomainFilter',
    'filter_jobs_by_domains',
    'DOMAIN_KEYWORDS',
    
    # Resume Generation
    'ResumeGenerator',
    'generate_docx_from_json',
    'generate_pdf_from_json',
    'format_resume_as_text',
    
    # Semantic Search
    'SemanticJobSearch',
    'fetch_jobs_with_cache',
    'is_cache_valid',
    'generate_and_store_resume_embedding',
    
    # Job Seeker Data Flow (3-step orchestration)
    'process_resume_and_create_profile',
    'save_job_seeker_profile',
    'get_job_seeker_profile',
    'search_and_match_jobs',
    'get_matched_jobs_for_seeker',
    'get_top_matched_jobs',
    'get_job_for_resume_tailoring',
    'generate_tailored_resume_for_job',
    'get_job_for_interview',
    'get_jobs_for_interview_from_matches',
    'convert_matched_job_to_interview_tuple',
    'convert_profile_to_interview_tuple',
    'get_current_job_seeker_id',
    'set_current_job_seeker_id',
    'clear_matched_jobs_for_seeker',
    'get_match_statistics',
    'MATCH_SCORE_THRESHOLD',
]
