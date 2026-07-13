import pytest

pytestmark = pytest.mark.regression


@pytest.fixture
def health_expenses(api, base_url, cleanup_expenses):
    """Two known expenses in the Health category."""
    created = []
    for amount in (111.11, 222.22):
        response = api.post(
            f"{base_url}/api/expenses",
            json={"amount": amount, "category": "Health", "description": "filter test"},
        )
        assert response.status_code == 201
        body = response.json()
        cleanup_expenses.append(body["_id"])
        created.append(body)
    return created


def test_filter_by_category(api, base_url, health_expenses):
    response = api.get(f"{base_url}/api/expenses", params={"category": "Health"})
    assert response.status_code == 200
    expenses = response.json()
    assert len(expenses) >= 2
    assert all(e["category"] == "Health" for e in expenses)


def test_summary_is_consistent_with_list(api, base_url, health_expenses):
    listed = api.get(
        f"{base_url}/api/expenses", params={"category": "Health"}
    ).json()
    summary = api.get(f"{base_url}/api/expenses/summary").json()
    health_row = next(s for s in summary if s["category"] == "Health")

    assert health_row["count"] == len(listed)
    assert health_row["total"] == pytest.approx(sum(e["amount"] for e in listed))