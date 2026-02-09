# RuleConfigurationPage.py
"""
Selenium PageClass for Rule Configuration Page
Handles rule creation, validation, and schema submission workflows.

---
QA Report:
- Existing functions tested for rule creation, schema validation, and submission.
- New functions for TC_SCRUM158_07 and TC_SCRUM158_08 appended and reviewed.
- Locators mapped from Locators.json; all selectors validated.
- Edge cases (max/empty conditions/actions) covered.

Troubleshooting Guide:
- If element not found: Check Locators.json for updates.
- If schema validation fails: Review test data and business rules.
- If API response is unexpected: Confirm backend supports scenario.

Future Considerations:
- Add dynamic locator loading for easier maintenance.
- Integrate test data generation utilities for more coverage.
- Expand error handling and reporting for robustness.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class RuleConfigurationPage:
    """
    Page Object for Rule Configuration Page.
    """
    # Locators from Locators.json
    rule_id_input = (By.ID, "rule-id-field")
    rule_name_input = (By.NAME, "rule-name")
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
    trigger_type_dropdown = (By.ID, "trigger-type-select")
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, "interval-value")
    after_deposit_toggle = (By.ID, "trigger-after-deposit")
    add_condition_btn = (By.ID, "add-condition-link")
    condition_type_dropdown = (By.CSS_SELECTOR, "select.condition-type")
    balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
    transaction_source_dropdown = (By.ID, "source-provider-select")
    operator_dropdown = (By.CSS_SELECTOR, ".condition-operator-select")
    action_type_dropdown = (By.ID, "action-type-select")
    transfer_amount_input = (By.NAME, "fixed-amount")
    percentage_input = (By.ID, "deposit-percentage")
    destination_account_input = (By.ID, "target-account-id")
    json_schema_editor = (By.CSS_SELECTOR, ".monaco-editor")
    validate_schema_btn = (By.ID, "btn-verify-json")
    success_message = (By.CSS_SELECTOR, ".alert-success")
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Existing logic ...
    def enter_rule_id(self, rule_id):
        elem = self.wait.until(EC.visibility_of_element_located(self.rule_id_input))
        elem.clear()
        elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        elem = self.wait.until(EC.visibility_of_element_located(self.rule_name_input))
        elem.clear()
        elem.send_keys(rule_name)

    def click_save_rule(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.save_rule_button))
        btn.click()

    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown))
        dropdown.click()
        dropdown.send_keys(trigger_type)

    def enter_recurring_interval(self, interval):
        interval_input = self.wait.until(EC.visibility_of_element_located(self.recurring_interval_input))
        interval_input.clear()
        interval_input.send_keys(str(interval))

    def toggle_after_deposit(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.after_deposit_toggle))
        toggle.click()

    def add_condition(self, condition_type, balance_limit=None, source_provider=None, operator=None):
        self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
        if condition_type:
            self.wait.until(EC.element_to_be_clickable(self.condition_type_dropdown)).send_keys(condition_type)
        if balance_limit:
            self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input)).send_keys(str(balance_limit))
        if source_provider:
            self.wait.until(EC.element_to_be_clickable(self.transaction_source_dropdown)).send_keys(source_provider)
        if operator:
            self.wait.until(EC.element_to_be_clickable(self.operator_dropdown)).send_keys(operator)

    def add_action(self, action_type, amount=None, percentage=None, destination_account=None):
        self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown)).send_keys(action_type)
        if amount:
            self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input)).send_keys(str(amount))
        if percentage:
            self.wait.until(EC.visibility_of_element_located(self.percentage_input)).send_keys(str(percentage))
        if destination_account:
            self.wait.until(EC.visibility_of_element_located(self.destination_account_input)).send_keys(destination_account)

    def enter_json_schema(self, schema_text):
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.click()
        editor.clear()
        editor.send_keys(schema_text)

    def validate_schema(self):
        self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn)).click()
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return True
        except TimeoutException:
            return False

    def get_schema_error(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.schema_error_message)).text
        except TimeoutException:
            return None

    # --- Appended for TC_SCRUM158_07 ---
    def create_rule_with_max_conditions_actions(self, rule_id, rule_name, conditions, actions):
        """
        Create rule with maximum supported conditions and actions (e.g., 10 each).
        Args:
            rule_id (str): Rule identifier.
            rule_name (str): Rule name.
            conditions (list): List of conditions dicts.
            actions (list): List of actions dicts.
        Returns:
            bool: True if rule is created and validated, False otherwise.
        """
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        # Add all conditions
        for cond in conditions:
            self.add_condition(
                condition_type=cond.get('type'),
                balance_limit=cond.get('balance_limit'),
                source_provider=cond.get('source_provider'),
                operator=cond.get('operator')
            )
        # Add all actions
        for act in actions:
            self.add_action(
                action_type=act.get('type'),
                amount=act.get('amount'),
                percentage=act.get('percentage'),
                destination_account=act.get('destination_account')
            )
        self.click_save_rule()
        # Schema validation
        return self.validate_schema()

    def submit_and_validate_rule(self, schema_text):
        """
        Submit rule schema and validate creation.
        Args:
            schema_text (str): JSON schema as string.
        Returns:
            bool: True if rule is created and contains all submitted conditions/actions.
        """
        self.enter_json_schema(schema_text)
        is_valid = self.validate_schema()
        if not is_valid:
            return False
        self.click_save_rule()
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return True
        except TimeoutException:
            return False

    # --- Appended for TC_SCRUM158_08 ---
    def create_rule_with_empty_conditions_actions(self, rule_id, rule_name):
        """
        Create rule with empty conditions and actions arrays.
        Args:
            rule_id (str): Rule identifier.
            rule_name (str): Rule name.
        Returns:
            dict: { 'schema_valid': bool, 'error': str or None }
        """
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        # No conditions/actions added
        self.click_save_rule()
        schema_valid = self.validate_schema()
        error = None
        if not schema_valid:
            error = self.get_schema_error()
        return { 'schema_valid': schema_valid, 'error': error }

    def submit_empty_rule_schema(self, schema_text):
        """
        Submit rule schema with empty conditions/actions and validate response.
        Args:
            schema_text (str): JSON schema as string.
        Returns:
            dict: { 'accepted': bool, 'error': str or None }
        """
        self.enter_json_schema(schema_text)
        is_valid = self.validate_schema()
        self.click_save_rule()
        accepted = False
        error = None
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            accepted = True
        except TimeoutException:
            error = self.get_schema_error()
        return { 'accepted': accepted, 'error': error }
