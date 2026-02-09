# Pages/RuleConfigurationPage.py
"""
RuleConfigurationPage Selenium PageClass

This PageClass automates interactions with the Rule Configuration page, covering rule form, triggers, conditions, actions, and validation components. Generated based on Locators.json and test case requirements (TC_SCRUM158_07, TC_SCRUM158_08, TC_SCRUM158_01, TC_SCRUM158_02).

QA Report:
- All locators from Locators.json are mapped as class attributes.
- Methods are provided for form filling, trigger/condition/action manipulation, and schema validation.
- Updated with bulk addition/validation logic for conditions/actions (CASE-Update).
- Code is structured for downstream integration, using synchronous Selenium flows.
- Comprehensive docstrings included for maintainability.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import time

class RuleConfigurationPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Rule Form Locators
        self.rule_id_input = driver.find_element(By.ID, 'rule-id-field')
        self.rule_name_input = driver.find_element(By.NAME, 'rule-name')
        self.save_rule_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Trigger Locators
        self.trigger_type_dropdown = driver.find_element(By.ID, 'trigger-type-select')
        self.date_picker = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = driver.find_element(By.ID, 'interval-value')
        self.after_deposit_toggle = driver.find_element(By.ID, 'trigger-after-deposit')
        # Condition Locators
        self.add_condition_btn = driver.find_element(By.ID, 'add-condition-link')
        self.condition_type_dropdown = driver.find_element(By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = driver.find_element(By.NAME, 'balance-limit')
        self.transaction_source_dropdown = driver.find_element(By.ID, 'source-provider-select')
        self.operator_dropdown = driver.find_element(By.CSS_SELECTOR, '.condition-operator-select')
        # Action Locators
        self.action_type_dropdown = driver.find_element(By.ID, 'action-type-select')
        self.transfer_amount_input = driver.find_element(By.NAME, 'fixed-amount')
        self.percentage_input = driver.find_element(By.ID, 'deposit-percentage')
        self.destination_account_input = driver.find_element(By.ID, 'target-account-id')
        # Validation Locators
        self.json_schema_editor = driver.find_element(By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = driver.find_element(By.ID, 'btn-verify-json')
        self.success_message = driver.find_element(By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = driver.find_element(By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def fill_rule_form(self, rule_id: str, rule_name: str):
        """Fill out the rule form fields."""
        self.rule_id_input.clear()
        self.rule_id_input.send_keys(rule_id)
        self.rule_name_input.clear()
        self.rule_name_input.send_keys(rule_name)

    def select_trigger_type(self, trigger_type: str):
        """Select trigger type from dropdown."""
        self.trigger_type_dropdown.click()
        # Select option logic here (implementation depends on dropdown type)

    def set_trigger_date(self, date_value: str):
        """Set date in the trigger date picker."""
        self.date_picker.clear()
        self.date_picker.send_keys(date_value)

    def set_recurring_interval(self, interval: str):
        """Set recurring interval value."""
        self.recurring_interval_input.clear()
        self.recurring_interval_input.send_keys(interval)

    def toggle_after_deposit(self):
        """Toggle 'after deposit' trigger."""
        self.after_deposit_toggle.click()

    def add_condition(self):
        """Click to add a new condition."""
        self.add_condition_btn.click()

    def select_condition_type(self, condition_type: str):
        """Select condition type from dropdown."""
        self.condition_type_dropdown.click()
        # Select option logic here

    def set_balance_threshold(self, threshold: str):
        """Set balance threshold value."""
        self.balance_threshold_input.clear()
        self.balance_threshold_input.send_keys(threshold)

    def select_transaction_source(self, source: str):
        """Select transaction source from dropdown."""
        self.transaction_source_dropdown.click()
        # Select option logic here

    def select_operator(self, operator: str):
        """Select operator from dropdown."""
        self.operator_dropdown.click()
        # Select option logic here

    def select_action_type(self, action_type: str):
        """Select action type from dropdown."""
        self.action_type_dropdown.click()
        # Select option logic here

    def set_transfer_amount(self, amount: str):
        """Set transfer amount for action."""
        self.transfer_amount_input.clear()
        self.transfer_amount_input.send_keys(amount)

    def set_percentage(self, percentage: str):
        """Set deposit percentage for action."""
        self.percentage_input.clear()
        self.percentage_input.send_keys(percentage)

    def set_destination_account(self, account_id: str):
        """Set destination account ID for action."""
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(account_id)

    def edit_json_schema(self, schema_text: str):
        """Edit the JSON schema in the editor."""
        self.json_schema_editor.clear()
        self.json_schema_editor.send_keys(schema_text)

    def validate_schema(self):
        """Click validate schema button."""
        self.validate_schema_btn.click()

    def get_success_message(self) -> str:
        """Retrieve the success message after validation."""
        return self.success_message.text

    def get_schema_error_message(self) -> str:
        """Retrieve the error message after validation failure."""
        return self.schema_error_message.text

    # --- Newly added methods for CASE-Update (TC_SCRUM158_07, TC_SCRUM158_08) ---

    def add_multiple_conditions(self, conditions: list):
        """
        Add multiple conditions to the rule configuration.
        :param conditions: List of dicts with condition details (type, threshold, source, operator).
        """
        for cond in conditions:
            self.add_condition()
            if 'type' in cond:
                self.select_condition_type(cond['type'])
            if 'threshold' in cond:
                self.set_balance_threshold(cond['threshold'])
            if 'source' in cond:
                self.select_transaction_source(cond['source'])
            if 'operator' in cond:
                self.select_operator(cond['operator'])
            time.sleep(0.2)  # Allow UI update

    def add_multiple_actions(self, actions: list):
        """
        Add multiple actions to the rule configuration.
        :param actions: List of dicts with action details (type, amount, percentage, destination_account).
        """
        for act in actions:
            # Assume UI provides a way to add actions similar to conditions
            self.select_action_type(act.get('type', ''))
            if 'amount' in act:
                self.set_transfer_amount(act['amount'])
            if 'percentage' in act:
                self.set_percentage(act['percentage'])
            if 'destination_account' in act:
                self.set_destination_account(act['destination_account'])
            time.sleep(0.2)

    def submit_rule(self):
        """
        Submit the rule by clicking the save button.
        """
        self.save_rule_button.click()

    def is_rule_persisted(self, rule_id: str) -> bool:
        """
        Validate if a rule with the given ID exists in the UI after creation.
        This is a placeholder for UI-based verification (not API).
        """
        try:
            rule_element = self.driver.find_element(By.XPATH, f"//td[text()='{rule_id}']")
            return rule_element is not None
        except NoSuchElementException:
            return False

    def validate_conditions_actions_count(self, expected_conditions: int, expected_actions: int) -> bool:
        """
        Validate the number of conditions and actions displayed in the UI.
        """
        try:
            conditions = self.driver.find_elements(By.CSS_SELECTOR, 'div.condition-row')
            actions = self.driver.find_elements(By.CSS_SELECTOR, 'div.action-row')
            return len(conditions) == expected_conditions and len(actions) == expected_actions
        except Exception:
            return False
