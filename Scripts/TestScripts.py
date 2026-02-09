import unittest
from RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage
from Pages.ForgotPasswordPage import ForgotPasswordPage
from selenium import webdriver

class TestRuleConfiguration(unittest.TestCase):
    # ... (existing test methods and logic remain unchanged)
    pass

# --- Append new test methods below ---

class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_TC05_login_empty_password(self):
        """
        TC05: Attempt login with valid username and empty password, expect error 'Password is required'.
        """
        self.login_page.navigate_to_login_page()
        self.login_page.enter_username("valid_user")
        self.login_page.leave_password_empty()
        self.login_page.click_login_button()
        error = self.login_page.validate_error_message()
        self.assertEqual(error, "Password is required")

    def test_TC06_login_remember_me(self):
        """
        TC06: Login with valid credentials, check 'Remember Me', validate session persists after browser restart.
        """
        self.login_page.navigate_to_login_page()
        self.login_page.enter_username("valid_user")
        self.login_page.enter_password("ValidPass123")
        self.login_page.check_remember_me()
        self.login_page.click_login_button()
        self.assertTrue(self.login_page.validate_session_persistence())
        # Simulate browser restart
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        session_persistent = self.login_page.validate_session_persistence()
        self.assertTrue(session_persistent)
