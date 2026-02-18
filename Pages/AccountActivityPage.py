# AccountActivityPage.py
"""
PageClass for Account Activity/Transaction History.
QA Notes:
- Locators strictly from Locators.json.
- Methods for transaction validation.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class AccountActivityPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.transaction_table = driver.find_element(By.ID, "transactionTable")
        self.latest_transaction = driver.find_element(By.CSS_SELECTOR, "#transactionTable tbody tr:first-child")

    def is_transaction_table_displayed(self):
        return self.transaction_table.is_displayed()

    def get_latest_transaction(self):
        return self.latest_transaction.text
