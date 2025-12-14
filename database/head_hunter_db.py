# database/head_hunter_db.py
"""
Headhunter Database operations.

This module handles all database operations for head_hunter_jobs.db:
- Storing headhunter job postings
- Retrieving job postings
- Job management for recruitment matching
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Dict, List
from datetime import datetime


# Database path constant
DB_PATH_HEAD_HUNTER = "head_hunter_jobs.db"


class HeadhunterDB:
    """Headhunter job postings database for head_hunter_jobs.db."""
    
    def __init__(self, db_path: str = None):
        self.db_path = Path(db_path or DB_PATH_HEAD_HUNTER)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
    
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
        """Save headhunter job posting to database.
        
        Args:
            job_data: Dictionary containing job posting fields
            
        Returns:
            True if saved successfully
        """
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
        """Get job posting by ID.
        
        Args:
            job_id: The job's database ID
            
        Returns:
            Job dictionary or None if not found
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM head_hunter_jobs WHERE id = ?
            """, (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all job postings as dictionaries."""
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
    
    def get_valid_jobs(self) -> List[Dict]:
        """Get all valid (not expired) job postings."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM head_hunter_jobs 
                WHERE job_valid_until >= date('now')
                ORDER BY id DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_jobs_for_interview(self) -> List[tuple]:
        """Get jobs formatted for interview module.
        
        Returns:
            List of tuples with fields needed for interviews
        """
        with self.get_connection() as conn:
            conn.row_factory = None
            cursor = conn.execute("""
                SELECT id, job_title, job_description, main_responsibilities, required_skills,
                       client_company, industry, experience_level
                FROM head_hunter_jobs
                WHERE job_valid_until >= date('now')
            """)
            return cursor.fetchall()
    
    def update_job(self, job_id: int, updates: Dict) -> bool:
        """Update an existing job posting.
        
        Args:
            job_id: The job's database ID
            updates: Dictionary of fields to update
            
        Returns:
            True if updated, False if not found
        """
        if not updates:
            return False
        
        set_clauses = []
        values = []
        for key, value in updates.items():
            if key != 'id':
                set_clauses.append(f"{key} = ?")
                values.append(value)
        
        if not set_clauses:
            return False
        
        values.append(job_id)
        
        with self.get_connection() as conn:
            cursor = conn.execute(f"""
                UPDATE head_hunter_jobs 
                SET {', '.join(set_clauses)}
                WHERE id = ?
            """, values)
            return cursor.rowcount > 0
    
    def delete_job(self, job_id: int) -> bool:
        """Delete a job posting.
        
        Args:
            job_id: The job's database ID
            
        Returns:
            True if deleted, False if not found
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                DELETE FROM head_hunter_jobs WHERE id = ?
            """, (job_id,))
            return cursor.rowcount > 0
