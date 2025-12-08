# 🔍 CareerLens - AI Career Intelligence Platform

An AI-powered career intelligence platform built with Streamlit.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

## 🚀 Features

### Core Features (streamlit_app.py)
- **Job Seeker**: Fill information → Automatic job recommendations
- **Job Match**: View AI-matched positions with Pinecone vector search
- **Recruiter**: Post jobs and find candidates
- **Recruitment Match**: Match candidates to job openings
- **AI Interview**: Mock interviews and skill assessment

### New Capabilities (app_new.py - Modular Dashboard)
- **Market Positioning Dashboard**: See your match score, estimated salary, and skill gaps
- **Resume Tailoring**: Generate ATS-optimized resumes tailored to specific jobs
- **Multi-format Export**: Download resumes as DOCX, PDF, or TXT
- **Industry Filtering**: Filter jobs by 15+ industries/domains
- **Salary Filtering**: Filter by minimum salary expectation
- **Indeed Job Source**: Alternative to LinkedIn via IndeedScraperAPI
- **Token Tracking**: Monitor API usage and costs
- **Enhanced Profile Extraction**: Two-pass verification for accuracy

## 📁 Project Structure

```
├── streamlit_app.py      # Main multi-page app (Job Seeker, Match, Recruiter, AI Interview)
├── app_new.py            # New modular dashboard (Market Positioning, Resume Tailoring)
├── backend.py            # Backend services (ResumeParser, GPT4JobRoleDetector, JobMatcher, etc.)
├── config.py             # Configuration settings
├── database.py           # Database operations (JobSeekerDB, HeadhunterDB)
├── modules/              # Modular components for new dashboard
│   ├── analysis/         # Match analysis
│   ├── resume_generator/ # Resume generation & formatting
│   ├── resume_upload/    # File extraction & profile parsing
│   ├── semantic_search/  # Embeddings, cache, job search
│   ├── ui/               # Dashboard UI components
│   └── utils/            # API clients, config, helpers, validation
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python version for deployment
└── *.db                  # SQLite databases (generated)
```

## 🔧 How to Run

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure secrets (create `.streamlit/secrets.toml`):
   ```toml
   AZURE_OPENAI_API_KEY = "your-key"
   AZURE_OPENAI_ENDPOINT = "your-endpoint"
   PINECONE_API_KEY = "your-key"
   RAPIDAPI_KEY = "your-key"
   ```

3. Run the app:
   ```bash
   # Original multi-page app
   streamlit run streamlit_app.py

   # New modular dashboard
   streamlit run app_new.py
   ```

## 📦 Key Dependencies

- `streamlit` - Web framework
- `pinecone-client` - Vector database for semantic search
- `sentence-transformers` - Embedding model
- `openai` - Azure OpenAI API
- `tiktoken` - Token counting
- `matplotlib`, `plotly` - Visualizations
- `reportlab` - PDF generation
- `python-docx` - DOCX generation
- `PyPDF2` - PDF parsing

## 📝 License

MIT License
