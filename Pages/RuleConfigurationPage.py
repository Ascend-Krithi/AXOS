# RuleConfigurationPage.py
"""
Selenium PageClass for Automated Transfers Rule Configuration Page.
Covers rule form, triggers, conditions, actions, and validation logic.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import subprocess

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
        self.add_condition_btn.click()
        self.condition_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'transaction_source')]")
        option.click()
        self.transaction_source_dropdown.click()
        source_option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{source_provider}')]")
        source_option.click()

    def add_fixed_transfer_action(self, amount: float, destination_account: str):
        """Add fixed amount transfer action."""
        self.action_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'fixed_amount')]")
        option.click()
        self.transfer_amount_input.clear()
        self.transfer_amount_input.send_keys(str(amount))
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(destination_account)

    def add_percentage_transfer_action(self, percentage: float, destination_account: str):
        """Add percentage transfer action."""
        self.action_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'percentage')]")
        option.click()
        self.percentage_input.clear()
        self.percentage_input.send_keys(str(percentage))
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(destination_account)

    def enter_json_schema(self, schema: str):
        """Enter JSON schema in the editor."""
        self.json_schema_editor.clear()
        self.json_schema_editor.send_keys(schema)

    def validate_json_schema(self):
        """Click validate schema button and check for success/error messages."""
        self.validate_schema_btn.click()
        try:
            self.wait.until(EC.visibility_of(self.success_message))
            return True
        except Exception:
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

    def simulate_deposit(self, source: str, amount: float):
        """
        Simulate deposit for trigger validation (for test automation only).
        Args:
            source (str): Deposit source (e.g., 'Employer Y')
            amount (float): Deposit amount
        """
        # This is a stub for test automation; implementation depends on test environment.
        pass

    def get_rule_id(self):
        """Retrieve generated rule ID after creation."""
        return self.rule_id_input.get_attribute('value')

    def is_success_message_displayed(self):
        """Check if success message is displayed."""
        return self.success_message.is_displayed()

    # --- New Methods for Security and DB Integrity Testing ---
    def inject_sql_payload_and_create_rule(self, trigger_type: str, condition_type: str, source: str, action_type: str, amount: float):
        """
        Injects a malicious SQL payload in the transaction_source field and attempts rule creation.
        Args:
            trigger_type (str)
            condition_type (str)
            source (str): SQL injection string
            action_type (str)
            amount (float)
        Returns:
            bool: True if rule creation proceeds, False otherwise.
        """
        self.select_trigger_type(trigger_type)
        self.add_transaction_source_condition(source)
        if action_type == 'fixed_amount':
            self.add_fixed_transfer_action(amount, 'test-account')
        self.save_rule_button.click()
        try:
            self.wait.until(EC.visibility_of(self.success_message))
            return True
        except Exception:
            return False

    def verify_security_log_for_injection_attempt(self, log_path: str = '/var/log/security/injection_attempts.log'):
        """
        Verifies that a security event is logged for SQL injection attempt.
        Args:
            log_path (str): Path to security log.
        Returns:
            str: Log entry if found, else None.
        """
        if not os.path.exists(log_path):
            return None
        with open(log_path, 'r') as log_file:
            for line in log_file:
                if 'SQL injection' in line:
                    return line.strip()
        return None

    def check_database_integrity(self, db_cmd: str = "psql -c \"SELECT * FROM information_schema.tables WHERE table_name='rules';\""):
        """
        Checks database integrity by confirming the rules table exists.
        Args:
            db_cmd (str): Command to check rules table in PostgreSQL.
        Returns:
            bool: True if table exists, False otherwise.
        """
        try:
            result = subprocess.run(db_cmd, shell=True, capture_output=True, text=True)
            return 'rules' in result.stdout
        except Exception:
            return False

    def verify_rule_in_postgres(self, rule_filter: str):
        """
        Verifies rule existence in PostgreSQL database.
        Args:
            rule_filter (str): SQL WHERE clause string.
        Returns:
            bool: True if rule exists, False otherwise.
        """
        db_cmd = f"psql -c \"SELECT * FROM rules WHERE {rule_filter};\""
        try:
            result = subprocess.run(db_cmd, shell=True, capture_output=True, text=True)
            return 'after_deposit' in result.stdout
        except Exception:
            return False

    def verify_rule_evaluation_service_log(self, log_path: str = 'rule_evaluation_service.log'):
        """
        Verifies that rule evaluation service processed the rule.
        Args:
            log_path (str): Path to rule evaluation log.
        Returns:
            str: Log entry if found, else None.
        """
        if not os.path.exists(log_path):
            return None
        with open(log_path, 'r') as log_file:
            for line in log_file:
                if 'Rule evaluated' in line:
                    return line.strip()
        return None

    def verify_account_balance(self, expected_balance: float):
        """
        Verifies account balance after rule execution (stub, to be implemented in test environment).
        Args:
            expected_balance (float)
        Returns:
            bool: True if balance matches, False otherwise.
        """
        # Implementation depends on test environment, e.g., API call or DB query
        pass
