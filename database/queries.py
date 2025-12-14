"""
Database query functions.
Consolidates all DB access from backend.py
"""
import sqlite3
from typing import List, Dict, Optional, Tuple
from .models import JobSeekerDB, HeadhunterDB

# Initialize singletons
_job_seeker_db = None
_headhunter_db = None


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
