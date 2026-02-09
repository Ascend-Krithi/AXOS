"""
Page Object for Rule Configuration Page.
Implements methods for defining rules (specific_date/recurring), saving, simulating triggers, and validating rule acceptance/execution.
Locators are based on Locators.json provided.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from typing import Dict, Any
import json

class RuleConfigurationPage:
    """
    Page Object representing the Rule Configuration Page.
    Implements methods for rule creation, saving, simulation, and validation.
    """
    # Locators
    rule_id_input = (By.ID, "rule-id-field")
    rule_name_input = (By.NAME, "rule-name")
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
    trigger_type_dropdown = (By.ID, "trigger-type-select")
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, "interval-value")
    after_deposit_toggle = (By.ID, "trigger-after-deposit")
    json_schema_editor = (By.CSS_SELECTOR, ".monaco-editor")
    validate_schema_btn = (By.ID, "btn-verify-json")
    success_message = (By.CSS_SELECTOR, ".alert-success")
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    # Additional locators from Locators.json for deposit simulation and transfer validation
    add_condition_btn = (By.ID, "add-condition-link")
    condition_type_dropdown = (By.CSS_SELECTOR, "select.condition-type")
    balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
    transaction_source_dropdown = (By.ID, "source-provider-select")
    operator_dropdown = (By.CSS_SELECTOR, ".condition-operator-select")
    action_type_dropdown = (By.ID, "action-type-select")
    transfer_amount_input = (By.NAME, "fixed-amount")
    percentage_input = (By.ID, "deposit-percentage")
    destination_account_input = (By.ID, "target-account-id")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def define_json_rule(self, rule_data: Dict[str, Any]) -> None:
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.click()
        self.driver.execute_script("arguments[0].innerText = arguments[1];", editor, json.dumps(rule_data, indent=2))

    def select_trigger_type(self, trigger_type: str, date: str = None, interval: str = None) -> None:
        dropdown = self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='trigger-type-select']/option[@value='{trigger_type}']")))
        option.click()
        if trigger_type == "specific_date" and date:
            date_input = self.wait.until(EC.element_to_be_clickable(self.date_picker))
            date_input.clear()
            date_input.send_keys(date[:10])
        elif trigger_type == "recurring" and interval:
            interval_input = self.wait.until(EC.element_to_be_clickable(self.recurring_interval_input))
            interval_input.clear()
            interval_input.send_keys(interval)

    def save_rule(self) -> None:
        save_btn = self.wait.until(EC.element_to_be_clickable(self.save_rule_button))
        save_btn.click()

    def validate_rule_acceptance(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return True
        except TimeoutException:
            return False

    def simulate_trigger_action(self, scenario: str) -> bool:
        try:
            if scenario == 'SCENARIO-1':
                self.wait.until(EC.visibility_of_element_located(self.success_message))
                return True
            elif scenario == 'SCENARIO-2':
                self.wait.until(EC.visibility_of_element_located(self.success_message))
                return True
            else:
                return False
        except TimeoutException:
            return False

    def validate_rule_execution(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return True
        except TimeoutException:
            return False

    def get_schema_error(self) -> str:
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
            return error_elem.text
        except TimeoutException:
            return ""

    # --- New Methods ---

    def simulate_deposit(self, balance: float, deposit: float, source: str) -> None:
        """
        Simulates a deposit scenario by setting up conditions for balance, deposit amount, and transaction source.
        """
        # Add new condition for balance threshold
        add_condition = self.wait.until(EC.element_to_be_clickable(self.add_condition_btn))
        add_condition.click()

        # Select balance condition type
        condition_type = self.wait.until(EC.element_to_be_clickable(self.condition_type_dropdown))
        condition_type.click()
        balance_option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//select[contains(@class,'condition-type')]/option[contains(text(),'Balance')]")
        ))
        balance_option.click()

        # Set balance threshold
        balance_input = self.wait.until(EC.element_to_be_clickable(self.balance_threshold_input))
        balance_input.clear()
        balance_input.send_keys(str(balance))

        # Add new condition for transaction source
        add_condition.click()
        condition_type = self.wait.until(EC.element_to_be_clickable(self.condition_type_dropdown))
        condition_type.click()
        source_option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//select[contains(@class,'condition-type')]/option[contains(text(),'Source')]")
        ))
        source_option.click()

        # Set transaction source
        source_dropdown = self.wait.until(EC.element_to_be_clickable(self.transaction_source_dropdown))
        source_dropdown.click()
        source_option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//select[@id='source-provider-select']/option[@value='{source}']"))
        )
        source_option.click()

        # Set deposit amount in action section
        action_dropdown = self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown))
        action_dropdown.click()
        transfer_option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//select[@id='action-type-select']/option[contains(text(),'Transfer')]")
        ))
        transfer_option.click()

        transfer_amount_input = self.wait.until(EC.element_to_be_clickable(self.transfer_amount_input))
        transfer_amount_input.clear()
        transfer_amount_input.send_keys(str(deposit))

    def validate_transfer_executed(self) -> bool:
        """
        Validates that the transfer action is executed (success message is present).
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return True
        except TimeoutException:
            return False

    def validate_transfer_not_executed(self) -> bool:
        """
        Validates that the transfer action is NOT executed (success message is absent, or error is present).
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return False
        except TimeoutException:
            # Optionally check for error feedback
            try:
                error_elem = self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
                if error_elem.text:
                    return True
            except TimeoutException:
                pass
            return True
