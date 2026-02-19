# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class AccountActivityPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.transaction_table = (By.ID, "transactionTable")
        self.latest_transaction = (By.CSS_SELECTOR, "#transactionTable tbody tr:first-child")

    def is_transaction_table_present(self):
        return self.driver.find_element(*self.transaction_table).is_displayed()

    def get_latest_transaction_details(self):
        row = self.driver.find_element(*self.latest_transaction)
        return [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]

    def verify_transaction(self, expected_details: dict):
        latest = self.get_latest_transaction_details()
        # Assumes table columns: date, description, amount, etc.
        # Customize index mapping as per actual table structure
        return (
            expected_details["payee_name"] in latest[1] and
            str(expected_details["amount"]) == latest[2]
        )
