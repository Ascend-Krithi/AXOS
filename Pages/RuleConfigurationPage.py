import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_rule_button = (By.ID, 'add-rule-btn')
        self.rule_name_input = (By.ID, 'rule-name-input')
        self.rule_condition_input = (By.ID, 'rule-condition-input')
        self.submit_button = (By.ID, 'submit-rule-btn')
        self.rules_table = (By.ID, 'rules-table')
        self.error_message = (By.ID, 'error-msg')
        self.evaluate_button = (By.ID, 'evaluate-all-btn')
        self.batch_upload_button = (By.ID, 'batch-upload-btn')
        self.batch_file_input = (By.ID, 'batch-file-input')
        self.batch_upload_confirm = (By.ID, 'batch-upload-confirm-btn')
        self.evaluation_status = (By.ID, 'evaluation-status')

    def add_rule(self, name, condition):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_rule_button)
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rule_name_input)
        ).send_keys(name)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rule_condition_input)
        ).send_keys(condition)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.submit_button)
        ).click()

    def get_error_message(self):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            ).text
        except Exception:
            return None

    def get_rules_count(self):
        table = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rules_table)
        )
        rows = table.find_elements(By.TAG_NAME, 'tr')
        return len(rows) - 1  # Assuming first row is header

    def evaluate_all_rules(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.evaluate_button)
        ).click()
        WebDriverWait(self.driver, 60).until(
            EC.text_to_be_present_in_element(self.evaluation_status, 'Completed'))

    def batch_upload_rules(self, file_path):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.batch_upload_button)
        ).click()
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.batch_file_input)
        )
        file_input.send_keys(file_path)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.batch_upload_confirm)
        ).click()
        time.sleep(5)

    # TC-FT-007: Load 10,000 rules and trigger evaluation
    def load_batch_rules_and_evaluate(self, batch_file_path):
        """
        Loads a batch file containing 10,000 rules, verifies upload, and triggers evaluation.
        Args:
            batch_file_path (str): Path to the batch rules CSV/JSON file.
        Returns:
            bool: True if evaluation completes successfully, False otherwise.
        """
        self.batch_upload_rules(batch_file_path)
        count = self.get_rules_count()
        if count < 10000:
            raise AssertionError(f"Expected 10,000 rules, found {count}.")
        self.evaluate_all_rules()
        status = WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located(self.evaluation_status)
        ).text
        return status == 'Completed'

    # TC-FT-008: Submit rule with SQL injection and verify rejection
    def submit_rule_with_sql_injection(self, name, sql_payload):
        """
        Attempts to submit a rule with SQL injection payload and verifies system rejection.
        Args:
            name (str): Name for the rule.
            sql_payload (str): SQL injection string for the condition field.
        Returns:
            bool: True if system rejects the rule, False otherwise.
        """
        self.add_rule(name, sql_payload)
        error = self.get_error_message()
        if error is None:
            raise AssertionError("No error message displayed for SQL injection attempt.")
        return 'sql injection' in error.lower() or 'invalid input' in error.lower()
