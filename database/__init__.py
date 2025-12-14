"""
Database package for CareerLens.
"""
from database.models import (
    DatabaseConnection,
    JobSeekerDB,
    HeadhunterDB,
    MatchedJobsDB,
    DB_PATH_JOB_SEEKER,
    DB_PATH_HEAD_HUNTER,
    DB_PATH_JOB_POST_API,
)
from database.queries import (
    get_job_seeker_db,
    get_headhunter_db,
    get_matched_jobs_db,
    get_all_job_seekers,
    get_job_seeker_profile,
    get_all_jobs_for_matching,
    save_job_seeker_info,
    save_head_hunter_job,
    # Matched jobs functions
    save_matched_job,
    save_matched_jobs_batch,
    get_matched_job,
    get_matched_jobs_for_seeker,
    get_top_job_matches,
    get_recent_job_matches,
    delete_matched_job,
    delete_matches_for_seeker,
    get_match_statistics,
    get_all_matched_jobs,
    # Backward compatibility functions
    init_database,
    init_head_hunter_database,
    init_matched_jobs_database,
    get_job_seeker_search_fields,
)

__all__ = [
    # Database classes
    'DatabaseConnection',
    'JobSeekerDB',
    'HeadhunterDB',
    'MatchedJobsDB',
    # Database paths
    'DB_PATH_JOB_SEEKER',
    'DB_PATH_HEAD_HUNTER',
    'DB_PATH_JOB_POST_API',
    # Database getters
    'get_job_seeker_db',
    'get_headhunter_db',
    'get_matched_jobs_db',
    # Job seeker functions
    'get_all_job_seekers',
    'get_job_seeker_profile',
    'save_job_seeker_info',
    # Headhunter functions
    'get_all_jobs_for_matching',
    'save_head_hunter_job',
    # Matched jobs functions
    'save_matched_job',
    'save_matched_jobs_batch',
    'get_matched_job',
    'get_matched_jobs_for_seeker',
    'get_top_job_matches',
    'get_recent_job_matches',
    'delete_matched_job',
    'delete_matches_for_seeker',
    'get_match_statistics',
    'get_all_matched_jobs',
    # Backward compatibility
    'init_database',
    'init_head_hunter_database',
    'init_matched_jobs_database',
    'get_job_seeker_search_fields',
]
