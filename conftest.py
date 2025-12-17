import os
from typing import Optional

import pytest


def _getenv_any(*names: str) -> Optional[str]:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


@pytest.fixture
def api_key() -> str:
    """API key for live endpoint diagnostics.

    These tests are intended to be run only when credentials are configured.
    """
    value = _getenv_any(
        "HKUST_API_KEY",
        "AZURE_OPENAI_API_KEY",
        "OPENAI_API_KEY",
    )
    if not value:
        pytest.skip("No API key configured (set HKUST_API_KEY or AZURE_OPENAI_API_KEY to run live endpoint tests)")
    return value


@pytest.fixture
def base_url() -> str:
    """Base URL for live endpoint diagnostics."""
    value = _getenv_any(
        "AZURE_OPENAI_ENDPOINT",
        "HKUST_AZURE_OPENAI_ENDPOINT",
        "BASE_URL",
    )
    if not value:
        pytest.skip("No base URL configured (set AZURE_OPENAI_ENDPOINT to run live endpoint tests)")
    return value


@pytest.fixture
def deployment() -> str:
    """Deployment name for live endpoint diagnostics."""
    value = _getenv_any(
        "AZURE_OPENAI_DEPLOYMENT",
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
    )
    if not value:
        pytest.skip("No deployment configured (set AZURE_OPENAI_DEPLOYMENT to run live endpoint tests)")
    return value
