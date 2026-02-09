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

    # --- New Login Test Methods ---
    def test_TC_Login_01_valid_login(self):
        '''
        TC_Login_01: Valid login - user@example.com / ValidPassword123
        Expects: Login successful, dashboard loaded.
        '''
        self.login_page.enter_username('user@example.com')
        self.login_page.enter_password('ValidPassword123')
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_login_successful(), "Dashboard was not loaded after valid login.")

    def test_TC_Login_02_invalid_login(self):
        '''
        TC_Login_02: Invalid login - wronguser@example.com / WrongPassword
        Expects: Error message 'Invalid credentials' displayed, login not successful.
        '''
        self.login_page.enter_username('wronguser@example.com')
        self.login_page.enter_password('WrongPassword')
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_error_displayed(), "Error message 'Invalid credentials' was not displayed.")
        self.assertFalse(self.login_page.is_login_successful(), "Login was successful with invalid credentials.")

if __name__ == '__main__':
    unittest.main()
