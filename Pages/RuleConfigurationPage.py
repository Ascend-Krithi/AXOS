from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators
    rule_id_input = (By.ID, 'rule-id-field')
    rule_name_input = (By.NAME, 'rule-name')
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
    trigger_type_dropdown = (By.ID, 'trigger-type-select')
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, 'interval-value')
    after_deposit_toggle = (By.ID, 'trigger-after-deposit')
    add_condition_btn = (By.ID, 'add-condition-link')
    condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
    balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
    transaction_source_dropdown = (By.ID, 'source-provider-select')
    operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')
    action_type_dropdown = (By.ID, 'action-type-select')
    transfer_amount_input = (By.NAME, 'fixed-amount')
    percentage_input = (By.ID, 'deposit-percentage')
    destination_account_input = (By.ID, 'target-account-id')
    json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
    validate_schema_btn = (By.ID, 'btn-verify-json')
    success_message = (By.CSS_SELECTOR, '.alert-success')
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def fill_rule_form(self, rule_id: str, rule_name: str):
        self.wait.until(EC.visibility_of_element_located(self.rule_id_input)).send_keys(rule_id)
        self.wait.until(EC.visibility_of_element_located(self.rule_name_input)).send_keys(rule_name)

    def select_trigger(self, trigger_type: str, interval_value: str = None):
        trigger_dropdown = self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown))
        trigger_dropdown.click()
        # Select trigger type
        option = self.driver.find_element(By.XPATH, f"//option[@value='{trigger_type}']")
        option.click()
        if trigger_type == 'interval' and interval_value:
            interval_input = self.wait.until(EC.visibility_of_element_located(self.recurring_interval_input))
            interval_input.clear()
            interval_input.send_keys(interval_value)

    def add_condition(self, condition_type: str, operator: str, value: str):
        self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
        dropdown = self.wait.until(EC.element_to_be_clickable(self.condition_type_dropdown))
        dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//option[@value='{condition_type}']")
        option.click()
        operator_dropdown = self.wait.until(EC.element_to_be_clickable(self.operator_dropdown))
        operator_dropdown.click()
        operator_option = self.driver.find_element(By.XPATH, f"//option[@value='{operator}']")
        operator_option.click()
        value_input = self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input))
        value_input.clear()
        value_input.send_keys(str(value))

    def add_action(self, action_type: str, account: str = None, amount: str = None, message: str = None):
        action_dropdown = self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown))
        action_dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//option[@value='{action_type}']")
        option.click()
        if action_type == 'transfer':
            account_input = self.wait.until(EC.visibility_of_element_located(self.destination_account_input))
            account_input.clear()
            account_input.send_keys(account)
            amount_input = self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input))
            amount_input.clear()
            amount_input.send_keys(str(amount))
        elif action_type == 'notify' and message:
            # Assuming a message input exists
            message_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='notify-message']")
            message_input.clear()
            message_input.send_keys(message)

    def input_json_schema(self, schema_json: str):
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.clear()
        editor.send_keys(schema_json)

    def validate_schema(self):
        self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn)).click()

    def save_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    def get_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.success_message)).text

    def get_schema_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.schema_error_message)).text

    def create_rule(self, rule_id: str, rule_name: str, trigger: dict, conditions: list, actions: list, schema_json: str):
        self.fill_rule_form(rule_id, rule_name)
        self.select_trigger(trigger['type'], trigger.get('value'))
        for cond in conditions:
            self.add_condition(cond['type'], cond['operator'], cond['value'])
        for act in actions:
            self.add_action(act['type'], act.get('account'), act.get('amount'), act.get('message'))
        self.input_json_schema(schema_json)
        self.validate_schema()
        self.save_rule()
        return self.get_success_message()
