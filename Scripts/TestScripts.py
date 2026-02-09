import unittest
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestScripts(unittest.TestCase):
    # Existing test methods...

    def test_TC_SCRUM158_01_rule_creation_and_retrieval(self):
        """TC_SCRUM158_01: Prepare a valid rule schema with trigger (interval/daily), condition (amount > 100), and action (transfer to A, amount 100); submit the schema and verify rule creation and retrieval."""
        rule_page = RuleConfigurationPage(self.driver)
        rule_schema = {
            "trigger": {"type": "interval", "frequency": "daily"},
            "conditions": [{"field": "amount", "operator": ">", "value": 100}],
            "actions": [{"type": "transfer", "target": "A", "amount": 100}]
        }
        rule_id = rule_page.create_rule(rule_schema)
        self.assertIsNotNone(rule_id, "Rule creation failed, rule_id is None.")
        submission_result = rule_page.submit_rule(rule_id)
        self.assertTrue(submission_result, "Rule submission failed.")
        retrieved_rule = rule_page.get_rule(rule_id)
        self.assertIsNotNone(retrieved_rule, "Rule retrieval failed.")
        self.assertEqual(retrieved_rule["trigger"], rule_schema["trigger"], "Trigger mismatch.")
        self.assertEqual(retrieved_rule["conditions"], rule_schema["conditions"], "Condition mismatch.")
        self.assertEqual(retrieved_rule["actions"], rule_schema["actions"], "Action mismatch.")

    def test_TC_SCRUM158_02_multiple_conditions_and_actions(self):
        """TC_SCRUM158_02: Prepare a schema with trigger (manual), two conditions (amount > 500, country == US), and two actions (transfer to B, amount 500; notify with message); submit the schema and verify all conditions/actions are stored."""
        rule_page = RuleConfigurationPage(self.driver)
        rule_schema = {
            "trigger": {"type": "manual"},
            "conditions": [
                {"field": "amount", "operator": ">", "value": 500},
                {"field": "country", "operator": "==", "value": "US"}
            ],
            "actions": [
                {"type": "transfer", "target": "B", "amount": 500},
                {"type": "notify", "message": "Threshold exceeded"}
            ]
        }
        rule_id = rule_page.create_rule(rule_schema)
        self.assertIsNotNone(rule_id, "Rule creation failed, rule_id is None.")
        submission_result = rule_page.submit_rule(rule_id)
        self.assertTrue(submission_result, "Rule submission failed.")
        retrieved_rule = rule_page.get_rule(rule_id)
        self.assertIsNotNone(retrieved_rule, "Rule retrieval failed.")
        self.assertEqual(retrieved_rule["trigger"], rule_schema["trigger"], "Trigger mismatch.")
        self.assertEqual(retrieved_rule["conditions"], rule_schema["conditions"], "Conditions mismatch.")
        self.assertEqual(retrieved_rule["actions"], rule_schema["actions"], "Actions mismatch.")

    def test_TC_SCRUM158_03_create_and_schedule_recurring_interval_rule(self):
        """TC_SCRUM158_03: Create and schedule recurring interval rule. Acceptance Criteria: Rule is accepted and scheduled for recurring evaluation."""
        rule_page = RuleConfigurationPage(self.driver)
        rule_schema = {
            "trigger": {"type": "interval", "value": "weekly"},
            "conditions": [{"type": "amount", "operator": ">=", "value": 1000}],
            "actions": [{"type": "transfer", "account": "C", "amount": 1000}]
        }
        scheduled = rule_page.create_recurring_interval_rule(rule_schema)
        self.assertTrue(scheduled, "Rule was not scheduled for recurring evaluation.")

    def test_TC_SCRUM158_04_validate_missing_trigger_schema(self):
        """TC_SCRUM158_04: Validate schema missing required field. Acceptance Criteria: Schema is rejected with error indicating missing required field."""
        rule_page = RuleConfigurationPage(self.driver)
        incomplete_schema = {
            "conditions": [{"type": "amount", "operator": "<", "value": 50}],
            "actions": [{"type": "transfer", "account": "D", "amount": 50}]
        }
        error_msg = rule_page.validate_missing_trigger_schema(incomplete_schema)
        self.assertIsNotNone(error_msg, "Error message was not returned for missing trigger field.")
        self.assertIn("trigger", error_msg.lower(), "Error message does not indicate missing trigger field.")

if __name__ == "__main__":
    unittest.main()
