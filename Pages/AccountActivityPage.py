from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AccountActivityPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.transaction_table = (By.ID, "transactionTable")
        self.latest_transaction = (By.CSS_SELECTOR, "#transactionTable tbody tr:first-child")

    def is_transaction_table_displayed(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.transaction_table)
        ).is_displayed()

    def get_latest_transaction(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.latest_transaction)
        )
        row = self.driver.find_element(*self.latest_transaction)
        return [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
