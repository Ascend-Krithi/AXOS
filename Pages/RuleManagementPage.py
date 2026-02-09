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
        """
        Uploads a batch file containing rules.
        Args:
            file_path (str): Path to the rules file to upload.
        """
        upload_input = self.driver.find_element(By.XPATH, self.locators['rule_upload_input'])
        upload_input.send_keys(file_path)
        upload_button = self.driver.find_element(By.XPATH, self.locators['rule_upload_button'])
        upload_button.click()
        # Wait for upload confirmation
        WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, self.locators['upload_success_message']))
        )

    def evaluate_all_rules(self):
        """
        Evaluates all rules in the system.
        """
        eval_button = self.driver.find_element(By.XPATH, self.locators['evaluate_all_button'])
        eval_button.click()
        # Wait for evaluation to complete
        WebDriverWait(self.driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, self.locators['evaluation_complete_message']))
        )

    def check_sql_injection_rejection(self, malicious_rule):
        """
        Attempts to upload a rule with SQL injection and verifies rejection.
        Args:
            malicious_rule (str): Rule string containing SQL injection.
        Returns:
            bool: True if rejected, False otherwise.
        """
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

    # NEW: Helper method for batch upload validation
    def validate_batch_upload(self, expected_count):
        """
        Validates that the expected number of rules are uploaded.
        Args:
            expected_count (int): Expected number of rules.
        Returns:
            bool: True if count matches, False otherwise.
        """
        rule_count_elem = self.driver.find_element(By.XPATH, self.locators['rule_count_display'])
        actual_count = int(rule_count_elem.text)
        return actual_count == expected_count

    # NEW: Helper method for evaluating rules status
    def get_evaluation_status(self):
        """
        Returns the evaluation status of all rules.
        Returns:
            dict: Status summary (e.g., {'passed': 9990, 'failed': 10})
        """
        status_elem = self.driver.find_element(By.XPATH, self.locators['evaluation_status_display'])
        status_text = status_elem.text
        # Parse status_text as needed
        import re
        match = re.search(r"Passed: (\d+), Failed: (\d+)", status_text)
        if match:
            return {
                'passed': int(match.group(1)),
                'failed': int(match.group(2))
            }
        return {}

    # NEW: SQL Injection test for batch
    def check_batch_sql_injection(self, file_path):
        """
        Uploads a batch file with SQL injection rules and checks for rejection.
        Args:
            file_path (str): Path to batch file.
        Returns:
            bool: True if all SQL injections are rejected, False otherwise.
        """
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
