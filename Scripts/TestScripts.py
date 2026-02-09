import unittest
from RuleManagementPage import RuleManagementPage

class TestRuleManagement(unittest.TestCase):
    def setUp(self):
        self.page = RuleManagementPage()

    # Existing tests...

    def test_define_rule_with_multiple_conditions_and_deposit_scenarios(self):
        """
        TC-FT-003:
        1. Define a rule with multiple conditions (balance >= 1000, source = 'salary').
        2. Simulate deposit from 'salary' when balance is 900, expect transfer NOT executed.
        3. Simulate deposit from 'salary' when balance is 1200, expect transfer executed.
        """
        # Step 1: Define rule with multiple conditions
        self.page.create_rule_with_multiple_conditions(balance=1000, source='salary')
        # Step 2: Simulate deposit from 'salary' when balance is 900
        self.page.simulate_deposit(source='salary', balance=900)
        transfer_executed = self.page.validate_transfer_execution()
        self.assertFalse(transfer_executed, "Transfer should NOT be executed when balance is 900")
        # Step 3: Simulate deposit from 'salary' when balance is 1200
        self.page.simulate_deposit(source='salary', balance=1200)
        transfer_executed = self.page.validate_transfer_execution()
        self.assertTrue(transfer_executed, "Transfer SHOULD be executed when balance is 1200")

    def test_submit_rule_with_missing_trigger_type(self):
        """
        TC-FT-004 Step 1:
        1. Submit rule with missing trigger type, expect error.
        """
        self.page.submit_rule_with_missing_trigger()
        error_message = self.page.validate_error_for_missing_trigger()
        self.assertIsNotNone(error_message, "Error message should be shown for missing trigger type")
        self.assertIn("trigger type", error_message.lower(), "Error message should mention trigger type")

    def test_submit_rule_with_unsupported_action_type(self):
        """
        TC-FT-004 Step 2:
        2. Submit rule with unsupported action type, expect error.
        """
        self.page.submit_rule_with_unsupported_action()
        error_message = self.page.validate_error_for_unsupported_action()
        self.assertIsNotNone(error_message, "Error message should be shown for unsupported action type")
        self.assertIn("unsupported action", error_message.lower(), "Error message should mention unsupported action type")

if __name__ == '__main__':
    unittest.main()
