# ScheduleSimulatorPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ScheduleSimulatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.simulate_date_button = (By.ID, 'simulate-date-btn')  # Placeholder locator
        self.simulate_interval_button = (By.ID, 'simulate-interval-btn')  # Placeholder locator
        self.transfer_action_msg = (By.CSS_SELECTOR, 'div.transfer-action-msg')  # Placeholder locator
        self.deposit_input = (By.ID, 'deposit-input')  # NEW: Placeholder locator
        self.simulate_deposit_button = (By.ID, 'simulate-deposit-btn')  # NEW: Placeholder locator

    def simulate_specific_date(self, date_str):
        simulate_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.simulate_date_button)
        )
        simulate_btn.click()
        # Optionally, enter date if UI requires

    def simulate_recurring_interval(self):
        interval_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.simulate_interval_button)
        )
        interval_btn.click()

    def verify_transfer_action_executed(self):
        action_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.transfer_action_msg)
        )
        return 'executed' in action_msg.text.lower()

    def simulate_deposit(self, amount):
        """
        Simulate a deposit action by entering the amount and clicking the deposit button.
        """
        deposit_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.deposit_input)
        )
        deposit_input.clear()
        deposit_input.send_keys(str(amount))
        deposit_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.simulate_deposit_button)
        )
        deposit_btn.click()

    def verify_transfer_amount(self, expected_amount):
        """
        Verifies that the transfer action message contains the expected amount.
        """
        action_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.transfer_action_msg)
        )
        return str(expected_amount) in action_msg.text
