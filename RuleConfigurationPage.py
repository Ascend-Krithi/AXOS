import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class RuleConfigurationPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Rule Form Methods ---
    def set_rule_id(self, rule_id):
        rule_id_input = self.wait.until(EC.visibility_of_element_located((By.ID, 'rule-id-field')))
        rule_id_input.clear()
        rule_id_input.send_keys(rule_id)

    def set_rule_name(self, rule_name):
        rule_name_input = self.wait.until(EC.visibility_of_element_located((By.NAME, 'rule-name')))
        rule_name_input.clear()
        rule_name_input.send_keys(rule_name)

    def save_rule(self):
        save_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")))
        save_btn.click()

    # --- Triggers ---
    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, 'trigger-type-select')))
        dropdown.click()
        dropdown.send_keys(trigger_type)
        dropdown.send_keys(Keys.RETURN)

    def set_trigger_date(self, date_str):
        date_picker = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='date']")))
        date_picker.clear()
        date_picker.send_keys(date_str)

    def set_recurring_interval(self, interval):
        interval_input = self.wait.until(EC.visibility_of_element_located((By.ID, 'interval-value')))
        interval_input.clear()
        interval_input.send_keys(str(interval))

    def toggle_after_deposit(self, enable=True):
        toggle = self.wait.until(EC.element_to_be_clickable((By.ID, 'trigger-after-deposit')))
        if (toggle.get_attribute('aria-checked') == 'false' and enable) or (toggle.get_attribute('aria-checked') == 'true' and not enable):
            toggle.click()

    # --- Conditions ---
    def add_condition(self):
        add_btn = self.wait.until(EC.element_to_be_clickable((By.ID, 'add-condition-link')))
        add_btn.click()

    def select_condition_type(self, condition_type):
        dropdown = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select.condition-type')))
        dropdown.click()
        dropdown.send_keys(condition_type)
        dropdown.send_keys(Keys.RETURN)

    def set_balance_threshold(self, amount):
        threshold_input = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='balance-limit']")))
        threshold_input.clear()
        threshold_input.send_keys(str(amount))

    def select_transaction_source(self, source):
        dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, 'source-provider-select')))
        dropdown.click()
        dropdown.send_keys(source)
        dropdown.send_keys(Keys.RETURN)

    def select_operator(self, operator):
        dropdown = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.condition-operator-select')))
        dropdown.click()
        dropdown.send_keys(operator)
        dropdown.send_keys(Keys.RETURN)

    # --- Actions ---
    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, 'action-type-select')))
        dropdown.click()
        dropdown.send_keys(action_type)
        dropdown.send_keys(Keys.RETURN)

    def set_transfer_amount(self, amount):
        amount_input = self.wait.until(EC.visibility_of_element_located((By.NAME, 'fixed-amount')))
        amount_input.clear()
        amount_input.send_keys(str(amount))

    def set_percentage(self, percentage):
        percentage_input = self.wait.until(EC.visibility_of_element_located((By.ID, 'deposit-percentage')))
        percentage_input.clear()
        percentage_input.send_keys(str(percentage))

    def set_destination_account(self, account_id):
        dest_input = self.wait.until(EC.visibility_of_element_located((By.ID, 'target-account-id')))
        dest_input.clear()
        dest_input.send_keys(account_id)

    # --- Validation ---
    def edit_json_schema(self, schema_text):
        editor = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.monaco-editor')))
        editor.click()
        editor.clear()
        editor.send_keys(schema_text)

    def validate_schema(self):
        validate_btn = self.wait.until(EC.element_to_be_clickable((By.ID, 'btn-verify-json')))
        validate_btn.click()

    def get_validation_success_message(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-success'))).text

    def get_schema_error_message(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='error-feedback-text']"))).text

    # --- Rule Retrieval & Verification ---
    def retrieve_rule_by_id(self, rule_id):
        self.set_rule_id(rule_id)
        # Assume retrieval is triggered by entering rule_id
        time.sleep(1)

    def verify_rule_components(self, expected):
        # expected: dict with keys 'trigger', 'condition', 'action'
        # Implement detailed checks as needed
        pass