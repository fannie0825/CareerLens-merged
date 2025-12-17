import os

import pytest


def _env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


@pytest.fixture
def api_key():
    """API key for endpoint/integration tests (skips if not configured)."""
    key = _env("API_KEY") or _env("AZURE_OPENAI_API_KEY") or _env("OPENAI_API_KEY")
    if not key:
        pytest.skip("API key not configured (set API_KEY/AZURE_OPENAI_API_KEY/OPENAI_API_KEY).")
    return key


@pytest.fixture
def base_url():
    """Base URL for endpoint tests (skips if not configured)."""
    url = _env("BASE_URL") or _env("AZURE_OPENAI_ENDPOINT")
    if not url:
        pytest.skip("Base URL not configured (set BASE_URL/AZURE_OPENAI_ENDPOINT).")
    return url


@pytest.fixture
def deployment():
    """Model deployment name for Azure/OpenAI tests (skips if not configured)."""
    dep = _env("DEPLOYMENT") or _env("AZURE_OPENAI_DEPLOYMENT") or _env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    if not dep:
        pytest.skip(
            "Deployment not configured (set DEPLOYMENT/AZURE_OPENAI_DEPLOYMENT/AZURE_OPENAI_EMBEDDING_DEPLOYMENT)."
        )
    return dep

