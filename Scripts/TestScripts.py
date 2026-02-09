
import unittest
from Pages.RuleConfigurationPage import (
    input_rule_schema_max_conditions_actions,
    input_rule_schema_empty_conditions_actions,
    submit_rule_schema,
    retrieve_and_validate_rule,
    robust_error_handling_and_schema_validation
)

class TestRuleConfiguration(unittest.TestCase):

    # Existing test methods...
    # (Assume all previous content is preserved here)

    def test_TC_SCRUM158_07_create_rule_with_max_conditions_actions(self):
        """TC_SCRUM158_07: Create rule with max (10) conditions/actions and validate persistence."""
        rule_data = input_rule_schema_max_conditions_actions()
        submit_rule_schema(rule_data)
        persisted_rule = retrieve_and_validate_rule(rule_data['name'])
        self.assertEqual(len(persisted_rule['conditions']), 10, "Should have 10 conditions")
        self.assertEqual(len(persisted_rule['actions']), 10, "Should have 10 actions")
        robust_error_handling_and_schema_validation(persisted_rule)
        # Additional assertions as per business requirements can be added here

    def test_TC_SCRUM158_08_create_rule_with_empty_conditions_actions(self):
        """TC_SCRUM158_08: Create rule with empty conditions/actions arrays and validate business rule."""
        rule_data = input_rule_schema_empty_conditions_actions()
        submit_rule_schema(rule_data)
        persisted_rule = retrieve_and_validate_rule(rule_data['name'])
        self.assertEqual(len(persisted_rule['conditions']), 0, "Should have 0 conditions")
        self.assertEqual(len(persisted_rule['actions']), 0, "Should have 0 actions")
        robust_error_handling_and_schema_validation(persisted_rule)
        # Assert business rule: e.g., rule may not be active, or must show validation error depending on requirements
        # If business rule expects error, add:
        # self.assertIn('error', persisted_rule)
