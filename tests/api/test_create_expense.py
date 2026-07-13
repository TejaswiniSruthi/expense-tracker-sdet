import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent.parent / "fixtures" / "expense_payloads.json"
DATA = json.loads(FIXTURES.read_text())

pytestmark = pytest.mark.regression


@pytest.mark.parametrize("case", DATA["valid"], ids=[c["case"] for c in DATA["valid"]])
def test_create_expense_valid(api, base_url, case, cleanup_expenses):
    response = api.post(f"{base_url}/api/expenses", json=case["payload"])

    assert response.status_code == 201
    body = response.json()
    cleanup_expenses.append(body["_id"])

    assert "_id" in body
    for field, expected in case["payload"].items():
        assert body[field] == expected, f"{field} mismatch"


@pytest.mark.parametrize("case", DATA["invalid"], ids=[c["case"] for c in DATA["invalid"]])
def test_create_expense_invalid_returns_400(api, base_url, case):
    response = api.post(f"{base_url}/api/expenses", json=case["payload"])

    assert response.status_code == 400
    assert case["error_contains"] in response.json()["error"]