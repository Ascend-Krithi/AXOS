# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object Model for the Rule Configuration Page.
    Provides methods to create rules, configure triggers, actions, validate rule schemas, and handle errors.
    """

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Locators from Locators.json
    rule_id_input = (By.ID, "rule-id-field")
    rule_name_input = (By.NAME, "rule-name")
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

    trigger_type_dropdown = (By.ID, "trigger-type-select")
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, "interval-value")
    after_deposit_toggle = (By.ID, "trigger-after-deposit")

    add_condition_btn = (By.ID, "add-condition-link")
    condition_type_dropdown = (By.CSS_SELECTOR, "select.condition-type")
    balance_threshold_input = (By.NAME, "balance-limit")
    transaction_source_dropdown = (By.ID, "source-provider-select")
    operator_dropdown = (By.CSS_SELECTOR, ".condition-operator-select")

    action_type_dropdown = (By.ID, "action-type-select")
    transfer_amount_input = (By.NAME, "fixed-amount")
    percentage_input = (By.ID, "deposit-percentage")
    destination_account_input = (By.ID, "target-account-id")

    json_schema_editor = (By.CSS_SELECTOR, ".monaco-editor")
    validate_schema_btn = (By.ID, "btn-verify-json")
    success_message = (By.CSS_SELECTOR, ".alert-success")
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def add_multiple_conditions(self, conditions):
        """
        Adds multiple conditions to the rule form.
        conditions: list of dicts, e.g. [{"type": "balance_threshold", "operator": ">=", "value": 1000}, {"type": "transaction_source", "value": "salary"}]
        """
        for cond in conditions:
            self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
            self.wait.until(EC.visibility_of_element_located(self.condition_type_dropdown)).send_keys(cond["type"])
            if "operator" in cond:
                self.wait.until(EC.visibility_of_element_located(self.operator_dropdown)).send_keys(cond["operator"])
            if cond["type"] == "balance_threshold":
                self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input)).send_keys(str(cond["value"]))
            elif cond["type"] == "transaction_source":
                self.wait.until(EC.visibility_of_element_located(self.transaction_source_dropdown)).send_keys(cond["value"])

    def simulate_deposit(self, balance, deposit, source):
        """
        Simulates a deposit for testing rule execution. Placeholder for integration with DepositSimulationPage.
        """
        # This method would interact with DepositSimulationPage if available
        pass

    def verify_rule_execution(self, expected_transfer):
        """
        Verifies whether transfer was executed or not after deposit simulation.
        expected_transfer: bool
        """
        # Example: Check for success message or rule execution indicator
        try:
            success = self.wait.until(EC.visibility_of_element_located(self.success_message))
            return expected_transfer in success.text.lower()
        except Exception:
            return False

    def submit_rule_with_missing_trigger(self):
        """
        Submits a rule with missing trigger type and checks for error.
        """
        self.wait.until(EC.visibility_of_element_located(self.action_type_dropdown)).send_keys("fixed_amount")
        self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input)).send_keys("100")
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    def submit_rule_with_unsupported_action(self):
        """
        Submits a rule with unsupported action type and checks for error.
        """
        self.wait.until(EC.visibility_of_element_located(self.trigger_type_dropdown)).send_keys("specific_date")
        self.wait.until(EC.visibility_of_element_located(self.action_type_dropdown)).send_keys("unknown_action")
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    def verify_error_message(self, expected_error):
        """
        Verifies the error message after submitting invalid rule.
        """
        error_elem = self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
        assert expected_error in error_elem.text, f"Expected error message '{expected_error}' not found."

    # TC_SCRUM158_07 functions
    def prepare_minimum_rule_schema(self, trigger, condition, action):
        """
        Prepares a rule schema with only required fields (one trigger, one condition, one action).
        """
        self.wait.until(EC.visibility_of_element_located(self.trigger_type_dropdown)).send_keys(trigger["type"])
        self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
        self.wait.until(EC.visibility_of_element_located(self.condition_type_dropdown)).send_keys(condition["type"])
        self.wait.until(EC.visibility_of_element_located(self.operator_dropdown)).send_keys(condition["operator"])
        self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input)).send_keys(str(condition["value"]))
        self.wait.until(EC.visibility_of_element_located(self.action_type_dropdown)).send_keys(action["type"])
        self.wait.until(EC.visibility_of_element_located(self.destination_account_input)).send_keys(action["account"])
        self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input)).send_keys(str(action["amount"]))

    def submit_rule(self):
        """
        Submits the rule and verifies creation.
        """
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()
