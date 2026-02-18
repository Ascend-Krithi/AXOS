# Existing imports and code...
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# Assume PageClass imports:
from Pages.LoginPage import LoginPage
from Pages.BillPayPage import BillPayPage
from Pages.AccountOverviewPage import AccountOverviewPage
from Pages.AccountActivityPage import AccountActivityPage

# Existing test classes and methods...

# --- APPENDED TEST METHODS BELOW ---

@pytest.mark.usefixtures("setup")
def test_valid_login(self):
    """
    Test Case: Valid Login
    Steps:
    1. Navigate to Login Page
    2. Enter valid username and password
    3. Click Login
    Validation:
    - User is navigated to Account Overview page
    """
    login_page = LoginPage(self.driver)
    login_page.go_to_login_page()
    login_page.enter_username("valid_user")
    login_page.enter_password("valid_password")
    login_page.click_login()
    account_overview = AccountOverviewPage(self.driver)
    assert account_overview.is_displayed(), "Account Overview page should be displayed after login"

@pytest.mark.usefixtures("setup")
def test_bill_payment_success(self):
    """
    Test Case: Bill Payment Success
    Steps:
    1. Login as valid user
    2. Navigate to Bill Pay
    3. Enter valid payee, amount, and account
    4. Submit payment
    Validation:
    - Payment confirmation message is displayed
    """
    login_page = LoginPage(self.driver)
    login_page.go_to_login_page()
    login_page.enter_username("valid_user")
    login_page.enter_password("valid_password")
    login_page.click_login()
    bill_pay_page = BillPayPage(self.driver)
    bill_pay_page.go_to_bill_pay()
    bill_pay_page.enter_payee("Test Payee")
    bill_pay_page.enter_amount("100")
    bill_pay_page.select_account("12345")
    bill_pay_page.submit_payment()
    assert bill_pay_page.is_confirmation_displayed(), "Payment confirmation should be displayed"

@pytest.mark.usefixtures("setup")
def test_account_activity_filter(self):
    """
    Test Case: Account Activity Filter
    Steps:
    1. Login as valid user
    2. Navigate to Account Activity
    3. Select account and date range
    4. Click Filter
    Validation:
    - Only filtered transactions are shown
    """
    login_page = LoginPage(self.driver)
    login_page.go_to_login_page()
    login_page.enter_username("valid_user")
    login_page.enter_password("valid_password")
    login_page.click_login()
    account_activity = AccountActivityPage(self.driver)
    account_activity.go_to_account_activity()
    account_activity.select_account("12345")
    account_activity.set_date_range("2024-01-01", "2024-01-31")
    account_activity.click_filter()
    assert account_activity.is_filtered("2024-01-01", "2024-01-31"), "Transactions should be filtered by date range"
