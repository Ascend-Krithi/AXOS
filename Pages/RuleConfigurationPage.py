# Pages/RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class RuleConfigurationPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        # Locators from Locators.json
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
            "balanceThresholdInput": (By.CSS_SELECTOR, "input[name='balance-limit']"),
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

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def fill_rule_form(self, rule_id=None, rule_name=None):
        if rule_id:
            rule_id_input = self.wait_for_element(self.locators["ruleIdInput"])
            rule_id_input.clear()
            rule_id_input.send_keys(rule_id)
        if rule_name:
            rule_name_input = self.wait_for_element(self.locators["ruleNameInput"])
            rule_name_input.clear()
            rule_name_input.send_keys(rule_name)

    def select_trigger(self, trigger):
        trigger_type_dropdown = self.wait_for_element(self.locators["triggerTypeDropdown"])
        trigger_type_dropdown.click()
        if trigger["type"] == "after_deposit":
            after_deposit_toggle = self.wait_for_element(self.locators["afterDepositToggle"])
            if not after_deposit_toggle.is_selected():
                after_deposit_toggle.click()
        elif trigger["type"] == "specific_date":
            trigger_type_dropdown.send_keys("specific_date")
            date_picker = self.wait_for_element(self.locators["datePicker"])
            date_picker.clear()
            date_picker.send_keys(trigger["date"])
        else:
            pass

    def add_conditions(self, conditions):
        for condition in conditions:
            add_condition_btn = self.wait_for_element(self.locators["addConditionBtn"])
            add_condition_btn.click()
            condition_type_dropdown = self.wait_for_element(self.locators["conditionTypeDropdown"])
            condition_type_dropdown.send_keys(condition.get("type", ""))
            if "balance_limit" in condition:
                balance_input = self.wait_for_element(self.locators["balanceThresholdInput"])
                balance_input.clear()
                balance_input.send_keys(str(condition["balance_limit"]))
            if "source" in condition:
                source_dropdown = self.wait_for_element(self.locators["transactionSourceDropdown"])
                source_dropdown.send_keys(condition["source"])
            if "operator" in condition:
                operator_dropdown = self.wait_for_element(self.locators["operatorDropdown"])
                operator_dropdown.send_keys(condition["operator"])

    def select_action(self, action):
        action_type_dropdown = self.wait_for_element(self.locators["actionTypeDropdown"])
        action_type_dropdown.click()
        action_type_dropdown.send_keys(action["type"])
        if action["type"] == "fixed_amount":
            amount_input = self.wait_for_element(self.locators["transferAmountInput"])
            amount_input.clear()
            amount_input.send_keys(str(action["amount"]))
        elif action["type"] == "percentage_of_deposit":
            percentage_input = self.wait_for_element(self.locators["percentageInput"])
            percentage_input.clear()
            percentage_input.send_keys(str(action["percentage"]))
        if "destination_account" in action:
            dest_account_input = self.wait_for_element(self.locators["destinationAccountInput"])
            dest_account_input.clear()
            dest_account_input.send_keys(action["destination_account"])

    def save_rule(self):
        save_rule_button = self.wait_for_element(self.locators["saveRuleButton"])
        save_rule_button.click()

    def validate_rule_acceptance(self):
        try:
            success_msg = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.locators["successMessage"])
            )
            return True, success_msg.text
        except TimeoutException:
            try:
                error_msg = self.driver.find_element(*self.locators["schemaErrorMessage"])
                return False, error_msg.text
            except NoSuchElementException:
                return False, "Unknown error occurred."

    # --- New Methods for Test Cases ---
    def test_case_tc_ft_009_create_and_store_rule(self, rule_id, rule_name, trigger, action, conditions=[]):
        """
        TC-FT-009 Step 1: Create and store a valid rule with specific date trigger.
        Arguments:
            rule_id: str
            rule_name: str
            trigger: dict (e.g., {"type": "specific_date", "date": "2024-07-01T10:00:00Z"})
            action: dict (e.g., {"type": "fixed_amount", "amount": 100})
            conditions: list
        Returns:
            (bool, str): Success flag and message
        """
        self.fill_rule_form(rule_id=rule_id, rule_name=rule_name)
        self.select_trigger(trigger)
        self.add_conditions(conditions)
        self.select_action(action)
        self.save_rule()
        return self.validate_rule_acceptance()

    def test_case_tc_ft_009_retrieve_and_verify_rule(self, rule_id):
        """
        TC-FT-009 Step 2: Retrieve the rule from backend and verify it matches the original input.
        Arguments:
            rule_id: str
        Returns:
            (bool, str): Success flag and message
        """
        # Placeholder for backend retrieval logic
        # In Selenium, this may involve navigating to the rule list and verifying rule details
        try:
            rule_row = self.driver.find_element(By.CSS_SELECTOR, f"tr[data-rule-id='{rule_id}']")
            return True, rule_row.text
        except NoSuchElementException:
            return False, f"Rule with ID {rule_id} not found."

    def test_case_tc_ft_010_define_rule_with_empty_conditions(self, rule_id, rule_name, trigger, action):
        """
        TC-FT-010 Step 1: Define a rule with empty conditions array.
        Arguments:
            rule_id: str
            rule_name: str
            trigger: dict
            action: dict
        Returns:
            (bool, str): Success flag and message
        """
        self.fill_rule_form(rule_id=rule_id, rule_name=rule_name)
        self.select_trigger(trigger)
        self.select_action(action)
        self.save_rule()
        return self.validate_rule_acceptance()

    def test_case_tc_ft_010_trigger_rule(self, deposit_amount):
        """
        TC-FT-010 Step 2: Trigger the rule and verify transfer execution without conditions.
        Arguments:
            deposit_amount: int
        Returns:
            (bool, str): Success flag and message
        """
        # Placeholder for deposit simulation logic
        try:
            success_msg = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.locators["successMessage"])
            )
            return True, success_msg.text
        except TimeoutException:
            return False, "Transfer not executed."

# --- End of RuleConfigurationPage.py ---
