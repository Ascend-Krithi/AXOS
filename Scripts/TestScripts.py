import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage

class TestLogin:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    # Existing test methods...
    def test_login_valid_credentials(self):
        # Stub - already present
        pass

    def test_login_invalid_credentials(self):
        # Stub - already present
        pass

    def test_login_valid_redirect_dashboard(self):
        """
        TC_LOGIN_001: Positive login with valid credentials, redirect to dashboard
        Steps:
        1. Navigate to login page
        2. Enter valid email and password
        3. Click Login
        4. Validate dashboard is displayed
        """
        url = "https://your-app-url.com/login"
        email = "user@example.com"
        password = "ValidPassword123"
        self.login_page.navigate_to_login_page(url)
        self.login_page.login_with_credentials(email, password, remember_me=False)
        assert self.dashboard_page.is_on_dashboard(), "User should be redirected to dashboard after valid login"

    def test_login_without_remember_me_session_expiry(self):
        """
        TC_Login_07: Login without 'Remember Me', session expiration after browser reopen
        Steps:
        1. Navigate to login page
        2. Enter valid credentials without selecting 'Remember Me'
        3. Click Login
        4. Close and reopen browser; navigate to site
        5. Validate session expired (redirect to login)
        """
        url = "https://your-app-url.com/login"
        email = "user@example.com"
        password = "ValidPassword123"
        self.login_page.navigate_to_login_page(url)
        self.login_page.login_with_credentials(email, password, remember_me=False)
        assert self.dashboard_page.is_on_dashboard(), "User should be redirected to dashboard after login"

        # Simulate browser close and reopen
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.driver.get("https://your-app-url.com/dashboard")
        assert self.dashboard_page.is_session_expired(), "Session should expire after browser restart without 'Remember Me'. User should be redirected to login page."

    def test_forgot_password_redirect(self):
        """
        TC_Login_08: Test clicking 'Forgot Password' link and validating redirection to password recovery page.
        Steps:
        1. Navigate to login page
        2. Click the 'Forgot Password' link
        3. Validate user is redirected to password recovery page
        """
        url = "https://your-app-url.com/login"
        self.login_page.navigate_to_login_page(url)
        assert self.login_page.click_forgot_password_and_validate_redirect(), "User should be redirected to password recovery page after clicking 'Forgot Password'"

    def test_email_max_length_login(self):
        """
        TC_Login_09: Test entering maximum allowed email/username length and valid password, then clicking login and validating that the field accepts max input.
        Steps:
        1. Navigate to login page
        2. Enter 255-character email and valid password
        3. Click Login
        4. Validate field accepts max input and login succeeds
        """
        url = "https://your-app-url.com/login"
        email = "a" * 255
        password = "ValidPassword123"
        self.login_page.navigate_to_login_page(url)
        assert self.login_page.validate_email_max_length(255, email, password), "Email field should accept maximum input length of 255 characters"

    def test_login_invalid_credentials_negative(self):
        """
        TC_LOGIN_002: Negative login scenario with invalid credentials.
        Steps:
        1. Navigate to login page
        2. Enter invalid email/username or password (wronguser@example.com / WrongPassword)
        3. Click Login
        Expected: User remains on login page. Error message for invalid credentials is displayed.
        """
        url = "https://your-app-url.com/login"
        invalid_email = "wronguser@example.com"
        invalid_password = "WrongPassword"
        self.login_page.navigate_to_login_page(url)
        result = self.login_page.login_with_invalid_credentials(invalid_email, invalid_password)
        assert result, "Error message for invalid credentials should be displayed and user should remain on login page."

    def test_login_empty_fields_negative(self):
        """
        TC_LOGIN_003: Negative login scenario with empty fields.
        Steps:
        1. Navigate to login page
        2. Leave email/username and/or password fields empty ('' / '')
        3. Click Login
        Expected: User remains on login page. Error or validation message for empty fields is displayed.
        """
        url = "https://your-app-url.com/login"
        self.login_page.navigate_to_login_page(url)
        results = self.login_page.login_with_empty_fields()
        assert results['both_empty'], "Error message for both fields empty should be displayed."
        assert results['email_empty'], "Error message for email empty should be displayed."
        assert results['password_empty'], "Error message for password empty should be displayed."

    def test_login_max_length_valid_credentials(self):
        """
        TC_Login_10: Login with valid email and password at maximum allowed length
        Steps:
        1. Navigate to login page
        2. Enter valid email and password at maximum allowed length (user@example.com / 128-char password)
        3. Click Login
        Expected: Fields accept max input. User is logged in if credentials are valid.
        """
        url = "https://your-app-url.com/login"
        email = "user@example.com"
        password = "A" * 128
        self.login_page.navigate_to_login_page(url)
        # Validate max length email and password fields
        email_ok = self.login_page.enter_max_length_email(email)
        password_ok = self.login_page.enter_max_length_password(password)
        assert email_ok, "Email field should accept maximum allowed length."
        assert password_ok, "Password field should accept maximum allowed length."
        # Login with max length credentials
        login_result = self.login_page.login_with_max_length_credentials(email, password)
        assert login_result['success'], "User should be logged in with valid max length credentials."
        assert self.dashboard_page.is_on_dashboard(), "User should be redirected to dashboard after login with max length credentials."

    def test_login_max_length_boundary(self):
        """
        TC_LOGIN_004: Login with email and password at maximum allowed character length
        Steps:
        1. Navigate to login page
        2. Enter email/username and password at maximum allowed character length (userwithverylongemailaddress@example.com [254 chars] / VeryLongPassword123! [64 chars])
        3. Click Login
        Expected: Fields accept input up to maximum length. User is logged in if credentials are valid; error if invalid.
        """
        url = "https://your-app-url.com/login"
        email = "u" * (254 - len("@example.com")) + "@example.com"
        password = "V" * 64
        self.login_page.navigate_to_login_page(url)
        # Validate max length email and password fields
        email_ok = self.login_page.enter_max_length_email(email)
        password_ok = self.login_page.enter_max_length_password(password)
        assert email_ok, "Email field should accept maximum allowed length (254 chars)."
        assert password_ok, "Password field should accept maximum allowed length (64 chars)."
        # Login with max length credentials
        login_result = self.login_page.login_with_max_length_credentials(email, password)
        if login_result['success']:
            assert self.dashboard_page.is_on_dashboard(), "User should be redirected to dashboard after login with max length credentials."
        else:
            assert login_result['error'], "Error message should be shown for invalid max length credentials."

    def test_login_special_characters(self):
        """
        TC_LOGIN_005: Login with email and password containing special characters
        Steps:
        1. Navigate to login page
        2. Enter email/username and password containing special characters (special_user!@#$/example.com / P@$$w0rd!#)
        3. Click Login
        Expected: Fields accept input. User is logged in if credentials are valid; error if invalid.
        """
        url = "https://your-app-url.com/login"
        email = "special_user!@#$/example.com"
        password = "P@$$w0rd!#"
        self.login_page.navigate(url)
        assert self.login_page.fields_accept_special_characters(email, password), "Fields should accept special characters as input."
        self.login_page.login(email, password)
        # Check login result: either user is logged in or error message is shown
        if self.dashboard_page.is_user_logged_in():
            assert True, "User should be logged in with valid credentials containing special characters."
        else:
            error = self.login_page.get_error_message()
            assert error is not None, "Error message should be displayed for invalid credentials with special characters."

    def test_remember_me_session_persistence(self):
        """
        TC_LOGIN_006: Login with 'Remember Me' checked and validate session persistence after browser reopen
        Steps:
        1. Navigate to login page
        2. Enter valid email/username and password. Select 'Remember Me' checkbox (user@example.com / ValidPassword123)
        3. Click Login
        4. Close and reopen browser
        Expected: 'Remember Me' checkbox is checked. User remains logged in; session persists.
        """
        url = "https://your-app-url.com/login"
        email = "user@example.com"
        password = "ValidPassword123"
        self.login_page.navigate(url)
        self.login_page.login(email, password, remember_me=True)
        assert self.login_page.is_remember_me_checked(), "'Remember Me' checkbox should be checked."
        assert self.dashboard_page.is_user_logged_in(), "User should be logged in after clicking Login with 'Remember Me' checked."
        # Simulate browser close and reopen
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.driver.get("https://your-app-url.com/dashboard")
        assert self.dashboard_page.session_persists(), "Session should persist after browser restart when 'Remember Me' is checked."
