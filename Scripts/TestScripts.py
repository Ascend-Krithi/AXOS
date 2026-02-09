# Placeholder for new TC_LOGIN_005 and TC_LOGIN_006 tests

import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_TC_LOGIN_009_max_char_boundary(self):
        # Step 1: Navigate to login page
        self.login_page.navigate_to_login('https://example.com/login')
        # Step 2: Verify max input length for username and password
        self.assertTrue(self.login_page.verify_max_input_length(LoginPage.LOGIN_USERNAME, 50), 'Username field did not enforce max length')
        self.assertTrue(self.login_page.verify_max_input_length(LoginPage.LOGIN_PASSWORD, 50), 'Password field did not enforce max length')
        # Enter 50 chars for each field
        username = 'X'*50
        password = 'X'*50
        self.login_page.enter_credentials(username, password)
        # Step 3: Click login
        self.login_page.click_login()
        # Assert error message or login success, and no field overflow
        error_shown = self.login_page.is_specific_error_message_displayed(["Invalid credentials"]) # or login_page.is_logged_in()
        self.assertTrue(error_shown or hasattr(self.login_page, 'is_logged_in') and self.login_page.is_logged_in(), 'No error message or login success detected')

    def test_TC_LOGIN_010_unregistered_user(self):
        # Step 1: Navigate to login page
        self.login_page.navigate_to_login('https://example.com/login')
        # Step 2: Enter unregistered credentials
        self.login_page.enter_credentials('unknown@example.com', 'RandomPass789')
        # Step 3: Click login
        self.login_page.click_login()
        # Assert error message 'User not found' or 'Invalid credentials', user remains on login page
        error_shown = self.login_page.is_specific_error_message_displayed(["User not found", "Invalid credentials"])
        self.assertTrue(error_shown, 'Expected error message not shown for unregistered user')

if __name__ == '__main__':
    unittest.main()
