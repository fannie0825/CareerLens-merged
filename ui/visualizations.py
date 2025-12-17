"""
Visualization components for job matching analysis.

Contains enhanced visualization functions for displaying job match analytics,
skill distributions, and comparative charts.
"""

import streamlit as st # pyright: ignore[reportMissingImports]
from collections import Counter
import datetime
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



import streamlit as st # pyright: ignore[reportMissingImports]
import plotly.graph_objs as go
from collections import Counter

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


def create_enhanced_visualizations(matched_jobs, job_seeker_data=None):
    if not matched_jobs or len(matched_jobs) == 0:
        st.info("No matched jobs available for visualization.")
        return

    job_titles = []
    sim_scores = []
    skill_scores = []
    exp_scores = []
    match_percentages = []
    avg_salaries = []
    salary_labels = []
    industries = []
    employment_types = []
    posting_dates = []
    skill_match_counts = []
    missing_skill_counts = []

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

        # Industry & employment type
        industries.append(job.get("industry", "N/A"))
        employment_types.append(job.get("employment_type", "N/A"))

        # Post date
        dtxt = job.get("posted_date")
        if dtxt:
            posting_dates.append(str(dtxt))

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
    # 4. Employment Type Frequencies
    st.subheader("Employment Type Frequencies")
    etypes = [e for e in employment_types if e and e != "N/A"]
    if etypes:
        emp_ct = Counter(etypes)
        fig = go.Figure([go.Bar(x=list(emp_ct.keys()), y=list(emp_ct.values()))])
        fig.update_layout(yaxis_title="Number of Jobs")
        fig = apply_chart_theme(fig)
        st.plotly_chart(fig, width="stretch")

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
