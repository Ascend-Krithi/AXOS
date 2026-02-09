# Existing imports and test methods preserved
from selenium import webdriver
import unittest
from Pages.RuleManagementPage import RuleManagementPage

class TestRuleManagement(unittest.TestCase):
    # ... Existing test methods ...

    def test_TC_FT_003_rule_creation_and_transfer_validation(self):
        """
        TC-FT-003: Rule creation with multiple conditions, deposit simulation, transfer validation (including negative and positive cases).
        Steps:
        1. Create a rule with multiple conditions.
        2. Simulate a deposit.
        3. Validate transfer - negative and positive cases.
        """
        driver = webdriver.Chrome()
        rule_page = RuleManagementPage(driver)
        try:
            # Step 1: Create rule with multiple conditions
            rule_name = "MultiConditionRule"
            conditions = [
                {"type": "amount", "operator": ">", "value": 1000},
                {"type": "currency", "operator": "==", "value": "USD"}
            ]
            actions = [
                {"type": "allow_transfer", "parameters": {"max_amount": 5000}}
            ]
            rule_page.open_rule_management()
            rule_page.create_rule(rule_name, conditions, actions)
            self.assertTrue(rule_page.is_rule_created(rule_name), "Rule creation failed.")

            # Step 2: Simulate deposit
            deposit_amount = 1500
            deposit_currency = "USD"
            rule_page.simulate_deposit(deposit_amount, deposit_currency)
            self.assertTrue(rule_page.is_deposit_successful(deposit_amount, deposit_currency), "Deposit simulation failed.")

            # Step 3: Validate transfer - negative case (amount exceeds max)
            transfer_amount = 6000
            transfer_currency = "USD"
            result = rule_page.validate_transfer(rule_name, transfer_amount, transfer_currency)
            self.assertFalse(result, "Transfer should not be allowed for amount exceeding max.")

            # Step 3: Validate transfer - positive case (amount within max)
            transfer_amount = 4000
            result = rule_page.validate_transfer(rule_name, transfer_amount, transfer_currency)
            self.assertTrue(result, "Transfer should be allowed for amount within max.")
        finally:
            driver.quit()

    def test_TC_FT_004_rule_submission_missing_trigger_and_unsupported_action(self):
        """
        TC-FT-004: Rule submission with missing trigger type and unsupported action type, error validation.
        Steps:
        1. Attempt to submit rule with missing trigger type.
        2. Attempt to submit rule with unsupported action type.
        3. Validate error messages.
        """
        driver = webdriver.Chrome()
        rule_page = RuleManagementPage(driver)
        try:
            # Step 1: Missing trigger type
            rule_name = "MissingTriggerRule"
            conditions = []  # No trigger type
            actions = [
                {"type": "allow_transfer", "parameters": {"max_amount": 1000}}
            ]
            rule_page.open_rule_management()
            rule_page.create_rule(rule_name, conditions, actions)
            error_msg = rule_page.get_last_error_message()
            self.assertIn("Trigger type is required", error_msg, "Missing trigger type error not shown.")

            # Step 2: Unsupported action type
            rule_name = "UnsupportedActionRule"
            conditions = [
                {"type": "amount", "operator": ">", "value": 500}
            ]
            actions = [
                {"type": "unsupported_action", "parameters": {}}
            ]
            rule_page.create_rule(rule_name, conditions, actions)
            error_msg = rule_page.get_last_error_message()
            self.assertIn("Unsupported action type", error_msg, "Unsupported action type error not shown.")
        finally:
            driver.quit()
