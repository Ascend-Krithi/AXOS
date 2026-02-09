import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://example.com/login')
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # Existing test methods...

    def test_TC_LOGIN_002_invalid_credentials(self):
        """
        TC_LOGIN_002: Navigate to login page, enter invalid credentials, click login, assert error message for invalid credentials is displayed.
        """
        self.login_page.enter_username('wronguser@example.com')
        self.login_page.enter_password('WrongPassword')
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_error_displayed(),
            "Error message for invalid credentials was not displayed."
        )

    def test_TC_LOGIN_003_empty_fields(self):
        """
        TC_LOGIN_003: Navigate to login page, leave email/username and/or password fields empty, click login, assert error or validation message for empty fields is displayed.
        """
        # Test with both fields empty
        self.login_page.enter_username('')
        self.login_page.enter_password('')
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_error_displayed(),
            "Error or validation message for empty fields was not displayed."
        )
        # Optionally, test with only username empty
        self.login_page.enter_username('')
        self.login_page.enter_password('SomePassword')
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_error_displayed(),
            "Error or validation message for empty username was not displayed."
        )
        # Optionally, test with only password empty
        self.login_page.enter_username('someuser@example.com')
        self.login_page.enter_password('')
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_error_displayed(),
            "Error or validation message for empty password was not displayed."
        )

if __name__ == '__main__':
    unittest.main()
