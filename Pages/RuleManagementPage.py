from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import json
import time

class RuleManagementPage:
    # Placeholder locators; update as per actual UI
    DEFINE_RULE_BUTTON = (By.ID, "define-rule-btn")
    RULE_TYPE_DROPDOWN = (By.ID, "rule-type-dropdown")
    RULE_TRIGGER_DROPDOWN = (By.ID, "rule-trigger-dropdown")
    DEPOSIT_AMOUNT_INPUT = (By.ID, "deposit-amount-input")
    PERCENTAGE_INPUT = (By.ID, "percentage-input")
    FIXED_AMOUNT_INPUT = (By.ID, "fixed-amount-input")
    CURRENCY_DROPDOWN = (By.ID, "currency-dropdown")
    ACCEPT_RULE_BUTTON = (By.ID, "accept-rule-btn")
    RULE_ACCEPTED_MESSAGE = (By.CSS_SELECTOR, "div.rule-accepted")
    RULE_REJECTED_MESSAGE = (By.CSS_SELECTOR, "div.rule-rejected")
    EXECUTE_DEPOSIT_BUTTON = (By.ID, "execute-deposit-btn")
    TRANSFER_EXECUTED_MESSAGE = (By.CSS_SELECTOR, "div.transfer-executed")
    EXISTING_RULES_LIST = (By.ID, "existing-rules-list")
    UPLOAD_RULES_BUTTON = (By.ID, "upload-rules-btn")  # Placeholder
    EVALUATE_ALL_RULES_BUTTON = (By.ID, "evaluate-all-rules-btn")  # Placeholder
    SQL_INJECTION_REJECTION_MESSAGE = (By.CSS_SELECTOR, "div.sql-injection-rejected")  # Placeholder

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def define_rule(self, rule_type: str, trigger_type: str, **kwargs):
        self.driver.find_element(*self.DEFINE_RULE_BUTTON).click()
        self.driver.find_element(*self.RULE_TYPE_DROPDOWN).send_keys(rule_type)
        self.driver.find_element(*self.RULE_TRIGGER_DROPDOWN).send_keys(trigger_type)
        if 'percentage' in kwargs:
            self.driver.find_element(*self.PERCENTAGE_INPUT).clear()
            self.driver.find_element(*self.PERCENTAGE_INPUT).send_keys(str(kwargs['percentage']))
        if 'amount' in kwargs:
            self.driver.find_element(*self.FIXED_AMOUNT_INPUT).clear()
            self.driver.find_element(*self.FIXED_AMOUNT_INPUT).send_keys(str(kwargs['amount']))
        if 'currency' in kwargs:
            self.driver.find_element(*self.CURRENCY_DROPDOWN).send_keys(kwargs['currency'])
        self.driver.find_element(*self.ACCEPT_RULE_BUTTON).click()

    def get_rule_acceptance_message(self):
        try:
            return self.driver.find_element(*self.RULE_ACCEPTED_MESSAGE).text
        except Exception:
            return self.driver.find_element(*self.RULE_REJECTED_MESSAGE).text

    def simulate_deposit(self, amount: int):
        self.driver.find_element(*self.DEPOSIT_AMOUNT_INPUT).clear()
        self.driver.find_element(*self.DEPOSIT_AMOUNT_INPUT).send_keys(str(amount))
        self.driver.find_element(*self.EXECUTE_DEPOSIT_BUTTON).click()

    def get_transfer_executed_message(self):
        return self.driver.find_element(*self.TRANSFER_EXECUTED_MESSAGE).text

    def verify_existing_rules(self):
        return self.driver.find_element(*self.EXISTING_RULES_LIST).text

    # --- New Methods for TC-FT-007 and TC-FT-008 ---
    def upload_rules_batch(self, batch_json_path: str):
        """
        Uploads a batch of rules from a JSON file.
        Args:
            batch_json_path (str): Path to JSON file containing rules.
        """
        self.driver.find_element(*self.UPLOAD_RULES_BUTTON).click()
        upload_input = self.driver.find_element(By.ID, "rules-upload-input")  # Placeholder
        upload_input.send_keys(batch_json_path)
        self.driver.find_element(*self.ACCEPT_RULE_BUTTON).click()
        # Wait for upload to complete
        time.sleep(5)  # Adjust as per system response

    def evaluate_all_rules(self):
        """
        Triggers evaluation for all rules simultaneously.
        """
        self.driver.find_element(*self.EVALUATE_ALL_RULES_BUTTON).click()
        # Wait for evaluation to complete
        time.sleep(10)  # Adjust as per system response

    def submit_rule_with_sql_injection(self, rule_data: dict):
        """
        Submits a rule with SQL injection payload.
        Args:
            rule_data (dict): Rule data with SQL injection in field value.
        """
        self.driver.find_element(*self.DEFINE_RULE_BUTTON).click()
        # Example for filling fields; update as per actual UI
        self.driver.find_element(*self.RULE_TYPE_DROPDOWN).send_keys(rule_data.get('type', ''))
        self.driver.find_element(*self.RULE_TRIGGER_DROPDOWN).send_keys(rule_data.get('trigger', {}).get('type', ''))
        self.driver.find_element(*self.FIXED_AMOUNT_INPUT).clear()
        self.driver.find_element(*self.FIXED_AMOUNT_INPUT).send_keys(str(rule_data.get('action', {}).get('amount', '')))
        # SQL injection field
        self.driver.find_element(By.ID, "balance-threshold-input").clear()
        self.driver.find_element(By.ID, "balance-threshold-input").send_keys(rule_data.get('conditions', [{}])[0].get('value', ''))
        self.driver.find_element(*self.ACCEPT_RULE_BUTTON).click()

    def get_sql_injection_rejection_message(self):
        """
        Returns the SQL injection rejection message.
        """
        try:
            return self.driver.find_element(*self.SQL_INJECTION_REJECTION_MESSAGE).text
        except Exception:
            return self.driver.find_element(*self.RULE_REJECTED_MESSAGE).text
