import unittest
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.rule_page = RuleConfigurationPage()

    # Existing test methods...

    def test_TC_SCRUM158_03_create_rule_with_recurring_interval_trigger(self):
        rule_id = 'TC03'
        rule_name = 'Recurring Weekly Rule'
        interval_value = 'weekly'
        action_type = 'transfer'
        action_amount = 1000

        result = self.rule_page.create_rule_with_recurring_interval_trigger(
            rule_id=rule_id,
            rule_name=rule_name,
            interval_value=interval_value,
            action_type=action_type,
            action_amount=action_amount
        )
        self.assertTrue(result['success'], f"Rule creation failed: {result.get('error', '')}")
        self.assertEqual(result['rule_id'], rule_id)
        self.assertEqual(result['rule_name'], rule_name)
        self.assertEqual(result['interval'], interval_value)
        self.assertEqual(result['action_type'], action_type)
        self.assertEqual(result['action_amount'], action_amount)
        self.assertTrue(result['scheduled'], "Rule was not scheduled as expected.")

    def test_TC_SCRUM158_04_validate_missing_trigger_field(self):
        rule_id = 'TC04'
        rule_name = 'Missing Trigger Rule'
        action_type = 'transfer'
        action_amount = 50

        result = self.rule_page.validate_missing_trigger_field(
            rule_id=rule_id,
            rule_name=rule_name,
            action_type=action_type,
            action_amount=action_amount
        )
        self.assertFalse(result['success'], "Validation should fail when trigger field is missing.")
        self.assertIn('trigger', result['error_fields'], "Missing trigger field should be reported.")
        self.assertIsNotNone(result.get('error_message'), "Error message should be returned for missing trigger.")

if __name__ == '__main__':
    unittest.main()
