"""
Database package for CareerLens.
"""
from database.models import (
    DatabaseConnection,
    JobSeekerDB,
    HeadhunterDB,
    DB_PATH_JOB_SEEKER,
    DB_PATH_HEAD_HUNTER,
)

__all__ = [
    'DatabaseConnection',
    'JobSeekerDB',
    'HeadhunterDB',
    'DB_PATH_JOB_SEEKER',
    'DB_PATH_HEAD_HUNTER',
]
