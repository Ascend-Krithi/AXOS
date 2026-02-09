# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Locators loaded from Locators.json (assumed structure)
        self.locators = {
            'ruleForm': {'by': By.ID, 'value': 'ruleForm'},
            'triggers': {'by': By.CSS_SELECTOR, 'value': '[data-testid="triggers-section"]'},
            'conditions': {'by': By.CSS_SELECTOR, 'value': '[data-testid="conditions-section"]'},
            'actions': {'by': By.CSS_SELECTOR, 'value': '[data-testid="actions-section"]'},
            'validation': {'by': By.CSS_SELECTOR, 'value': '[data-testid="validation-message"]'}
        }

    def open_rule_form(self):
        return self.wait.until(EC.visibility_of_element_located((self.locators['ruleForm']['by'], self.locators['ruleForm']['value'])))

    def set_trigger(self, trigger_name, params=None):
        triggers_section = self.wait.until(EC.visibility_of_element_located((self.locators['triggers']['by'], self.locators['triggers']['value'])))
        # Example: select trigger by name
        trigger_input = triggers_section.find_element(By.XPATH, f".//input[@name='triggerName']")
        trigger_input.clear()
        trigger_input.send_keys(trigger_name)
        if params:
            for key, value in params.items():
                param_input = triggers_section.find_element(By.XPATH, f".//input[@name='{key}']")
                param_input.clear()
                param_input.send_keys(value)

    def set_condition(self, condition_name, params=None):
        conditions_section = self.wait.until(EC.visibility_of_element_located((self.locators['conditions']['by'], self.locators['conditions']['value'])))
        condition_input = conditions_section.find_element(By.XPATH, f".//input[@name='conditionName']")
        condition_input.clear()
        condition_input.send_keys(condition_name)
        if params:
            for key, value in params.items():
                param_input = conditions_section.find_element(By.XPATH, f".//input[@name='{key}']")
                param_input.clear()
                param_input.send_keys(value)

    def set_action(self, action_name, params=None):
        actions_section = self.wait.until(EC.visibility_of_element_located((self.locators['actions']['by'], self.locators['actions']['value'])))
        action_input = actions_section.find_element(By.XPATH, f".//input[@name='actionName']")
        action_input.clear()
        action_input.send_keys(action_name)
        if params:
            for key, value in params.items():
                param_input = actions_section.find_element(By.XPATH, f".//input[@name='{key}']")
                param_input.clear()
                param_input.send_keys(value)

    def submit_rule(self):
        rule_form = self.open_rule_form()
        submit_button = rule_form.find_element(By.XPATH, ".//button[@type='submit']")
        submit_button.click()

    def get_validation_message(self):
        validation_elem = self.wait.until(EC.visibility_of_element_located((self.locators['validation']['by'], self.locators['validation']['value'])))
        return validation_elem.text

    def validate_rule_creation(self, expected_message):
        actual_message = self.get_validation_message()
        assert actual_message == expected_message, f"Expected validation message '{expected_message}', got '{actual_message}'"
