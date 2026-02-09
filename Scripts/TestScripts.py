import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver, base_url="http://localhost:8000")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Existing test methods preserved below
    # ... (existing methods here)

    def test_TC01_valid_login(self):
        """Test valid login scenario."""
        self.login_page.go_to_login_page()
        self.login_page.set_username('valid_user')
        self.login_page.set_password('ValidPass123')
        self.login_page.click_login()
        # Add your dashboard assertion here

    def test_TC02_invalid_login(self):
        """Test invalid login scenario."""
        self.login_page.go_to_login_page()
        self.login_page.set_username('invalid_user')
        self.login_page.set_password('WrongPass')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        self.assertEqual(error_message, 'Invalid username or password', "Error message should match expected.")
        # Add dashboard assertion here

    def test_TC03_empty_credentials(self):
        """Test empty username and password, expect error message 'Username and password are required'."""
        self.login_page.go_to_login_page()
        self.login_page.set_username('')
        self.login_page.set_password('')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        self.assertEqual(error_message, 'Username and password are required', "Error message should match expected for empty credentials.")

    def test_TC04_empty_username_valid_password(self):
        """Test empty username and valid password, expect error message 'Username is required'."""
        self.login_page.go_to_login_page()
        self.login_page.set_username('')
        self.login_page.set_password('ValidPass123')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        self.assertEqual(error_message, 'Username is required', "Error message should match expected for empty username.")

if __name__ == '__main__':
    unittest.main()
