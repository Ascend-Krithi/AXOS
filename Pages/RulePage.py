from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class RulePage:
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
        self.rule_definition_button.click()
        self.rule_type_dropdown.send_keys("percentage_of_deposit")
        self.percentage_input.clear()
        self.percentage_input.send_keys(str(percentage))
        self.submit_button.click()

    def define_currency_conversion_rule(self, currency: str, amount: int):
        self.rule_definition_button.click()
        self.rule_type_dropdown.send_keys("currency_conversion")
        self.currency_dropdown.send_keys(currency)
        self.amount_input.clear()
        self.amount_input.send_keys(str(amount))
        self.submit_button.click()

    def get_acceptance_message(self):
        return self.acceptance_message.text

    def get_error_message(self):
        return self.error_message.text
