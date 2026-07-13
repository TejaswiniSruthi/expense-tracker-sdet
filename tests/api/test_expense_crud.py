import pytest

pytestmark = pytest.mark.regression

MISSING_ID = "0" * 24          # valid ObjectId format, doesn't exist
MALFORMED_ID = "not-an-id"


# GET by id

def test_get_by_id_returns_expense(api, base_url, new_expense):
    response = api.get(f"{base_url}/api/expenses/{new_expense['_id']}")
    assert response.status_code == 200
    assert response.json() == new_expense


def test_get_missing_id_returns_404(api, base_url):
    response = api.get(f"{base_url}/api/expenses/{MISSING_ID}")
    assert response.status_code == 404


def test_get_malformed_id_returns_400(api, base_url):
    response = api.get(f"{base_url}/api/expenses/{MALFORMED_ID}")
    assert response.status_code == 400


# PUT

def test_update_amount(api, base_url, new_expense):
    expense_id = new_expense["_id"]
    response = api.put(f"{base_url}/api/expenses/{expense_id}", json={"amount": 750})
    assert response.status_code == 200
    assert response.json()["amount"] == 750

    fetched = api.get(f"{base_url}/api/expenses/{expense_id}").json()
    assert fetched["amount"] == 750           # persisted, not just echoed
    assert fetched["category"] == new_expense["category"]  # untouched field intact


def test_update_with_invalid_amount_returns_400(api, base_url, new_expense):
    response = api.put(
        f"{base_url}/api/expenses/{new_expense['_id']}", json={"amount": -10}
    )
    assert response.status_code == 400


def test_update_missing_id_returns_404(api, base_url):
    response = api.put(f"{base_url}/api/expenses/{MISSING_ID}", json={"amount": 100})
    assert response.status_code == 404


# DELETE

def test_delete_removes_expense(api, base_url, new_expense):
    expense_id = new_expense["_id"]
    response = api.delete(f"{base_url}/api/expenses/{expense_id}")
    assert response.status_code == 204

    assert api.get(f"{base_url}/api/expenses/{expense_id}").status_code == 404


def test_delete_missing_id_returns_404(api, base_url):
    response = api.delete(f"{base_url}/api/expenses/{MISSING_ID}")
    assert response.status_code == 404