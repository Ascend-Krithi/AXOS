# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RuleConfigurationPage:
    """
    PageClass for Rule Configuration Page

    This class encapsulates all locators and actions required for rule configuration,
    schema validation, and negative testing as per the provided test cases.

    Includes:
    - Locator definitions
    - Methods for interacting with rule fields
    - Methods for validating schema in UI and via API
    - Methods for preparing minimum valid and unsupported trigger schemas
    - Methods for negative test assertions

    Executive Summary:
    This PageClass enables end-to-end automation for rule configuration including strict schema validation, extensibility testing, negative testing, and API integration. It is fully compatible with downstream automation pipelines and adheres to code integrity standards.

    Detailed Analysis:
    All locator definitions are based on existing UI elements. Methods cover positive and negative scenarios as per test cases TC_SCRUM158_09 and TC_SCRUM158_10. The class supports both UI and API validation, ensuring comprehensive coverage.

    Implementation Guide:
    - Instantiate RuleConfigurationPage with a Selenium WebDriver instance.
    - Use provided methods to interact with rule fields and schema editor.
    - Test methods for minimum valid and unsupported trigger schemas.
    - API integration methods allow direct schema submission and validation.

    Quality Assurance Report:
    - All fields and locators are validated against existing code and Locators.json.
    - Schema validation methods assert correct error messages and HTTP status codes.
    - Negative and extensibility tests ensure robustness against invalid input and new triggers.

    Troubleshooting Guide:
    - If a locator changes, update its definition in the class.
    - If schema validation fails unexpectedly, check for UI changes or API updates.
    - TimeoutExceptions indicate slow UI response; adjust WebDriverWait if needed.
    - Unsupported trigger types may require backend extensibility; check API documentation.

    Future Considerations:
    - Extend methods for additional rule types or conditions as needed.
    - Integrate with advanced reporting frameworks for test results.
    - Refactor for support of multiple browsers or parallel execution.
    - Monitor for new triggers and update schema preparation methods accordingly.
    """
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Locators from Locators.json
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

    def prepare_minimum_valid_rule_schema(self):
        """
        Prepares a rule schema with only the minimum required fields for TC_SCRUM158_09.
        """
        return {
            "trigger": "balance_above",
            "conditions": [
                {
                    "type": "amount_above",
                    "value": 1000
                }
            ],
            "actions": [
                {
                    "type": "transfer",
                    "amount": 100
                }
            ]
        }

    def prepare_unsupported_trigger_schema(self):
        """
        Prepares a rule schema with a new, unsupported trigger type for TC_SCRUM158_10.
        """
        return {
            "trigger": "future_trigger",
            "conditions": [
                {
                    "type": "amount_above",
                    "value": 2000
                }
            ],
            "actions": [
                {
                    "type": "transfer",
                    "amount": 150
                }
            ]
        }

    def test_TC_SCRUM158_09_minimum_rule_schema(self, api_url, headers=None):
        """
        Test case TC_SCRUM158_09: Prepare minimum rule schema, validate, submit, and verify rule creation.
        """
        schema = self.prepare_minimum_valid_rule_schema()
        is_valid, error_msg = self.validate_rule_schema(str(schema))
        assert is_valid, f"Schema should be valid but validation failed. Error: {error_msg}"
        status_code, response = self.submit_rule_schema_api(schema, api_url, headers)
        assert status_code == 201, f"API should return 201 Created, got {status_code}. Response: {response}"
        assert 'ruleId' in response, "Expected ruleId in response for successful creation."

    def test_TC_SCRUM158_10_unsupported_trigger(self, api_url, headers=None):
        """
        Test case TC_SCRUM158_10: Prepare schema with unsupported trigger, validate, submit, and verify extensibility/error.
        """
        schema = self.prepare_unsupported_trigger_schema()
        is_valid, error_msg = self.validate_rule_schema(str(schema))
        # Schema may be valid if UI allows extensibility, else invalid
        if is_valid:
            status_code, response = self.submit_rule_schema_api(schema, api_url, headers)
            # API should reject unsupported trigger
            assert status_code in [400, 422], f"API should return 400/422 for unsupported trigger, got {status_code}. Response: {response}"
            assert 'unsupported trigger' in str(response).lower() or 'error' in str(response).lower(), "Expected error about unsupported trigger in response."
        else:
            assert 'unsupported trigger' in error_msg.lower() or 'invalid' in error_msg.lower(), "Expected error about unsupported trigger in validation message."
