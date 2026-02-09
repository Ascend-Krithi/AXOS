import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = {
            "ruleIdInput": (By.ID, "rule-id-field"),
            "ruleNameInput": (By.NAME, "rule-name"),
            "saveRuleButton": (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']"),
            "triggerTypeDropdown": (By.ID, "trigger-type-select"),
            "datePicker": (By.CSS_SELECTOR, "input[type='date']"),
            "recurringIntervalInput": (By.ID, "interval-value"),
            "afterDepositToggle": (By.ID, "trigger-after-deposit"),
            "addConditionBtn": (By.ID, "add-condition-link"),
            "conditionTypeDropdown": (By.CSS_SELECTOR, "select.condition-type"),
            "balanceThresholdInput": (By.CSS_SELECTOR, "input[name='balance-limit'"),
            "transactionSourceDropdown": (By.ID, "source-provider-select"),
            "operatorDropdown": (By.CSS_SELECTOR, ".condition-operator-select"),
            "actionTypeDropdown": (By.ID, "action-type-select"),
            "transferAmountInput": (By.NAME, "fixed-amount"),
            "percentageInput": (By.ID, "deposit-percentage"),
            "destinationAccountInput": (By.ID, "target-account-id"),
            "jsonSchemaEditor": (By.CSS_SELECTOR, ".monaco-editor"),
            "validateSchemaBtn": (By.ID, "btn-verify-json"),
            "successMessage": (By.CSS_SELECTOR, ".alert-success"),
            "schemaErrorMessage": (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")
        }

    def load_rules_batch(self, rules_json):
        '''
        Loads a batch of rules into the system using the JSON schema editor.
        Args:
            rules_json: str - JSON string containing the rules batch.
        Returns:
            bool - True if success message is displayed, False otherwise.
        '''
        editor = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.locators["jsonSchemaEditor"])
        )
        # Clear and input JSON
        self.driver.execute_script("arguments[0].innerText = '';", editor)
        self.driver.execute_script("arguments[0].innerText = arguments[1];", editor, rules_json)
        validate_btn = self.driver.find_element(*self.locators["validateSchemaBtn"])
        validate_btn.click()
        try:
            WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located(self.locators["successMessage"])
            )
            return True
        except:
            return False

    def submit_rule_with_sql_injection(self, rule_data):
        '''
        Submits a rule with SQL injection in a field value and checks for schema error.
        Args:
            rule_data: dict - Rule data with SQL injection.
        Returns:
            bool - True if schema error message is displayed, False otherwise.
        '''
        editor = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.locators["jsonSchemaEditor"])
        )
        rule_json = str(rule_data)
        self.driver.execute_script("arguments[0].innerText = '';", editor)
        self.driver.execute_script("arguments[0].innerText = arguments[1];", editor, rule_json)
        validate_btn = self.driver.find_element(*self.locators["validateSchemaBtn"])
        validate_btn.click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.locators["schemaErrorMessage"])
            )
            return True
        except:
            return False

    def trigger_evaluation_for_all_rules(self):
        '''
        Triggers evaluation for all rules. Assumes there is a UI element to trigger evaluation.
        Returns:
            bool - True if evaluation started, False otherwise.
        '''
        # Placeholder: Implementation depends on actual trigger element.
        # Example:
        # trigger_btn = self.driver.find_element(By.ID, "trigger-all-evaluation")
        # trigger_btn.click()
        # return True
        return True  # Stub for demo

    # Existing methods preserved below...
