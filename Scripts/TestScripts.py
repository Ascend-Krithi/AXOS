import unittest
from Pages.FinancialTransferPage import FinancialTransferPage
from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage

class TestScripts(unittest.TestCase):
    # ... (existing methods remain unchanged)

    def test_TC_SCRUM158_09_minimum_required_fields_rule_schema(self):
        """
        TC_SCRUM158_09: Validate and submit minimum required fields rule schema.
        Steps:
          1. Prepare a rule schema with only the minimum required fields.
          2. Submit the schema.
          3. Expect: JSON schema is valid, rule is created successfully.
        """
        rule_page = RuleConfigurationPage(self.driver)
        minimum_rule_schema = {
            'trigger': 'balance_above',
            'conditions': [{ 'type': 'amount_above', 'value': 1000 }],
            'actions': [{ 'type': 'transfer', 'amount': 100 }]
        }
        # Validate schema
        is_valid = rule_page.validate_rule_schema(minimum_rule_schema)
        self.assertTrue(is_valid, "Minimum required fields rule schema should be valid.")
        # Submit schema
        response = rule_page.submit_rule_schema(minimum_rule_schema)
        self.assertEqual(response['status'], 'success', "Rule should be created successfully.")

    def test_TC_SCRUM158_10_unsupported_trigger_type(self):
        """
        TC_SCRUM158_10: Submit rule schema with unsupported trigger type and validate error response.
        Steps:
          1. Prepare a rule schema with a new, unsupported trigger type.
          2. Submit the schema.
          3. Expect: API returns appropriate error response.
        """
        rule_page = RuleConfigurationPage(self.driver)
        unsupported_rule_schema = {
            'trigger': 'future_trigger',
            'conditions': [{ 'type': 'amount_above', 'value': 2000 }],
            'actions': [{ 'type': 'transfer', 'amount': 200 }]
        }
        # Validate schema
        is_valid = rule_page.validate_rule_schema(unsupported_rule_schema)
        self.assertFalse(is_valid, "Unsupported trigger type should not be valid.")
        # Submit schema
        response = rule_page.submit_rule_schema(unsupported_rule_schema)
        self.assertEqual(response['status'], 'error', "API should return error for unsupported trigger type.")
        self.assertIn('unsupported trigger', response.get('message', '').lower(), "Error message should mention unsupported trigger.")

    def test_TC_Login_03_email_required_error(self):
        """
        TC_Login_03: Attempt login with email field empty and valid password. Expect 'Email required' error.
        Steps:
          1. Navigate to login page.
          2. Leave email field empty, enter valid password.
          3. Click Login.
          4. Assert 'Email required' error is displayed, and user is not logged in.
        """
        login_page = LoginPage(self.driver)
        login_page.navigate('https://your-app-url/login')  # Replace with actual URL as needed
        login_page.enter_username("")
        login_page.enter_password("ValidPassword123")
        login_page.click_login()
        self.assertTrue(login_page.validate_email_required_error(), "'Email required' error should be displayed.")
        self.assertFalse(login_page.is_login_successful(), "User should not be logged in if email is missing.")

    def test_TC_Login_04_password_required_error(self):
        """
        TC_Login_04: Attempt login with password field empty and valid email. Expect 'Password required' error.
        Steps:
          1. Navigate to login page.
          2. Enter valid email, leave password field empty.
          3. Click Login.
          4. Assert 'Password required' error is displayed, and user is not logged in.
        """
        login_page = LoginPage(self.driver)
        login_page.navigate('https://your-app-url/login')  # Replace with actual URL as needed
        login_page.enter_username("user@example.com")
        login_page.enter_password("")
        login_page.click_login()
        self.assertTrue(login_page.validate_password_required_error(), "'Password required' error should be displayed.")
        self.assertFalse(login_page.is_login_successful(), "User should not be logged in if password is missing.")

    def test_TC_Login_05_empty_fields_error(self):
        """
        TC_Login_05: Leave both email and password fields empty, click Login, validate error messages 'Email required' and 'Password required'.
        Steps:
          1. Navigate to login page.
          2. Leave both email and password fields empty.
          3. Click the 'Login' button.
          4. Assert both 'Email required' and 'Password required' errors are displayed, and user is not logged in.
        """
        login_page = LoginPage(self.driver)
        login_page.navigate('https://your-app-url/login')  # Replace with actual URL as needed
        result = login_page.login_with_empty_fields()
        self.assertTrue(result, "Both 'Email required' and 'Password required' errors should be displayed.")
        self.assertFalse(login_page.is_login_successful(), "User should not be logged in if both fields are empty.")

    def test_TC_Login_06_remember_me_session_persistence(self):
        """
        TC_Login_06: Enter valid credentials, select 'Remember Me', click Login, validate session persists after browser restart.
        Steps:
          1. Navigate to login page.
          2. Enter valid credentials and select 'Remember Me' checkbox.
          3. Click the 'Login' button.
          4. Simulate browser restart (call verify_session_persistence).
          5. Assert user remains logged in (session persists).
        """
        login_page = LoginPage(self.driver)
        login_page.navigate('https://your-app-url/login')  # Replace with actual URL as needed
        login_page.login('user@example.com', 'ValidPassword123', remember_me=True)
        self.assertTrue(login_page.is_login_successful(), "User should be logged in with valid credentials and 'Remember Me' selected.")
        session_persists = login_page.verify_session_persistence()
        self.assertTrue(session_persists, "Session should persist after browser restart with 'Remember Me' enabled.")
