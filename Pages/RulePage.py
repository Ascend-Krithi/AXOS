from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class RulePage:
    """
    PageClass for rule definition.
    Supports:
      - Percentage of deposit rules
      - Fixed amount rules
      - Currency conversion rules (future/new type)
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
