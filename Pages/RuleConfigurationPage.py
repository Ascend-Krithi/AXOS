from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        # Rule Form Locators
        self.rule_id_input = (By.ID, 'rule-id-field')
        self.rule_name_input = (By.NAME, 'rule-name')
        self.save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Trigger Locators
        self.trigger_type_dropdown = (By.ID, 'trigger-type-select')
        self.date_picker = (By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = (By.ID, 'interval-value')
        self.after_deposit_toggle = (By.ID, 'trigger-after-deposit')
        # Condition Locators
        self.add_condition_btn = (By.ID, 'add-condition-link')
        self.condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit'")
        self.transaction_source_dropdown = (By.ID, 'source-provider-select')
        self.operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')
        # Action Locators
        self.action_type_dropdown = (By.ID, 'action-type-select')
        self.transfer_amount_input = (By.NAME, 'fixed-amount')
        self.percentage_input = (By.ID, 'deposit-percentage')
        self.destination_account_input = (By.ID, 'target-account-id')
        # Validation Locators
        self.json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = (By.ID, 'btn-verify-json')
        self.success_message = (By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def enter_rule_id(self, rule_id):
        self.driver.find_element(*self.rule_id_input).clear()
        self.driver.find_element(*self.rule_id_input).send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        self.driver.find_element(*self.rule_name_input).clear()
        self.driver.find_element(*self.rule_name_input).send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = self.driver.find_element(*self.trigger_type_dropdown)
        dropdown.click()
        option = dropdown.find_element(By.XPATH, f"//option[text()='{trigger_type}']")
        option.click()

    def set_date_picker(self, date_str):
        self.driver.find_element(*self.date_picker).send_keys(date_str)

    def set_recurring_interval(self, interval):
        self.driver.find_element(*self.recurring_interval_input).clear()
        self.driver.find_element(*self.recurring_interval_input).send_keys(str(interval))

    def toggle_after_deposit(self, enable=True):
        toggle = self.driver.find_element(*self.after_deposit_toggle)
        if (toggle.is_selected() != enable):
            toggle.click()

    def add_condition(self, condition_type, balance_threshold=None, transaction_source=None, operator=None):
        self.driver.find_element(*self.add_condition_btn).click()
        self.driver.find_element(*self.condition_type_dropdown).click()
        option = self.driver.find_element(By.XPATH, f"//option[text()='{condition_type}']")
        option.click()
        if balance_threshold is not None:
            self.driver.find_element(*self.balance_threshold_input).clear()
            self.driver.find_element(*self.balance_threshold_input).send_keys(str(balance_threshold))
        if transaction_source is not None:
            self.driver.find_element(*self.transaction_source_dropdown).click()
            src_option = self.driver.find_element(By.XPATH, f"//option[text()='{transaction_source}']")
            src_option.click()
        if operator is not None:
            self.driver.find_element(*self.operator_dropdown).click()
            op_option = self.driver.find_element(By.XPATH, f"//option[text()='{operator}']")
            op_option.click()

    def add_action(self, action_type, amount=None, percentage=None, destination_account=None):
        self.driver.find_element(*self.action_type_dropdown).click()
        option = self.driver.find_element(By.XPATH, f"//option[text()='{action_type}']")
        option.click()
        if amount is not None:
            self.driver.find_element(*self.transfer_amount_input).clear()
            self.driver.find_element(*self.transfer_amount_input).send_keys(str(amount))
        if percentage is not None:
            self.driver.find_element(*self.percentage_input).clear()
            self.driver.find_element(*self.percentage_input).send_keys(str(percentage))
        if destination_account is not None:
            self.driver.find_element(*self.destination_account_input).clear()
            self.driver.find_element(*self.destination_account_input).send_keys(destination_account)

    def enter_json_schema(self, schema_text):
        editor = self.driver.find_element(*self.json_schema_editor)
        editor.clear()
        editor.send_keys(schema_text)

    def validate_schema(self):
        self.driver.find_element(*self.validate_schema_btn).click()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.success_message)
            )
            return True
        except TimeoutException:
            return False

    def get_schema_error(self):
        try:
            error = self.driver.find_element(*self.schema_error_message)
            return error.text
        except Exception:
            return None

    def save_rule(self):
        self.driver.find_element(*self.save_rule_button).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.success_message)
        )

    def is_rule_saved_successfully(self):
        try:
            success = self.driver.find_element(*self.success_message)
            return success.is_displayed()
        except Exception:
            return False
