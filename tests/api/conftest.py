import os

import pytest
import requests
from pymongo import MongoClient


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


@pytest.fixture
def new_expense(api, base_url, cleanup_expenses):
    """Create a fresh expense; returns the created body (id included)."""
    payload = {
        "amount": 500,
        "category": "Food",
        "description": "crud test expense",
        "paymentMethod": "card",
    }
    response = api.post(f"{base_url}/api/expenses", json=payload)
    assert response.status_code == 201, "fixture failed to create expense"
    body = response.json()
    cleanup_expenses.append(body["_id"])
    return body


@pytest.fixture(scope="session")
def db():
    """Direct handle to the app's MongoDB database."""
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    yield client["expense_tracker"]
    client.close()
