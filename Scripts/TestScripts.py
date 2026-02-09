import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_TC01_valid_login(self):
        self.login_page.navigate_to_login()
        self.login_page.enter_username('valid_user')
        self.login_page.enter_password('valid_pass')
        self.login_page.submit()
        self.assertTrue(self.login_page.validate_successful_login())

    def test_TC02_invalid_login(self):
        self.login_page.navigate_to_login()
        self.login_page.enter_username('invalid_user')
        self.login_page.enter_password('invalid_pass')
        self.login_page.submit()
        error = self.login_page.get_error_message()
        self.assertEqual(error, 'Invalid username or password')

    def test_TC03_empty_username_and_password(self):
        self.login_page.navigate_to_login()
        self.login_page.submit_empty_credentials()
        error = self.login_page.validate_error_for_empty_credentials()
        self.assertEqual(error, 'Username and password are required')

    def test_TC04_empty_username_valid_password(self):
        self.login_page.navigate_to_login()
        self.login_page.submit_empty_username_valid_password('valid_pass')
        error = self.login_page.validate_error_for_empty_credentials()
        self.assertEqual(error, 'Username is required')

if __name__ == "__main__":
    unittest.main()
