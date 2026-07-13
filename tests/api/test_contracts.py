import json
from pathlib import Path

import pytest
from jsonschema import validate

from tests.schemas.expense_schema import ExpenseResponse

SUMMARY_SCHEMA = json.loads(
    (Path(__file__).parent.parent / "schemas" / "summary_schema.json").read_text()
)

pytestmark = pytest.mark.regression


def test_created_expense_matches_contract(new_expense):
    ExpenseResponse.model_validate(new_expense)


def test_listed_expenses_match_contract(api, base_url, new_expense):
    expenses = api.get(f"{base_url}/api/expenses").json()
    assert expenses, "expected at least one expense"
    for expense in expenses:
        ExpenseResponse.model_validate(expense)


def test_summary_matches_json_schema(api, base_url, new_expense):
    body = api.get(f"{base_url}/api/expenses/summary").json()
    validate(instance=body, schema=SUMMARY_SCHEMA)