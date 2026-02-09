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

    def test_TC_FT_007_load_batch_rules_and_trigger_evaluation(self):
        """
        TC-FT-007: Load 10,000 valid rules from JSON file and trigger evaluation.
        1. Load rules using load_rules_batch(rules_json_path), expect successful and timely loading.
        2. Trigger evaluation for all rules using trigger_evaluation(), expect processing within performance thresholds.
        """
        rule_engine = RuleEnginePage()
        # Path to batch JSON file with 10,000 valid rules
        rules_json_path = "data/rules_batch_10000.json"
        import time
        start_load = time.time()
        result_load = rule_engine.load_rules_batch(rules_json_path)
        end_load = time.time()
        load_duration = end_load - start_load
        self.assertTrue(result_load, "Batch rule loading failed")
        self.assertLess(load_duration, 60, "Loading 10,000 rules exceeded acceptable time (60s)")

        start_eval = time.time()
        result_eval = rule_engine.trigger_evaluation()
        end_eval = time.time()
        eval_duration = end_eval - start_eval
        self.assertTrue(result_eval, "Rule evaluation failed for batch")
        self.assertLess(eval_duration, 120, "Evaluation of 10,000 rules exceeded performance threshold (120s)")

    def test_TC_FT_008_submit_rule_with_sql_injection(self):
        """
        TC-FT-008: Submit a rule with SQL injection in a field value and expect rejection.
        1. Submit rule with SQL injection payload using submit_rule_with_sql_injection(rule_data).
        2. Expect system to reject rule and not execute any SQL.
        """
        rule_engine = RuleEnginePage()
        sql_injection_payload = {
            "trigger": {
                "type": "specific_date",
                "date": "2024-07-01T10:00:00Z"
            },
            "action": {
                "type": "fixed_amount",
                "amount": 100
            },
            "conditions": [
                {
                    "type": "balance_threshold",
                    "value": "1000; DROP TABLE users;--"
                }
            ]
        }
        response = rule_engine.submit_rule_with_sql_injection(sql_injection_payload)
        # Assert system rejects rule and does not execute SQL
        if isinstance(response, dict) or isinstance(response, str):
            response_str = str(response).lower()
            self.assertTrue("reject" in response_str or "error" in response_str,
                            "System did not reject rule with SQL injection payload")
            self.assertFalse("drop table" in response_str or "users" in response_str,
                             "System response should not contain evidence of SQL execution")
        else:
            self.fail("Unexpected response type from submit_rule_with_sql_injection")

if __name__ == "__main__":
    unittest.main()
