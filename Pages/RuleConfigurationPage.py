# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class RuleConfigurationPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Locators
    ruleIdInput = (By.ID, "rule-id-field")
    ruleNameInput = (By.NAME, "rule-name")
    saveRuleButton = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

    triggerTypeDropdown = (By.ID, "trigger-type-select")
    datePicker = (By.CSS_SELECTOR, "input[type='date']")
    recurringIntervalInput = (By.ID, "interval-value")
    afterDepositToggle = (By.ID, "trigger-after-deposit")

    addConditionBtn = (By.ID, "add-condition-link")
    conditionTypeDropdown = (By.CSS_SELECTOR, "select.condition-type")
    balanceThresholdInput = (By.CSS_SELECTOR, "input[name='balance-limit'")
    transactionSourceDropdown = (By.ID, "source-provider-select")
    operatorDropdown = (By.CSS_SELECTOR, ".condition-operator-select")

    actionTypeDropdown = (By.ID, "action-type-select")
    transferAmountInput = (By.NAME, "fixed-amount")
    percentageInput = (By.ID, "deposit-percentage")
    destinationAccountInput = (By.ID, "target-account-id")

    jsonSchemaEditor = (By.CSS_SELECTOR, ".monaco-editor")
    validateSchemaBtn = (By.ID, "btn-verify-json")
    successMessage = (By.CSS_SELECTOR, ".alert-success")
    schemaErrorMessage = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    # --- Rule Creation ---
    def enter_rule_id(self, rule_id):
        rule_id_element = self.wait.until(EC.visibility_of_element_located(self.ruleIdInput))
        rule_id_element.clear()
        rule_id_element.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        rule_name_element = self.wait.until(EC.visibility_of_element_located(self.ruleNameInput))
        rule_name_element.clear()
        rule_name_element.send_keys(rule_name)

    # --- Trigger Setup ---
    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.triggerTypeDropdown))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='trigger-type-select']/option[text()='{trigger_type}']")))
        option.click()

    def set_trigger_date(self, date_value):
        date_picker = self.wait.until(EC.element_to_be_clickable(self.datePicker))
        date_picker.clear()
        date_picker.send_keys(date_value)

    def set_recurring_interval(self, interval_value):
        interval_input = self.wait.until(EC.visibility_of_element_located(self.recurringIntervalInput))
        interval_input.clear()
        interval_input.send_keys(str(interval_value))

    def toggle_after_deposit(self, enable=True):
        toggle = self.wait.until(EC.element_to_be_clickable(self.afterDepositToggle))
        if (toggle.is_selected() != enable):
            toggle.click()

    # --- Condition Setup ---
    def add_condition(self):
        add_btn = self.wait.until(EC.element_to_be_clickable(self.addConditionBtn))
        add_btn.click()

    def select_condition_type(self, condition_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.conditionTypeDropdown))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[contains(@class,'condition-type')]/option[text()='{condition_type}']")))
        option.click()

    def set_balance_threshold(self, threshold):
        balance_input = self.wait.until(EC.visibility_of_element_located(self.balanceThresholdInput))
        balance_input.clear()
        balance_input.send_keys(str(threshold))

    def select_transaction_source(self, source):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.transactionSourceDropdown))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='source-provider-select']/option[text()='{source}']")))
        option.click()

    def select_operator(self, operator):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.operatorDropdown))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[contains(@class,'condition-operator-select')]/option[text()='{operator}']")))
        option.click()

    # --- Action Setup ---
    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.actionTypeDropdown))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='action-type-select']/option[text()='{action_type}']")))
        option.click()

    def set_transfer_amount(self, amount):
        amount_input = self.wait.until(EC.visibility_of_element_located(self.transferAmountInput))
        amount_input.clear()
        amount_input.send_keys(str(amount))

    def set_percentage(self, percentage):
        percentage_input = self.wait.until(EC.visibility_of_element_located(self.percentageInput))
        percentage_input.clear()
        percentage_input.send_keys(str(percentage))

    def set_destination_account(self, account_id):
        destination_input = self.wait.until(EC.visibility_of_element_located(self.destinationAccountInput))
        destination_input.clear()
        destination_input.send_keys(account_id)

    # --- Rule Saving ---
    def save_rule(self):
        save_btn = self.wait.until(EC.element_to_be_clickable(self.saveRuleButton))
        save_btn.click()

    def verify_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.successMessage)).is_displayed()

    # --- Validation ---
    def enter_json_schema(self, schema_text):
        editor = self.wait.until(EC.visibility_of_element_located(self.jsonSchemaEditor))
        ActionChains(self.driver).move_to_element(editor).click().send_keys(schema_text).perform()

    def validate_schema(self):
        validate_btn = self.wait.until(EC.element_to_be_clickable(self.validateSchemaBtn))
        validate_btn.click()

    def get_schema_error_message(self):
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.schemaErrorMessage))
            return error.text
        except:
            return None

    # --- Rule Retrieval ---
    def get_rule_id(self):
        rule_id_element = self.wait.until(EC.visibility_of_element_located(self.ruleIdInput))
        return rule_id_element.get_attribute("value")

    def get_rule_name(self):
        rule_name_element = self.wait.until(EC.visibility_of_element_located(self.ruleNameInput))
        return rule_name_element.get_attribute("value")

    # --- Execution Log Verification ---
    def verify_execution_log(self, log_text):
        # Assuming execution log is displayed in a success message or another element
        log_element = self.wait.until(EC.visibility_of_element_located(self.successMessage))
        return log_text in log_element.text