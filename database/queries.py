"""
Database query functions.
Consolidates all DB access from backend.py
"""
import sqlite3
from typing import List, Dict, Optional, Tuple
from .models import JobSeekerDB, HeadhunterDB, MatchedJobsDB

# Initialize singletons
_job_seeker_db = None
_headhunter_db = None
_matched_jobs_db = None


def get_job_seeker_db() -> JobSeekerDB:
    """Get job seeker database instance (singleton)."""
    global _job_seeker_db
    if _job_seeker_db is None:
        _job_seeker_db = JobSeekerDB()
    return _job_seeker_db


def get_headhunter_db() -> HeadhunterDB:
    """Get headhunter database instance (singleton)."""
    global _headhunter_db
    if _headhunter_db is None:
        _headhunter_db = HeadhunterDB()
    return _headhunter_db


def get_matched_jobs_db() -> MatchedJobsDB:
    """Get matched jobs database instance (singleton)."""
    global _matched_jobs_db
    if _matched_jobs_db is None:
        _matched_jobs_db = MatchedJobsDB()
    return _matched_jobs_db


# ============================================================================
# QUERY FUNCTIONS (from backend.py)
# ============================================================================

def get_all_job_seekers() -> List[Dict]:
    """Get all job seekers as dictionaries."""
    return get_job_seeker_db().get_all_profiles()


def get_all_job_seekers_formatted() -> List[Tuple]:
    """Get all job seekers formatted for matching UI.
    
    Returns:
        List of tuples with formatted seeker data for matching
    """
    try:
        conn = sqlite3.connect('job_seeker.db')
        c = conn.cursor()
        c.execute("""
            SELECT
                id,
                education_level as education,
                work_experience as experience,
                hard_skills as skills,
                industry_preference as target_industry,
                location_preference as target_location,
                salary_expectation as expected_salary,
                university_background as current_title,
                major,
                languages,
                certificates,
                soft_skills,
                project_experience,
                benefits_expectation
            FROM job_seekers
        """)
        seekers = c.fetchall()
        conn.close()

        # Change the structure to match the expected output
        formatted_seekers = []
        for seeker in seekers:
            # Create a virtual name field (using education background + major)
            virtual_name = f"Seeker#{seeker[0]} - {seeker[1]}"

            formatted_seekers.append((
                seeker[0],  # id
                virtual_name,  # name (constructed)
                seeker[3] or "",  # skills (hard_skills)
                seeker[2] or "",  # experience (work_experience)
                seeker[1] or "",  # education (education_level)
                seeker[8] or "",  # target_position (major)
                seeker[4] or "",  # target_industry (industry_preference)
                seeker[5] or "",  # target_location (location_preference)
                seeker[6] or "",  # expected_salary (salary_expectation)
                seeker[7] or ""   # current_title (university_background)
            ))

        return formatted_seekers
    except Exception as e:
        print(f"Failed to get job seekers: {e}")
        return []


def get_job_seeker_profile(job_seeker_id: str) -> Optional[Dict]:
    """Get specific job seeker profile."""
    return get_job_seeker_db().get_profile(job_seeker_id)


def get_job_seeker_profile_tuple() -> Optional[Tuple]:
    """Get current job seeker information as tuple.
    
    Returns:
        Tuple of (education_level, work_experience, hard_skills, soft_skills, project_experience)
    """
    try:
        conn = sqlite3.connect('job_seeker.db')
        c = conn.cursor()
        c.execute("""
            SELECT education_level, work_experience, hard_skills, soft_skills,
                   project_experience
            FROM job_seekers
            ORDER BY id DESC
            LIMIT 1
        """)
        profile = c.fetchone()
        conn.close()
        return profile
    except Exception as e:
        print(f"Failed to get job seeker information: {e}")
        return None


def get_all_jobs_for_matching() -> List[Dict]:
    """Get all jobs for matching as dictionaries."""
    return get_headhunter_db().get_all_jobs()


def get_all_jobs_for_matching_tuples() -> List[Tuple]:
    """Get all head hunter jobs for matching as tuples.
    
    Returns:
        List of job tuples from database
    """
    try:
        conn = sqlite3.connect('head_hunter_jobs.db')
        c = conn.cursor()
        c.execute("""
            SELECT id, job_title, job_description, main_responsibilities, required_skills,
                   client_company, industry, work_location, work_type, company_size,
                   employment_type, experience_level, visa_support,
                   min_salary, max_salary, currency, benefits
            FROM head_hunter_jobs
            WHERE job_valid_until >= date('now')
        """)
        jobs = c.fetchall()
        conn.close()
        return jobs
    except Exception as e:
        print(f"Failed to get job positions: {e}")
        return []


def get_jobs_for_interview() -> List[Tuple]:
    """Get available positions for interviews.
    
    Returns:
        List of job tuples with fields needed for interviews
    """
    try:
        conn = sqlite3.connect('head_hunter_jobs.db')
        c = conn.cursor()
        c.execute("""
            SELECT id, job_title, job_description, main_responsibilities, required_skills,
                   client_company, industry, experience_level
            FROM head_hunter_jobs
            WHERE job_valid_until >= date('now')
        """)
        jobs = c.fetchall()
        conn.close()
        return jobs
    except Exception as e:
        print(f"Failed to get positions: {e}")
        return []


def save_job_seeker_info(profile: Dict) -> str:
    """Save job seeker information."""
    return get_job_seeker_db().save_profile(profile)


def save_head_hunter_job(job: Dict) -> bool:
    """Save headhunter job posting."""
    return get_headhunter_db().save_job(job)


# ============================================================================
# BACKWARD COMPATIBILITY FUNCTIONS
# ============================================================================

def init_database() -> None:
    """Initialize job seeker database.
    
    Note: Schema is auto-initialized when JobSeekerDB is instantiated.
    This function exists for backward compatibility.
    """
    get_job_seeker_db()  # Triggers schema initialization


def init_head_hunter_database() -> None:
    """Initialize headhunter database.
    
    Note: Schema is auto-initialized when HeadhunterDB is instantiated.
    This function exists for backward compatibility.
    """
    get_headhunter_db()  # Triggers schema initialization


def get_job_seeker_search_fields(job_seeker_id: str) -> Optional[Dict]:
    """Get job seeker search fields by ID.
    
    Backward compatibility wrapper for JobSeekerDB.get_search_fields().
    """
    return get_job_seeker_db().get_search_fields(job_seeker_id)


# ============================================================================
# MATCHED JOBS QUERY FUNCTIONS (job_post_API.db)
# ============================================================================

def save_matched_job(job_data: Dict) -> int:
    """Save a matched job to the database.
    
    Args:
        job_data: Dictionary containing job and matching metadata
        
    Returns:
        The ID of the inserted record
    """
    return get_matched_jobs_db().save_matched_job(job_data)


def save_matched_jobs_batch(jobs: List[Dict]) -> int:
    """Save multiple matched jobs in a batch.
    
    Args:
        jobs: List of job dictionaries
        
    Returns:
        Number of jobs saved
    """
    return get_matched_jobs_db().save_matched_jobs_batch(jobs)


def get_matched_job(job_id: str) -> Optional[Dict]:
    """Get a matched job by its external job ID.
    
    Args:
        job_id: External job ID from Indeed/LinkedIn
        
    Returns:
        Job dictionary or None
    """
    return get_matched_jobs_db().get_matched_job(job_id)


def get_matched_jobs_for_seeker(
    job_seeker_id: str, 
    min_score: float = 0.0,
    limit: int = 100
) -> List[Dict]:
    """Get all matched jobs for a job seeker.
    
    Args:
        job_seeker_id: The job seeker's ID
        min_score: Minimum cosine similarity score filter
        limit: Maximum number of results
        
    Returns:
        List of matched job dictionaries, ordered by similarity score
    """
    return get_matched_jobs_db().get_matched_jobs_by_seeker(job_seeker_id, min_score, limit)


def get_top_job_matches(job_seeker_id: str, limit: int = 10) -> List[Dict]:
    """Get top matched jobs for a job seeker by similarity score.
    
    Args:
        job_seeker_id: The job seeker's ID
        limit: Maximum number of results
        
    Returns:
        List of top matched job dictionaries
    """
    return get_matched_jobs_db().get_top_matches(job_seeker_id, limit)


def get_recent_job_matches(job_seeker_id: str, limit: int = 20) -> List[Dict]:
    """Get recently matched jobs for a job seeker.
    
    Args:
        job_seeker_id: The job seeker's ID
        limit: Maximum number of results
        
    Returns:
        List of recently matched job dictionaries
    """
    return get_matched_jobs_db().get_recent_matches(job_seeker_id, limit)


def delete_matched_job(job_id: str) -> bool:
    """Delete a matched job by its external job ID.
    
    Args:
        job_id: External job ID
        
    Returns:
        True if deleted, False if not found
    """
    return get_matched_jobs_db().delete_matched_job(job_id)


def delete_matches_for_seeker(job_seeker_id: str) -> int:
    """Delete all matched jobs for a job seeker.
    
    Args:
        job_seeker_id: The job seeker's ID
        
    Returns:
        Number of records deleted
    """
    return get_matched_jobs_db().delete_matches_for_seeker(job_seeker_id)


def get_match_statistics(job_seeker_id: str) -> Dict:
    """Get matching statistics for a job seeker.
    
    Args:
        job_seeker_id: The job seeker's ID
        
    Returns:
        Dictionary with statistics (total_matches, avg_similarity, etc.)
    """
    return get_matched_jobs_db().get_match_statistics(job_seeker_id)


def get_all_matched_jobs() -> List[Dict]:
    """Get all matched jobs in the database.
    
    Returns:
        List of all matched job dictionaries
    """
    return get_matched_jobs_db().get_all_matched_jobs()


def init_matched_jobs_database() -> None:
    """Initialize matched jobs database.
    
    Note: Schema is auto-initialized when MatchedJobsDB is instantiated.
    This function exists for explicit initialization if needed.
    """
    get_matched_jobs_db()  # Triggers schema initialization


# ============================================================================
# NEW FUNCTIONS: Step 0 Cache Check & Unified Access
# ============================================================================

def has_recent_matches(job_seeker_id: str, max_age_hours: int = 24) -> bool:
    """Check if job seeker has recent matches (Step 0 optimization).
    
    Args:
        job_seeker_id: The job seeker's ID
        max_age_hours: Maximum age of matches in hours
        
    Returns:
        True if recent matches exist
    """
    return get_matched_jobs_db().has_recent_matches(job_seeker_id, max_age_hours)


def get_recent_match_info(job_seeker_id: str, max_age_hours: int = 24) -> Optional[Dict]:
    """Get info about recent matches for cache decision.
    
    Args:
        job_seeker_id: The job seeker's ID
        max_age_hours: Maximum age of matches in hours
        
    Returns:
        Dict with count and match times, or None
    """
    return get_matched_jobs_db().get_recent_match_info(job_seeker_id, max_age_hours)


def get_matched_jobs(
    job_seeker_id: str,
    min_match: int = 60,
    purpose: str = 'general',
    limit: int = 50
) -> List[Dict]:
    """Unified function to get matched jobs with purpose-specific fields.
    
    Args:
        job_seeker_id: The job seeker's ID
        min_match: Minimum match percentage
        purpose: 'general', 'resume', or 'interview'
        limit: Maximum number of results
        
    Returns:
        List of matched job dictionaries
    """
    return get_matched_jobs_db().get_matched_jobs(job_seeker_id, min_match, purpose, limit)


def cleanup_old_matches(job_seeker_id: str, days: int = 30) -> int:
    """Delete matches older than X days to keep DB lean.
    
    Args:
        job_seeker_id: The job seeker's ID
        days: Delete matches older than this many days
        
    Returns:
        Number of records deleted
    """
    return get_matched_jobs_db().cleanup_old_matches(job_seeker_id, days)


def cleanup_all_old_matches(days: int = 30) -> int:
    """Delete all matches older than X days (global cleanup).
    
    Args:
        days: Delete matches older than this many days
        
    Returns:
        Number of records deleted
    """
    return get_matched_jobs_db().cleanup_all_old_matches(days)
