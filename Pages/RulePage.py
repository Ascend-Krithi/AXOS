import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RulePage:
    def __init__(self, driver):
        self.driver = driver

    def create_and_store_rule(self, trigger_type, trigger_date, action_type, amount, conditions=None):
        '''
        Creates and stores a valid rule.
        :param trigger_type: The type of trigger (e.g., 'specific_date', 'after_deposit')
        :param trigger_date: The date for specific_date trigger (ISO format string)
        :param action_type: The action type (e.g., 'fixed_amount')
        :param amount: The fixed amount for the action
        :param conditions: List of conditions (can be empty)
        '''
        add_rule_btn = self.driver.find_element(By.ID, 'add-rule')
        add_rule_btn.click()
        trigger_dropdown = self.driver.find_element(By.ID, 'trigger-type')
        trigger_dropdown.click()
        trigger_option = self.driver.find_element(By.XPATH, f"//option[@value='{trigger_type}']")
        trigger_option.click()
        if trigger_type == 'specific_date':
            date_field = self.driver.find_element(By.ID, 'trigger-date')
            date_field.clear()
            date_field.send_keys(trigger_date)
        action_dropdown = self.driver.find_element(By.ID, 'action-type')
        action_dropdown.click()
        action_option = self.driver.find_element(By.XPATH, f"//option[@value='{action_type}']")
        action_option.click()
        amount_field = self.driver.find_element(By.ID, 'fixed-amount')
        amount_field.clear()
        amount_field.send_keys(str(amount))
        # Handle conditions if present
        if conditions is not None and len(conditions) > 0:
            for cond in conditions:
                # Add logic to input each condition if UI supports it
                pass
        save_btn = self.driver.find_element(By.ID, 'save-rule')
        save_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.rule-success'))
        )

    def retrieve_rule(self, rule_identifier=None):
        '''
        Retrieves a rule from backend (UI simulation).
        :param rule_identifier: Optional identifier to locate the rule
        '''
        # This assumes rules are listed in a table or list
        rules_list = self.driver.find_elements(By.CSS_SELECTOR, 'div.rule-item')
        if rule_identifier:
            for rule in rules_list:
                if rule_identifier in rule.text:
                    return rule.text
        return [r.text for r in rules_list]

    def verify_rule_stored(self, expected_rule):
        '''
        Verifies that the rule is stored.
        :param expected_rule: Dictionary of expected rule values
        '''
        rules_list = self.driver.find_elements(By.CSS_SELECTOR, 'div.rule-item')
        for rule in rules_list:
            if all(str(expected_rule[k]) in rule.text for k in expected_rule):
                return True
        return False

    def define_rule_with_empty_conditions(self, trigger_type, action_type, amount):
        '''
        Defines a rule with an empty conditions array.
        :param trigger_type: The type of trigger
        :param action_type: The action type
        :param amount: The fixed amount
        '''
        self.create_and_store_rule(trigger_type, '', action_type, amount, conditions=[])

    def verify_rule_accepted_and_executes_unconditionally(self, trigger_type):
        '''
        Verifies that the rule is accepted and executes unconditionally.
        :param trigger_type: The trigger type
        '''
        rules_list = self.driver.find_elements(By.CSS_SELECTOR, 'div.rule-item')
        for rule in rules_list:
            if trigger_type in rule.text and 'unconditional' in rule.text.lower():
                return True
        return False
