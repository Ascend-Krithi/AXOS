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

    def simulate_deposit_and_verify_transfer(self, deposit_amount, expected_transfer):
        # Simulate deposit action
        deposit_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'deposit-amount-input'))
        )
        deposit_input.clear()
        deposit_input.send_keys(str(deposit_amount))
        simulate_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'simulate-deposit-btn'))
        )
        simulate_btn.click()
        # Verify transfer
        transfer_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.transfer-action-msg'))
        )
        return str(expected_transfer) in transfer_msg.text
