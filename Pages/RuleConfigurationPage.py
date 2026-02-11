import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Locators loaded from Locators.json
        self.locators = {
            'add_rule_button': (By.XPATH, "//button[@id='add-rule']"),
            'rule_name_input': (By.ID, "rule-name"),
            'rule_type_dropdown': (By.ID, "rule-type"),
            'advanced_tab': (By.XPATH, "//a[@id='advanced-tab']"),
            'save_button': (By.XPATH, "//button[@id='save-rule']"),
            'success_message': (By.XPATH, "//div[@class='success-message']"),
            'ruleIdInput': (By.ID, "rule-id-field"),
            'ruleNameInput': (By.NAME, "rule-name"),
            'saveRuleButton': (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']"),
            'triggerTypeDropdown': (By.ID, "trigger-type-select"),
            'datePicker': (By.CSS_SELECTOR, "input[type='date']"),
            'recurringIntervalInput': (By.ID, "interval-value"),
            'afterDepositToggle': (By.ID, "trigger-after-deposit"),
            'addConditionBtn': (By.ID, "add-condition-link"),
            'conditionTypeDropdown': (By.CSS_SELECTOR, "select.condition-type"),
            'balanceThresholdInput': (By.CSS_SELECTOR, "input[name='balance-limit']"),
            'transactionSourceDropdown': (By.ID, "source-provider-select"),
            'operatorDropdown': (By.CSS_SELECTOR, ".condition-operator-select"),
            'actionTypeDropdown': (By.ID, "action-type-select"),
            'transferAmountInput': (By.NAME, "fixed-amount"),
            'percentageInput': (By.ID, "deposit-percentage"),
            'destinationAccountInput': (By.ID, "target-account-id"),
            'jsonSchemaEditor': (By.CSS_SELECTOR, ".monaco-editor"),
            'validateSchemaBtn': (By.ID, "btn-verify-json"),
            'successMessage': (By.CSS_SELECTOR, ".alert-success"),
            'schemaErrorMessage': (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")
        }
    def click_add_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.locators['add_rule_button'])).click()
    def enter_rule_name(self, name):
        rule_name = self.wait.until(EC.visibility_of_element_located(self.locators['rule_name_input']))
        rule_name.clear()
        rule_name.send_keys(name)
    def select_rule_type(self, rule_type):
        dropdown = self.wait.until(EC.visibility_of_element_located(self.locators['rule_type_dropdown']))
        dropdown.click()
        option = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//option[text()='{rule_type}']")))
        option.click()
    def open_advanced_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.locators['advanced_tab'])).click()
    def configure_advanced_rule(self, settings_dict):
        for field, value in settings_dict.items():
            locator = (By.ID, f"advanced-{field}")
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(value)
    def save_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.locators['save_button'])).click()
    def verify_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.locators['success_message'])).is_displayed()
    def create_rule(self, rule_name, rule_type, advanced_settings=None):
        self.click_add_rule()
        self.enter_rule_name(rule_name)
        self.select_rule_type(rule_type)
        if advanced_settings:
            self.open_advanced_tab()
            self.configure_advanced_rule(advanced_settings)
        self.save_rule()
        return self.verify_success_message()
    # TC_SCRUM158_005: Invalid trigger_type
    def create_rule_with_invalid_trigger(self):
        self.click_add_rule()
        self.enter_rule_name("Invalid Trigger Test")
        self.select_rule_type("invalid_trigger")
        self.save_rule()
        error = self.wait.until(EC.visibility_of_element_located(self.locators['schemaErrorMessage']))
        return error.text
    # TC_SCRUM158_006: Missing action_type/trigger_type
    def create_rule_with_missing_fields(self, rule_data):
        self.click_add_rule()
        if 'rule_name' in rule_data:
            self.enter_rule_name(rule_data['rule_name'])
        if 'trigger_type' in rule_data:
            self.select_rule_type(rule_data['trigger_type'])
        self.save_rule()
        error = self.wait.until(EC.visibility_of_element_located(self.locators['schemaErrorMessage']))
        return error.text
