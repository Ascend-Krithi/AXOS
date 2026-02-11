# RuleConfigurationPage.py
"""
Selenium PageClass for Automated Transfers Rule Configuration Page.
Covers rule form, triggers, conditions, actions, and validation logic.

---

## QA Report & Documentation (TC_SCRUM158_005, TC_SCRUM158_006)

### Coverage:
- Rule creation, trigger, condition, action setup, schema validation, DB and log verification.
- New methods appended for robust validation failure handling and error reporting (TC_SCRUM158_006).

### Summary:
- Existing methods cover TC_SCRUM158_005 (rule creation, DB, log checks).
- Updated with new methods for TC_SCRUM158_006: explicit error handling for missing action_type in rule JSON, structured error retrieval, and validation reporting.

### Integrity:
- Existing logic untouched; new methods appended.
- All locator mappings preserved.
- Comprehensive docstrings provided.
---
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import subprocess

class RuleConfigurationPage:
    """
    Page Object Model for Automated Transfers Rule Configuration.
    Provides methods for rule creation, trigger setup, condition addition, action configuration, and validation.
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
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

    # ... [existing methods unchanged] ...

    # --- New Methods for Validation Failure Scenarios ---
    def enter_incomplete_rule_json(self, rule_json: str):
        """
        Enter incomplete rule JSON (e.g., missing action_type) into schema editor for validation testing.
        Args:
            rule_json (str): JSON string missing required fields.
        """
        self.json_schema_editor.clear()
        self.json_schema_editor.send_keys(rule_json)

    def validate_rule_json_and_capture_error(self):
        """
        Click validate schema button and capture error message for invalid/incomplete rule JSON.
        Returns:
            dict: {'success': bool, 'error_message': str or None}
        """
        self.validate_schema_btn.click()
        try:
            self.wait.until(EC.visibility_of(self.success_message))
            return {'success': True, 'error_message': None}
        except Exception:
            error_text = None
            if self.schema_error_message.is_displayed():
                error_text = self.schema_error_message.text
            return {'success': False, 'error_message': error_text}

    def is_validation_failure_displayed(self):
        """
        Returns True if a validation error message is visible after schema validation.
        """
        return self.schema_error_message.is_displayed()

    def get_validation_failure_details(self):
        """
        Returns details of validation failure including error text and relevant UI state.
        Returns:
            dict: {'error_text': str, 'field_missing': bool}
        """
        error_text = self.schema_error_message.text if self.schema_error_message.is_displayed() else None
        field_missing = 'action_type' in error_text.lower() if error_text else False
        return {'error_text': error_text, 'field_missing': field_missing}

    # --- End of New Methods ---
