import unittest
from RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.page = RuleConfigurationPage()
        self.page.open()

    def tearDown(self):
        self.page.close()

    # Existing test methods (preserved)
    # ... [existing methods here] ...

    def test_TC_SCRUM158_07_create_rule_with_required_fields(self):
        """TC_SCRUM158_07: Create rule with required fields only."""
        rule_name = "RequiredFieldsRule"
        rule_description = "Rule with only required fields"
        required_fields = {
            "name": rule_name,
            "description": rule_description,
            # Add other required fields as per PageClass definition
        }
        self.page.navigate_to_rule_creation()
        self.page.fill_rule_form(**required_fields)
        self.page.submit_rule_form()
        success_message = self.page.get_success_message()
        self.assertIn("Rule created successfully", success_message)
        rule_exists = self.page.verify_rule_exists(rule_name)
        self.assertTrue(rule_exists, "Rule should exist after creation.")

    def test_TC_SCRUM158_08_create_rule_with_large_metadata(self):
        """TC_SCRUM158_08: Create rule with large metadata."""
        rule_name = "LargeMetadataRule"
        rule_description = "Rule with large metadata"
        large_metadata = "A" * 10000  # Example: 10,000 characters
        rule_fields = {
            "name": rule_name,
            "description": rule_description,
            "metadata": large_metadata,
            # Add other required fields as per PageClass definition
        }
        self.page.navigate_to_rule_creation()
        self.page.fill_rule_form(**rule_fields)
        self.page.submit_rule_form()
        success_message = self.page.get_success_message()
        self.assertIn("Rule created successfully", success_message)
        rule_exists = self.page.verify_rule_exists(rule_name)
        self.assertTrue(rule_exists, "Rule with large metadata should exist after creation.")

if __name__ == "__main__":
    unittest.main()
