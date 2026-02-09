from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time

class RuleEnginePage:
    """
    PageClass for rule definition and deposit simulation actions.
    Locators are placeholders and must be updated when UI details are available.
    Supports:
      - Percentage of deposit rules
      - Fixed amount rules
      - Currency conversion rules (future/new type)
      - Batch loading and evaluation of rules (TC-FT-007)
    """
    # Locators (Placeholder - update when UI details available)
    DEFINE_RULE_BUTTON = (By.ID, "define-rule-btn")
    RULE_TYPE_DROPDOWN = (By.ID, "rule-type-dropdown")
    PERCENTAGE_INPUT = (By.ID, "percentage-input")
    FIXED_AMOUNT_INPUT = (By.ID, "fixed-amount-input")
    CURRENCY_DROPDOWN = (By.ID, "currency-dropdown")
    ACCEPT_RULE_BUTTON = (By.ID, "accept-rule-btn")
    DEPOSIT_INPUT = (By.ID, "deposit-input")
    SIMULATE_DEPOSIT_BUTTON = (By.ID, "simulate-deposit-btn")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.success-message")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.error-message")
    EXISTING_RULES_LIST = (By.ID, "existing-rules-list")
    BATCH_UPLOAD_INPUT = (By.ID, "batch-upload-input")  # Placeholder for batch upload
    BATCH_UPLOAD_BUTTON = (By.ID, "batch-upload-btn")  # Placeholder for batch upload trigger
    EVALUATE_ALL_BUTTON = (By.ID, "evaluate-all-btn")  # Placeholder for simultaneous evaluation

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self, url: str):
        """Navigate to Rule Engine page."""
        self.driver.get(url)

    def define_rule(self, rule_data: dict):
        """
        Define a rule based on rule_data.
        Example:
        {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        Supports new types: currency_conversion, fixed_amount
        """
        self.driver.find_element(*self.DEFINE_RULE_BUTTON).click()
        rule_type = rule_data.get("trigger", {}).get("type", "")
        self.driver.find_element(*self.RULE_TYPE_DROPDOWN).send_keys(rule_type)
        action = rule_data.get("action", {})
        if action.get("type") == "percentage_of_deposit":
            self.driver.find_element(*self.PERCENTAGE_INPUT).clear()
            self.driver.find_element(*self.PERCENTAGE_INPUT).send_keys(str(action.get("percentage", "")))
        elif action.get("type") == "fixed_amount":
            self.driver.find_element(*self.FIXED_AMOUNT_INPUT).clear()
            self.driver.find_element(*self.FIXED_AMOUNT_INPUT).send_keys(str(action.get("amount", "")))
        if rule_type == "currency_conversion":
            self.driver.find_element(*self.CURRENCY_DROPDOWN).send_keys(rule_data.get("trigger", {}).get("currency", ""))
        self.driver.find_element(*self.ACCEPT_RULE_BUTTON).click()

    def simulate_deposit(self, amount: int):
        """Simulate deposit action."""
        self.driver.find_element(*self.DEPOSIT_INPUT).clear()
        self.driver.find_element(*self.DEPOSIT_INPUT).send_keys(str(amount))
        self.driver.find_element(*self.SIMULATE_DEPOSIT_BUTTON).click()

    def get_success_message(self):
        """Return success message text."""
        return self.driver.find_element(*self.SUCCESS_MESSAGE).text

    def get_error_message(self):
        """Return error message text."""
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def list_existing_rules(self):
        """Return list of existing rules."""
        rules = self.driver.find_elements(*self.EXISTING_RULES_LIST)
        return [rule.text for rule in rules]

    # --- TC-FT-007 Batch Loading and Evaluation ---
    def batch_load_rules(self, rules: list):
        """
        Batch load 10,000 rules into the system.
        Args:
            rules (list): List of rule dicts to upload.
        Returns:
            bool: True if upload is successful, False otherwise.
        """
        import json
        # Convert rules to JSON
        rules_json = json.dumps(rules)
        # Find batch upload input
        upload_input = self.driver.find_element(*self.BATCH_UPLOAD_INPUT)
        upload_input.clear()
        upload_input.send_keys(rules_json)
        # Click upload button
        self.driver.find_element(*self.BATCH_UPLOAD_BUTTON).click()
        # Wait for success message
        try:
            time.sleep(2)  # Adjust as needed
            msg = self.get_success_message()
            return "successfully uploaded" in msg.lower()
        except Exception:
            return False

    def evaluate_all_rules(self):
        """
        Trigger evaluation for all rules simultaneously.
        Returns:
            bool: True if evaluation completes within threshold, False otherwise.
        """
        self.driver.find_element(*self.EVALUATE_ALL_BUTTON).click()
        # Wait for completion indicator (success message or similar)
        try:
            start_time = time.time()
            while True:
                msg = self.get_success_message()
                if "evaluation complete" in msg.lower():
                    elapsed = time.time() - start_time
                    # Acceptable threshold: 60 seconds (example)
                    return elapsed < 60
                time.sleep(1)
        except Exception:
            return False
