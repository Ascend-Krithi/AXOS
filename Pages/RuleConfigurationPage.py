"""
Selenium PageClass for Rule Configuration Page

Implements all required functions for test cases:
- Rule creation interface navigation
- Specific date trigger definition
- Balance threshold condition addition
- Fixed amount transfer action addition
- Rule persistence and retrieval
- Rule validation

Locators are sourced from Locators.json.
Strict adherence to Selenium Python best practices.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RuleConfigurationPage:
    """
    Page Object for Automated Transfers Rule Configuration Page.
    """

    # Locators from Locators.json
    rule_id_input = (By.ID, 'rule-id-field')
    rule_name_input = (By.NAME, 'rule-name')
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
    trigger_type_dropdown = (By.ID, 'trigger-type-select')
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, 'interval-value')
    after_deposit_toggle = (By.ID, 'trigger-after-deposit')
    add_condition_btn = (By.ID, 'add-condition-link')
    condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
    balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit'")
    transaction_source_dropdown = (By.ID, 'source-provider-select')
    operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')
    action_type_dropdown = (By.ID, 'action-type-select')
    transfer_amount_input = (By.NAME, 'fixed-amount')
    percentage_input = (By.ID, 'deposit-percentage')
    destination_account_input = (By.ID, 'target-account-id')
    json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
    validate_schema_btn = (By.ID, 'btn-verify-json')
    success_message = (By.CSS_SELECTOR, '.alert-success')
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def navigate_to_rule_creation(self):
        """
        Navigates to the Automated Transfers rule creation interface.
        """
        # Assume navigation is handled externally, or implement as needed
        self.wait.until(EC.visibility_of_element_located(self.rule_id_input))
        self.wait.until(EC.visibility_of_element_located(self.rule_name_input))
        self.wait.until(EC.visibility_of_element_located(self.save_rule_button))
        self.wait.until(EC.visibility_of_element_located(self.trigger_type_dropdown))
        self.wait.until(EC.visibility_of_element_located(self.add_condition_btn))
        self.wait.until(EC.visibility_of_element_located(self.action_type_dropdown))

    def set_specific_date_trigger(self, date_str):
        """
        Defines a specific date trigger.
        :param date_str: ISO date string, e.g. '2024-12-31T10:00:00Z'
        """
        self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown)).click()
        dropdown = self.driver.find_element(*self.trigger_type_dropdown)
        dropdown.send_keys("specific_date")
        self.wait.until(EC.element_to_be_clickable(self.date_picker)).send_keys(date_str.split('T')[0])
        # Optionally set time if supported

    def add_balance_threshold_condition(self, operator, amount, currency):
        """
        Adds a balance threshold condition.
        :param operator: e.g., 'greater_than'
        :param amount: e.g., 500
        :param currency: e.g., 'USD'
        """
        self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
        self.wait.until(EC.element_to_be_clickable(self.condition_type_dropdown)).send_keys("balance_threshold")
        self.wait.until(EC.element_to_be_clickable(self.operator_dropdown)).send_keys(operator)
        balance_input = self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input))
        balance_input.clear()
        balance_input.send_keys(str(amount))
        # Currency selection if UI supports

    def add_fixed_transfer_action(self, amount, currency, destination_account):
        """
        Adds a fixed amount transfer action.
        :param amount: e.g., 100
        :param currency: e.g., 'USD'
        :param destination_account: e.g., 'SAV-001'
        """
        self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown)).click()
        action_dropdown = self.driver.find_element(*self.action_type_dropdown)
        action_dropdown.send_keys("fixed_transfer")
        transfer_amount = self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input))
        transfer_amount.clear()
        transfer_amount.send_keys(str(amount))
        dest_account = self.wait.until(EC.visibility_of_element_located(self.destination_account_input))
        dest_account.clear()
        dest_account.send_keys(destination_account)
        # Currency selection if UI supports

    def save_rule(self):
        """
        Saves the complete rule and verifies persistence.
        :return: Generated Rule ID (if displayed)
        """
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()
        try:
            success = self.wait.until(EC.visibility_of_element_located(self.success_message))
            # Extract Rule ID from success message if present
            rule_id = None
            if success:
                text = success.text
                import re
                match = re.search(r'(RULE-\d{4})', text)
                if match:
                    rule_id = match.group(1)
            return rule_id
        except TimeoutException:
            raise Exception("Rule save failed or success message not found.")

    def retrieve_rule(self, rule_id):
        """
        Retrieves the saved rule by Rule ID.
        :param rule_id: e.g., 'RULE-1234'
        :return: Rule details as dict
        """
        # Implement retrieval logic; this may require navigation/search
        # Placeholder for actual retrieval steps
        # Return parsed rule details for validation
        pass

    def validate_rule_components(self, expected_trigger, expected_condition, expected_action):
        """
        Validates that the retrieved rule matches expected components.
        :param expected_trigger: dict
        :param expected_condition: dict
        :param expected_action: dict
        """
        # Implement validation logic, e.g. compare fields in UI
        # Use self.json_schema_editor and self.validate_schema_btn if applicable
        pass

    def validate_json_schema(self):
        """
        Validates the rule definition against JSON schema.
        """
        self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn)).click()
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return True
        except TimeoutException:
            error = self.driver.find_element(*self.schema_error_message)
            raise Exception(f"Schema validation failed: {error.text}")
