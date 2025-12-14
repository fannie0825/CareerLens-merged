"""
AI Interview functionality.

This module provides:
- Interview question generation
- Answer evaluation
- Final summary generation
- Interview session management
"""

import json
import streamlit as st
from typing import Dict, Optional, Tuple


def initialize_interview_session(job_data: tuple) -> None:
    """Initialize interview session in Streamlit state.
    
    Args:
        job_data: Tuple of job fields from database query
    """
    if 'interview' not in st.session_state:
        st.session_state.interview = {
            'job_id': job_data[0],
            'job_title': job_data[1],
            'company': job_data[5],
            'current_question': 0,
            'total_questions': 2,
            'questions': [],
            'answers': [],
            'scores': [],
            'completed': False,
            'summary': None
        }


def generate_interview_question(job_data: tuple, seeker_profile: tuple, 
                                 previous_qa: Dict = None, config=None) -> str:
    """Generate interview questions using Azure OpenAI.
    
    Args:
        job_data: Tuple of job fields from database
        seeker_profile: Tuple of seeker fields from database
        previous_qa: Optional dict with 'question' and 'answer' keys for follow-up
        config: Optional config object
        
    Returns:
        Generated interview question string, or error message
    """
    try:
        if config is None:
            from config import Config
            config = Config
        
        # Check if API keys are configured
        is_configured, error_msg = config.check_azure_credentials()
        if not is_configured:
            return f"Error: {error_msg}"
        
        from openai import AzureOpenAI
        client = AzureOpenAI(
            azure_endpoint=config.AZURE_ENDPOINT,
            api_key=config.AZURE_API_KEY,
            api_version=config.AZURE_API_VERSION
        )

        # Prepare position information
        job_info = f"""
Position Title: {job_data[1]}
Company: {job_data[5]}
Industry: {job_data[6]}
Experience Requirement: {job_data[7]}
Job Description: {job_data[2]}
Main Responsibilities: {job_data[3]}
Required Skills: {job_data[4]}
        """

        # Prepare job seeker information
        seeker_info = ""
        if seeker_profile:
            seeker_info = f"""
Job Seeker Background:
- Education: {seeker_profile[0]}
- Experience: {seeker_profile[1]}
- Hard Skills: {seeker_profile[2]}
- Soft Skills: {seeker_profile[3]}
- Project Experience: {seeker_profile[4]}
            """

        # Build prompt
        if previous_qa:
            prompt = f"""
As a professional interviewer, please continue the interview based on the following information:

【Position Information】
{job_info}

【Job Seeker Information】
{seeker_info}

【Previous Q&A】
Question: {previous_qa['question']}
Answer: {previous_qa['answer']}

Based on the job seeker's previous answer, please ask a relevant follow-up question. The question should:
1. Deeply explore key points from the previous answer
2. Assess the job seeker's thinking depth and professional abilities
3. Be closely related to position requirements

Please only return the question content, without additional explanations.
            """
        else:
            prompt = f"""
As a professional interviewer, please design an interview question for the following position:

【Position Information】
{job_info}

【Job Seeker Information】
{seeker_info}

Please ask a professional interview question that should:
1. Assess core abilities related to the position
2. Examine the job seeker's experience and skills
3. Have appropriate challenge level
4. Can be behavioral, technical, or situational questions

Please only return the question content, without additional explanations.
            """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional recruitment interviewer, skilled at asking targeted interview questions to assess candidates' abilities and suitability."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"AI question generation failed: {str(e)}"


def evaluate_answer(question: str, answer: str, job_data: tuple, config=None) -> str:
    """Evaluate job seeker's answer.
    
    Args:
        question: The interview question asked
        answer: The job seeker's answer
        job_data: Tuple of job fields from database
        config: Optional config object
        
    Returns:
        JSON string with evaluation results
    """
    try:
        if config is None:
            from config import Config
            config = Config
        
        # Check if API keys are configured
        is_configured, error_msg = config.check_azure_credentials()
        if not is_configured:
            return f'{{"error": "{error_msg}"}}'
        
        from openai import AzureOpenAI
        client = AzureOpenAI(
            azure_endpoint=config.AZURE_ENDPOINT,
            api_key=config.AZURE_API_KEY,
            api_version=config.AZURE_API_VERSION
        )

        prompt = f"""
Please evaluate the following interview answer:

【Position Information】
Position: {job_data[1]}
Company: {job_data[5]}
Requirements: {job_data[4]}

【Interview Question】
{question}

【Job Seeker Answer】
{answer}

Please evaluate and provide scores (0-10 points) from the following dimensions:
1. Relevance and accuracy of the answer
2. Professional knowledge and skills demonstrated
3. Communication expression and logic
4. Match with position requirements

Please return evaluation results in the following JSON format:
{{
    "score": score,
    "feedback": "Specific feedback and suggestions",
    "strengths": ["Strength1", "Strength2"],
    "improvements": ["Improvement suggestion1", "Improvement suggestion2"]
}}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional interview evaluation expert, capable of objectively assessing the quality of interview answers."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=800
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f'{{"error": "Evaluation failed: {str(e)}"}}'


def generate_final_summary(interview_data: Dict, job_data: tuple, config=None) -> str:
    """Generate final interview summary.
    
    Args:
        interview_data: Dictionary with 'questions', 'answers', 'scores' keys
        job_data: Tuple of job fields from database
        config: Optional config object
        
    Returns:
        JSON string with summary results
    """
    try:
        if config is None:
            from config import Config
            config = Config
        
        # Check if API keys are configured
        is_configured, error_msg = config.check_azure_credentials()
        if not is_configured:
            return f'{{"error": "{error_msg}"}}'
        
        from openai import AzureOpenAI
        client = AzureOpenAI(
            azure_endpoint=config.AZURE_ENDPOINT,
            api_key=config.AZURE_API_KEY,
            api_version=config.AZURE_API_VERSION
        )

        # Prepare all Q&A records
        qa_history = ""
        for i, (q, a, score_data) in enumerate(zip(
            interview_data['questions'],
            interview_data['answers'],
            interview_data['scores']
        )):
            qa_history += f"""
Question {i+1}: {q}
Answer: {a}
Score: {score_data.get('score', 'N/A')}
Feedback: {score_data.get('feedback', '')}
            """

        prompt = f"""
Please generate a comprehensive summary report for the following interview:

【Position Information】
Position: {job_data[1]}
Company: {job_data[5]}
Requirements: {job_data[4]}

【Interview Q&A Records】
{qa_history}

Please provide:
1. Overall performance score (0-100 points)
2. Core strengths analysis
3. Areas needing improvement
4. Match assessment for this position
5. Specific improvement suggestions

Please return in the following JSON format:
{{
    "overall_score": overall_score,
    "summary": "Overall evaluation summary",
    "key_strengths": ["Strength1", "Strength2", "Strength3"],
    "improvement_areas": ["Improvement area1", "Improvement area2", "Improvement area3"],
    "job_fit": "High/Medium/Low",
    "recommendations": ["Recommendation1", "Recommendation2", "Recommendation3"]
}}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional career advisor, capable of providing comprehensive interview performance analysis and career development suggestions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f'{{"error": "Summary generation failed: {str(e)}"}}'


def ai_interview_page():
    """AI Interview Page - Streamlit UI.
    
    This function renders the complete AI mock interview interface.
    """
    from database.queries import get_jobs_for_interview, get_job_seeker_profile_tuple
    
    st.title("🤖 AI Mock Interview")

    # Get position information
    jobs = get_jobs_for_interview()
    seeker_profile = get_job_seeker_profile_tuple()

    if not jobs:
        st.warning("❌ No available position information, please first publish positions in the headhunter module")
        return

    if not seeker_profile:
        st.warning("❌ Please first fill in your information on the Job Seeker page")
        return

    st.success("🎯 Select the position you want to interview for to start the mock interview")

    # Select position
    job_options = {f"#{job[0]} {job[1]} - {job[5]}": job for job in jobs}
    selected_job_key = st.selectbox("Select Interview Position", list(job_options.keys()))
    selected_job = job_options[selected_job_key]

    # Display position information
    with st.expander("📋 Position Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Position:** {selected_job[1]}")
            st.write(f"**Company:** {selected_job[5]}")
            st.write(f"**Industry:** {selected_job[6]}")
        with col2:
            st.write(f"**Experience Requirement:** {selected_job[7]}")
            st.write(f"**Skill Requirements:** {selected_job[4][:100]}...")

    # Initialize interview session
    initialize_interview_session(selected_job)
    interview = st.session_state.interview

    # Start/continue interview
    if not interview['completed']:
        if interview['current_question'] == 0:
            if st.button("🚀 Start Mock Interview", type="primary", use_container_width=True):
                # Generate first question
                with st.spinner("AI is preparing interview questions..."):
                    first_question = generate_interview_question(selected_job, seeker_profile)
                    if not first_question.startswith("AI question generation failed"):
                        interview['questions'].append(first_question)
                        interview['current_question'] = 1
                        st.rerun()
                    else:
                        st.error(first_question)

        # Display current question
        if interview['current_question'] > 0 and interview['current_question'] <= interview['total_questions']:
            st.subheader(f"❓ Question {interview['current_question']}/{interview['total_questions']}")
            st.info(interview['questions'][-1])

            # Answer input
            answer = st.text_area("Your Answer:", height=150,
                                placeholder="Please describe your answer in detail...",
                                key=f"answer_{interview['current_question']}")

            if st.button("📤 Submit Answer", type="primary", use_container_width=True):
                if answer.strip():
                    with st.spinner("AI is evaluating your answer..."):
                        # Evaluate current answer
                        evaluation = evaluate_answer(
                            interview['questions'][-1],
                            answer,
                            selected_job
                        )

                        try:
                            eval_data = json.loads(evaluation)
                            if 'error' not in eval_data:
                                # Save answer and evaluation
                                interview['answers'].append(answer)
                                interview['scores'].append(eval_data)

                                # Check if all questions are completed
                                if interview['current_question'] == interview['total_questions']:
                                    # Generate final summary
                                    with st.spinner("AI is generating interview summary..."):
                                        summary = generate_final_summary(interview, selected_job)
                                        try:
                                            summary_data = json.loads(summary)
                                            interview['summary'] = summary_data
                                            interview['completed'] = True
                                        except (json.JSONDecodeError, KeyError, TypeError):
                                            interview['summary'] = {"error": "Summary parsing failed"}
                                            interview['completed'] = True
                                else:
                                    # Generate next question
                                    previous_qa = {
                                        'question': interview['questions'][-1],
                                        'answer': answer
                                    }
                                    next_question = generate_interview_question(
                                        selected_job, seeker_profile, previous_qa
                                    )
                                    if not next_question.startswith("AI question generation failed"):
                                        interview['questions'].append(next_question)
                                        interview['current_question'] += 1
                                    else:
                                        st.error(next_question)

                                st.rerun()
                            else:
                                st.error(eval_data['error'])
                        except json.JSONDecodeError:
                            st.error("Evaluation result parsing failed")
                else:
                    st.warning("Please enter your answer")

            # Display progress
            progress = interview['current_question'] / interview['total_questions']
            st.progress(progress)
            st.write(f"Progress: {interview['current_question']}/{interview['total_questions']} questions")

    # Display interview results
    if interview['completed'] and interview['summary']:
        st.subheader("🎯 Interview Summary Report")

        summary = interview['summary']

        if 'error' in summary:
            st.error(summary['error'])
        else:
            # Overall score
            col1, col2, col3 = st.columns(3)
            with col1:
                score = summary.get('overall_score', 0)
                st.metric("Overall Score", f"{score}/100")
            with col2:
                st.metric("Job Fit", summary.get('job_fit', 'N/A'))
            with col3:
                st.metric("Questions Answered", f"{len(interview['answers'])}/{interview['total_questions']}")

            # Overall evaluation
            st.write("### 📊 Overall Evaluation")
            st.info(summary.get('summary', ''))

            # Core strengths
            st.write("### ✅ Core Strengths")
            strengths = summary.get('key_strengths', [])
            for strength in strengths:
                st.write(f"🎯 {strength}")

            # Improvement areas
            st.write("### 📈 Improvement Suggestions")
            improvements = summary.get('improvement_areas', [])
            for improvement in improvements:
                st.write(f"💡 {improvement}")

            # Detailed recommendations
            st.write("### 🎯 Career Development Recommendations")
            recommendations = summary.get('recommendations', [])
            for rec in recommendations:
                st.write(f"🌟 {rec}")

            # Detailed Q&A records
            with st.expander("📝 View Detailed Q&A Records"):
                for i, (question, answer, score_data) in enumerate(zip(
                    interview['questions'],
                    interview['answers'],
                    interview['scores']
                )):
                    st.write(f"#### Question {i+1}")
                    st.write(f"**Question:** {question}")
                    st.write(f"**Answer:** {answer}")
                    if isinstance(score_data, dict):
                        st.write(f"**Score:** {score_data.get('score', 'N/A')}/10")
                        st.write(f"**Feedback:** {score_data.get('feedback', '')}")
                    st.markdown("---")

            # Restart interview
            if st.button("🔄 Restart Interview", use_container_width=True):
                del st.session_state.interview
                st.rerun()
