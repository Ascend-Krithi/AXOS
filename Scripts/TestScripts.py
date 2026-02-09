
import unittest
from RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):
    # Existing test methods...

    def test_TC_SCRUM158_05_invalid_trigger(self):
        """TC_SCRUM158_05: Verify error handling for invalid trigger input."""
        page = RuleConfigurationPage()
        result = page.run_invalid_trigger_test()
        self.assertTrue(result['error_detected'], f"Expected error for invalid trigger, got: {result}")

    def test_TC_SCRUM158_06_missing_condition_param(self):
        """TC_SCRUM158_06: Verify error handling when condition parameter is missing."""
        page = RuleConfigurationPage()
        result = page.run_missing_condition_param_test()
        self.assertTrue(result['error_detected'], f"Expected error for missing condition parameter, got: {result}")

if __name__ == '__main__':
    unittest.main()
