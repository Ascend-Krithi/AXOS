# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object Model for the Rule Configuration Page.
    Provides methods to create rules, configure triggers, actions, and validate rule schemas.
    """

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Locators from Locators.json
    rule_id_input = (By.ID, "rule-id-field")
    rule_name_input = (By.NAME, "rule-name")
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

    trigger_type_dropdown = (By.ID, "trigger-type-select")
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, "interval-value")
    after_deposit_toggle = (By.ID, "trigger-after-deposit")

    add_condition_btn = (By.ID, "add-condition-link")
    condition_type_dropdown = (By.CSS_SELECTOR, "select.condition-type")
    balance_threshold_input = (By.NAME, "balance-limit")
    transaction_source_dropdown = (By.ID, "source-provider-select")
    operator_dropdown = (By.CSS_SELECTOR, ".condition-operator-select")

    action_type_dropdown = (By.ID, "action-type-select")
    transfer_amount_input = (By.NAME, "fixed-amount")
    percentage_input = (By.ID, "deposit-percentage")
    destination_account_input = (By.ID, "target-account-id")

    json_schema_editor = (By.CSS_SELECTOR, ".monaco-editor")
    validate_schema_btn = (By.ID, "btn-verify-json")
    success_message = (By.CSS_SELECTOR, ".alert-success")
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    # Methods

    def enter_rule_id(self, rule_id):
        elem = self.wait.until(EC.visibility_of_element_located(self.rule_id_input))
        elem.clear()
        elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        elem = self.wait.until(EC.visibility_of_element_located(self.rule_name_input))
        elem.clear()
        elem.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown))
        dropdown.click()
        option = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//select[@id='trigger-type-select']/option[@value='{trigger_type}']")))
        option.click()

    def set_specific_date(self, date_str):
        date_input = self.wait.until(EC.visibility_of_element_located(self.date_picker))
        date_input.clear()
        date_input.send_keys(date_str)

    def set_recurring_interval(self, interval_value):
        interval_input = self.wait.until(EC.visibility_of_element_located(self.recurring_interval_input))
        interval_input.clear()
        interval_input.send_keys(interval_value)

    def toggle_after_deposit(self, enable=True):
        toggle = self.wait.until(EC.element_to_be_clickable(self.after_deposit_toggle))
        if (toggle.is_selected() != enable):
            toggle.click()

    def add_condition(self, condition_type, operator, threshold=None, source=None):
        self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
        condition_type_elem = self.wait.until(EC.visibility_of_element_located(self.condition_type_dropdown))
        condition_type_elem.click()
        option = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//select[contains(@class,'condition-type')]/option[@value='{condition_type}']")))
        option.click()

        operator_elem = self.wait.until(EC.visibility_of_element_located(self.operator_dropdown))
        operator_elem.click()
        op_option = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//select[contains(@class,'condition-operator-select')]/option[@value='{operator}']")))
        op_option.click()

        if threshold is not None:
            threshold_elem = self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input))
            threshold_elem.clear()
            threshold_elem.send_keys(str(threshold))

        if source is not None:
            source_elem = self.wait.until(EC.visibility_of_element_located(self.transaction_source_dropdown))
            source_elem.click()
            src_option = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, f"//select[@id='source-provider-select']/option[@value='{source}']")))
            src_option.click()

    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown))
        dropdown.click()
        option = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//select[@id='action-type-select']/option[@value='{action_type}']")))
        option.click()

    def set_fixed_amount(self, amount):
        amount_input = self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input))
        amount_input.clear()
        amount_input.send_keys(str(amount))

    def set_percentage_of_deposit(self, percentage):
        percentage_input = self.wait.until(EC.visibility_of_element_located(self.percentage_input))
        percentage_input.clear()
        percentage_input.send_keys(str(percentage))

    def set_destination_account(self, account_id):
        dest_input = self.wait.until(EC.visibility_of_element_located(self.destination_account_input))
        dest_input.clear()
        dest_input.send_keys(account_id)

    def enter_json_schema(self, json_text):
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.click()
        # Assuming direct input is supported; otherwise, use JS executor
        self.driver.execute_script("arguments[0].innerText = arguments[1];", editor, json_text)

    def validate_schema(self):
        self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn)).click()

    def get_success_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.success_message)).text
        except Exception:
            return None

    def get_schema_error_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.schema_error_message)).text
        except Exception:
            return None

    def save_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    # Composite actions

    def create_rule(self, rule_id, rule_name, trigger_type, trigger_data, action_type, action_data, conditions=None, destination_account=None):
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.select_trigger_type(trigger_type)

        if trigger_type == "specific_date":
            self.set_specific_date(trigger_data.get("date"))
        elif trigger_type == "recurring":
            self.set_recurring_interval(trigger_data.get("interval"))
        elif trigger_type == "after_deposit":
            self.toggle_after_deposit(True)

        self.select_action_type(action_type)
        if action_type == "fixed_amount":
            self.set_fixed_amount(action_data.get("amount"))
        elif action_type == "percentage_of_deposit":
            self.set_percentage_of_deposit(action_data.get("percentage"))

        if destination_account:
            self.set_destination_account(destination_account)

        if conditions:
            for cond in conditions:
                self.add_condition(**cond)

        self.save_rule()

    def submit_json_rule(self, json_rule):
        self.enter_json_schema(json_rule)
        self.validate_schema()
        return self.get_success_message(), self.get_schema_error_message()
