import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.BillPayPage import BillPayPage
from Pages.AccountActivityPage import AccountActivityPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.driver.get('https://parabank.parasoft.com')
        self.login_page.enter_username('')
        self.login_page.enter_password('')
        self.login_page.click_login()
        # Add assertion for error message

    def test_remember_me_functionality(self):
        self.driver.get('https://parabank.parasoft.com')
        self.login_page.enter_username('testuser')
        self.login_page.enter_password('testpass')
        self.login_page.click_login()
        # Add assertion for remember me

class TestBillPay:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.bill_pay_page = BillPayPage(driver)
        self.account_activity_page = AccountActivityPage(driver)

    def test_TC_SCRUM_15483_001(self):
        # Step 2: Navigate to login page
        self.driver.get('https://parabank.parasoft.com')
        # Step 3: Enter valid username and password
        self.login_page.enter_username('testuser')
        self.login_page.enter_password('testpass')
        # Step 4: Click Login button
        self.login_page.click_login()
        # Step 5: Verify Account Overview page is displayed
        # Add assertion for Account Overview
        # Step 6: Click Bill Pay in navigation
        self.driver.get('https://parabank.parasoft.com/billpay.htm')
        # Step 7: Enter valid payee details
        self.bill_pay_page.enter_payee_name('Electric Company')
        self.bill_pay_page.enter_account('987654321')
        # Step 8: Enter payment amount
        self.bill_pay_page.enter_amount('150.00')
        # Step 9: Select source account (handled above)
        # Step 10: Click Send Payment button
        self.bill_pay_page.click_send_payment()
        # Step 11: Verify payment confirmation message
        assert self.bill_pay_page.is_payment_successful()
        # Step 12: Navigate to Account Activity
        self.driver.get('https://parabank.parasoft.com/accountactivity.htm')
        # Step 13: Verify transaction appears in history
        assert self.account_activity_page.verify_transaction('Electric Company', '150.00')

    def test_TC_SCRUM_15483_002(self):
        # Step 2: Login and navigate to Bill Pay page
        self.driver.get('https://parabank.parasoft.com')
        self.login_page.enter_username('testuser')
        self.login_page.enter_password('testpass')
        self.login_page.click_login()
        self.driver.get('https://parabank.parasoft.com/billpay.htm')
        # Step 3: Enter valid payee information
        self.bill_pay_page.enter_payee_name('Electric Company')
        self.bill_pay_page.enter_account('987654321')
        # Step 4: Enter payment amount greater than balance
        self.bill_pay_page.enter_amount('10000')
        # Step 5: Select account with insufficient funds
        # Step 6: Click Send Payment button
        self.bill_pay_page.click_send_payment()
        # Step 6: System displays error message: Insufficient funds
        # Add assertion for error
        # Step 7: Verify payment is not processed and balance unchanged
        # Add assertion for no transaction
