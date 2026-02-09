# RuleManagementPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleManagementPage:
    """
    Page Object Model for Rule Management actions:
    - Create and store rules (TC-FT-009)
    - Define rules with empty conditions (TC-FT-010)
    - Trigger rules and validate backend persistence
    """

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Locators (strictly validated from RuleConfigurationPage)
    CREATE_RULE_BUTTON = (By.ID, 'create-rule-btn')
    TRIGGER_TYPE_DROPDOWN = (By.ID, 'trigger-type-select')
    TRIGGER_DATE_INPUT = (By.CSS_SELECTOR, "input[type='date']")
    ACTION_TYPE_DROPDOWN = (By.ID, 'action-type-select')
    ACTION_AMOUNT_INPUT = (By.NAME, 'fixed-amount')
    CONDITIONS_ARRAY_INPUT = (By.ID, 'add-condition-link')
    SUBMIT_RULE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
    RULE_LIST = (By.ID, 'rule-list')
    TRIGGER_RULE_BUTTON = (By.ID, 'trigger-after-deposit')

    def create_rule(self, trigger_type, trigger_date, action_type, action_amount, conditions):
        self.wait.until(EC.element_to_be_clickable(self.CREATE_RULE_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.TRIGGER_TYPE_DROPDOWN)).send_keys(trigger_type)
        if trigger_date:
            self.wait.until(EC.visibility_of_element_located(self.TRIGGER_DATE_INPUT)).send_keys(trigger_date)
        self.wait.until(EC.visibility_of_element_located(self.ACTION_TYPE_DROPDOWN)).send_keys(action_type)
        self.wait.until(EC.visibility_of_element_located(self.ACTION_AMOUNT_INPUT)).send_keys(str(action_amount))
        if conditions:
            self.wait.until(EC.element_to_be_clickable(self.CONDITIONS_ARRAY_INPUT)).click()
            for condition in conditions:
                pass
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_RULE_BUTTON)).click()

    def retrieve_rule(self, rule_id):
        rule_elements = self.driver.find_elements(*self.RULE_LIST)
        for rule in rule_elements:
            if rule_id in rule.text:
                return rule.text
        return None

    def define_rule_with_empty_conditions(self, trigger_type, action_type, action_amount):
        self.create_rule(trigger_type, None, action_type, action_amount, [])

    def trigger_rule(self, rule_id):
        self.wait.until(EC.element_to_be_clickable(self.TRIGGER_RULE_BUTTON)).click()

    # TC_SCRUM158_07 function
    def verify_rule_creation(self, rule_name):
        """
        Verifies that the rule was created successfully.
        """
        rule_list = self.wait.until(EC.visibility_of_element_located(self.RULE_LIST))
        rules = rule_list.find_elements(By.CSS_SELECTOR, ".rule-name")
        for rule in rules:
            if rule.text.strip() == rule_name:
                return True
        return False
