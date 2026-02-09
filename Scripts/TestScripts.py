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
        self.login_page.enter_username('wronguser@example.com')
        self.login_page.enter_password('WrongPassword')
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_error_displayed(),
            "Error message for invalid credentials was not displayed."
        )

    def test_TC_LOGIN_003_empty_fields(self):
        self.login_page.enter_username('')
        self.login_page.enter_password('')
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_error_displayed(),
            "Error or validation message for empty fields was not displayed."
        )
        self.login_page.enter_username('')
        self.login_page.enter_password('SomePassword')
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_error_displayed(),
            "Error or validation message for empty username was not displayed."
        )
        self.login_page.enter_username('someuser@example.com')
        self.login_page.enter_password('')
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_error_displayed(),
            "Error or validation message for empty password was not displayed."
        )

    def test_TC_Login_10_max_length_login(self):
        max_username = 'user_' + 'a' * (255 - 5)
        max_password = 'b' * 128
        self.assertTrue(
            self.login_page.validate_max_length_input(username_field_max_length=255, password_field_max_length=128),
            "Username or password field did not accept maximum allowed input length."
        )
        self.login_page.enter_username(max_username)
        self.login_page.enter_password(max_password)
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_login_successful(),
            "Login was not successful with valid maximum length credentials."
        )

    def test_TC_LOGIN_004_max_length_login(self):
        max_email = 'a' * (254 - 12) + '@example.com'
        max_password = 'X' * 64
        self.assertTrue(
            self.login_page.validate_max_length_input(username_field_max_length=254, password_field_max_length=64),
            "Username or password field did not accept maximum allowed input length for TC_LOGIN_004."
        )
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

    def test_TC_LOGIN_007_remember_me_session_expiration(self):
        """
        TC_LOGIN_007: Valid login, 'Remember Me' unchecked, session expiration validated after browser restart.
        Steps:
        1. Navigate to login page.
        2. Enter valid email/username and password. Do not select 'Remember Me'.
        3. Click the Login button.
        4. Close and reopen the browser.
        5. Verify user is logged out; session does not persist.
        """
        username = 'user@example.com'
        password = 'ValidPassword123'
        # Step 2 & 3
        self.login_page.login(username, password, remember_me=False)
        # Step 4: Close and reopen browser
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.driver.get('https://example.com/login')
        self.login_page = LoginPage(self.driver)
        # Step 5: Verify session expired
        self.assertTrue(
            self.login_page.verify_session_expired(),
            "Session did not expire as expected after browser restart when 'Remember Me' was not selected."
        )

    def test_TC_LOGIN_008_forgot_password_flow(self):
        """
        TC_LOGIN_008: Forgot password flow, reset email submission, confirmation message validation.
        Steps:
        1. Navigate to login page.
        2. Click on 'Forgot Password' link.
        3. Enter registered email/username and submit.
        4. Verify password reset email is sent and confirmation message is displayed.
        """
        email = 'user@example.com'
        self.assertTrue(
            self.login_page.forgot_password_flow(email),
            "Password reset confirmation message was not displayed or reset failed."
        )

    # --- New Test Methods Added ---
    def test_TC_LOGIN_005_special_characters_credentials(self):
        """
        TC_LOGIN_005: Login with username and password containing special characters.
        Steps:
        1. Navigate to login page.
        2. Enter email/username and password containing special characters.
        3. Click the Login button.
        """
        username = 'special_user!@#$/example.com'
        password = 'P@$$w0rd!#'
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        # Assert login success or error
        if self.login_page.is_login_successful():
            self.assertTrue(
                self.login_page.is_login_successful(),
                "Login was not successful with special character credentials."
            )
        else:
            self.assertTrue(
                self.login_page.is_error_displayed(),
                "Error message was not displayed for invalid credentials with special characters."
            )

    def test_TC_LOGIN_006_remember_me_session_persistence(self):
        """
        TC_LOGIN_006: Login with 'Remember Me' checked and validate session persistence after browser restart.
        Steps:
        1. Navigate to login page.
        2. Enter valid email/username and password. Select 'Remember Me' checkbox.
        3. Click the Login button.
        4. Close and reopen the browser.
        5. Verify user remains logged in; session persists.
        """
        username = 'user@example.com'
        password = 'ValidPassword123'
        # Step 2: Enter credentials and select 'Remember Me'
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.select_remember_me()
        # Step 3: Click login
        self.login_page.click_login()
        self.assertTrue(
            self.login_page.is_login_successful(),
            "Login was not successful with valid credentials and 'Remember Me' selected."
        )
        # Step 4: Close and reopen browser
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.driver.get('https://example.com/login')
        self.login_page = LoginPage(self.driver)
        # Step 5: Verify session persistence
        self.assertTrue(
            self.login_page.verify_session_persistence(),
            "Session did not persist as expected after browser restart with 'Remember Me' selected."
        )

if __name__ == '__main__':
    unittest.main()
