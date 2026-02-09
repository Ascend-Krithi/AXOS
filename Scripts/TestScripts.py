import unittest
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestScripts(unittest.TestCase):
    # Existing test methods...
    # (full content from previous step)

    def test_TC_SCRUM158_07_create_rule_with_required_fields(self):
        """
        Test Case TC_SCRUM158_07:
        - Create a rule with only required fields.
        - Verify rule creation success.
        """
        rule_id = 'TS07'
        rule_name = 'Required Fields Rule'
        trigger_type = 'manual'
        condition_type = 'amount'
        operator = '=='
        value = 1
        action_type = 'transfer'
        account = 'G'
        amount = 1

        page = RuleConfigurationPage()
        result = page.create_rule_with_required_fields(
            rule_id=rule_id,
            rule_name=rule_name,
            trigger_type=trigger_type,
            condition_type=condition_type,
            operator=operator,
            value=value,
            action_type=action_type,
            account=account,
            amount=amount
        )
        self.assertIn('success', result.lower(), f"Rule creation failed: {result}")

    def test_TC_SCRUM158_08_create_rule_with_large_metadata(self):
        """
        Test Case TC_SCRUM158_08:
        - Create a rule with a large metadata field (~10,000 chars).
        - Verify acceptance and performance.
        """
        rule_id = 'TS08'
        rule_name = 'Large Metadata Rule'
        trigger_type = 'manual'
        metadata = 'A' * 10000

        page = RuleConfigurationPage()
        result = page.create_rule_with_large_metadata(
            rule_id=rule_id,
            rule_name=rule_name,
            trigger_type=trigger_type,
            metadata=metadata
        )
        self.assertIn('success', result.lower(), f"Large metadata rule creation failed or not accepted: {result}")
        # Optionally, check performance (e.g., response time if available)
