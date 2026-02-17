import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.BillPayPage import BillPayPage
from Pages.AccountActivityPage import AccountActivityPage

class TestLoginFunctionality:
    ...
class TestBillPay:
    ...

    def test_account_number_mismatch_error(self):
        """
        TC-15483-003: Account numbers do not match error, payment not processed
        Steps:
        1. Login and navigate to Bill Pay page
        2. Enter payee info: Gas Company, 789 Elm St, Springfield, IL, 62703, 217-555-0300
        3. Enter account number: 11111
        4. Enter verify account number: 22222 (different)
        5. Enter amount: 75.00 and select from account: 13344
        6. Click 'Send Payment' button
        7. Verify error 'Account numbers do not match' and payment not processed
        """
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.login("validuser", "validpass123")
            login_page.navigate_to_bill_pay()

            bill_pay_page = BillPayPage(driver)
            bill_pay_page.enter_payee_info(
                name="Gas Company",
                address="789 Elm St",
                city="Springfield",
                state="IL",
                zip="62703",
                phone="217-555-0300"
            )
            bill_pay_page.enter_account_number("11111")
            bill_pay_page.enter_verify_account_number("22222")
            bill_pay_page.enter_payment_details(amount="75.00", from_account_id="13344")
            bill_pay_page.click_send_payment()

            bill_pay_page.validate_account_mismatch_error()
            bill_pay_page.validate_payment_not_processed()
        finally:
            driver.quit()

    def test_minimum_payment_success(self):
        """
        TC-15483-004: Minimum payment amount (0.01), confirmation, transaction history, balance update
        Steps:
        1. Login and navigate to Bill Pay page
        2. Enter valid payee info: Charity Org, 321 Pine Rd, Springfield, IL, 62704, 217-555-0400, Account: 99999, Verify: 99999
        3. Enter minimum payment amount: 0.01
        4. Select from account: 13344 (Balance: $500.00)
        5. Click 'Send Payment' button
        6. Verify confirmation page shows $0.01 to Charity Org
        7. Check transaction history for this payment
        8. Verify account balance is reduced by $0.01 (new balance: $499.99)
        """
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.login("validuser", "validpass123")
            login_page.navigate_to_bill_pay()

            bill_pay_page = BillPayPage(driver)
            bill_pay_page.enter_payee_info(
                name="Charity Org",
                address="321 Pine Rd",
                city="Springfield",
                state="IL",
                zip="62704",
                phone="217-555-0400"
            )
            bill_pay_page.enter_account_number("99999")
            bill_pay_page.enter_verify_account_number("99999")
            bill_pay_page.enter_payment_details(amount="0.01", from_account_id="13344")
            bill_pay_page.click_send_payment()

            bill_pay_page.validate_confirmation_page(payee_name="Charity Org", amount="0.01")

            account_activity_page = AccountActivityPage(driver)
            account_activity_page.check_transaction_history(amount="0.01", payee_name="Charity Org")
            account_activity_page.verify_account_balance_updated(from_account_id="13344", expected_balance="499.99")
        finally:
            driver.quit()
