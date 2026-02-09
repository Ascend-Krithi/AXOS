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

    # ... [rest of file omitted for brevity, but you have the full content above]

    def test_TC_LOGIN_009_rapid_invalid_login_attempts(self):
        """
        TC_LOGIN_009: Rapid invalid login attempts
        Steps:
        1. Attempt to log in 10 times with invalid credentials (wronguser@example.com / WrongPassword).
        2. After each attempt, verify error message is displayed.
        3. After rapid attempts, validate rate limiting, lockout, or captcha is triggered.
        Expected:
        - Error message shown for each invalid attempt.
        - After 10 rapid failures, rate limiting, account lockout, or captcha is enforced by the system.
        """
        email = "wronguser@example.com"
        password = "WrongPassword"
        attempts = 10
        lockout_triggered = False
        for i in range(attempts):
            self.login_page.enter_email(email)
            self.login_page.enter_password(password)
            self.login_page.click_login()
            assert self.login_page.is_error_message_displayed(), f"Error message not displayed on attempt {i+1}"
            # Check for lockout/captcha after each attempt
            if self.login_page.is_lockout_message_displayed() or self.login_page.is_captcha_displayed():
                lockout_triggered = True
                break
        # After all attempts, verify lockout/rate limiting/captcha
        assert lockout_triggered or self.login_page.is_lockout_message_displayed() or self.login_page.is_captcha_displayed(), \
            "Rate limiting, lockout, or captcha was not triggered after 10 rapid invalid login attempts."

    def test_TC_LOGIN_010_case_sensitivity_validation(self):
        """
        TC_LOGIN_010: Case sensitivity validation for credentials
        Steps:
        1. Attempt to log in with uppercase email (USER@EXAMPLE.COM) and valid password (ValidPassword123).
        2. Verify login fails if credentials do not match exactly (case-sensitive).
        3. Attempt login with correct case (user@example.com / ValidPassword123) and verify login succeeds.
        Expected:
        - Login fails for case mismatch.
        - Login succeeds for exact match.
        """
        email_upper = "USER@EXAMPLE.COM"
        email_exact = "user@example.com"
        password = "ValidPassword123"

        # Attempt with uppercase email
        self.login_page.enter_email(email_upper)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        assert self.login_page.is_error_message_displayed(), "Login should fail when email case does not match."

        # Attempt with exact case
        self.login_page.enter_email(email_exact)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        assert self.dashboard_page.is_logged_in(), "Login should succeed when credentials match exactly (case-sensitive)."
