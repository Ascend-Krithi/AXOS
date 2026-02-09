# RuleManagementPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class RuleManagementPage:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators

    def upload_rules_batch(self, file_path):
        upload_input = self.driver.find_element(By.XPATH, self.locators['rule_upload_input'])
        upload_input.send_keys(file_path)
        upload_button = self.driver.find_element(By.XPATH, self.locators['rule_upload_button'])
        upload_button.click()
        WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, self.locators['upload_success_message']))
        )

    def evaluate_all_rules(self):
        eval_button = self.driver.find_element(By.XPATH, self.locators['evaluate_all_button'])
        eval_button.click()
        WebDriverWait(self.driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, self.locators['evaluation_complete_message']))
        )

    def check_sql_injection_rejection(self, malicious_rule):
        upload_input = self.driver.find_element(By.XPATH, self.locators['rule_upload_input'])
        upload_input.clear()
        upload_input.send_keys(malicious_rule)
        upload_button = self.driver.find_element(By.XPATH, self.locators['rule_upload_button'])
        upload_button.click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.locators['sql_injection_error_message']))
            )
            return True
        except TimeoutException:
            return False

    def validate_batch_upload(self, expected_count):
        rule_count_elem = self.driver.find_element(By.XPATH, self.locators['rule_count_display'])
        actual_count = int(rule_count_elem.text)
        return actual_count == expected_count

    def get_evaluation_status(self):
        status_elem = self.driver.find_element(By.XPATH, self.locators['evaluation_status_display'])
        status_text = status_elem.text
        import re
        match = re.search(r"Passed: (\d+), Failed: (\d+)", status_text)
        if match:
            return {
                'passed': int(match.group(1)),
                'failed': int(match.group(2))
            }
        return {}

    def check_batch_sql_injection(self, file_path):
        upload_input = self.driver.find_element(By.XPATH, self.locators['rule_upload_input'])
        upload_input.send_keys(file_path)
        upload_button = self.driver.find_element(By.XPATH, self.locators['rule_upload_button'])
        upload_button.click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.locators['sql_injection_error_message']))
            )
            return True
        except TimeoutException:
            return False

    # NEW METHOD for currency_conversion rule
    def define_currency_conversion_rule(self, currency, amount):
        # Placeholder for actual UI interaction
        # Should be updated when UI locators are available
        rule_input = self.driver.find_element(By.ID, "rule-currency-conversion")  # Add this locator to Locators.json
        rule_input.clear()
        rule_input.send_keys(f"Currency: {currency}, Amount: {amount}")
        submit_button = self.driver.find_element(By.ID, "rule-submit")  # Add this locator to Locators.json
        submit_button.click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "rule-success-message"))  # Add this locator to Locators.json
            )
            return True
        except TimeoutException:
            # Graceful rejection
            error_elem = self.driver.find_element(By.ID, "rule-error-message")  # Add this locator to Locators.json
            return error_elem.text
