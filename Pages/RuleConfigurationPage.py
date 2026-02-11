# RuleConfigurationPage.py
# Selenium PageClass for Rule Configuration Page
# Covers rule creation, triggers, conditions, actions, saving, retrieving, and validation

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver

class RuleConfigurationPage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Locators
    locators = {
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

    # --- Rule Form ---
    def set_rule_id(self, rule_id: str):
        rule_id_input = self.wait.until(EC.visibility_of_element_located(self.locators["ruleIdInput"]))
        rule_id_input.clear()
        rule_id_input.send_keys(rule_id)

    def set_rule_name(self, rule_name: str):
        rule_name_input = self.wait.until(EC.visibility_of_element_located(self.locators["ruleNameInput"]))
        rule_name_input.clear()
        rule_name_input.send_keys(rule_name)

    # --- Triggers ---
    def select_trigger_type(self, trigger_type: str):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.locators["triggerTypeDropdown"]))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='trigger-type-select']/option[@value='{trigger_type}']")))
        option.click()

    def set_specific_date_trigger(self, date_str: str):
        self.select_trigger_type("specific_date")
        date_picker = self.wait.until(EC.visibility_of_element_located(self.locators["datePicker"]))
        date_picker.clear()
        date_picker.send_keys(date_str)

    def set_recurring_trigger(self, interval_value: str):
        self.select_trigger_type("recurring")
        interval_input = self.wait.until(EC.visibility_of_element_located(self.locators["recurringIntervalInput"]))
        interval_input.clear()
        interval_input.send_keys(interval_value)

    def toggle_after_deposit(self, enable: bool):
        toggle = self.wait.until(EC.element_to_be_clickable(self.locators["afterDepositToggle"]))
        if toggle.is_selected() != enable:
            toggle.click()

    # --- Conditions ---
    def add_condition(self):
        add_btn = self.wait.until(EC.element_to_be_clickable(self.locators["addConditionBtn"]))
        add_btn.click()

    def select_condition_type(self, condition_type: str):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.locators["conditionTypeDropdown"]))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[contains(@class, 'condition-type')]/option[@value='{condition_type}']")))
        option.click()

    def set_balance_threshold_condition(self, operator: str, amount: float):
        self.select_condition_type("balance_threshold")
        operator_dropdown = self.wait.until(EC.element_to_be_clickable(self.locators["operatorDropdown"]))
        operator_dropdown.click()
        operator_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[contains(@class, 'condition-operator-select')]/option[@value='{operator}']")))
        operator_option.click()
        balance_input = self.wait.until(EC.visibility_of_element_located(self.locators["balanceThresholdInput"]))
        balance_input.clear()
        balance_input.send_keys(str(amount))

    def select_transaction_source(self, source_provider: str):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.locators["transactionSourceDropdown"]))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='source-provider-select']/option[@value='{source_provider}']")))
        option.click()

    # --- Actions ---
    def select_action_type(self, action_type: str):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.locators["actionTypeDropdown"]))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='action-type-select']/option[@value='{action_type}']")))
        option.click()

    def set_fixed_transfer_action(self, amount: float, destination_account: str):
        self.select_action_type("fixed_transfer")
        amount_input = self.wait.until(EC.visibility_of_element_located(self.locators["transferAmountInput"]))
        amount_input.clear()
        amount_input.send_keys(str(amount))
        destination_input = self.wait.until(EC.visibility_of_element_located(self.locators["destinationAccountInput"]))
        destination_input.clear()
        destination_input.send_keys(destination_account)

    def set_percentage_transfer_action(self, percentage: float, destination_account: str):
        self.select_action_type("percentage_transfer")
        percentage_input = self.wait.until(EC.visibility_of_element_located(self.locators["percentageInput"]))
        percentage_input.clear()
        percentage_input.send_keys(str(percentage))
        destination_input = self.wait.until(EC.visibility_of_element_located(self.locators["destinationAccountInput"]))
        destination_input.clear()
        destination_input.send_keys(destination_account)

    # --- Validation ---
    def validate_json_schema(self):
        validate_btn = self.wait.until(EC.element_to_be_clickable(self.locators["validateSchemaBtn"]))
        validate_btn.click()
        try:
            success_msg = self.wait.until(EC.visibility_of_element_located(self.locators["successMessage"]))
            return True, success_msg.text
        except TimeoutException:
            error_msg = self.wait.until(EC.visibility_of_element_located(self.locators["schemaErrorMessage"]))
            return False, error_msg.text

    # --- Save Rule ---
    def save_rule(self):
        save_btn = self.wait.until(EC.element_to_be_clickable(self.locators["saveRuleButton"]))
        save_btn.click()
        try:
            success_msg = self.wait.until(EC.visibility_of_element_located(self.locators["successMessage"]))
            return True, success_msg.text
        except TimeoutException:
            return False, "Rule save failed or success message not found."

    # --- Retrieve Rule ---
    def get_rule_id(self):
        rule_id_input = self.wait.until(EC.visibility_of_element_located(self.locators["ruleIdInput"]))
        return rule_id_input.get_attribute("value")

    def get_rule_name(self):
        rule_name_input = self.wait.until(EC.visibility_of_element_located(self.locators["ruleNameInput"]))
        return rule_name_input.get_attribute("value")

    def get_trigger_type(self):
        dropdown = self.wait.until(EC.visibility_of_element_located(self.locators["triggerTypeDropdown"]))
        selected_option = dropdown.find_element(By.XPATH, "./option[@selected]")
        return selected_option.get_attribute("value")

    def get_trigger_date(self):
        date_picker = self.wait.until(EC.visibility_of_element_located(self.locators["datePicker"]))
        return date_picker.get_attribute("value")

    def get_balance_threshold(self):
        balance_input = self.wait.until(EC.visibility_of_element_located(self.locators["balanceThresholdInput"]))
        return balance_input.get_attribute("value")

    def get_action_amount(self):
        amount_input = self.wait.until(EC.visibility_of_element_located(self.locators["transferAmountInput"]))
        return amount_input.get_attribute("value")

    def get_destination_account(self):
        destination_input = self.wait.until(EC.visibility_of_element_located(self.locators["destinationAccountInput"]))
        return destination_input.get_attribute("value")

    # --- Composite Methods for End-to-End Steps ---
    def create_rule(self, rule_id: str, rule_name: str, trigger_type: str, trigger_date: str, condition_operator: str, condition_amount: float, action_amount: float, destination_account: str):
        self.set_rule_id(rule_id)
        self.set_rule_name(rule_name)
        if trigger_type == "specific_date":
            self.set_specific_date_trigger(trigger_date)
        # Add more trigger types as needed
        self.add_condition()
        self.set_balance_threshold_condition(condition_operator, condition_amount)
        self.set_fixed_transfer_action(action_amount, destination_account)
        valid, msg = self.validate_json_schema()
        if not valid:
            raise AssertionError(f"Schema validation failed: {msg}")
        saved, save_msg = self.save_rule()
        if not saved:
            raise AssertionError(f"Rule save failed: {save_msg}")
        return self.get_rule_id()

    def retrieve_and_validate_rule(self, expected_trigger_type: str, expected_trigger_date: str, expected_condition_amount: float, expected_action_amount: float, expected_destination_account: str):
        actual_trigger_type = self.get_trigger_type()
        actual_trigger_date = self.get_trigger_date()
        actual_condition_amount = float(self.get_balance_threshold())
        actual_action_amount = float(self.get_action_amount())
        actual_destination_account = self.get_destination_account()
        assert actual_trigger_type == expected_trigger_type, f"Trigger type mismatch: {actual_trigger_type} != {expected_trigger_type}"
        assert actual_trigger_date == expected_trigger_date, f"Trigger date mismatch: {actual_trigger_date} != {expected_trigger_date}"
        assert actual_condition_amount == expected_condition_amount, f"Condition amount mismatch: {actual_condition_amount} != {expected_condition_amount}"
        assert actual_action_amount == expected_action_amount, f"Action amount mismatch: {actual_action_amount} != {expected_action_amount}"
        assert actual_destination_account == expected_destination_account, f"Destination account mismatch: {actual_destination_account} != {expected_destination_account}"
        return True
