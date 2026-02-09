import unittest
from RuleConfigurationPage import RuleConfigurationPage
from LoginPage import LoginPage
from selenium import webdriver

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

class TestLoginPage(unittest.TestCase):
    """Test cases for LoginPage."""

    def setUp(self):
        # Setup WebDriver and base_url as per your environment/config
        self.driver = webdriver.Chrome()  # Or any other WebDriver
        self.base_url = "http://localhost:8000"  # Update as needed
        self.login_page = LoginPage(self.driver, self.base_url)

    def tearDown(self):
        self.driver.quit()

    def test_TC01_valid_login_redirects_to_dashboard(self):
        """TC01: Valid login should redirect to dashboard/home."""
        username = "valid_user"
        password = "ValidPass123"
        self.login_page.go_to_login_page()
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        login_success = self.login_page.is_login_successful()
        self.assertTrue(login_success, "Valid login should redirect to dashboard/home.")

    def test_TC02_invalid_login_shows_error_message(self):
        """TC02: Invalid login should display error message and not log in."""
        username = "invalid_user"
        password = "WrongPass"
        self.login_page.go_to_login_page()
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        error_displayed = self.login_page.is_error_message_displayed()
        self.assertTrue(error_displayed, "Error message should be displayed for invalid login.")
        login_success = self.login_page.is_login_successful()
        self.assertFalse(login_success, "Invalid login should not redirect to dashboard/home.")

if __name__ == "__main__":
    unittest.main()
