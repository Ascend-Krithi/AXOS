# RuleConfigurationPage.py
"""
Selenium PageClass for Automated Transfers Rule Configuration Page.
Covers rule form, triggers, conditions, actions, and validation logic per Locators.json.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object Model for Automated Transfers Rule Configuration.
    Provides methods for rule creation, trigger setup, condition addition, action configuration, and validation.
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Rule Form
        self.rule_id_input = driver.find_element(By.ID, 'rule-id-field')
        self.rule_name_input = driver.find_element(By.NAME, 'rule-name')
        self.save_rule_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Triggers
        self.trigger_type_dropdown = driver.find_element(By.ID, 'trigger-type-select')
        self.date_picker = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = driver.find_element(By.ID, 'interval-value')
        self.after_deposit_toggle = driver.find_element(By.ID, 'trigger-after-deposit')
        # Conditions
        self.add_condition_btn = driver.find_element(By.ID, 'add-condition-link')
        self.condition_type_dropdown = driver.find_element(By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = driver.find_element(By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = driver.find_element(By.ID, 'source-provider-select')
        self.operator_dropdown = driver.find_element(By.CSS_SELECTOR, '.condition-operator-select')
        # Actions
        self.action_type_dropdown = driver.find_element(By.ID, 'action-type-select')
        self.transfer_amount_input = driver.find_element(By.NAME, 'fixed-amount')
        self.percentage_input = driver.find_element(By.ID, 'deposit-percentage')
        self.destination_account_input = driver.find_element(By.ID, 'target-account-id')
        # Validation
        self.json_schema_editor = driver.find_element(By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = driver.find_element(By.ID, 'btn-verify-json')
        self.success_message = driver.find_element(By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = driver.find_element(By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    def enter_rule_details(self, rule_id: str, rule_name: str):
        """Enter Rule ID and Name."""
        self.rule_id_input.clear()
        self.rule_id_input.send_keys(rule_id)
        self.rule_name_input.clear()
        self.rule_name_input.send_keys(rule_name)

    def select_trigger_type(self, trigger_type: str):
        """Select trigger type from dropdown."""
        self.trigger_type_dropdown.click()
        # Assume dropdown options are visible and selectable by text
        option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{trigger_type}')]")
        option.click()

    def set_specific_date_trigger(self, date_str: str):
        """Set specific date trigger value."""
        self.date_picker.clear()
        self.date_picker.send_keys(date_str)

    def set_recurring_interval(self, interval_value: str):
        """Set recurring interval value."""
        self.recurring_interval_input.clear()
        self.recurring_interval_input.send_keys(interval_value)

    def toggle_after_deposit(self, enable: bool):
        """Enable or disable 'after deposit' trigger."""
        if self.after_deposit_toggle.is_selected() != enable:
            self.after_deposit_toggle.click()

    def add_balance_threshold_condition(self, operator: str, amount: float):
        """Add balance threshold condition."""
        self.add_condition_btn.click()
        self.condition_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'balance_threshold')]")
        option.click()
        self.balance_threshold_input.clear()
        self.balance_threshold_input.send_keys(str(amount))
        self.operator_dropdown.click()
        operator_option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{operator}')]")
        operator_option.click()

    def add_transaction_source_condition(self, source_provider: str):
        """Add transaction source condition."""
        self.transaction_source_dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{source_provider}')]")
        option.click()

    def add_fixed_transfer_action(self, amount: float, destination_account: str):
        """Add fixed amount transfer action."""
        self.action_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'fixed_transfer')]")
        option.click()
        self.transfer_amount_input.clear()
        self.transfer_amount_input.send_keys(str(amount))
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(destination_account)

    def add_percentage_transfer_action(self, percentage: float, destination_account: str):
        """Add percentage transfer action."""
        self.action_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'percentage_transfer')]")
        option.click()
        self.percentage_input.clear()
        self.percentage_input.send_keys(str(percentage))
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(destination_account)

    def validate_json_schema(self):
        """Click validate schema button and check for success/error messages."""
        self.validate_schema_btn.click()
        try:
            self.wait.until(EC.visibility_of(self.success_message))
            return True
        except:
            return False

    def get_schema_error_message(self):
        """Return schema error message if present."""
        if self.schema_error_message.is_displayed():
            return self.schema_error_message.text
        return None

    def save_rule(self):
        """Click save rule button."""
        self.save_rule_button.click()
        self.wait.until(EC.visibility_of(self.success_message))
        return self.success_message.text
