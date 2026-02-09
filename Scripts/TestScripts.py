import unittest
from RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.page = RuleConfigurationPage()

    # Existing test methods...

    def test_TC_SCRUM158_01(self):
        ...
    def test_TC_SCRUM158_02(self):
        ...
    def test_TC_SCRUM158_03(self):
        ...
    def test_TC_SCRUM158_04(self):
        ...
    def test_TC_SCRUM158_05(self):
        ...
    def test_TC_SCRUM158_06(self):
        ...

    def test_TC_SCRUM158_07(self):
        """TC_SCRUM158_07: minimal schema with one trigger, one condition, one action"""
        rule_id = "SCRUM158_07"
        rule_name = "Minimal Rule"
        trigger_type = "manual"
        condition_type = "amount"
        action_type = "transfer"
        schema_text = '{"trigger":{"type":"manual"},"conditions":[{"type":"amount","operator":"==","value":1}],"actions":[{"type":"transfer","account":"G","amount":1}]}'
        page = self.page
        page.create_minimal_rule(rule_id, rule_name, trigger_type, condition_type, action_type, schema_text)
        self.assertTrue(page.is_success_message_displayed(), "Minimal rule was not created successfully.")

    def test_TC_SCRUM158_08(self):
        """TC_SCRUM158_08: schema with large metadata field (10,000 characters)"""
        rule_id = "SCRUM158_08"
        rule_name = "Large Metadata Rule"
        large_metadata = "x" * 10000
        schema_text = '{"trigger":{"type":"manual"},"metadata":"' + large_metadata + '"}'
        page = self.page
        page.create_rule_with_large_metadata(rule_id, rule_name, schema_text)
        self.assertTrue(page.is_success_message_displayed(), "Rule with large metadata was not created successfully.")

if __name__ == "__main__":
    unittest.main()
