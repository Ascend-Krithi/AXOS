
import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage

class TestLogin:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://your-app-url.com')
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

    # New test method for TC_LOGIN_001: Standard valid login and dashboard redirection
    def test_login_valid_redirect_dashboard(self):
        """
        TC_LOGIN_001: Standard valid login and dashboard redirection
        Steps:
        1. Enter valid email and password.
        2. Click Login.
        3. Verify dashboard is displayed.
        """
        email = "user@example.com"
        password = "ValidPassword123"
        self.login_page.enter_email(email)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        assert self.dashboard_page.is_dashboard_displayed(), "Dashboard page should be displayed after valid login."

    # New test method for TC_Login_07: Login without 'Remember Me', verify session expiration after browser reopen
    def test_login_without_remember_me_session_expiry(self):
        """
        TC_Login_07: Login without 'Remember Me', verify session expiration after browser reopen
        Steps:
        1. Enter valid email and password.
        2. Uncheck 'Remember Me'.
        3. Click Login.
        4. Verify dashboard is displayed.
        5. Close browser and reopen.
        6. Navigate to dashboard URL.
        7. Verify session expired and redirected to login.
        """
        email = "user@example.com"
        password = "ValidPassword123"
        self.login_page.enter_email(email)
        self.login_page.enter_password(password)
        self.login_page.uncheck_remember_me()
        self.login_page.click_login()
        assert self.dashboard_page.is_dashboard_displayed(), "Dashboard page should be displayed after login without 'Remember Me'."

        # Simulate browser close and reopen
        self.driver.quit()
        self.driver = webdriver.Chrome()
        self.driver.get('https://your-app-url.com/dashboard')
        # Re-initialize page objects with new driver
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        # Session should be expired, so login page should be displayed
        assert self.login_page.is_login_page_displayed(), "Session should expire after browser restart without 'Remember Me'. User should be redirected to login page."
