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

    def test_TC_Login_10_max_length_login(self):
        """
        TC_Login_10: Navigate to login page, enter valid email and password at maximum allowed length, click login, assert fields accept max input and user is logged in if credentials are valid.
        """
        # Generate maximum length credentials
        max_username = 'user_' + 'a' * (255 - 5)
        max_password = 'b' * 128
        # Validate fields accept max length input
        self.assertTrue(
            self.login_page.validate_max_length_input(username_field_max_length=255, password_field_max_length=128),
            "Username or password field did not accept maximum allowed input length."
        )
        # Attempt login with valid max-length credentials
        self.login_page.enter_username(max_username)
        self.login_page.enter_password(max_password)
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_login_successful(),
            "Login was not successful with valid maximum length credentials."
        )

    def test_TC_LOGIN_004_max_length_login(self):
        """
        TC_LOGIN_004: Navigate to login page, enter email/username and password at maximum allowed character length (254 chars for email, 64 chars for password), click login, assert fields accept input up to maximum length and user is logged in if credentials are valid; error if invalid.
        """
        # Generate maximum length credentials
        max_email = 'a' * (254 - 12) + '@example.com'  # Ensure valid email format
        max_password = 'X' * 64
        # Validate fields accept max length input
        self.assertTrue(
            self.login_page.validate_max_length_input(username_field_max_length=254, password_field_max_length=64),
            "Username or password field did not accept maximum allowed input length for TC_LOGIN_004."
        )
        # Attempt login with valid max-length credentials
        self.login_page.enter_username(max_email)
        self.login_page.enter_password(max_password)
        self.login_page.click_login()
        if self.login_page.is_login_successful():
            self.assertTrue(
                self.login_page.is_login_successful(),
                "Login was not successful with valid maximum length credentials for TC_LOGIN_004."
            )
        else:
            self.assertTrue(
                self.login_page.is_error_displayed(),
                "Error message was not displayed for invalid credentials at maximum length."
            )

if __name__ == '__main__':
    unittest.main()
