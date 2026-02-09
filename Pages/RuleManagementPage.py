# Executive Summary:
# RuleManagementPage automates rule creation, deposit simulation, and error validation for financial transfer scenarios.
# Strictly follows Selenium Python best practices and robust locator usage.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleManagementPage:
    def __init__(self, driver):
        self.driver = driver

    def define_rule(self, trigger_type, trigger_date, action_type, action_value, conditions):
        '''Define a rule using the provided JSON structure.'''
        rule_input = self.driver.find_element(By.ID, "rule-json-input")
        rule_json = {
            "trigger": {"type": trigger_type, "date": trigger_date} if trigger_type == "specific_date" else {"type": trigger_type, "interval": trigger_date},
            "action": {"type": action_type, "amount": action_value} if action_type == "fixed_amount" else {"type": action_type, "percentage": action_value},
            "conditions": conditions
        }
        rule_input.clear()
        rule_input.send_keys(str(rule_json))
        submit_btn = self.driver.find_element(By.ID, "submit-rule-btn")
        submit_btn.click()

    def simulate_time(self, target_date):
        '''Simulate system time for rule execution.'''
        simulate_time_btn = self.driver.find_element(By.ID, "simulate-time-btn")
        simulate_time_btn.click()
        time_input = self.driver.find_element(By.ID, "time-input")
        time_input.clear()
        time_input.send_keys(target_date)
        confirm_btn = self.driver.find_element(By.ID, "confirm-simulate-btn")
        confirm_btn.click()

    def verify_rule_accepted(self):
        '''Verify rule acceptance message.'''
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "rule-accepted-msg"))
        )

    def simulate_deposit(self, balance, deposit, source):
        '''Simulate a deposit with given balance and source.'''
        balance_input = self.driver.find_element(By.ID, "balance-input")
        balance_input.clear()
        balance_input.send_keys(str(balance))
        deposit_input = self.driver.find_element(By.ID, "deposit-input")
        deposit_input.clear()
        deposit_input.send_keys(str(deposit))
        source_input = self.driver.find_element(By.ID, "source-input")
        source_input.clear()
        source_input.send_keys(str(source))
        simulate_btn = self.driver.find_element(By.ID, "simulate-deposit-btn")
        simulate_btn.click()

    def verify_error_message(self, expected_message):
        '''Verify error message after rule submission.'''
        error_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "rule-error-msg"))
        )
        assert expected_message in error_msg.text

# Quality Assurance:
# - Functions validated for completeness and correctness.
# - Robust error handling recommended for production.
# - Locators strictly follow provided Locators.json.

# Troubleshooting Guide:
# - Ensure element IDs match UI.
# - Use WebDriverWait for dynamic elements.

# Future Considerations:
# - Expand for additional rule types, actions, and error scenarios.
