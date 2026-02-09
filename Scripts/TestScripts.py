# Existing imports
import unittest
from RuleEnginePage import RuleEnginePage

class RuleEngineTests(unittest.TestCase):
    # Existing test methods...

    def test_TC_FT_005_define_percentage_rule_and_verify_transfer(self):
        """
        TC-FT-005: Define a rule for 10% of deposit action using define_percentage_rule('after_deposit', 10).
        Simulate deposit of 500 units and verify transfer of 50 units using simulate_deposit_and_verify_transfer(500, 50).
        """
        rule_engine = RuleEnginePage()
        # Define percentage rule
        result_define = rule_engine.define_percentage_rule('after_deposit', 10)
        self.assertTrue(result_define, "Failed to define 10% deposit rule")

        # Simulate deposit and verify transfer
        result_transfer = rule_engine.simulate_deposit_and_verify_transfer(500, 50)
        self.assertTrue(result_transfer, "Transfer of 50 units after deposit of 500 units not verified")

    def test_TC_FT_006_define_future_rule_and_verify_response(self):
        """
        TC-FT-006: Define a rule with trigger_type 'currency_conversion', currency 'EUR', action_type 'fixed_amount', amount 100 using define_future_rule_and_verify_response(...).
        Assert system accepts or gracefully rejects with a clear error message.
        Verify existing rules continue to execute as before using verify_existing_rules_execution().
        Assert result is True.
        """
        rule_engine = RuleEnginePage()
        # Define future rule and verify response
        response = rule_engine.define_future_rule_and_verify_response('currency_conversion', 'EUR', 'fixed_amount', 100)
        if isinstance(response, bool):
            self.assertTrue(response, "Future rule definition did not return True")
        else:
            self.assertIn("error", response.lower(), "System did not gracefully reject or provide a clear error message")

        # Verify existing rules continue to execute
        result_existing = rule_engine.verify_existing_rules_execution()
        self.assertTrue(result_existing, "Existing rules did not execute as before after future rule definition")

if __name__ == "__main__":
    unittest.main()
