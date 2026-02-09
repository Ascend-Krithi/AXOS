# RuleDefinitionPage.py

from selenium.webdriver.common.by import By

class RuleDefinitionPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators (stubbed, must be updated)
        self.rule_form = (By.ID, 'rule-form')
        self.trigger_type_field = (By.ID, 'trigger-type')
        self.action_type_field = (By.ID, 'action-type')
        self.amount_field = (By.ID, 'amount')
        self.conditions_field = (By.ID, 'conditions')
        self.submit_button = (By.ID, 'submit-rule')
        self.error_message = (By.CSS_SELECTOR, 'div.error-message')
        self.accepted_message = (By.CSS_SELECTOR, 'div.success-message')

    def navigate_to_rule_definition(self):
        self.driver.get("https://example-ecommerce.com/rule-definition")

    def define_rule(self, trigger, action, conditions):
        # Fill in trigger, action, and conditions fields
        pass  # Implementation depends on locators

    def submit_rule(self):
        self.driver.find_element(*self.submit_button).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_message).text

    def is_rule_accepted(self):
        return self.driver.find_element(*self.accepted_message).is_displayed()
