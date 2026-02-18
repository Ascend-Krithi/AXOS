from selenium.webdriver.common.by import By

class AccountActivityPage:
    def __init__(self, driver):
        self.driver = driver
        self.transaction_table = driver.find_element(By.ID, 'transactionTable')

    def get_latest_transaction(self):
        latest_transaction = self.driver.find_element(By.CSS_SELECTOR, '#transactionTable tbody tr:first-child')
        return latest_transaction.text

    def is_transaction_present(self, details):
        rows = self.transaction_table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            if details in row.text:
                return True
        return False
