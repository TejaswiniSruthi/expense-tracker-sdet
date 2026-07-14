import allure
import pytest
from bson import ObjectId

pytestmark = pytest.mark.regression

@allure.feature("Expenses API")
@allure.story("Database persistence")
@allure.severity(allure.severity_level.CRITICAL)
def test_created_expense_is_persisted_in_mongo(db, new_expense):
    doc = db.expenses.find_one({"_id": ObjectId(new_expense["_id"])})

    assert doc is not None, "expense missing from database"
    assert doc["amount"] == new_expense["amount"]
    assert doc["category"] == new_expense["category"]
    assert doc["paymentMethod"] == new_expense["paymentMethod"]


def test_updated_amount_is_persisted_in_mongo(api, base_url, db, new_expense):
    api.put(f"{base_url}/api/expenses/{new_expense['_id']}", json={"amount": 888})

    doc = db.expenses.find_one({"_id": ObjectId(new_expense["_id"])})
    assert doc["amount"] == 888

@allure.feature("Expenses API")
@allure.story("Database persistence")
@allure.severity(allure.severity_level.CRITICAL)
def test_deleted_expense_is_removed_from_mongo(api, base_url, db, new_expense):
    api.delete(f"{base_url}/api/expenses/{new_expense['_id']}")

    assert db.expenses.find_one({"_id": ObjectId(new_expense["_id"])}) is None