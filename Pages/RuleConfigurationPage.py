# RuleConfigurationPage.py
# Selenium Page Object for Rule Configuration Page

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class RuleConfigurationPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Rule Form Locators
        self.rule_id_input = driver.find_element(By.ID, "rule-id-field")
        self.rule_name_input = driver.find_element(By.NAME, "rule-name")
        self.save_rule_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Triggers Locators
        self.trigger_type_dropdown = driver.find_element(By.ID, "trigger-type-select")
        self.date_picker = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = driver.find_element(By.ID, "interval-value")
        self.after_deposit_toggle = driver.find_element(By.ID, "trigger-after-deposit")
        # Conditions Locators
        self.add_condition_btn = driver.find_element(By.ID, "add-condition-link")
        self.condition_type_dropdown = driver.find_element(By.CSS_SELECTOR, "select.condition-type")
        self.balance_threshold_input = driver.find_element(By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = driver.find_element(By.ID, "source-provider-select")
        self.operator_dropdown = driver.find_element(By.CSS_SELECTOR, ".condition-operator-select")
        # Actions Locators
        self.action_type_dropdown = driver.find_element(By.ID, "action-type-select")
        self.transfer_amount_input = driver.find_element(By.NAME, "fixed-amount")
        self.percentage_input = driver.find_element(By.ID, "deposit-percentage")
        self.destination_account_input = driver.find_element(By.ID, "target-account-id")
        # Validation Locators
        self.json_schema_editor = driver.find_element(By.CSS_SELECTOR, ".monaco-editor")
        self.validate_schema_btn = driver.find_element(By.ID, "btn-verify-json")
        self.success_message = driver.find_element(By.CSS_SELECTOR, ".alert-success")
        self.schema_error_message = driver.find_element(By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    # --- Rule Form Methods ---
    def enter_rule_id(self, rule_id: str):
        self.rule_id_input.clear()
        self.rule_id_input.send_keys(rule_id)

    def enter_rule_name(self, rule_name: str):
        self.rule_name_input.clear()
        self.rule_name_input.send_keys(rule_name)

    def click_save_rule(self):
        self.save_rule_button.click()

    # --- Triggers Methods ---
    def select_trigger_type(self, trigger_type: str):
        self.trigger_type_dropdown.click()
        # Implement dropdown selection logic for trigger_type

    def set_date_picker(self, date_value: str):
        self.date_picker.clear()
        self.date_picker.send_keys(date_value)

    def set_recurring_interval(self, interval_value: str):
        self.recurring_interval_input.clear()
        self.recurring_interval_input.send_keys(interval_value)

    def toggle_after_deposit(self):
        self.after_deposit_toggle.click()

    # --- Conditions Methods ---
    def click_add_condition(self):
        self.add_condition_btn.click()

    def select_condition_type(self, condition_type: str):
        self.condition_type_dropdown.click()
        # Implement dropdown selection logic for condition_type

    def enter_balance_threshold(self, threshold: str):
        self.balance_threshold_input.clear()
        self.balance_threshold_input.send_keys(threshold)

    def select_transaction_source(self, source: str):
        self.transaction_source_dropdown.click()
        # Implement dropdown selection logic for source

    def select_operator(self, operator: str):
        self.operator_dropdown.click()
        # Implement dropdown selection logic for operator

    # --- Actions Methods ---
    def select_action_type(self, action_type: str):
        self.action_type_dropdown.click()
        # Implement dropdown selection logic for action_type

    def enter_transfer_amount(self, amount: str):
        self.transfer_amount_input.clear()
        self.transfer_amount_input.send_keys(amount)

    def enter_percentage(self, percentage: str):
        self.percentage_input.clear()
        self.percentage_input.send_keys(percentage)

    def enter_destination_account(self, account_id: str):
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(account_id)

    # --- Validation Methods ---
    def enter_json_schema(self, schema_text: str):
        self.json_schema_editor.clear()
        self.json_schema_editor.send_keys(schema_text)

    def click_validate_schema(self):
        self.validate_schema_btn.click()

    def get_success_message(self) -> str:
        return self.success_message.text

    def get_schema_error_message(self) -> str:
        return self.schema_error_message.text
