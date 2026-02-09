from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class DepositPage:
    """
    PageClass for deposit simulation.
    Supports:
      - Deposit action
      - Transfer success message validation
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Locators (example, must be aligned with actual app)
        self.deposit_input = driver.find_element(By.ID, "deposit-amount-input")
        self.deposit_button = driver.find_element(By.ID, "deposit-submit-btn")
        self.transfer_message = driver.find_element(By.CSS_SELECTOR, ".transfer-success-msg")

    def simulate_deposit(self, amount: int):
        """Simulate deposit of specified amount."""
        self.deposit_input.clear()
        self.deposit_input.send_keys(str(amount))
        self.deposit_button.click()

    def get_transfer_message(self):
        """Return transfer success message text."""
        return self.transfer_message.text
