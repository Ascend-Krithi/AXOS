# RuleManagementPage.py
# Selenium PageClass for Rule Management functionality
# Updated for TC-FT-009 and TC-FT-010 with strict locator usage

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
        """
        Creates and stores a rule.
        Args:
            trigger_type (str): Type of trigger.
            trigger_date (str): Date string (ISO format) or None.
            action_type (str): Action type.
            action_amount (int): Amount value.
            conditions (list): Conditions array.
        """
        self.wait.until(EC.element_to_be_clickable(self.CREATE_RULE_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.TRIGGER_TYPE_DROPDOWN)).send_keys(trigger_type)
        if trigger_date:
            self.wait.until(EC.visibility_of_element_located(self.TRIGGER_DATE_INPUT)).send_keys(trigger_date)
        self.wait.until(EC.visibility_of_element_located(self.ACTION_TYPE_DROPDOWN)).send_keys(action_type)
        self.wait.until(EC.visibility_of_element_located(self.ACTION_AMOUNT_INPUT)).send_keys(str(action_amount))
        # For empty conditions, skip adding
        if conditions:
            self.wait.until(EC.element_to_be_clickable(self.CONDITIONS_ARRAY_INPUT)).click()
            for condition in conditions:
                # Add each condition (expand as per locator structure)
                pass
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_RULE_BUTTON)).click()

    def retrieve_rule(self, rule_id):
        """
        Retrieves a rule from backend (simulated via UI).
        Args:
            rule_id (str): Rule identifier.
        Returns:
            dict: Rule data (simulate retrieval).
        """
        rule_elements = self.driver.find_elements(*self.RULE_LIST)
        for rule in rule_elements:
            if rule_id in rule.text:
                return rule.text
        return None

    def define_rule_with_empty_conditions(self, trigger_type, action_type, action_amount):
        """
        Defines a rule with empty conditions array.
        Args:
            trigger_type (str): Type of trigger.
            action_type (str): Action type.
            action_amount (int): Amount value.
        """
        self.create_rule(trigger_type, None, action_type, action_amount, [])

    def trigger_rule(self, rule_id):
        """
        Triggers a rule by rule_id.
        Args:
            rule_id (str): Rule identifier.
        """
        self.wait.until(EC.element_to_be_clickable(self.TRIGGER_RULE_BUTTON)).click()
