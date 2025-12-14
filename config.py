# config.py
import os
from pathlib import Path

class Config:
    # Project root
    PROJECT_ROOT = Path(__file__).parent.absolute()
    
    # Database paths
    DB_PATH_JOB_SEEKER = os.getenv(
        'DB_PATH_JOB_SEEKER',
        str(PROJECT_ROOT / 'job_seeker.db')
    )
    DB_PATH_HEAD_HUNTER = os.getenv(
        'DB_PATH_HEAD_HUNTER',
        str(PROJECT_ROOT / 'head_hunter_jobs.db')
    )
    DB_PATH_CHROMA = os.getenv(
        'DB_PATH_CHROMA',
        str(PROJECT_ROOT / '.chroma_db')
    )
    
    # API Keys
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT')
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT')
    
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
