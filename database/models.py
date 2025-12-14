# database/models.py
"""
Database models and shared table definitions.

This module provides:
- Re-exports from individual database modules for backward compatibility
- Shared DatabaseConnection base class
- Database path constants

Database Structure:
    database/
    ├── job_seeker_db.py      # JobSeekerDB - job_seeker.db
    ├── head_hunter_db.py     # HeadhunterDB - head_hunter_jobs.db
    ├── job_post_api_db.py    # MatchedJobsDB - job_post_API.db
    └── models.py             # This file - shared definitions
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Dict, List
from datetime import datetime
import uuid

# Import from individual database modules
from database.job_seeker_db import (
    JobSeekerDB,
    DB_PATH_JOB_SEEKER
)
from database.head_hunter_db import (
    HeadhunterDB,
    DB_PATH_HEAD_HUNTER
)
from database.job_post_api_db import (
    MatchedJobsDB,
    DB_PATH_JOB_POST_API
)


class DatabaseConnection:
    """Base database connection manager.
    
    This class provides a common interface for all database connections
    with context management support.
    """
    
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


# Re-export for backward compatibility
__all__ = [
    # Base class
    'DatabaseConnection',
    # Database classes
    'JobSeekerDB',
    'HeadhunterDB',
    'MatchedJobsDB',
    # Database paths
    'DB_PATH_JOB_SEEKER',
    'DB_PATH_HEAD_HUNTER',
    'DB_PATH_JOB_POST_API',
]
