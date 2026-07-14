import pytest
import uuid

from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e

BASE_URL = "http://localhost:3000"


def add_expense(page: Page, amount: str, description: str):
    page.fill("#amount", amount)
    page.select_option("#category", "Food")
    page.fill("#description", description)
    page.select_option("#paymentMethod", "upi")
    page.click("button[type=submit]")


def test_added_expense_appears_in_list(page: Page):
    page.goto(BASE_URL)
    description = f"e2e add {uuid.uuid4().hex[:8]}"
    add_expense(page, "123.45", description)

    row = page.locator("#expense-list tr", has_text=description)
    expect(row).to_be_visible()


def test_added_expense_updates_summary(page: Page):
    page.goto(BASE_URL)
    add_expense(page, "50", "e2e summary test")

    expect(page.locator("#summary")).to_contain_text("Food")


def test_deleted_expense_disappears(page: Page):
    page.goto(BASE_URL)
    add_expense(page, "77", "e2e delete me")

    row = page.locator("#expense-list tr", has_text="e2e delete me")
    expect(row).to_be_visible()
    row.locator("button.del").click()

    expect(page.locator("#expense-list tr", has_text="e2e delete me")).to_have_count(0)