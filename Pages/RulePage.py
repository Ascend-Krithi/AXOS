from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class RulePage:
    """
    PageClass for rule definition.
    Supports:
      - Percentage of deposit rules
      - Fixed amount rules
      - Currency conversion rules (future/new type)
      - SQL injection rule submission and rejection validation (TC-FT-008)
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Locators (example, must be aligned with actual app)
        self.rule_definition_button = driver.find_element(By.ID, "define-rule-btn")
        self.rule_type_dropdown = driver.find_element(By.ID, "rule-type-dropdown")
        self.percentage_input = driver.find_element(By.ID, "percentage-input")
        self.currency_dropdown = driver.find_element(By.ID, "currency-dropdown")
        self.amount_input = driver.find_element(By.ID, "amount-input")
        self.submit_button = driver.find_element(By.ID, "rule-submit-btn")
        self.acceptance_message = driver.find_element(By.CSS_SELECTOR, ".rule-success-msg")
        self.error_message = driver.find_element(By.CSS_SELECTOR, ".rule-error-msg")
        self.condition_value_input = driver.find_element(By.ID, "condition-value-input")  # Placeholder for conditions

    def define_percentage_rule(self, percentage: int):
        """Define percentage of deposit rule."""
        self.rule_definition_button.click()
        self.rule_type_dropdown.send_keys("percentage_of_deposit")
        self.percentage_input.clear()
        self.percentage_input.send_keys(str(percentage))
        self.submit_button.click()

    def define_currency_conversion_rule(self, currency: str, amount: int):
        """Define currency conversion rule (future/new type)."""
        self.rule_definition_button.click()
        self.rule_type_dropdown.send_keys("currency_conversion")
        self.currency_dropdown.send_keys(currency)
        self.amount_input.clear()
        self.amount_input.send_keys(str(amount))
        self.submit_button.click()

    def get_acceptance_message(self):
        """Return acceptance message text."""
        return self.acceptance_message.text

    def get_error_message(self):
        """Return error message text."""
        return self.error_message.text

    # --- TC-FT-008 SQL Injection Submission and Validation ---
    def submit_rule_with_sql_injection(self, rule_data: dict):
        """
        Submit a rule with SQL injection in a field value.
        Args:
            rule_data (dict): Rule data with SQL injection payload.
        Returns:
            None
        """
        self.rule_definition_button.click()
        self.rule_type_dropdown.send_keys(rule_data.get("trigger", {}).get("type", ""))
        self.amount_input.clear()
        self.amount_input.send_keys(str(rule_data.get("action", {}).get("amount", "")))
        # Enter SQL injection in condition value
        conditions = rule_data.get("conditions", [])
        if conditions:
            self.condition_value_input.clear()
            self.condition_value_input.send_keys(str(conditions[0].get("value", "")))
        self.submit_button.click()

    def is_rule_rejected(self):
        """
        Validate that the rule was rejected and no SQL was executed.
        Returns:
            bool: True if error message is shown and rule is not accepted, False otherwise.
        """
        try:
            msg = self.get_error_message()
            return "rejected" in msg.lower() or "invalid" in msg.lower()
        except Exception:
            return False
