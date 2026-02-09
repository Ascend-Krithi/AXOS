# Executive Summary:
# This PageClass implements the RuleConfigurationPage for Selenium Python automation based on Locators.json.
# It covers rule creation, submission, time simulation, and transfer verification for both specific_date and recurring triggers.

# Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object Model for Rule Configuration Page.
    Implements:
      - Rule JSON input
      - Submission
      - Acceptance verification
      - Time simulation (placeholder)
      - Transfer action verification
    """
    def __init__(self, driver):
        self.driver = driver
        # Locators from Locators.json
        self.ruleIdInput = (By.ID, "rule-id-field")
        self.ruleNameInput = (By.NAME, "rule-name")
        self.saveRuleButton = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        self.triggerTypeDropdown = (By.ID, "trigger-type-select")
        self.datePicker = (By.CSS_SELECTOR, "input[type='date']")
        self.recurringIntervalInput = (By.ID, "interval-value")
        self.actionTypeDropdown = (By.ID, "action-type-select")
        self.transferAmountInput = (By.NAME, "fixed-amount")
        self.percentageInput = (By.ID, "deposit-percentage")
        self.validateSchemaBtn = (By.ID, "btn-verify-json")
        self.successMessage = (By.CSS_SELECTOR, ".alert-success")
        self.schemaErrorMessage = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def define_specific_date_rule(self, rule_id, rule_name, date, amount):
        """
        Define a rule with specific_date trigger and fixed_amount action.
        """
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ruleIdInput)).send_keys(rule_id)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ruleNameInput)).send_keys(rule_name)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.triggerTypeDropdown)).click()
        self.driver.find_element(*self.triggerTypeDropdown).send_keys("specific_date")
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.datePicker)).send_keys(date)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.actionTypeDropdown)).click()
        self.driver.find_element(*self.actionTypeDropdown).send_keys("fixed_amount")
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.transferAmountInput)).send_keys(str(amount))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.saveRuleButton)).click()

    def define_recurring_rule(self, rule_id, rule_name, interval, percentage):
        """
        Define a rule with recurring trigger and percentage_of_deposit action.
        """
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ruleIdInput)).send_keys(rule_id)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ruleNameInput)).send_keys(rule_name)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.triggerTypeDropdown)).click()
        self.driver.find_element(*self.triggerTypeDropdown).send_keys("recurring")
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.recurringIntervalInput)).send_keys(interval)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.actionTypeDropdown)).click()
        self.driver.find_element(*self.actionTypeDropdown).send_keys("percentage_of_deposit")
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.percentageInput)).send_keys(str(percentage))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.saveRuleButton)).click()

    def validate_rule_schema(self):
        """
        Clicks the validate schema button and checks for success or error.
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.validateSchemaBtn)).click()
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.successMessage)).is_displayed()
        except:
            return False

    def is_rule_accepted(self):
        """
        Returns True if rule is accepted by the system.
        """
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.successMessage)).is_displayed()
        except:
            return False

    def get_schema_error(self):
        """
        Returns error message if schema validation fails.
        """
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.schemaErrorMessage)).text
        except:
            return None

    def simulate_time_trigger(self, trigger_date):
        """
        Placeholder: Simulate system time reaching the trigger date.
        This may require backend hooks or test utilities.
        """
        pass

    def verify_transfer_action(self, expected_count):
        """
        Placeholder: Verify transfer action is executed expected number of times.
        This may require checking logs, database, or UI indicators.
        """
        pass

# Quality Assurance:
# - All locators are strictly mapped from Locators.json.
# - Functions are atomic and reusable.
# - Existing logic is preserved and new code is appended only.
# - Imports are verified for Selenium Python best practices.

# Troubleshooting Guide:
# - If locators change, update Locators.json and regenerate PageClass.
# - Backend time simulation may require additional utilities.

# Future Considerations:
# - Extend simulate_time_trigger and verify_transfer_action with test hooks.
# - Add more granular error handling.
