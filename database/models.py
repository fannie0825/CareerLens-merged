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
