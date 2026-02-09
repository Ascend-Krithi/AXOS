import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage
import json

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://example.com/login')
        self.login_page = LoginPage(self.driver)
        # For RuleConfigurationPage tests
        self.locators = self.load_locators()
        self.rule_config_page = RuleConfigurationPage(self.driver, self.locators)

    def tearDown(self):
        self.driver.quit()

    def load_locators(self):
        with open('Locators.json', 'r') as f:
            return json.load(f)

    # Existing test methods...
    # ... (existing methods unchanged)

    # --- New Test Methods for Rule Configuration Negative Cases ---
    def test_TC_SCRUM158_05_invalid_trigger(self):
        '''
        TC_SCRUM158_05: Prepare a rule schema with an invalid trigger value and submit.
        Expects API to return 400 Bad Request with error about invalid value.
        '''
        invalid_rule_schema = {
            "trigger": "unknown_trigger",
            "conditions": [
                {"type": "balance_above", "value": 1000}
            ],
            "actions": [
                {"type": "notify", "message": "Invalid trigger test"}
            ]
        }
        response = self.rule_config_page.submit_invalid_trigger_rule_schema(invalid_rule_schema)
        self.assertEqual(response.get('status'), 'error', "API did not return error for invalid trigger.")
        self.assertEqual(response.get('code'), 400, "API did not return 400 Bad Request for invalid trigger.")
        self.assertIn('Invalid trigger value', response.get('message', ''), "Error message not about invalid trigger value.")

    def test_TC_SCRUM158_06_incomplete_condition(self):
        '''
        TC_SCRUM158_06: Prepare a rule schema with a condition missing required parameters and submit.
        Expects API to return 400 Bad Request with error about incomplete condition.
        '''
        incomplete_condition_rule_schema = {
            "trigger": "balance_above",
            "conditions": [
                {"type": "amount_above"}  # Missing 'value'
            ],
            "actions": [
                {"type": "notify", "message": "Incomplete condition test"}
            ]
        }
        response = self.rule_config_page.submit_incomplete_condition_rule_schema(incomplete_condition_rule_schema)
        self.assertEqual(response.get('status'), 'error', "API did not return error for incomplete condition.")
        self.assertEqual(response.get('code'), 400, "API did not return 400 Bad Request for incomplete condition.")
        self.assertIn('Incomplete condition parameters', response.get('message', ''), "Error message not about incomplete condition parameters.")

if __name__ == '__main__':
    unittest.main()
