from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        # Rule Form
        self.rule_id_input = (By.ID, 'rule-id-field')
        self.rule_name_input = (By.NAME, 'rule-name')
        self.save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Triggers
        self.trigger_type_dropdown = (By.ID, 'trigger-type-select')
        self.date_picker = (By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = (By.ID, 'interval-value')
        self.after_deposit_toggle = (By.ID, 'trigger-after-deposit')
        # Conditions
        self.add_condition_btn = (By.ID, 'add-condition-link')
        self.condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = (By.ID, 'source-provider-select')
        self.operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')
        # Actions
        self.action_type_dropdown = (By.ID, 'action-type-select')
        self.transfer_amount_input = (By.NAME, 'fixed-amount')
        self.percentage_input = (By.ID, 'deposit-percentage')
        self.destination_account_input = (By.ID, 'target-account-id')
        # Validation
        self.json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = (By.ID, 'btn-verify-json')
        self.success_message = (By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def navigate_to_rule_creation(self):
        # Placeholder: Implement navigation logic as required by test framework
        pass

    def select_trigger_type(self, trigger_type):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.trigger_type_dropdown)
        )
        dropdown.click()
        dropdown.send_keys(trigger_type)

    def set_specific_date_trigger(self, date_str):
        date_picker = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.date_picker)
        )
        date_picker.clear()
        date_picker.send_keys(date_str)

    def add_balance_threshold_condition(self, operator, amount):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_condition_btn)
        )
        add_btn.click()
        operator_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.operator_dropdown)
        )
        operator_dropdown.click()
        operator_dropdown.send_keys(operator)
        balance_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.balance_threshold_input)
        )
        balance_input.clear()
        balance_input.send_keys(str(amount))

    def add_fixed_transfer_action(self, amount, destination_account):
        action_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.action_type_dropdown)
        )
        action_dropdown.click()
        action_dropdown.send_keys('fixed_transfer')
        amount_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.transfer_amount_input)
        )
        amount_input.clear()
        amount_input.send_keys(str(amount))
        destination_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.destination_account_input)
        )
        destination_input.clear()
        destination_input.send_keys(destination_account)

    def save_rule(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.save_rule_button)
        )
        save_btn.click()

    def validate_rule_schema(self):
        validate_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.validate_schema_btn)
        )
        validate_btn.click()
        try:
            success = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.success_message)
            )
            return True
        except:
            error = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(self.schema_error_message)
            )
            return False

    def get_rule_id(self):
        rule_id_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.rule_id_input)
        )
        return rule_id_input.get_attribute('value')

    def retrieve_saved_rule(self, rule_id):
        # Placeholder: Implement retrieval logic as per application interface
        pass

    def verify_rule_components(self, expected_trigger, expected_condition, expected_action):
        # Placeholder: Implement verification logic as per UI structure
        pass
