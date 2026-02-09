# Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from typing import List, Dict, Any

class RuleConfigurationPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Existing methods...

    # --- Appended for TC-FT-003 ---
    def create_rule_with_conditions(self, trigger: Dict[str, Any], action: Dict[str, Any], conditions: List[Dict[str, Any]]):
        """
        Automates rule creation with multiple conditions.
        """
        # Click 'Add Rule' button
        add_rule_btn = self.driver.find_element(By.XPATH, Locators['add_rule_button'])
        add_rule_btn.click()

        # Set trigger type
        if 'type' in trigger:
            trigger_type_dropdown = self.driver.find_element(By.XPATH, Locators['trigger_type_dropdown'])
            trigger_type_dropdown.click()
            trigger_option = self.driver.find_element(By.XPATH, Locators['trigger_type_option'].format(trigger['type']))
            trigger_option.click()
        if 'date' in trigger:
            date_field = self.driver.find_element(By.XPATH, Locators['trigger_date_field'])
            date_field.send_keys(trigger['date'])

        # Set action type and amount
        action_type_dropdown = self.driver.find_element(By.XPATH, Locators['action_type_dropdown'])
        action_type_dropdown.click()
        action_option = self.driver.find_element(By.XPATH, Locators['action_type_option'].format(action['type']))
        action_option.click()
        if 'amount' in action:
            amount_field = self.driver.find_element(By.XPATH, Locators['action_amount_field'])
            amount_field.clear()
            amount_field.send_keys(str(action['amount']))

        # Add conditions
        for condition in conditions:
            add_condition_btn = self.driver.find_element(By.XPATH, Locators['add_condition_button'])
            add_condition_btn.click()
            condition_type_dropdown = self.driver.find_element(By.XPATH, Locators['condition_type_dropdown'])
            condition_type_dropdown.click()
            condition_option = self.driver.find_element(By.XPATH, Locators['condition_type_option'].format(condition['type']))
            condition_option.click()
            if 'operator' in condition:
                operator_dropdown = self.driver.find_element(By.XPATH, Locators['condition_operator_dropdown'])
                operator_dropdown.click()
                operator_option = self.driver.find_element(By.XPATH, Locators['condition_operator_option'].format(condition['operator']))
                operator_option.click()
            if 'value' in condition:
                value_field = self.driver.find_element(By.XPATH, Locators['condition_value_field'])
                value_field.clear()
                value_field.send_keys(str(condition['value']))

        # Save rule
        save_rule_btn = self.driver.find_element(By.XPATH, Locators['save_rule_button'])
        save_rule_btn.click()

    def simulate_deposit(self, balance: float, deposit: float, source: str):
        """
        Simulates deposit scenario for rule evaluation.
        """
        balance_field = self.driver.find_element(By.XPATH, Locators['balance_field'])
        balance_field.clear()
        balance_field.send_keys(str(balance))
        deposit_field = self.driver.find_element(By.XPATH, Locators['deposit_field'])
        deposit_field.clear()
        deposit_field.send_keys(str(deposit))
        source_dropdown = self.driver.find_element(By.XPATH, Locators['source_dropdown'])
        source_dropdown.click()
        source_option = self.driver.find_element(By.XPATH, Locators['source_option'].format(source))
        source_option.click()
        simulate_btn = self.driver.find_element(By.XPATH, Locators['simulate_deposit_button'])
        simulate_btn.click()

    def validate_transfer_execution(self, expected: bool):
        """
        Validates whether transfer was executed based on rule.
        """
        try:
            transfer_status = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, Locators['transfer_status_label']))
            )
            if expected:
                assert 'executed' in transfer_status.text.lower(), "Transfer was not executed when expected."
            else:
                assert 'not executed' in transfer_status.text.lower(), "Transfer was executed when not expected."
        except Exception as e:
            raise AssertionError(f"Transfer execution validation failed: {e}")

    # --- Appended for TC-FT-004 ---
    def submit_rule_missing_trigger(self, action: Dict[str, Any], conditions: List[Dict[str, Any]]):
        """
        Submits a rule with missing trigger type and checks for error.
        """
        add_rule_btn = self.driver.find_element(By.XPATH, Locators['add_rule_button'])
        add_rule_btn.click()
        action_type_dropdown = self.driver.find_element(By.XPATH, Locators['action_type_dropdown'])
        action_type_dropdown.click()
        action_option = self.driver.find_element(By.XPATH, Locators['action_type_option'].format(action['type']))
        action_option.click()
        if 'amount' in action:
            amount_field = self.driver.find_element(By.XPATH, Locators['action_amount_field'])
            amount_field.clear()
            amount_field.send_keys(str(action['amount']))
        for condition in conditions:
            add_condition_btn = self.driver.find_element(By.XPATH, Locators['add_condition_button'])
            add_condition_btn.click()
            # ... (as above)
        save_rule_btn = self.driver.find_element(By.XPATH, Locators['save_rule_button'])
        save_rule_btn.click()

    def submit_rule_unsupported_action(self, trigger: Dict[str, Any], action: Dict[str, Any], conditions: List[Dict[str, Any]]):
        """
        Submits a rule with unsupported action type and checks for error.
        """
        add_rule_btn = self.driver.find_element(By.XPATH, Locators['add_rule_button'])
        add_rule_btn.click()
        if 'type' in trigger:
            trigger_type_dropdown = self.driver.find_element(By.XPATH, Locators['trigger_type_dropdown'])
            trigger_type_dropdown.click()
            trigger_option = self.driver.find_element(By.XPATH, Locators['trigger_type_option'].format(trigger['type']))
            trigger_option.click()
        if 'date' in trigger:
            date_field = self.driver.find_element(By.XPATH, Locators['trigger_date_field'])
            date_field.send_keys(trigger['date'])
        action_type_dropdown = self.driver.find_element(By.XPATH, Locators['action_type_dropdown'])
        action_type_dropdown.click()
        action_option = self.driver.find_element(By.XPATH, Locators['action_type_option'].format(action['type']))
        action_option.click()
        for condition in conditions:
            add_condition_btn = self.driver.find_element(By.XPATH, Locators['add_condition_button'])
            add_condition_btn.click()
            # ... (as above)
        save_rule_btn = self.driver.find_element(By.XPATH, Locators['save_rule_button'])
        save_rule_btn.click()

    def validate_error_message(self, expected_message: str):
        """
        Validates system error message after rule submission.
        """
        error_label = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, Locators['rule_error_label']))
        )
        assert expected_message in error_label.text, f"Expected error '{expected_message}' not found."
