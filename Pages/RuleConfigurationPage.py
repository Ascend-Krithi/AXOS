# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Locators
        self.ruleIdInput = (By.ID, 'rule-id-field')
        self.ruleNameInput = (By.NAME, 'rule-name')
        self.saveRuleButton = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        self.triggerTypeDropdown = (By.ID, 'trigger-type-select')
        self.datePicker = (By.CSS_SELECTOR, "input[type='date']")
        self.recurringIntervalInput = (By.ID, 'interval-value')
        self.afterDepositToggle = (By.ID, 'trigger-after-deposit')
        self.addConditionBtn = (By.ID, 'add-condition-link')
        self.conditionTypeDropdown = (By.CSS_SELECTOR, 'select.condition-type')
        self.balanceThresholdInput = (By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transactionSourceDropdown = (By.ID, 'source-provider-select')
        self.operatorDropdown = (By.CSS_SELECTOR, '.condition-operator-select')
        self.actionTypeDropdown = (By.ID, 'action-type-select')
        self.transferAmountInput = (By.NAME, 'fixed-amount')
        self.percentageInput = (By.ID, 'deposit-percentage')
        self.destinationAccountInput = (By.ID, 'target-account-id')
        self.jsonSchemaEditor = (By.CSS_SELECTOR, '.monaco-editor')
        self.validateSchemaBtn = (By.ID, 'btn-verify-json')
        self.successMessage = (By.CSS_SELECTOR, '.alert-success')
        self.schemaErrorMessage = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def enter_rule_id(self, rule_id):
        rule_id_elem = self.wait.until(EC.visibility_of_element_located(self.ruleIdInput))
        rule_id_elem.clear()
        rule_id_elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        rule_name_elem = self.wait.until(EC.visibility_of_element_located(self.ruleNameInput))
        rule_name_elem.clear()
        rule_name_elem.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.triggerTypeDropdown))
        dropdown.click()
        dropdown.send_keys(trigger_type)

    def add_condition(self, condition_type, balance_threshold=None, transaction_source=None, operator=None):
        self.wait.until(EC.element_to_be_clickable(self.addConditionBtn)).click()
        self.wait.until(EC.element_to_be_clickable(self.conditionTypeDropdown)).send_keys(condition_type)
        if balance_threshold is not None:
            self.wait.until(EC.visibility_of_element_located(self.balanceThresholdInput)).send_keys(balance_threshold)
        if transaction_source is not None:
            self.wait.until(EC.visibility_of_element_located(self.transactionSourceDropdown)).send_keys(transaction_source)
        if operator is not None:
            self.wait.until(EC.visibility_of_element_located(self.operatorDropdown)).send_keys(operator)

    def select_action_type(self, action_type):
        self.wait.until(EC.element_to_be_clickable(self.actionTypeDropdown)).send_keys(action_type)

    def enter_transfer_amount(self, amount):
        self.wait.until(EC.visibility_of_element_located(self.transferAmountInput)).send_keys(amount)

    def enter_percentage(self, percentage):
        self.wait.until(EC.visibility_of_element_located(self.percentageInput)).send_keys(percentage)

    def enter_destination_account(self, account_id):
        self.wait.until(EC.visibility_of_element_located(self.destinationAccountInput)).send_keys(account_id)

    def validate_rule_schema(self, schema_json):
        """
        Validates the rule schema using the JSON Schema Editor and Validate button.
        Returns (is_valid, error_message)
        """
        editor = self.wait.until(EC.visibility_of_element_located(self.jsonSchemaEditor))
        editor.clear()
        editor.send_keys(schema_json)
        self.wait.until(EC.element_to_be_clickable(self.validateSchemaBtn)).click()
        try:
            self.wait.until(EC.visibility_of_element_located(self.successMessage))
            return True, None
        except TimeoutException:
            error_elem = self.driver.find_element(*self.schemaErrorMessage)
            return False, error_elem.text

    def submit_rule_schema_api(self, schema_json, api_url, headers=None):
        """
        Submits the rule schema via API (POST /rules).
        Returns (status_code, response_json)
        """
        import requests
        response = requests.post(api_url, json=schema_json, headers=headers or {})
        return response.status_code, response.json()

    def prepare_invalid_trigger_schema(self):
        """
        Prepares a rule schema with an invalid trigger value for testing.
        """
        return {
            "trigger": "unknown_trigger",
            "conditions": [
                {
                    "type": "amount_above",
                    "balance_limit": 1000,
                    "operator": "greater_than"
                }
            ],
            "actions": [
                {
                    "type": "transfer",
                    "fixed-amount": 500,
                    "target-account-id": "ACC123"
                }
            ]
        }

    def prepare_condition_missing_params_schema(self):
        """
        Prepares a rule schema with a condition missing required parameters for testing.
        """
        return {
            "trigger": "deposit",
            "conditions": [
                {
                    "type": "amount_above"
                    # missing balance_limit and operator
                }
            ],
            "actions": [
                {
                    "type": "transfer",
                    "fixed-amount": 500,
                    "target-account-id": "ACC123"
                }
            ]
        }

    def test_invalid_trigger_schema(self, api_url, headers=None):
        """
        Test case: Prepare invalid trigger schema, validate, submit, and verify API returns 400 Bad Request.
        """
        schema = self.prepare_invalid_trigger_schema()
        is_valid, error_msg = self.validate_rule_schema(str(schema))
        assert not is_valid, f"Schema should be invalid but validation passed. Error: {error_msg}"
        status_code, response = self.submit_rule_schema_api(schema, api_url, headers)
        assert status_code == 400, f"API should return 400 Bad Request, got {status_code}. Response: {response}"
        assert 'invalid value' in str(response), "Expected error about invalid value in response."

    def test_condition_missing_params_schema(self, api_url, headers=None):
        """
        Test case: Prepare condition missing params schema, validate, submit, and verify API returns 400 Bad Request.
        """
        schema = self.prepare_condition_missing_params_schema()
        is_valid, error_msg = self.validate_rule_schema(str(schema))
        assert not is_valid, f"Schema should be invalid but validation passed. Error: {error_msg}"
        status_code, response = self.submit_rule_schema_api(schema, api_url, headers)
        assert status_code == 400, f"API should return 400 Bad Request, got {status_code}. Response: {response}"
        assert 'incomplete condition' in str(response), "Expected error about incomplete condition in response."
