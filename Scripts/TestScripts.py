import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)
        cls.base_url = "http://localhost:8000"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_TC01_valid_login(self):
        """Test valid login scenario."""
        self.login_page.navigate_to_login(self.base_url)
        self.login_page.enter_username('valid_user')
        self.login_page.enter_password('ValidPass123')
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_dashboard_displayed(), "Dashboard should be displayed after valid login.")

    def test_TC02_invalid_login(self):
        """Test invalid login scenario."""
        self.login_page.navigate_to_login(self.base_url)
        self.login_page.enter_username('invalid_user')
        self.login_page.enter_password('WrongPass')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        self.assertEqual(error_message, 'Invalid username or password', "Error message should match expected.")

    def test_TC03_empty_credentials(self):
        """Test empty username and password, expect error message 'Username and password are required'."""
        self.login_page.navigate_to_login(self.base_url)
        self.login_page.enter_username('')
        self.login_page.enter_password('')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        self.assertEqual(error_message, 'Username and password are required', "Error message should match expected for empty credentials.")

    def test_TC04_empty_username_valid_password(self):
        """Test empty username and valid password, expect error message 'Username is required'."""
        self.login_page.navigate_to_login(self.base_url)
        self.login_page.enter_username('')
        self.login_page.enter_password('ValidPass123')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        self.assertEqual(error_message, 'Username is required', "Error message should match expected for empty username.")

    def test_TC05_empty_password_error(self):
        """TC05: Enter valid username, leave password empty, click login, expect error 'Password is required'."""
        self.login_page.navigate_to_login(self.base_url)
        result = self.login_page.login_with_empty_password('valid_user', 'Password is required')
        self.assertTrue(result, "Error message should match 'Password is required' for empty password.")

    def test_TC06_remember_me_session_persistence(self):
        """TC06: Enter valid credentials, check 'Remember Me', click login, validate session persists after browser restart."""
        self.login_page.navigate_to_login(self.base_url)
        self.login_page.login_with_remember_me('valid_user', 'ValidPass123')
        # Simulate session persistence check (actual browser restart may be handled in framework)
        session_persists = self.login_page.validate_session_persistence(self.base_url)
        self.assertTrue(session_persists, "Session should persist after browser restart when 'Remember Me' is checked.")

if __name__ == '__main__':
    unittest.main()
