import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class RuleConfigurationPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Rule Form
        self.rule_id_input = driver.find_element(By.ID, 'rule-id-field')
        self.rule_name_input = driver.find_element(By.NAME, 'rule-name')
        self.save_rule_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Triggers
        self.trigger_type_dropdown = driver.find_element(By.ID, 'trigger-type-select')
        self.date_picker = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = driver.find_element(By.ID, 'interval-value')
        self.after_deposit_toggle = driver.find_element(By.ID, 'trigger-after-deposit')
        # Conditions
        self.add_condition_btn = driver.find_element(By.ID, 'add-condition-link')
        self.condition_type_dropdown = driver.find_element(By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = driver.find_element(By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = driver.find_element(By.ID, 'source-provider-select')
        self.operator_dropdown = driver.find_element(By.CSS_SELECTOR, '.condition-operator-select')
        # Actions
        self.action_type_dropdown = driver.find_element(By.ID, 'action-type-select')
        self.transfer_amount_input = driver.find_element(By.NAME, 'fixed-amount')
        self.percentage_input = driver.find_element(By.ID, 'deposit-percentage')
        self.destination_account_input = driver.find_element(By.ID, 'target-account-id')
        # Validation
        self.json_schema_editor = driver.find_element(By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = driver.find_element(By.ID, 'btn-verify-json')
        self.success_message = driver.find_element(By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = driver.find_element(By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    def set_rule_id(self, rule_id):
        self.rule_id_input.clear()
        self.rule_id_input.send_keys(rule_id)

    def set_rule_name(self, rule_name):
        self.rule_name_input.clear()
        self.rule_name_input.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        self.trigger_type_dropdown.click()
        self.trigger_type_dropdown.send_keys(trigger_type)

    def set_trigger_date(self, date_str):
        self.date_picker.clear()
        self.date_picker.send_keys(date_str)

    def set_recurring_interval(self, interval):
        self.recurring_interval_input.clear()
        self.recurring_interval_input.send_keys(str(interval))

    def toggle_after_deposit(self):
        self.after_deposit_toggle.click()

    def add_condition(self):
        self.add_condition_btn.click()

    def select_condition_type(self, condition_type):
        self.condition_type_dropdown.click()
        self.condition_type_dropdown.send_keys(condition_type)

    def set_balance_threshold(self, amount):
        self.balance_threshold_input.clear()
        self.balance_threshold_input.send_keys(str(amount))

    def select_transaction_source(self, source):
        self.transaction_source_dropdown.click()
        self.transaction_source_dropdown.send_keys(source)

    def select_operator(self, operator):
        self.operator_dropdown.click()
        self.operator_dropdown.send_keys(operator)

    def select_action_type(self, action_type):
        self.action_type_dropdown.click()
        self.action_type_dropdown.send_keys(action_type)

    def set_transfer_amount(self, amount):
        self.transfer_amount_input.clear()
        self.transfer_amount_input.send_keys(str(amount))

    def set_percentage(self, percentage):
        self.percentage_input.clear()
        self.percentage_input.send_keys(str(percentage))

    def set_destination_account(self, account_id):
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(account_id)

    def validate_json_schema(self):
        self.validate_schema_btn.click()

    def get_success_message(self):
        return self.success_message.text

    def get_schema_error_message(self):
        return self.schema_error_message.text

    def save_rule(self):
        self.save_rule_button.click()

    # --- New Methods for Negative Testing and Validation ---
    def submit_rule_form(self):
        """
        Submits the rule form by clicking the save button.
        """
        self.save_rule_button.click()

    def get_validation_errors(self):
        """
        Returns structured validation errors from the schema error message area.
        """
        return self.schema_error_message.text

    def is_error_message_displayed(self):
        """
        Checks if error message is displayed after form submission.
        """
        try:
            return self.schema_error_message.is_displayed()
        except Exception:
            return False

    def get_error_fields_and_messages(self):
        """
        Extracts error fields and messages from the validation response.
        Returns: List[Dict[str, str]]
        """
        import json
        try:
            error_text = self.schema_error_message.text
            if error_text:
                # Attempt to parse structured error if possible
                return json.loads(error_text)
        except Exception:
            pass
        return []

    def fill_rule_form(self, rule_data):
        """
        Fills the rule form with provided data dictionary.
        """
        if 'rule_id' in rule_data:
            self.set_rule_id(rule_data['rule_id'])
        if 'rule_name' in rule_data:
            self.set_rule_name(rule_data['rule_name'])
        # Triggers
        triggers = rule_data.get('triggers', [])
        if isinstance(triggers, list):
            for trigger in triggers:
                if 'type' in trigger:
                    self.select_trigger_type(trigger['type'])
        # Conditions
        conditions = rule_data.get('conditions', [])
        if isinstance(conditions, list):
            for cond in conditions:
                self.add_condition()
                if 'field' in cond:
                    self.select_condition_type(cond['field'])
                if 'operator' in cond:
                    self.select_operator(cond['operator'])
                if 'value' in cond:
                    self.set_balance_threshold(cond['value'])
        # Actions
        actions = rule_data.get('actions', [])
        if isinstance(actions, list):
            for act in actions:
                if 'type' in act:
                    self.select_action_type(act['type'])
                if 'amount' in act:
                    self.set_transfer_amount(act['amount'])
                if 'percentage' in act:
                    self.set_percentage(act['percentage'])
                if 'destination_account' in act:
                    self.set_destination_account(act['destination_account'])

    def fill_and_submit_rule(self, rule_data):
        """
        Fills the rule form and submits it, for negative validation flows.
        """
        self.fill_rule_form(rule_data)
        self.save_rule_button.click()
        return self.get_validation_errors()
