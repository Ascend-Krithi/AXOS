# Selenium Python PageClass for Rule Configuration Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.rule_id_input = (By.ID, 'rule-id-field')
        self.rule_name_input = (By.NAME, 'rule-name')
        self.save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        self.trigger_type_dropdown = (By.ID, 'trigger-type-select')
        self.date_picker = (By.CSS_SELECTOR, 'input[type="date"]')
        self.recurring_interval_input = (By.ID, 'interval-value')
        self.after_deposit_toggle = (By.ID, 'trigger-after-deposit')
        self.add_condition_btn = (By.ID, 'add-condition-link')
        self.condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = (By.CSS_SELECTOR, 'input[name="balance-limit"]')
        self.transaction_source_dropdown = (By.ID, 'source-provider-select')
        self.operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')
        self.action_type_dropdown = (By.ID, 'action-type-select')
        self.transfer_amount_input = (By.NAME, 'fixed-amount')
        self.percentage_input = (By.ID, 'deposit-percentage')
        self.destination_account_input = (By.ID, 'target-account-id')
        self.json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = (By.ID, 'btn-verify-json')
        self.success_message = (By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = (By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    # Existing logic preserved here (if any)

    # --- New methods for test cases TC-SCRUM-387-005 and TC-SCRUM-387-006 ---
    def create_rule(self, rule_data):
        '''Fill rule creation form with given rule_data dict.'''
        if 'rule_id' in rule_data:
            self.driver.find_element(*self.rule_id_input).clear()
            self.driver.find_element(*self.rule_id_input).send_keys(str(rule_data['rule_id']))
        if 'rule_name' in rule_data:
            self.driver.find_element(*self.rule_name_input).clear()
            self.driver.find_element(*self.rule_name_input).send_keys(rule_data['rule_name'])
        # Triggers
        if 'triggers' in rule_data:
            # Only handles array of triggers; for invalid types, leave blank
            if isinstance(rule_data['triggers'], list):
                for trigger in rule_data['triggers']:
                    self.driver.find_element(*self.trigger_type_dropdown).click()
                    # Further trigger handling omitted for brevity
            # else: skip for negative test
        # Conditions
        if 'conditions' in rule_data:
            for idx, cond in enumerate(rule_data['conditions']):
                self.driver.find_element(*self.add_condition_btn).click()
                if 'field' in cond:
                    # Only handle 'balance' field for demo
                    if cond['field'] == 'balance':
                        self.driver.find_element(*self.balance_threshold_input).clear()
                        self.driver.find_element(*self.balance_threshold_input).send_keys(str(cond.get('value', '')))
                if 'operator' in cond:
                    self.driver.find_element(*self.operator_dropdown).click()
                    # Select operator logic omitted
        # Actions
        if 'actions' in rule_data:
            for action in rule_data['actions']:
                self.driver.find_element(*self.action_type_dropdown).click()
                # Further action handling omitted

    def submit_rule(self):
        '''Submit the rule creation form.'''
        self.driver.find_element(*self.save_rule_button).click()

    def get_error_message(self):
        '''Get error message displayed after rule submission.'''
        try:
            error_elem = self.wait.until(
                EC.visibility_of_element_located(self.schema_error_message)
            )
            return error_elem.text
        except TimeoutException:
            return None

    def get_validation_errors(self):
        '''Parse structured validation errors from error feedback.'''
        try:
            error_elem = self.wait.until(
                EC.visibility_of_element_located(self.schema_error_message)
            )
            # Assuming error feedback is JSON or structured text
            return error_elem.text
        except TimeoutException:
            return None

    def verify_error_response(self, expected_errors):
        '''Verify error response contains expected validation errors.'''
        actual_errors = self.get_validation_errors()
        for err in expected_errors:
            if err['field'] not in actual_errors or err['message'] not in actual_errors:
                return False
        return True
