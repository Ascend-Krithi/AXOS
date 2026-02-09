import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class RulePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def define_rule(self, trigger_type=None, action_type=None, amount=None, conditions=None):
        # Placeholder: Update with real locators
        if trigger_type:
            self.driver.find_element(By.ID, 'trigger-type').send_keys(trigger_type)
        if action_type:
            self.driver.find_element(By.ID, 'action-type').send_keys(action_type)
        if amount:
            self.driver.find_element(By.ID, 'action-amount').send_keys(str(amount))
        if conditions:
            for cond in conditions:
                if cond['type'] == 'balance_threshold':
                    self.driver.find_element(By.ID, 'balance-threshold').send_keys(str(cond['value']))
                if cond['type'] == 'transaction_source':
                    self.driver.find_element(By.ID, 'transaction-source').send_keys(cond['value'])
        self.driver.find_element(By.ID, 'submit-rule').click()

    def get_rule_submission_result(self):
        # Placeholder: Update with real locators
        return self.driver.find_element(By.ID, 'rule-result').text

    def submit_rule_with_missing_trigger(self, action_type=None, amount=None, conditions=None):
        # Simulate missing trigger
        if action_type:
            self.driver.find_element(By.ID, 'action-type').send_keys(action_type)
        if amount:
            self.driver.find_element(By.ID, 'action-amount').send_keys(str(amount))
        self.driver.find_element(By.ID, 'submit-rule').click()

    def get_error_message(self):
        # Placeholder: Update with real locators
        return self.driver.find_element(By.ID, 'error-message').text

    def load_bulk_rules_and_evaluate(self, rules_batch):
        """
        Loads a batch of rules and triggers evaluation for all rules simultaneously.
        Args:
            rules_batch (list): List of rule dicts to load.
        Returns:
            dict: {'load_time': float, 'evaluation_time': float, 'performance_ok': bool}
        """
        # Placeholder locators for bulk upload and evaluation
        bulk_upload_btn = self.driver.find_element(By.ID, 'bulk-upload-btn')
        bulk_upload_btn.click()
        upload_input = self.driver.find_element(By.ID, 'bulk-upload-input')
        # Convert rules_batch to JSON string for upload
        import json
        rules_json = json.dumps(rules_batch)
        upload_input.send_keys(rules_json)
        start = time.time()
        self.driver.find_element(By.ID, 'bulk-upload-submit').click()
        # Wait for upload completion indicator
        self._wait_for_element(By.ID, 'bulk-upload-success', timeout=120)
        load_time = time.time() - start

        # Trigger evaluation for all rules
        eval_btn = self.driver.find_element(By.ID, 'evaluate-all-rules-btn')
        eval_btn.click()
        eval_start = time.time()
        self._wait_for_element(By.ID, 'evaluation-complete', timeout=300)
        evaluation_time = time.time() - eval_start

        # Check performance criteria
        performance_ok = (load_time <= 60) and (evaluation_time <= 180)
        return {
            'load_time': load_time,
            'evaluation_time': evaluation_time,
            'performance_ok': performance_ok
        }

    def submit_rule_with_sql_injection(self, rule_data):
        """
        Submits a rule with SQL injection payload and verifies system rejection.
        Args:
            rule_data (dict): Rule payload with SQL injection.
        Returns:
            dict: {'rejected': bool, 'error_message': str}
        """
        # Fill rule fields using locators
        trigger = rule_data.get('trigger', {})
        action = rule_data.get('action', {})
        conditions = rule_data.get('conditions', [])

        if trigger.get('type'):
            self.driver.find_element(By.ID, 'trigger-type').send_keys(trigger['type'])
        if trigger.get('date'):
            self.driver.find_element(By.ID, 'trigger-date').send_keys(trigger['date'])
        if action.get('type'):
            self.driver.find_element(By.ID, 'action-type').send_keys(action['type'])
        if action.get('amount'):
            self.driver.find_element(By.ID, 'action-amount').send_keys(str(action['amount']))
        for cond in conditions:
            if cond['type'] == 'balance_threshold':
                self.driver.find_element(By.ID, 'balance-threshold').send_keys(str(cond['value']))
            if cond['type'] == 'transaction_source':
                self.driver.find_element(By.ID, 'transaction-source').send_keys(cond['value'])
        self.driver.find_element(By.ID, 'submit-rule').click()

        # Wait for error message
        error_message = self._wait_for_element(By.ID, 'error-message', timeout=10).text
        rejected = 'SQL' in error_message or 'invalid' in error_message.lower() or 'rejected' in error_message.lower()
        return {'rejected': rejected, 'error_message': error_message}

    def _wait_for_element(self, by, value, timeout=30):
        """
        Waits for an element to be present and visible.
        Args:
            by (By): Selenium By selector.
            value (str): Locator value.
            timeout (int): Timeout in seconds.
        Returns:
            WebElement: Found element.
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
