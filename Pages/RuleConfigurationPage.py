# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Existing methods preserved below
    # ... (existing code, unchanged) ...

    # --- TC-FT-003: Rule with Multiple Conditions ---
    def define_rule_with_multiple_conditions(self, rule_data):
        # Fill Rule ID and Name
        if 'ruleId' in rule_data:
            self.driver.find_element(By.ID, 'rule-id-field').send_keys(rule_data['ruleId'])
        if 'ruleName' in rule_data:
            self.driver.find_element(By.NAME, 'rule-name').send_keys(rule_data['ruleName'])
        # Set Trigger
        if 'trigger' in rule_data:
            trigger = rule_data['trigger']
            if trigger.get('type') == 'after_deposit':
                self.driver.find_element(By.ID, 'trigger-after-deposit').click()
            elif trigger.get('type') == 'specific_date':
                self.driver.find_element(By.ID, 'trigger-type-select').click()
                self.driver.find_element(By.CSS_SELECTOR, "input[type='date']").send_keys(trigger.get('date', ''))
        # Set Conditions
        for cond in rule_data.get('conditions', []):
            self.driver.find_element(By.ID, 'add-condition-link').click()
            if cond['type'] == 'balance_threshold':
                self.driver.find_element(By.CSS_SELECTOR, 'select.condition-type').send_keys('Balance Threshold')
                self.driver.find_element(By.NAME, 'balance-limit').send_keys(str(cond['value']))
                self.driver.find_element(By.CSS_SELECTOR, '.condition-operator-select').send_keys(cond['operator'])
            elif cond['type'] == 'transaction_source':
                self.driver.find_element(By.CSS_SELECTOR, 'select.condition-type').send_keys('Transaction Source')
                self.driver.find_element(By.ID, 'source-provider-select').send_keys(cond['value'])
        # Set Action
        if 'action' in rule_data:
            action = rule_data['action']
            self.driver.find_element(By.ID, 'action-type-select').send_keys(action['type'])
            if action['type'] == 'fixed_amount':
                self.driver.find_element(By.NAME, 'fixed-amount').send_keys(str(action['amount']))
            elif action['type'] == 'percentage':
                self.driver.find_element(By.ID, 'deposit-percentage').send_keys(str(action['percentage']))
            elif action['type'] == 'transfer':
                self.driver.find_element(By.ID, 'target-account-id').send_keys(action['destination_account'])
        # Save Rule
        self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']").click()

    def verify_rule_accepted(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-success')))

    def simulate_deposit(self, balance, deposit, source):
        # This method assumes there is a way to simulate deposit in the UI
        # Placeholders for demonstration
        # Navigate to deposit simulation page or section
        # Set balance
        self.driver.find_element(By.ID, 'balance-input').clear()
        self.driver.find_element(By.ID, 'balance-input').send_keys(str(balance))
        # Set deposit amount
        self.driver.find_element(By.ID, 'deposit-input').clear()
        self.driver.find_element(By.ID, 'deposit-input').send_keys(str(deposit))
        # Set source
        self.driver.find_element(By.ID, 'deposit-source-input').clear()
        self.driver.find_element(By.ID, 'deposit-source-input').send_keys(source)
        # Submit deposit
        self.driver.find_element(By.ID, 'submit-deposit-btn').click()

    def verify_transfer_executed(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-success')))

    def verify_transfer_not_executed(self):
        # Check that success message is NOT present
        try:
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-success')))
            return False
        except:
            return True

    # --- TC-FT-004: Rule Validation ---
    def submit_rule_with_missing_trigger(self, rule_data):
        # Fill Rule Name
        if 'ruleName' in rule_data:
            self.driver.find_element(By.NAME, 'rule-name').send_keys(rule_data['ruleName'])
        # Set Action
        if 'action' in rule_data:
            action = rule_data['action']
            self.driver.find_element(By.ID, 'action-type-select').send_keys(action['type'])
            if action['type'] == 'fixed_amount':
                self.driver.find_element(By.NAME, 'fixed-amount').send_keys(str(action['amount']))
        # No trigger set
        self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']").click()

    def submit_rule_with_unsupported_action(self, rule_data):
        # Fill Rule Name
        if 'ruleName' in rule_data:
            self.driver.find_element(By.NAME, 'rule-name').send_keys(rule_data['ruleName'])
        # Set Trigger
        if 'trigger' in rule_data:
            trigger = rule_data['trigger']
            if trigger.get('type') == 'specific_date':
                self.driver.find_element(By.ID, 'trigger-type-select').click()
                self.driver.find_element(By.CSS_SELECTOR, "input[type='date']").send_keys(trigger.get('date', ''))
        # Set unsupported action
        if 'action' in rule_data:
            action = rule_data['action']
            self.driver.find_element(By.ID, 'action-type-select').send_keys(action['type'])
        self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']").click()

    def verify_missing_trigger_error(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='error-feedback-text']")))

    def verify_unsupported_action_error(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='error-feedback-text']")))
