"""
Database models and connection management.
"""
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Dict, List
from datetime import datetime
import uuid


# Database path constants
DB_PATH_JOB_SEEKER = "job_seeker.db"
DB_PATH_HEAD_HUNTER = "head_hunter_jobs.db"
DB_PATH_JOB_POST_API = "job_post_API.db"


class DatabaseConnection:
    """Base database connection manager."""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


class JobSeekerDB(DatabaseConnection):
    """Job seeker database operations."""
    
    def __init__(self):
        super().__init__(DB_PATH_JOB_SEEKER)
        self._init_schema()
    
    def _init_schema(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS job_seekers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_seeker_id TEXT UNIQUE NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    education_level TEXT,
                    major TEXT,
                    graduation_status TEXT,
                    university_background TEXT,
                    languages TEXT,
                    certificates TEXT,
                    hard_skills TEXT,
                    soft_skills TEXT,
                    work_experience TEXT,
                    project_experience TEXT,
                    location_preference TEXT,
                    industry_preference TEXT,
                    salary_expectation TEXT,
                    benefits_expectation TEXT,
                    primary_role TEXT,
                    simple_search_terms TEXT
                )
            """)
            # Add indexes
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_job_seeker_id 
                ON job_seekers(job_seeker_id)
            """)
    
    @staticmethod
    def generate_job_seeker_id() -> str:
        """Generate unique job seeker ID."""
        return f"JS_{uuid.uuid4().hex[:8].upper()}"
    
    def save_profile(self, profile: Dict) -> str:
        """Save job seeker profile."""
        job_seeker_id = profile.get('job_seeker_id') or self.generate_job_seeker_id()
        timestamp = profile.get('timestamp') or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO job_seekers (
                    job_seeker_id, timestamp, education_level, major, graduation_status,
                    university_background, languages, certificates, hard_skills, soft_skills,
                    work_experience, project_experience, location_preference, industry_preference,
                    salary_expectation, benefits_expectation, primary_role, simple_search_terms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job_seeker_id,
                timestamp,
                profile.get('education_level', ''),
                profile.get('major', ''),
                profile.get('graduation_status', ''),
                profile.get('university_background', ''),
                profile.get('languages', ''),
                profile.get('certificates', ''),
                profile.get('hard_skills', ''),
                profile.get('soft_skills', ''),
                profile.get('work_experience', ''),
                profile.get('project_experience', ''),
                profile.get('location_preference', ''),
                profile.get('industry_preference', ''),
                profile.get('salary_expectation', ''),
                profile.get('benefits_expectation', ''),
                profile.get('primary_role', ''),
                profile.get('simple_search_terms', '')
            ))
            return job_seeker_id
    
    def get_profile(self, job_seeker_id: str) -> Optional[Dict]:
        """Get job seeker profile by ID."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM job_seekers WHERE job_seeker_id = ?
            """, (job_seeker_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_latest_job_seeker_id(self) -> Optional[str]:
        """Get the latest job_seeker_id."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT job_seeker_id FROM job_seekers ORDER BY id DESC LIMIT 1"
            )
            row = cursor.fetchone()
            return row['job_seeker_id'] if row else None
    
    def get_latest_profile(self) -> Optional[Dict]:
        """Get complete data of the latest job seeker."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM job_seekers ORDER BY id DESC LIMIT 1"
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_profiles(self) -> List[Dict]:
        """Get all job seeker profiles."""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM job_seekers")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_search_fields(self, job_seeker_id: str) -> Optional[Dict]:
        """Get job seeker search fields by ID."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    education_level, major, graduation_status, university_background,
                    languages, certificates, hard_skills, soft_skills,
                    work_experience, project_experience, location_preference,
                    industry_preference, salary_expectation, benefits_expectation,
                    primary_role, simple_search_terms
                FROM job_seekers
                WHERE job_seeker_id = ?
            """, (job_seeker_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return {
                "education_level": row['education_level'] or "",
                "major": row['major'] or "",
                "graduation_status": row['graduation_status'] or "",
                "university_background": row['university_background'] or "",
                "languages": row['languages'] or "",
                "certificates": row['certificates'] or "",
                "hard_skills": row['hard_skills'] or "",
                "soft_skills": row['soft_skills'] or "",
                "work_experience": row['work_experience'] or "",
                "project_experience": row['project_experience'] or "",
                "location_preference": row['location_preference'] or "",
                "industry_preference": row['industry_preference'] or "",
                "salary_expectation": row['salary_expectation'] or "",
                "benefits_expectation": row['benefits_expectation'] or "",
                "primary_role": row['primary_role'] or "",
                "simple_search_terms": row['simple_search_terms'] or "",
            }


class HeadhunterDB(DatabaseConnection):
    """Headhunter job postings database."""
    
    def __init__(self):
        super().__init__(DB_PATH_HEAD_HUNTER)
        self._init_schema()
    
    def _init_schema(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS head_hunter_jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    job_title TEXT,
                    job_description TEXT,
                    main_responsibilities TEXT,
                    required_skills TEXT,
                    client_company TEXT,
                    industry TEXT,
                    work_location TEXT,
                    work_type TEXT,
                    company_size TEXT,
                    employment_type TEXT,
                    experience_level TEXT,
                    visa_support TEXT,
                    min_salary REAL,
                    max_salary REAL,
                    currency TEXT,
                    benefits TEXT,
                    application_method TEXT,
                    job_valid_until TEXT
                )
            """)
            # Add indexes
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_job_title 
                ON head_hunter_jobs(job_title)
            """)
    
    def save_job(self, job_data: Dict) -> bool:
        """Save headhunter job posting to database."""
        timestamp = job_data.get('timestamp') or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO head_hunter_jobs (
                    timestamp, job_title, job_description, main_responsibilities, required_skills,
                    client_company, industry, work_location, work_type, company_size,
                    employment_type, experience_level, visa_support,
                    min_salary, max_salary, currency, benefits, application_method, job_valid_until
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp,
                job_data.get('job_title', ''),
                job_data.get('job_description', ''),
                job_data.get('main_responsibilities', ''),
                job_data.get('required_skills', ''),
                job_data.get('client_company', ''),
                job_data.get('industry', ''),
                job_data.get('work_location', ''),
                job_data.get('work_type', ''),
                job_data.get('company_size', ''),
                job_data.get('employment_type', ''),
                job_data.get('experience_level', ''),
                job_data.get('visa_support', ''),
                job_data.get('min_salary'),
                job_data.get('max_salary'),
                job_data.get('currency', ''),
                job_data.get('benefits', ''),
                job_data.get('application_method', ''),
                job_data.get('job_valid_until', '')
            ))
            return True
    
    def get_job(self, job_id: int) -> Optional[Dict]:
        """Get job posting by ID."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM head_hunter_jobs WHERE id = ?
            """, (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all job postings."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM head_hunter_jobs ORDER BY id DESC"
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def get_all_jobs_as_tuples(self) -> List[tuple]:
        """Get all job postings as tuples (for backward compatibility)."""
        with self.get_connection() as conn:
            # Don't use row_factory for this query
            conn.row_factory = None
            cursor = conn.execute(
                "SELECT * FROM head_hunter_jobs ORDER BY id DESC"
            )
            return cursor.fetchall()


class MatchedJobsDB(DatabaseConnection):
    """Matched jobs database for storing job matches from Indeed/LinkedIn APIs."""
    
    def __init__(self):
        super().__init__(DB_PATH_JOB_POST_API)
        self._init_schema()
    
    def _init_schema(self):
        """Initialize database schema for matched jobs."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS matched_jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_seeker_id TEXT NOT NULL,
                    
                    -- Job Details from API
                    job_id TEXT UNIQUE NOT NULL,
                    job_title TEXT NOT NULL,
                    company_name TEXT,
                    location TEXT,
                    job_description TEXT,
                    required_skills TEXT,
                    preferred_skills TEXT,
                    experience_required TEXT,
                    salary_min REAL,
                    salary_max REAL,
                    employment_type TEXT,
                    industry TEXT,
                    posted_date TEXT,
                    application_url TEXT,
                    
                    -- Matching Metadata
                    cosine_similarity_score REAL,
                    match_percentage INTEGER,
                    skill_match_score REAL,
                    experience_match_score REAL,
                    matched_skills TEXT,
                    missing_skills TEXT,
                    
                    -- Timestamps
                    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (job_seeker_id) REFERENCES job_seeker(job_seeker_id)
                )
            """)
            # Add indexes for efficient querying
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_job_seeker 
                ON matched_jobs(job_seeker_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_similarity 
                ON matched_jobs(cosine_similarity_score DESC)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_match_date 
                ON matched_jobs(matched_at DESC)
            """)
    
    def save_matched_job(self, job_data: Dict) -> int:
        """Save a matched job to the database.
        
        Args:
            job_data: Dictionary containing job and matching data
            
        Returns:
            The ID of the inserted record
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO matched_jobs (
                    job_seeker_id, job_id, job_title, company_name, location,
                    job_description, required_skills, preferred_skills, experience_required,
                    salary_min, salary_max, employment_type, industry, posted_date,
                    application_url, cosine_similarity_score, match_percentage,
                    skill_match_score, experience_match_score, matched_skills, missing_skills
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    job_seeker_id = excluded.job_seeker_id,
                    job_title = excluded.job_title,
                    company_name = excluded.company_name,
                    location = excluded.location,
                    job_description = excluded.job_description,
                    required_skills = excluded.required_skills,
                    preferred_skills = excluded.preferred_skills,
                    experience_required = excluded.experience_required,
                    salary_min = excluded.salary_min,
                    salary_max = excluded.salary_max,
                    employment_type = excluded.employment_type,
                    industry = excluded.industry,
                    posted_date = excluded.posted_date,
                    application_url = excluded.application_url,
                    cosine_similarity_score = excluded.cosine_similarity_score,
                    match_percentage = excluded.match_percentage,
                    skill_match_score = excluded.skill_match_score,
                    experience_match_score = excluded.experience_match_score,
                    matched_skills = excluded.matched_skills,
                    missing_skills = excluded.missing_skills,
                    last_updated = CURRENT_TIMESTAMP
            """, (
                job_data.get('job_seeker_id'),
                job_data.get('job_id'),
                job_data.get('job_title'),
                job_data.get('company_name'),
                job_data.get('location'),
                job_data.get('job_description'),
                job_data.get('required_skills'),
                job_data.get('preferred_skills'),
                job_data.get('experience_required'),
                job_data.get('salary_min'),
                job_data.get('salary_max'),
                job_data.get('employment_type'),
                job_data.get('industry'),
                job_data.get('posted_date'),
                job_data.get('application_url'),
                job_data.get('cosine_similarity_score'),
                job_data.get('match_percentage'),
                job_data.get('skill_match_score'),
                job_data.get('experience_match_score'),
                job_data.get('matched_skills'),
                job_data.get('missing_skills'),
            ))
            return cursor.lastrowid
    
    def save_matched_jobs_batch(self, jobs: List[Dict]) -> int:
        """Save multiple matched jobs in a batch.
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            Number of jobs saved
        """
        count = 0
        for job in jobs:
            try:
                self.save_matched_job(job)
                count += 1
            except Exception as e:
                print(f"Error saving job {job.get('job_id')}: {e}")
        return count
    
    def get_matched_job(self, job_id: str) -> Optional[Dict]:
        """Get a matched job by its external job ID.
        
        Args:
            job_id: External job ID from Indeed/LinkedIn
            
        Returns:
            Job dictionary or None
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM matched_jobs WHERE job_id = ?
            """, (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_matched_jobs_by_seeker(
        self, 
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
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM matched_jobs 
                WHERE job_seeker_id = ? 
                AND (cosine_similarity_score >= ? OR cosine_similarity_score IS NULL)
                ORDER BY cosine_similarity_score DESC
                LIMIT ?
            """, (job_seeker_id, min_score, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_top_matches(
        self, 
        job_seeker_id: str, 
        limit: int = 10
    ) -> List[Dict]:
        """Get top matched jobs for a job seeker by similarity score.
        
        Args:
            job_seeker_id: The job seeker's ID
            limit: Maximum number of results
            
        Returns:
            List of top matched job dictionaries
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM matched_jobs 
                WHERE job_seeker_id = ?
                ORDER BY cosine_similarity_score DESC
                LIMIT ?
            """, (job_seeker_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_recent_matches(
        self, 
        job_seeker_id: str, 
        limit: int = 20
    ) -> List[Dict]:
        """Get recently matched jobs for a job seeker.
        
        Args:
            job_seeker_id: The job seeker's ID
            limit: Maximum number of results
            
        Returns:
            List of recently matched job dictionaries
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM matched_jobs 
                WHERE job_seeker_id = ?
                ORDER BY matched_at DESC
                LIMIT ?
            """, (job_seeker_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_matched_job(self, job_id: str) -> bool:
        """Delete a matched job by its external job ID.
        
        Args:
            job_id: External job ID
            
        Returns:
            True if deleted, False if not found
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                DELETE FROM matched_jobs WHERE job_id = ?
            """, (job_id,))
            return cursor.rowcount > 0
    
    def delete_matches_for_seeker(self, job_seeker_id: str) -> int:
        """Delete all matched jobs for a job seeker.
        
        Args:
            job_seeker_id: The job seeker's ID
            
        Returns:
            Number of records deleted
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                DELETE FROM matched_jobs WHERE job_seeker_id = ?
            """, (job_seeker_id,))
            return cursor.rowcount
    
    def get_match_statistics(self, job_seeker_id: str) -> Dict:
        """Get matching statistics for a job seeker.
        
        Args:
            job_seeker_id: The job seeker's ID
            
        Returns:
            Dictionary with statistics
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_matches,
                    AVG(cosine_similarity_score) as avg_similarity,
                    MAX(cosine_similarity_score) as max_similarity,
                    MIN(cosine_similarity_score) as min_similarity,
                    AVG(match_percentage) as avg_match_percentage,
                    AVG(skill_match_score) as avg_skill_match,
                    AVG(experience_match_score) as avg_experience_match
                FROM matched_jobs 
                WHERE job_seeker_id = ?
            """, (job_seeker_id,))
            row = cursor.fetchone()
            return dict(row) if row else {}
    
    def get_all_matched_jobs(self) -> List[Dict]:
        """Get all matched jobs in the database.
        
        Returns:
            List of all matched job dictionaries
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM matched_jobs 
                ORDER BY matched_at DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
