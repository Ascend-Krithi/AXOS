import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # Existing test cases...
    # ...<rest of file>...

    def test_TC09_special_character_login(self):
        """
        TC09: Login with special characters in username and password.
        Expects either successful login or proper error message.
        """
        self.login_page.enter_username('user!@#')
        self.login_page.enter_password('pass$%^&*')
        self.login_page.click_login()
        # Check for error or successful login
        if self.login_page.is_error_displayed():
            error_message = self.login_page.get_error_message()
            self.assertTrue('invalid' in error_message.lower() or 'special' in error_message.lower())
        else:
            # Optionally check if dashboard is loaded
            self.assertTrue(self.dashboard_page.is_loaded())

    def test_TC10_server_error_during_login(self):
        """
        TC10: Simulate server/network error during login.
        Expects proper error message and login not processed.
        """
        self.login_page.enter_username('valid_user')
        self.login_page.enter_password('ValidPass123')
        self.login_page.simulate_server_error()
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_server_error_displayed())
        error_message = self.login_page.get_server_error_message()
        self.assertIn('server', error_message.lower())
        self.assertIn('error', error_message.lower())
        # Ensure dashboard is not loaded
        self.assertFalse(self.dashboard_page.is_loaded())

if __name__ == '__main__':
    unittest.main()
