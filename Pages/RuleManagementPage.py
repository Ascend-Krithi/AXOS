from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleManagementPage:
    def __init__(self, driver):
        self.driver = driver

    def create_rule(self, conditions, actions):
        # Example: conditions = {'balance': '>=1000', 'source': 'salary'}
        # actions = {'transfer': 'execute'}
        self.driver.find_element(By.ID, "add-rule-btn").click()
        for cond_key, cond_value in conditions.items():
            self.driver.find_element(By.ID, f"condition-{cond_key}").send_keys(cond_value)
        for action_key, action_value in actions.items():
            self.driver.find_element(By.ID, f"action-{action_key}").send_keys(action_value)
        self.driver.find_element(By.ID, "submit-rule-btn").click()

    def simulate_deposit(self, amount, source):
        self.driver.find_element(By.ID, "simulate-deposit-btn").click()
        self.driver.find_element(By.ID, "deposit-amount").send_keys(str(amount))
        self.driver.find_element(By.ID, "deposit-source").send_keys(source)
        self.driver.find_element(By.ID, "deposit-submit-btn").click()

    def validate_transfer_execution(self, expected):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "transfer-success-msg"))
            )
            actual = True
        except:
            actual = False
        assert actual == expected, f"Transfer execution validation failed: expected {expected}, got {actual}"

    def submit_rule_with_invalid_data(self, trigger_type, action_type):
        self.driver.find_element(By.ID, "add-rule-btn").click()
        if trigger_type:
            self.driver.find_element(By.ID, "trigger-type").send_keys(trigger_type)
        if action_type:
            self.driver.find_element(By.ID, "action-type").send_keys(action_type)
        self.driver.find_element(By.ID, "submit-rule-btn").click()

    def validate_error_messages(self, expected_errors):
        error_elements = self.driver.find_elements(By.CLASS_NAME, "error-msg")
        errors = [elem.text for elem in error_elements]
        for expected_error in expected_errors:
            assert expected_error in errors, f"Expected error '{expected_error}' not found in {errors}"