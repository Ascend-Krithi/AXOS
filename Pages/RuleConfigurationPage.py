from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        # Rule Form Locators
        self.rule_id_input = driver.find_element(By.ID, 'rule-id-field')
        self.rule_name_input = driver.find_element(By.NAME, 'rule-name')
        self.save_rule_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Trigger Locators
        self.trigger_type_dropdown = driver.find_element(By.ID, 'trigger-type-select')
        self.date_picker = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = driver.find_element(By.ID, 'interval-value')
        self.after_deposit_toggle = driver.find_element(By.ID, 'trigger-after-deposit')
        # Condition Locators
        self.add_condition_btn = driver.find_element(By.ID, 'add-condition-link')
        self.condition_type_dropdown = driver.find_element(By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = driver.find_element(By.CSS_SELECTOR, "input[name='balance-limit'")
        self.transaction_source_dropdown = driver.find_element(By.ID, 'source-provider-select')
        self.operator_dropdown = driver.find_element(By.CSS_SELECTOR, '.condition-operator-select')
        # Action Locators
        self.action_type_dropdown = driver.find_element(By.ID, 'action-type-select')
        self.transfer_amount_input = driver.find_element(By.NAME, 'fixed-amount')
        self.percentage_input = driver.find_element(By.ID, 'deposit-percentage')
        self.destination_account_input = driver.find_element(By.ID, 'target-account-id')
        # Validation Locators
        self.json_schema_editor = driver.find_element(By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = driver.find_element(By.ID, 'btn-verify-json')
        self.success_message = driver.find_element(By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = driver.find_element(By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    def fill_rule_form(self, rule_id, rule_name):
        self.rule_id_input.clear()
        self.rule_id_input.send_keys(rule_id)
        self.rule_name_input.clear()
        self.rule_name_input.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        self.trigger_type_dropdown.click()
        # Add selection logic as needed

    def set_date(self, date_value):
        self.date_picker.clear()
        self.date_picker.send_keys(date_value)

    def set_recurring_interval(self, interval):
        self.recurring_interval_input.clear()
        self.recurring_interval_input.send_keys(interval)

    def toggle_after_deposit(self, enable=True):
        current_state = self.after_deposit_toggle.is_selected()
        if enable != current_state:
            self.after_deposit_toggle.click()

    def add_condition(self, condition_type, balance_threshold, transaction_source, operator):
        self.add_condition_btn.click()
        self.condition_type_dropdown.click()
        # Add selection logic as needed
        self.balance_threshold_input.clear()
        self.balance_threshold_input.send_keys(balance_threshold)
        self.transaction_source_dropdown.click()
        # Add selection logic as needed
        self.operator_dropdown.click()
        # Add selection logic as needed

    def add_action(self, action_type, amount, percentage, destination_account):
        self.action_type_dropdown.click()
        # Add selection logic as needed
        self.transfer_amount_input.clear()
        self.transfer_amount_input.send_keys(amount)
        self.percentage_input.clear()
        self.percentage_input.send_keys(percentage)
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(destination_account)

    def edit_json_schema(self, schema_text):
        self.json_schema_editor.clear()
        self.json_schema_editor.send_keys(schema_text)

    def validate_schema(self):
        self.validate_schema_btn.click()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of(self.success_message)
            )
            return True
        except:
            return False

    def get_schema_error(self):
        return self.schema_error_message.text

    def save_rule(self):
        self.save_rule_button.click()
