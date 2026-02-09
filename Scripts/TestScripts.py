import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestScripts(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/login")
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # ... existing test methods ...

    def test_TC_Login_05_empty_email_and_password(self):
        """TC_Login_05: Leave both email and password fields empty, click Login, assert both 'Email required' and 'Password required' errors are displayed, user is not logged in."""
        self.login_page.login_with_empty_fields()
        email_error = self.login_page.get_email_error()
        password_error = self.login_page.get_password_error()
        self.assertEqual(email_error, "Email required", "Email required error not displayed")
        self.assertEqual(password_error, "Password required", "Password required error not displayed")
        self.assertFalse(self.login_page.is_logged_in(), "User should not be logged in with empty fields")

    def test_TC_Login_06_remember_me_session_persistence(self):
        """TC_Login_06: Login with valid credentials and 'Remember Me', restart browser and verify session persists (user remains logged in)."""
        valid_email = "user@example.com"
        valid_password = "ValidPassword123"
        self.login_page.enter_email(valid_email)
        self.login_page.enter_password(valid_password)
        self.login_page.select_remember_me()
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_logged_in(), "User should be logged in after valid credentials with 'Remember Me'")

        # Simulate browser restart for session persistence check
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/")
        self.login_page = LoginPage(self.driver)
        session_persistent = self.login_page.verify_session_persistence()
        self.assertTrue(session_persistent, "Session should persist after browser restart when 'Remember Me' is selected")

        # Clean up
        self.driver.quit()
        self.driver = None
