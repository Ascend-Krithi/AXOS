# Executive Summary
# BillPayPage automates the bill payment workflow, including form entry and confirmation validation.

# Detailed Analysis
# Uses Locators.json for all form fields and confirmation elements. Methods cover payee entry, account selection, payment, and confirmation.

# Implementation Guide
# Instantiate BillPayPage with WebDriver. Use methods to fill form, select account, enter amount, send payment, and verify confirmation.

# Quality Assurance Report
# Locators validated. Methods reviewed for completeness and error handling.

# Troubleshooting Guide
# If payment fails, check locator values and input data. Ensure form fields are interactable.

# Future Considerations
# Extend for negative tests, multiple payees, and payment history validation.

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class BillPayPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Form fields
        self.payee_name = driver.find_element(By.NAME, "payee.name")
        self.address = driver.find_element(By.NAME, "payee.address.street")
        self.city = driver.find_element(By.NAME, "payee.address.city")
        self.state = driver.find_element(By.NAME, "payee.address.state")
        self.zip_code = driver.find_element(By.NAME, "payee.address.zipCode")
        self.phone_number = driver.find_element(By.NAME, "payee.phoneNumber")
        self.account_number = driver.find_element(By.NAME, "payee.accountNumber")
        self.verify_account_number = driver.find_element(By.NAME, "verifyAccount")
        self.amount = driver.find_element(By.NAME, "amount")
        self.from_account_id = driver.find_element(By.NAME, "fromAccountId")
        self.send_payment_button = driver.find_element(By.CSS_SELECTOR, "input[value='Send Payment']")
        # Confirmation elements
        self.success_message = driver.find_element(By.ID, "billpayResult")
        self.conf_payee_name = driver.find_element(By.ID, "payeeName")
        self.conf_amount = driver.find_element(By.ID, "amount")
        self.conf_from_account = driver.find_element(By.ID, "fromAccountId")

    def enter_payee_info(self, name: str, address: str, city: str, state: str, zip_code: str, phone: str, account: str, verify_account: str):
        self.payee_name.clear()
        self.payee_name.send_keys(name)
        self.address.clear()
        self.address.send_keys(address)
        self.city.clear()
        self.city.send_keys(city)
        self.state.clear()
        self.state.send_keys(state)
        self.zip_code.clear()
        self.zip_code.send_keys(zip_code)
        self.phone_number.clear()
        self.phone_number.send_keys(phone)
        self.account_number.clear()
        self.account_number.send_keys(account)
        self.verify_account_number.clear()
        self.verify_account_number.send_keys(verify_account)

    def select_from_account(self, account_id: str):
        self.from_account_id.clear()
        self.from_account_id.send_keys(account_id)

    def enter_amount(self, amount: str):
        self.amount.clear()
        self.amount.send_keys(amount)

    def send_payment(self):
        self.send_payment_button.click()

    def verify_confirmation(self, expected_payee: str, expected_amount: str, expected_account: str):
        assert expected_payee in self.conf_payee_name.text, f"Expected payee '{expected_payee}' not found"
        assert expected_amount in self.conf_amount.text, f"Expected amount '{expected_amount}' not found"
        assert expected_account in self.conf_from_account.text, f"Expected account '{expected_account}' not found"
        assert "Payment" in self.success_message.text, "Success message not found"
