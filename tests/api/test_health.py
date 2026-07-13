import pytest

pytestmark = pytest.mark.smoke


def test_health_returns_200(api, base_url):
    response = api.get(f"{base_url}/health")
    assert response.status_code == 200


def test_health_reports_db_connected(api, base_url):
    body = api.get(f"{base_url}/health").json()
    assert body["status"] == "ok"
    assert body["db"] == "connected"


def test_list_expenses_returns_array(api, base_url):
    response = api.get(f"{base_url}/api/expenses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)