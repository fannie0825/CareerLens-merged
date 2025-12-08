#!/usr/bin/env python3
"""
Helper script to extract code sections from app.py into modules
This script helps identify and extract code sections for modularization
"""

import re

def extract_section(file_path, start_pattern, end_pattern=None, include_start=True, include_end=False):
    """Extract a code section between two patterns"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    start_idx = None
    end_idx = None
    
    for i, line in enumerate(lines):
        if start_pattern in line and start_idx is None:
            start_idx = i if include_start else i + 1
        if end_pattern and end_pattern in line and start_idx is not None:
            end_idx = i if include_end else i
            break
    
    if start_idx is None:
        return None
    
    if end_idx is None:
        end_idx = len(lines)
    
    return ''.join(lines[start_idx:end_idx])

# This is a helper script - the actual extraction will be done manually
# to ensure proper imports and dependencies
