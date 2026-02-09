# Pages/RuleConfigurationPage.py

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class RuleConfigurationPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # --- ruleForm ---
    def get_rule_id_input(self):
        return self.driver.find_element(By.ID, "rule-id-field")

    def get_rule_name_input(self):
        return self.driver.find_element(By.NAME, "rule-name")

    def get_save_rule_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

    # --- triggers ---
    def get_trigger_type_dropdown(self):
        return self.driver.find_element(By.ID, "trigger-type-select")

    def get_date_picker(self):
        return self.driver.find_element(By.CSS_SELECTOR, "input[type='date']")

    def get_recurring_interval_input(self):
        return self.driver.find_element(By.ID, "interval-value")

    def get_after_deposit_toggle(self):
        return self.driver.find_element(By.ID, "trigger-after-deposit")

    # --- conditions ---
    def get_add_condition_btn(self):
        return self.driver.find_element(By.ID, "add-condition-link")

    def get_condition_type_dropdown(self):
        return self.driver.find_element(By.CSS_SELECTOR, "select.condition-type")

    def get_balance_threshold_input(self):
        return self.driver.find_element(By.CSS_SELECTOR, "input[name='balance-limit']")

    def get_transaction_source_dropdown(self):
        return self.driver.find_element(By.ID, "source-provider-select")

    def get_operator_dropdown(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".condition-operator-select")

    # --- actions ---
    def get_action_type_dropdown(self):
        return self.driver.find_element(By.ID, "action-type-select")

    def get_transfer_amount_input(self):
        return self.driver.find_element(By.NAME, "fixed-amount")

    def get_percentage_input(self):
        return self.driver.find_element(By.ID, "deposit-percentage")

    def get_destination_account_input(self):
        return self.driver.find_element(By.ID, "target-account-id")

    # --- validation ---
    def get_json_schema_editor(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".monaco-editor")

    def get_validate_schema_btn(self):
        return self.driver.find_element(By.ID, "btn-verify-json")

    def get_success_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".alert-success")

    def get_schema_error_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "[data-testid='error-feedback-text']")