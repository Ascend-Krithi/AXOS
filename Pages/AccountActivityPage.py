from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AccountActivityPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    TRANSACTION_TABLE = (By.ID, "transactionTable")
    LATEST_TRANSACTION = (By.CSS_SELECTOR, "#transactionTable tbody tr:first-child")

    def get_latest_transaction(self):
        self.wait.until(EC.visibility_of_element_located(self.TRANSACTION_TABLE))
        latest_row = self.driver.find_element(*self.LATEST_TRANSACTION)
        return latest_row.text

    def verify_transaction(self, payee_name: str, amount: str):
        transaction_text = self.get_latest_transaction()
        return payee_name in transaction_text and amount in transaction_text
