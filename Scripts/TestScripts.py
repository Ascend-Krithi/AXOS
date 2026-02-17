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
        ...

    def test_minimum_payment_success(self):
        ...

    # TC-15483-005: Large payment flow
    def test_large_payment_success(self):
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.enter_username('richuser')
            login_page.enter_password('validpass123')
            login_page.click_login()

            navigation = Navigation(driver)
            navigation.go_to_bill_pay()

            bill_pay_page = BillPayPage(driver)
            bill_pay_page.fill_payee_info(
                name='Tax Authority',
                address='555 Government Blvd',
                city='Springfield',
                state='IL',
                zip_code='62705',
                phone='217-555-0500'
            )
            bill_pay_page.enter_account_numbers('88888', '88888')
            bill_pay_page.enter_amount(50000.00)
            bill_pay_page.select_from_account('13344')
            bill_pay_page.click_send_payment()

            assert bill_pay_page.is_success_message_displayed(), 'Payment confirmation not displayed.'
            assert bill_pay_page.is_confirmation_amount_formatted('$50,000.00'), 'Amount not formatted correctly.'

            account_activity_page = AccountActivityPage(driver)
            assert account_activity_page.verify_latest_transaction('Tax Authority', 50000.00), 'Transaction not recorded.'
            assert account_activity_page.verify_balance(49999.99), 'Balance not updated correctly.'
        finally:
            driver.quit()

    # TC-15483-006: Required fields validation
    def test_bill_pay_required_fields(self):
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.enter_username('validuser')
            login_page.enter_password('validpass123')
            login_page.click_login()

            navigation = Navigation(driver)
            navigation.go_to_bill_pay()

            bill_pay_page = BillPayPage(driver)
            # Leave Payee Name empty
            bill_pay_page.fill_payee_info(
                name='',
                address='123 Test St',
                city='Springfield',
                state='IL',
                zip_code='62706',
                phone='217-555-0600'
            )
            bill_pay_page.enter_account_numbers('12345', '12345')
            bill_pay_page.enter_amount(100.00)
            bill_pay_page.select_from_account('13344')
            bill_pay_page.click_send_payment()
            assert bill_pay_page.is_payee_name_error_displayed(), 'Payee Name error not displayed.'

            # Leave Address empty
            bill_pay_page.fill_payee_info(
                name='Test Payee',
                address='',
                city='Springfield',
                state='IL',
                zip_code='62706',
                phone='217-555-0600'
            )
            bill_pay_page.enter_account_numbers('12345', '12345')
            bill_pay_page.enter_amount(100.00)
            bill_pay_page.select_from_account('13344')
            bill_pay_page.click_send_payment()
            assert bill_pay_page.is_address_error_displayed(), 'Address error not displayed.'

            # Leave Amount empty
            bill_pay_page.fill_payee_info(
                name='Test Payee',
                address='123 Test St',
                city='Springfield',
                state='IL',
                zip_code='62706',
                phone='217-555-0600'
            )
            bill_pay_page.enter_account_numbers('12345', '12345')
            bill_pay_page.enter_amount('')
            bill_pay_page.select_from_account('13344')
            bill_pay_page.click_send_payment()
            assert bill_pay_page.is_amount_error_displayed(), 'Amount error not displayed.'

            # Leave Account number empty
            bill_pay_page.fill_payee_info(
                name='Test Payee',
                address='123 Test St',
                city='Springfield',
                state='IL',
                zip_code='62706',
                phone='217-555-0600'
            )
            bill_pay_page.enter_account_numbers('', '')
            bill_pay_page.enter_amount(100.00)
            bill_pay_page.select_from_account('13344')
            bill_pay_page.click_send_payment()
            assert bill_pay_page.is_account_number_error_displayed(), 'Account number error not displayed.'

            # Verify no payment processed for any missing field
            assert not bill_pay_page.is_success_message_displayed(), 'Payment should not be processed.'
        finally:
            driver.quit()
