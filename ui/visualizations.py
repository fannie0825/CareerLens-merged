"""
Visualization components for job matching analysis.

Contains enhanced visualization functions for displaying job match analytics,
skill distributions, and comparative charts.
"""

import streamlit as st  # pyright: ignore[reportMissingImports]
from collections import Counter
import datetime
import re
from typing import Dict, List

# Lazy imports for heavy visualization libraries
_pd = None
_plt = None
_go = None
_np = None


def _get_pandas():
    """Lazy load pandas"""
    global _pd
    if _pd is None:
        import pandas as pd
        _pd = pd
    return _pd


def _get_matplotlib():
    """Lazy load matplotlib"""
    global _plt
    if _plt is None:
        import matplotlib.pyplot as plt
        _plt = plt
    return _plt


def _get_plotly():
    """Lazy load plotly"""
    global _go
    if _go is None:
        import plotly.graph_objects as go
        _go = go
    return _go


def _get_numpy():
    """Lazy load numpy"""
    global _np
    if _np is None:
        import numpy as np
        _np = np
    return _np


def apply_chart_theme(fig):
    """Apply consistent dark theme to Plotly figures"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        xaxis=dict(
            gridcolor='#334155',
            linecolor='#334155',
            zerolinecolor='#334155',
            tickfont=dict(color='#E2E8F0')
        ),
        yaxis=dict(
            gridcolor='#334155',
            linecolor='#334155',
            zerolinecolor='#334155',
            tickfont=dict(color='#E2E8F0')
        ),
        legend=dict(
            font=dict(color='#E2E8F0'),
            bgcolor='rgba(0,0,0,0)'
        )
    )
    return fig


def infer_seniority_bucket(job: dict) -> str:
    """
    Infer a coarse seniority bucket from job fields.

    Buckets:
    - Entry / Associate
    - Mid-level
    - Senior
    - Lead / Manager
    - Unknown
    """
    title = (job.get("title") or job.get("job_title") or "")
    exp_level = job.get("experience_level") or ""
    description = job.get("description") or job.get("job_description") or ""

    # Normalize text (avoid None issues)
    t = f"{title} {exp_level}".lower()
    d = str(description).lower()

    # Title-based inference (most reliable + cheapest)
    # Order matters: "senior manager" should map to Lead / Manager, not Senior.
    if re.search(r"\b(lead|manager|head|principal|director|vp|vice president|chief)\b", t):
        return "Lead / Manager"
    if re.search(r"\b(senior|sr\.?|staff)\b", t):
        return "Senior"
    if re.search(r"\b(mid(?:-|\s)?level|intermediate)\b", t):
        return "Mid-level"
    if re.search(r"\b(intern|junior|jr\.?|associate|entry(?:-|\s)?level|graduate|grad)\b", t):
        return "Entry / Associate"

    # Years-required inference from description (fallback)
    # Examples: "3+ years", "5 years of experience", "2 yrs experience", "5-7 years"
    years_matches = re.findall(r"\b(\d{1,2})\s*(?:\+)?\s*(?:years|yrs)\b", d)
    years = None
    if years_matches:
        try:
            years = min(int(x) for x in years_matches)
        except Exception:
            years = None

    if years is not None:
        if years <= 2:
            return "Entry / Associate"
        if 3 <= years <= 5:
            return "Mid-level"
        if 6 <= years <= 8:
            return "Senior"
        if years >= 9:
            return "Lead / Manager"

    return "Unknown"


def create_enhanced_visualizations(matched_jobs, job_seeker_data=None):
    if not matched_jobs or len(matched_jobs) == 0:
        st.info("No matched jobs available for visualization.")
        return
    
    # Lazy-load plotly only when charts are rendered
    go = _get_plotly()

    job_titles = []
    sim_scores = []
    skill_scores = []
    exp_scores = []
    match_percentages = []
    avg_salaries = []
    salary_labels = []
    industries = []
    posting_dates = []
    skill_match_counts = []
    missing_skill_counts = []
    seniority_buckets = []

    for j in matched_jobs:
        job = j.get("job", j)
        
        label = f"{job.get('title', 'N/A')} @ {job.get('company', '')}"
        job_titles.append(label)
        sim_scores.append(j.get("semantic_score", 0))
        skill_scores.append(j.get("skill_match_percentage", 0))
        exp_scores.append(j.get("experience_match_score", 0))
        match_percentages.append(j.get("combined_score", 0))

        # Salary
        sal_min = job.get("salary_min")
        sal_max = job.get("salary_max")
        if sal_min is not None and sal_max is not None:
            try:
                salary = (float(sal_min) + float(sal_max)) / 2
                labelstr = f"{sal_min:.0f}-{sal_max:.0f}"
            except Exception:
                salary = None
                labelstr = "N/A"
        elif sal_min is not None:
            salary = float(sal_min)
            labelstr = f"{sal_min:.0f}"
        elif sal_max is not None:
            salary = float(sal_max)
            labelstr = f"{sal_max:.0f}"
        else:
            salary = None
            labelstr = "N/A"
        avg_salaries.append(salary)
        salary_labels.append(labelstr)

        # Industry
        industries.append(job.get("industry", "N/A"))

        # Post date
        dtxt = job.get("posted_date")
        if dtxt:
            posting_dates.append(str(dtxt))

        # Seniority / experience level (inferred)
        seniority_buckets.append(infer_seniority_bucket(job))

        # Skills
        skill_val = j.get("matched_skills")
        if isinstance(skill_val, list):
            skill_match_counts.append(len(skill_val))
        elif isinstance(skill_val, str):
            skill_match_counts.append(len([x.strip() for x in skill_val.split(",") if x.strip()]))
        else:
            skill_match_counts.append(0)

        miss_val = j.get("missing_skills")
        if isinstance(miss_val, list):
            missing_skill_counts.append(len(miss_val))
        elif isinstance(miss_val, str):
            missing_skill_counts.append(len([x.strip() for x in miss_val.split(",") if x.strip()]))
        else:
            missing_skill_counts.append(0)

    # 1. Match Score Comparison
    st.subheader("Match Scores for Each Job")
    match_fig = go.Figure()
    match_fig.add_trace(go.Bar(x=job_titles, y=sim_scores, name="Cosine Similarity"))
    match_fig.add_trace(go.Bar(x=job_titles, y=skill_scores, name="Skill Match Score"))
    #match_fig.add_trace(go.Bar(x=job_titles, y=exp_scores, name="Experience Match Score"))
    match_fig.add_trace(go.Bar(x=job_titles, y=match_percentages, name="Match Percentage"))
    match_fig.update_layout(barmode='group', xaxis_tickangle=-45, yaxis=dict(title="Score / Percent"))
    match_fig = apply_chart_theme(match_fig)
    st.plotly_chart(match_fig, width="stretch")
    """
    # 2. Salary Distribution
    st.subheader("Average Salary per Job")
    if any(s is not None for s in avg_salaries):
        base_salary = [s if s is not None else 0 for s in avg_salaries]
        salary_fig = go.Figure([go.Bar(x=job_titles, y=base_salary, text=salary_labels, textposition='auto')])
        salary_fig.update_layout(xaxis_tickangle=-45, yaxis_title="Average Salary")
        salary_fig = apply_chart_theme(salary_fig)
        st.plotly_chart(salary_fig, width="stretch")
    """
    # 4. Seniority / Experience Level Distribution
    st.subheader("Seniority / Experience Level Distribution")
    st.caption("Question it answers: **At what level is the market currently valuing you?**")
    buckets = [b for b in seniority_buckets if b and b != "Unknown"]
    if buckets:
        bucket_ct = Counter(buckets)
        ordered = ["Entry / Associate", "Mid-level", "Senior", "Lead / Manager"]
        labels = [b for b in ordered if b in bucket_ct]
        values = [bucket_ct[b] for b in labels]

        dominant_bucket = bucket_ct.most_common(1)[0][0] if bucket_ct else None
        if dominant_bucket:
            st.write(f"Market signal: your matched roles skew **{dominant_bucket}**.")

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.45,
                    sort=False,
                    textinfo="label+percent",
                )
            ]
        )
        fig.update_layout(showlegend=True)
        fig = apply_chart_theme(fig)
        st.plotly_chart(fig, width="stretch")
    else:
        st.caption("Not enough job data to infer seniority buckets (missing titles/experience signals).")

    # 5. Posting Date Histogram
    if posting_dates:
        st.subheader("Job Posting Trend")
        date_ct = Counter(posting_dates)
        xs = sorted(date_ct.keys())
        ys = [date_ct[x] for x in xs]
        fig = go.Figure([go.Bar(x=xs, y=ys)])
        fig.update_layout(xaxis_title="Posting Date", yaxis_title="Jobs Posted")
        fig = apply_chart_theme(fig)
        st.plotly_chart(fig, width="stretch")

    # 6. Skill Match/Gap Comparison
    st.subheader("Matched and Missing Skill Counts per Job")
    skills_fig = go.Figure()
    skills_fig.add_trace(go.Bar(x=job_titles, y=skill_match_counts, name='Matched Skills Count'))
    skills_fig.add_trace(go.Bar(x=job_titles, y=missing_skill_counts, name='Missing Skills Count'))
    skills_fig.update_layout(barmode='group', xaxis_tickangle=-45, yaxis_title='Skill Count')
    skills_fig = apply_chart_theme(skills_fig)
    st.plotly_chart(skills_fig, width="stretch")

# Estimate salary expectation from job seeker data
def find_salary_expectation(job, job_seeker_data: dict) -> float:
    import re
    """Estimate job seeker's salary expectation based on profile data"""
    text = job_seeker_data.get("salary_expectation")
    if not text or not isinstance(text, str):
        return 0
    
    # Convert 'k' notation to thousands
    text = re.sub(r'(\d+(?:\.\d+)?)\s*k', 
                  lambda m: str(int(float(m.group(1)) * 1000)), 
                  text, flags=re.IGNORECASE)
    
    # Find all numbers (with or without commas)
    numbers = re.findall(r'\d[\d,]*\.?\d*', text)
    
    # Convert to integers (remove commas, handle decimals)
    result = []
    for num in numbers:
        try:
            # Remove commas and convert to integer
            clean_num = num.replace(',', '')
            if '.' in clean_num:
                # Handle decimals by rounding
                value = int(float(clean_num))
            else:
                value = int(clean_num)
            result.append(value)
        except ValueError:
            continue
    
    seeker_expectation = (sum(result) / len(result)) if result else 0

    hunter_min = job.get("salary_min", 0)
    hunter_max = job.get("salary_max", 0)
    hunter_avg = (hunter_min + hunter_max) / 2 if hunter_min and hunter_max else max(hunter_min, hunter_max)

    return min(100, 100 * hunter_avg / seeker_expectation if seeker_expectation else 0)

def match_location(job, job_seeker_data: dict) -> float:
    """Simple location match scoring"""
    job_location = job.get("location", "").lower()
    user_location_pref = job_seeker_data.get("location_preference", "hong kong").lower() #default is hk
    if not job_location or not user_location_pref:
        return 50.0  # Neutral score if missing data
    
    job_loc_lower = job_location.lower()
    user_loc_lower = user_location_pref.lower()
    
    # Exact match or contains
    if user_loc_lower in job_loc_lower or job_loc_lower in user_loc_lower:
        return 100.0
    
    # Remote work compatibility
    if 'remote' in job_loc_lower or 'remote' in user_loc_lower:
        return 80.0
    
    # Same city/region detection (simplified)
    common_locations = {
        'hong kong': ['hk', 'hongkong', 'hong-kong'],
        'new york': ['ny', 'nyc', 'newyork'],
        'london': ['ldn'],
        'singapore': ['sg', 'sing'],
        'tokyo': ['tyo']
    }
    
    for main_loc, aliases in common_locations.items():
        if (user_loc_lower == main_loc and any(alias in job_loc_lower for alias in aliases)) or \
           (job_loc_lower == main_loc and any(alias in user_loc_lower for alias in aliases)):
            return 100.0
    
    return 30.0  # Low score for no match

def create_job_comparison_radar(matched_job: dict, job: dict, job_seeker_data: dict, chart_key: str):
    """Create radar chart for top 3 job comparisons"""
    
    # Lazy load plotly only when radar chart is created
    go = _get_plotly()
        
    try:
        st.markdown("### 📊 Job Comparison Radar")
        
        # Define comparison categories
        categories = ['Skill Match', 'Role Relevance', 'Total Fit', 'Location Match', 'Salary Alignment']
        
        # Calculate scores for each category (simplified for demo)
        job_scores = []
        scores = [
                matched_job.get('skill_match_percentage', 0),
                matched_job.get('semantic_score', 0),
                matched_job.get('combined_score', 0), 
                match_location(job, job_seeker_data),  # Simulated location match
                find_salary_expectation(job, job_seeker_data)
        ]
        job_scores.append(scores)
        
        fig = go.Figure()

        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        for i, scores in enumerate(job_scores):
            job_title = matched_job.get('title', f'Job {i+1}')[:25]
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]],  # Close the radar
                theta=categories + [categories[0]],
                fill='toself',
                name=f"{job_title}",
                line=dict(color=colors[i], width=2),
                opacity=0.7
            ))

        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10, color='#94A3B8'),
                    gridcolor='#334155',
                    linecolor='#334155'
                ),
                angularaxis=dict(
                    tickfont=dict(size=11, color='#E2E8F0'),
                    gridcolor='#334155',
                    linecolor='#334155'
                )
            ),
            showlegend=True,
            title=dict(
                text="Multi-dimensional Job Comparison",
                x=0.5,
                font=dict(size=16, color='#E2E8F0')
            ),
            height=500,
            margin=dict(l=80, r=80, t=80, b=80),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E2E8F0'),
            legend=dict(
                font=dict(color='#E2E8F0'),
                bgcolor='rgba(0,0,0,0)'
            )
        )
        
        st.plotly_chart(fig, width="stretch", key=f"radar_chart_{chart_key}")
        
    except Exception as e:
        st.error(f"Error creating radar chart: {str(e)}")
