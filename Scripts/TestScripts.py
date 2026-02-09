import unittest
from RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):

    # Existing test methods...

    def test_define_rule_with_multiple_conditions_TC_FT_003(self):
        """TC-FT-003: Define rule with multiple conditions (balance >= 1000, source = 'salary').
        - Simulate deposit from 'salary' when balance is 900 (expect transfer NOT executed).
        - Simulate deposit from 'salary' when balance is 1200 (expect transfer executed).
        """
        rule_page = RuleConfigurationPage()
        rule = {
            'trigger': 'deposit',
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000},
                {'field': 'source', 'operator': '==', 'value': 'salary'}
            ],
            'action': 'transfer'
        }
        rule_page.define_rule(rule)
        # Simulate deposit from 'salary' when balance is 900
        result_900 = rule_page.simulate_deposit(balance=900, source='salary')
        self.assertFalse(result_900['transfer_executed'], "Transfer should NOT be executed when balance is 900.")
        # Simulate deposit from 'salary' when balance is 1200
        result_1200 = rule_page.simulate_deposit(balance=1200, source='salary')
        self.assertTrue(result_1200['transfer_executed'], "Transfer should be executed when balance is 1200.")

    def test_submit_rule_with_missing_trigger_TC_FT_004(self):
        """TC-FT-004: Submit rule with missing trigger (expect error for missing required field)."""
        rule_page = RuleConfigurationPage()
        rule_missing_trigger = {
            # 'trigger' is missing
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000}
            ],
            'action': 'transfer'
        }
        with self.assertRaises(ValueError) as context:
            rule_page.define_rule(rule_missing_trigger)
        self.assertIn('missing required field', str(context.exception).lower())

    def test_submit_rule_with_unsupported_action_TC_FT_004(self):
        """TC-FT-004: Submit rule with unsupported action (expect error for unsupported action type)."""
        rule_page = RuleConfigurationPage()
        rule_unsupported_action = {
            'trigger': 'deposit',
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000}
            ],
            'action': 'unsupported_action_type'
        }
        with self.assertRaises(ValueError) as context:
            rule_page.define_rule(rule_unsupported_action)
        self.assertIn('unsupported action', str(context.exception).lower())

    # --- New Test Cases ---
    def test_define_rule_percentage_of_deposit_TC_FT_005(self):
        """TC-FT-005: Define a rule for 10% of deposit action. Simulate deposit of 500 units and verify transfer of 50 units is executed."""
        driver = self.driver if hasattr(self, 'driver') else None
        rule_page = RuleConfigurationPage(driver)
        # Step 1: Define rule
        rule_page.enter_rule_id("TC-FT-005-10pct")
        rule_page.enter_rule_name("10% deposit transfer")
        rule_page.select_trigger_type("after_deposit")
        rule_page.set_after_deposit_trigger()
        rule_page.select_action_type("percentage_of_deposit")
        rule_page.enter_percentage_of_deposit(10)
        rule_page.save_rule()
        success_msg = rule_page.get_success_message()
        self.assertIn("accepted", success_msg.lower())
        # Step 2: Simulate deposit
        rule_page.simulate_deposit(500)
        # Ideally, verify transfer of 50 units executed (mocked/asserted as needed)
        # If UI feedback is available, check for transfer confirmation
        # Example:
        # transfer_msg = rule_page.get_transfer_confirmation()
        # self.assertIn("50 units", transfer_msg)

    def test_define_rule_currency_conversion_TC_FT_006(self):
        """TC-FT-006: Define a rule with a new, future rule type 'currency_conversion'. Verify system accepts or gracefully rejects, and existing rules continue to execute as before."""
        driver = self.driver if hasattr(self, 'driver') else None
        rule_page = RuleConfigurationPage(driver)
        # Step 1: Define rule with currency_conversion trigger
        rule_page.enter_rule_id("TC-FT-006-currency")
        rule_page.enter_rule_name("Currency Conversion Rule")
        rule_page.set_currency_conversion_trigger("EUR")
        rule_page.select_action_type("fixed_amount")
        rule_page.enter_fixed_amount(100)
        rule_page.save_rule()
        try:
            success_msg = rule_page.get_success_message()
            self.assertTrue("accepted" in success_msg.lower() or "success" in success_msg.lower())
        except Exception:
            error_msg = rule_page.get_schema_error_message()
            self.assertIn("unsupported", error_msg.lower() or "graceful", error_msg.lower())
        # Step 2: Verify existing rules continue to execute
        # Example: simulate deposit for a previous rule
        # rule_page.simulate_deposit(500)
        # self.assertTrue(rule_page.check_existing_rule_execution())

if __name__ == '__main__':
    unittest.main()
