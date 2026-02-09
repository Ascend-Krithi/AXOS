import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_valid_login(self):
        # Existing test method for valid login
        self.login_page.navigate_to_login()
        self.login_page.login_with_credentials('validuser@example.com', 'ValidPassword')
        self.assertTrue(self.login_page.validate_login_success())

    # TC_LOGIN_002: Invalid credentials
    def test_invalid_login(self):
        """TC_LOGIN_002: Enter invalid email/username or password and verify error message."""
        self.login_page.navigate_to_login()
        self.login_page.login_with_credentials('wronguser@example.com', 'WrongPassword')
        # Assert that the error message for invalid credentials is displayed
        self.assertTrue(self.login_page.validate_invalid_credentials_error())

    # TC_Login_01: Valid login, redirect to dashboard
    def test_TC_Login_01_valid_login_redirect_dashboard(self):
        """TC_Login_01: Navigate to login, enter valid credentials, expect redirect to dashboard."""
        self.login_page.navigate_to_login()
        self.login_page.login_with_credentials('user@example.com', 'ValidPassword123')
        self.assertTrue(self.login_page.is_dashboard_loaded(), msg="Dashboard should be loaded after valid login.")

    # TC_Login_02: Invalid login, error message
    def test_TC_Login_02_invalid_login_error_message(self):
        """TC_Login_02: Navigate to login, enter invalid credentials, expect error message 'Invalid credentials'."""
        self.login_page.navigate_to_login()
        self.login_page.login_with_credentials('wronguser@example.com', 'WrongPassword')
        error_msg = self.login_page.get_error_message()
        self.assertEqual(error_msg, 'Invalid credentials', msg="Error message should be 'Invalid credentials' for invalid login.")
        self.assertFalse(self.login_page.is_dashboard_loaded(), msg="Dashboard should NOT be loaded after invalid login.")

    # ... (other tests)
