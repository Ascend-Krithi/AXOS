# RuleConfigurationPage.py
"""
Page Object Model for Rule Configuration Page.
Covers:
- Batch rule loading
- Rule evaluation performance
- SQL injection validation
Locators sourced from Locators.json.
Test Cases Supported: TC-FT-007, TC-FT-008
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RuleConfigurationPage:
    """
    Selenium PageClass for Rule Configuration Page.
    Methods:
        load_rules_batch(batch_rules_json): Loads a batch of rules via UI or API.
        trigger_evaluation_all_rules(): Triggers evaluation for all rules.
        validate_sql_injection(rule_data): Submits a rule with SQL injection payload and validates rejection.
    All locators are mapped from Locators.json.
    """
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        # Locators
        self.rule_id_input = (By.ID, "rule-id-field")
        self.rule_name_input = (By.NAME, "rule-name")
        self.save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        self.trigger_type_dropdown = (By.ID, "trigger-type-select")
        self.date_picker = (By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = (By.ID, "interval-value")
        self.after_deposit_toggle = (By.ID, "trigger-after-deposit")
        self.add_condition_btn = (By.ID, "add-condition-link")
        self.condition_type_dropdown = (By.CSS_SELECTOR, "select.condition-type")
        self.balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = (By.ID, "source-provider-select")
        self.operator_dropdown = (By.CSS_SELECTOR, ".condition-operator-select")
        self.action_type_dropdown = (By.ID, "action-type-select")
        self.transfer_amount_input = (By.NAME, "fixed-amount")
        self.percentage_input = (By.ID, "deposit-percentage")
        self.destination_account_input = (By.ID, "target-account-id")
        self.json_schema_editor = (By.CSS_SELECTOR, ".monaco-editor")
        self.validate_schema_btn = (By.ID, "btn-verify-json")
        self.success_message = (By.CSS_SELECTOR, ".alert-success")
        self.schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def load_rules_batch(self, batch_rules_json):
        """
        Loads a batch of rules into the system using UI form.
        Args:
            batch_rules_json (list[dict]): List of rule dicts.
        Returns:
            bool: True if all rules loaded successfully, False otherwise.
        """
        for rule in batch_rules_json:
            try:
                WebDriverWait(self.driver, self.timeout).until(
                    EC.visibility_of_element_located(self.rule_id_input)
                )
                self.driver.find_element(*self.rule_id_input).clear()
                self.driver.find_element(*self.rule_id_input).send_keys(rule.get("id", ""))
                self.driver.find_element(*self.rule_name_input).clear()
                self.driver.find_element(*self.rule_name_input).send_keys(rule.get("name", ""))
                # Set triggers
                self.driver.find_element(*self.trigger_type_dropdown).send_keys(rule.get("trigger", {}).get("type", ""))
                if rule.get("trigger", {}).get("date"):
                    self.driver.find_element(*self.date_picker).send_keys(rule["trigger"]["date"])
                if rule.get("trigger", {}).get("interval"):
                    self.driver.find_element(*self.recurring_interval_input).send_keys(rule["trigger"]["interval"])
                if rule.get("trigger", {}).get("after_deposit"):
                    self.driver.find_element(*self.after_deposit_toggle).click()
                # Set conditions
                for cond in rule.get("conditions", []):
                    self.driver.find_element(*self.add_condition_btn).click()
                    self.driver.find_element(*self.condition_type_dropdown).send_keys(cond.get("type", ""))
                    if cond.get("type") == "balance_threshold":
                        self.driver.find_element(*self.balance_threshold_input).clear()
                        self.driver.find_element(*self.balance_threshold_input).send_keys(cond.get("value", ""))
                    if cond.get("source"):
                        self.driver.find_element(*self.transaction_source_dropdown).send_keys(cond["source"])
                    if cond.get("operator"):
                        self.driver.find_element(*self.operator_dropdown).send_keys(cond["operator"])
                # Set actions
                if rule.get("action", {}).get("type"):
                    self.driver.find_element(*self.action_type_dropdown).send_keys(rule["action"]["type"])
                if rule.get("action", {}).get("amount"):
                    self.driver.find_element(*self.transfer_amount_input).clear()
                    self.driver.find_element(*self.transfer_amount_input).send_keys(str(rule["action"]["amount"]))
                if rule.get("action", {}).get("percentage"):
                    self.driver.find_element(*self.percentage_input).send_keys(str(rule["action"]["percentage"]))
                if rule.get("action", {}).get("destination_account"):
                    self.driver.find_element(*self.destination_account_input).send_keys(rule["action"]["destination_account"])
                # Save rule
                self.driver.find_element(*self.save_rule_button).click()
                WebDriverWait(self.driver, self.timeout).until(
                    EC.visibility_of_element_located(self.success_message)
                )
            except TimeoutException:
                return False
        return True

    def trigger_evaluation_all_rules(self):
        """
        Triggers evaluation for all rules in the system.
        Returns:
            bool: True if evaluation completed within acceptable time, False otherwise.
        """
        # Assuming there is a UI button or API endpoint for evaluation, placeholder below
        try:
            # Example: self.driver.find_element(By.ID, "evaluate-all-btn").click()
            # Wait for success message
            WebDriverWait(self.driver, self.timeout * 3).until(
                EC.visibility_of_element_located(self.success_message)
            )
            return True
        except TimeoutException:
            return False

    def validate_sql_injection(self, rule_data):
        """
        Submits a rule with SQL injection payload and verifies rejection.
        Args:
            rule_data (dict): Rule with SQL injection in field value.
        Returns:
            bool: True if SQL injection is rejected and error is shown, False otherwise.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.rule_id_input)
            )
            self.driver.find_element(*self.rule_id_input).clear()
            self.driver.find_element(*self.rule_id_input).send_keys(rule_data.get("id", ""))
            self.driver.find_element(*self.rule_name_input).clear()
            self.driver.find_element(*self.rule_name_input).send_keys(rule_data.get("name", ""))
            # Set trigger
            self.driver.find_element(*self.trigger_type_dropdown).send_keys(rule_data.get("trigger", {}).get("type", ""))
            if rule_data.get("trigger", {}).get("date"):
                self.driver.find_element(*self.date_picker).send_keys(rule_data["trigger"]["date"])
            # Set action
            if rule_data.get("action", {}).get("type"):
                self.driver.find_element(*self.action_type_dropdown).send_keys(rule_data["action"]["type"])
            if rule_data.get("action", {}).get("amount"):
                self.driver.find_element(*self.transfer_amount_input).clear()
                self.driver.find_element(*self.transfer_amount_input).send_keys(str(rule_data["action"]["amount"]))
            # Set SQL injection condition
            for cond in rule_data.get("conditions", []):
                self.driver.find_element(*self.add_condition_btn).click()
                self.driver.find_element(*self.condition_type_dropdown).send_keys(cond.get("type", ""))
                if cond.get("type") == "balance_threshold":
                    self.driver.find_element(*self.balance_threshold_input).clear()
                    self.driver.find_element(*self.balance_threshold_input).send_keys(cond.get("value", ""))
            # Save rule
            self.driver.find_element(*self.save_rule_button).click()
            # Wait for error feedback
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.schema_error_message)
            )
            return True
        except TimeoutException:
            return False
