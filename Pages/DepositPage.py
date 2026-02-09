# DepositPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DepositPage:
    DEPOSIT_FIELD = (By.ID, "deposit-amount")  # Add this locator to Locators.json
    DEPOSIT_SUBMIT = (By.ID, "deposit-submit")  # Add this locator to Locators.json
    DEPOSIT_SUCCESS = (By.CSS_SELECTOR, "div.deposit-success")  # Add this locator to Locators.json
    TRANSFER_AMOUNT = (By.CSS_SELECTOR, "span.transfer-amount")  # Add this locator to Locators.json

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def enter_deposit_amount(self, amount: int):
        deposit_field = self.driver.find_element(*self.DEPOSIT_FIELD)
        deposit_field.clear()
        deposit_field.send_keys(str(amount))

    def submit_deposit(self):
        self.driver.find_element(*self.DEPOSIT_SUBMIT).click()

    def wait_for_success(self):
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.DEPOSIT_SUCCESS)
        )

    def get_transfer_amount(self):
        return self.driver.find_element(*self.TRANSFER_AMOUNT).text
