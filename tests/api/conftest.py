import os

import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    """API root - override with API_BASE_URL env var (e.g. against staging)."""
    return os.getenv("API_BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="session")
def api(base_url):
    """One shared HTTP session for the whole test run."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()


@pytest.fixture
def cleanup_expenses(api, base_url):
    """Tests append created ids; everything gets deleted after the test."""
    created_ids = []
    yield created_ids
    for expense_id in created_ids:
        api.delete(f"{base_url}/api/expenses/{expense_id}")