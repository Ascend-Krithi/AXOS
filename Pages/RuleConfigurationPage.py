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
        # Select trigger type
        if trigger["type"] == "after_deposit":
            after_deposit_toggle = self.wait_for_element(self.locators["afterDepositToggle"])
            if not after_deposit_toggle.is_selected():
                after_deposit_toggle.click()
        elif trigger["type"] == "currency_conversion":
            # Attempt to select currency_conversion if present
            try:
                dropdown = self.wait_for_element(self.locators["triggerTypeDropdown"])
                dropdown.send_keys("currency_conversion")
                if "currency" in trigger:
                    date_picker = self.wait_for_element(self.locators["datePicker"])
                    date_picker.clear()
                    date_picker.send_keys(trigger["currency"])
            except (TimeoutException, NoSuchElementException):
                pass  # Gracefully handle unsupported trigger
        else:
            # Handle other trigger types as needed
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
        if action["type"] == "percentage_of_deposit":
            percentage_input = self.wait_for_element(self.locators["percentageInput"])
            percentage_input.clear()
            percentage_input.send_keys(str(action["percentage"]))
        elif action["type"] == "fixed_amount":
            amount_input = self.wait_for_element(self.locators["transferAmountInput"])
            amount_input.clear()
            amount_input.send_keys(str(action["amount"]))
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

    def define_rule(self, rule_id, rule_name, trigger, action, conditions=[]):
        self.fill_rule_form(rule_id=rule_id, rule_name=rule_name)
        self.select_trigger(trigger)
        self.add_conditions(conditions)
        self.select_action(action)
        self.save_rule()
        return self.validate_rule_acceptance()

    def simulate_deposit(self, amount):
        # This method assumes testability hooks or UI for deposit simulation
        # Placeholder for actual simulation logic
        # For demonstration, we'll assume a deposit triggers a rule and verify transfer
        # Wait for success message indicating transfer
        try:
            success_msg = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.locators["successMessage"])
            )
            return True, success_msg.text
        except TimeoutException:
            return False, "Transfer not executed."

    def define_future_rule_type(self, rule_id, rule_name, trigger, action, conditions=[]):
        self.fill_rule_form(rule_id=rule_id, rule_name=rule_name)
        self.select_trigger(trigger)
        self.add_conditions(conditions)
        self.select_action(action)
        self.save_rule()
        return self.validate_rule_acceptance()

    def verify_existing_rules_execution(self):
        # Placeholder for actual verification logic
        # This could involve checking that existing rules still trigger as expected
        try:
            success_msg = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.locators["successMessage"])
            )
            return True, success_msg.text
        except TimeoutException:
            return False, "Existing rules not executed as expected."

    # Test case methods
    def tc_define_10_percent_deposit_rule(self, rule_id, rule_name):
        trigger = {"type": "after_deposit"}
        action = {"type": "percentage_of_deposit", "percentage": 10}
        conditions = []
        return self.define_rule(rule_id, rule_name, trigger, action, conditions)

    def tc_simulate_deposit_and_verify_transfer(self, deposit_amount, expected_transfer):
        result, msg = self.simulate_deposit(deposit_amount)
        if result and str(expected_transfer) in msg:
            return True, msg
        return False, msg

    def tc_define_currency_conversion_rule(self, rule_id, rule_name):
        trigger = {"type": "currency_conversion", "currency": "EUR"}
        action = {"type": "fixed_amount", "amount": 100}
        conditions = []
        return self.define_future_rule_type(rule_id, rule_name, trigger, action, conditions)

    def tc_verify_existing_rules(self):
        return self.verify_existing_rules_execution()
