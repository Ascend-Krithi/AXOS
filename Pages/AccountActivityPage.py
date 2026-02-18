from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AccountActivityPage:
    def __init__(self, driver):
        self.driver = driver
        self.transaction_table = (By.ID, "transactionTable")
        self.latest_transaction = (By.CSS_SELECTOR, "#transactionTable tbody tr:first-child")

    def get_latest_transaction(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.transaction_table))
        row = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.latest_transaction))
        return row.text

    def verify_transaction(self, expected_details):
        latest = self.get_latest_transaction()
        return all(detail in latest for detail in expected_details)
