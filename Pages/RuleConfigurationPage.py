import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        # Existing locators
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
        # New locators from Locators.json
        self.rule_id_input = (By.ID, 'rule-id-field')
        self.rule_name_input_new = (By.NAME, 'rule-name')
        self.save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        self.trigger_type_dropdown = (By.ID, 'trigger-type-select')
        self.date_picker = (By.CSS_SELECTOR, "input[type='date']")
        self.after_deposit_toggle = (By.ID, 'trigger-after-deposit')
        self.action_type_dropdown = (By.ID, 'action-type-select')
        self.transfer_amount_input = (By.NAME, 'fixed-amount')
        self.add_condition_btn = (By.ID, 'add-condition-link')
        self.condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = (By.NAME, 'balance-limit')
        self.destination_account_input = (By.ID, 'target-account-id')
        self.success_message = (By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

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

    # TC-FT-009: Create and store a valid rule
    def create_and_store_valid_rule(self, rule_id, rule_name, trigger_type, trigger_date, action_type, action_amount, conditions):
        """
        Creates and stores a valid rule with the given parameters.
        Args:
            rule_id (str): Rule identifier.
            rule_name (str): Rule name.
            trigger_type (str): Trigger type (e.g., 'specific_date').
            trigger_date (str): Date string for the trigger.
            action_type (str): Action type (e.g., 'fixed_amount').
            action_amount (int): Amount for the action.
            conditions (list): List of condition dicts.
        Returns:
            bool: True if rule is stored successfully.
        """
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rule_id_input)
        ).send_keys(rule_id)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rule_name_input_new)
        ).send_keys(rule_name)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.trigger_type_dropdown)
        ).click()
        self.driver.find_element(*self.trigger_type_dropdown).send_keys(trigger_type)
        if trigger_type == 'specific_date':
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.date_picker)
            ).send_keys(trigger_date)
        elif trigger_type == 'after_deposit':
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.after_deposit_toggle)
            ).click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.action_type_dropdown)
        ).click()
        self.driver.find_element(*self.action_type_dropdown).send_keys(action_type)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.transfer_amount_input)
        ).send_keys(str(action_amount))
        if conditions:
            for cond in conditions:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.add_condition_btn)
                ).click()
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.condition_type_dropdown)
                ).click()
                self.driver.find_element(*self.condition_type_dropdown).send_keys(cond.get('type', ''))
                if 'balance_threshold' in cond:
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located(self.balance_threshold_input)
                    ).send_keys(str(cond['balance_threshold']))
                if 'destination_account' in cond:
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located(self.destination_account_input)
                    ).send_keys(cond['destination_account'])
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.save_rule_button)
        ).click()
        try:
            success = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.success_message)
            )
            return True
        except Exception:
            return False

    # TC-FT-009: Retrieve rule and validate
    def retrieve_and_validate_rule(self, rule_id, expected_rule):
        """
        Retrieves the rule from backend and validates it matches expected input.
        Args:
            rule_id (str): Rule identifier.
            expected_rule (dict): Expected rule structure.
        Returns:
            bool: True if rule matches expected input.
        """
        # Implementation here depends on UI/backend exposure
        # For UI: search for rule in table, validate fields
        table = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rules_table)
        )
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if cells and cells[0].text == rule_id:
                # Validate rule fields
                return all(
                    cells[i].text == str(v)
                    for i, v in enumerate(expected_rule.values())
                )
        return False

    # TC-FT-010: Define rule with empty conditions and trigger
    def define_rule_with_empty_conditions_and_trigger(self, rule_id, rule_name, trigger_type, action_type, action_amount):
        """
        Defines a rule with empty conditions and triggers it.
        Args:
            rule_id (str): Rule identifier.
            rule_name (str): Rule name.
            trigger_type (str): Trigger type (e.g., 'after_deposit').
            action_type (str): Action type (e.g., 'fixed_amount').
            action_amount (int): Amount for the action.
        Returns:
            bool: True if rule is accepted and executes unconditionally.
        """
        self.create_and_store_valid_rule(
            rule_id, rule_name, trigger_type, None, action_type, action_amount, []
        )
        # Simulate deposit trigger
        # This depends on UI implementation
        # Example:
        deposit_input = self.driver.find_element(By.ID, 'deposit-input')
        deposit_input.send_keys('1000')
        trigger_button = self.driver.find_element(By.ID, 'trigger-rule-btn')
        trigger_button.click()
        try:
            success = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.success_message)
            )
            return True
        except Exception:
            return False
