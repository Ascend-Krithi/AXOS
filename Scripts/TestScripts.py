# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from Pages.LoginPage import LoginPage
from Pages.BillPayPage import BillPayPage
from Pages.AccountActivityPage import AccountActivityPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        # Example placeholder
        pass

    def test_remember_me_functionality(self):
        # Example placeholder
        pass

class TestParabankBillPay:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.bill_pay_page = BillPayPage(driver)
        self.account_activity_page = AccountActivityPage(driver)

    def test_TC001_bill_payment_flow(self):
        # Step 2: Login
        self.login_page.login("testuser123", "Pass@1234")
        # Step 3: Navigate to Bill Pay (assume navigation via driver, adjust as needed)
        self.driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
        # Step 4: Enter payee info
        payee_details = {
            "payee_name": "Electric Power Company",
            "address": "123 Main Street",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62701",
            "phone_number": "555-0123",
            "account_number": "987654321",
            "verify_account_number": "987654321",
            "amount": 150.00,
            "from_account_id": 12345
        }
        self.bill_pay_page.fill_payee_details(payee_details)
        # Step 5/6: Amount and account already in payee_details
        # Step 7: Submit payment
        self.bill_pay_page.submit_payment()
        # Step 7: Confirm
        confirmation = self.bill_pay_page.get_confirmation_details()
        assert confirmation["payee_name"] == "Electric Power Company"
        assert confirmation["amount"] == "$150.00" or confirmation["amount"] == "150.00"
        assert str(confirmation["from_account"]) == "12345" or confirmation["from_account"] == "Savings Account #12345"
        # Step 8: Go to Account Activity
        self.driver.get("https://parabank.parasoft.com/parabank/activity.htm")
        assert self.account_activity_page.is_transaction_table_present()
        assert self.account_activity_page.verify_transaction({"payee_name": "Electric Power Company", "amount": 150.00})

    def test_TC002_bill_payment_minimum_amount(self):
        # Step 2: Login
        self.login_page.login("testuser123", "Pass@1234")
        # Step 3: Navigate to Bill Pay
        self.driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
        # Step 4: Enter payee info with minimum amount
        payee_details = {
            "payee_name": "Electric Power Company",
            "address": "123 Main Street",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62701",
            "phone_number": "555-0123",
            "account_number": "987654321",
            "verify_account_number": "987654321",
            "amount": 0.01,
            "from_account_id": 12345
        }
        self.bill_pay_page.fill_payee_details(payee_details)
        self.bill_pay_page.submit_payment()
        confirmation = self.bill_pay_page.get_confirmation_details()
        assert confirmation["payee_name"] == "Electric Power Company"
        assert confirmation["amount"] == "$0.01" or confirmation["amount"] == "0.01"
        assert str(confirmation["from_account"]) == "12345" or confirmation["from_account"] == "Savings Account #12345"
