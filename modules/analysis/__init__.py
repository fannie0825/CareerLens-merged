"""Analysis module for job match analysis.

This package provides:
- Salary extraction and filtering
- Domain/industry filtering
- Salary band calculation
"""
from .match_analysis import (
    calculate_salary_band,
    filter_jobs_by_domains,
    filter_jobs_by_salary,
    extract_salary_from_text,
    extract_salary_from_text_regex,
    DOMAIN_KEYWORDS,
)

__all__ = [
    'calculate_salary_band',
    'filter_jobs_by_domains',
    'filter_jobs_by_salary',
    'extract_salary_from_text',
    'extract_salary_from_text_regex',
    'DOMAIN_KEYWORDS',
]
