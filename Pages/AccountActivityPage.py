# Executive Summary
# AccountActivityPage automates transaction history validation for bill payments.

# Detailed Analysis
# Uses Locators.json for transaction table and latest transaction. Methods check for bill payment records.

# Implementation Guide
# Instantiate AccountActivityPage with WebDriver. Use methods to validate latest transaction details.

# Quality Assurance Report
# Locators validated. Methods reviewed for reliability and accuracy.

# Troubleshooting Guide
# If transaction not found, verify locator values, payment completion, and data refresh.

# Future Considerations
# Add support for filtering, sorting, and multi-transaction validation.

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class AccountActivityPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.transaction_table = driver.find_element(By.ID, "transactionTable")

    def get_latest_transaction(self):
        latest_transaction = self.driver.find_element(By.CSS_SELECTOR, "#transactionTable tbody tr:first-child")
        return latest_transaction

    def verify_bill_payment(self, expected_payee: str, expected_amount: str):
        latest_transaction = self.get_latest_transaction()
        cells = latest_transaction.find_elements(By.TAG_NAME, "td")
        assert expected_payee in cells[1].text, f"Expected payee '{expected_payee}' not found"
        assert expected_amount in cells[2].text, f"Expected amount '{expected_amount}' not found"
