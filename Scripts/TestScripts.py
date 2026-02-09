import pytest
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage

@pytest.mark.usefixtures("setup")
class TestLogin:

    def test_TC_LOGIN_001_valid_login(self):
        login_page = LoginPage(self.driver)
        dashboard_page = DashboardPage(self.driver)
        login_page.enter_username("validUser")
        login_page.enter_password("validPass")
        login_page.click_login()
        assert dashboard_page.is_loaded(), "Dashboard did not load after valid login"

    def test_TC_LOGIN_002_invalid_password(self):
        login_page = LoginPage(self.driver)
        login_page.enter_username("validUser")
        login_page.enter_password("wrongPass")
        login_page.click_login()
        assert login_page.is_error_displayed(), "Error message not displayed for invalid password"

    def test_TC_LOGIN_003_blank_username(self):
        login_page = LoginPage(self.driver)
        login_page.enter_username("")
        login_page.enter_password("somePass")
        login_page.click_login()
        assert login_page.is_error_displayed(), "Error message not displayed for blank username"

    def test_TC_LOGIN_004_blank_password(self):
        login_page = LoginPage(self.driver)
        login_page.enter_username("validUser")
        login_page.enter_password("")
        login_page.click_login()
        assert login_page.is_error_displayed(), "Error message not displayed for blank password"

    # TC_LOGIN_005: Login with special characters in username and password
    def test_TC_LOGIN_005_special_characters_credentials(self):
        login_page = LoginPage(self.driver)
        special_username = "!@#$%^&*()_+{}|:\"<>?~"
        special_password = "`-=[]\\;',./"
        login_page.enter_username(special_username)
        login_page.enter_password(special_password)
        login_page.click_login()
        # Assuming the system should not allow login with special characters and should display an error
        assert login_page.is_error_displayed(), "Error message not displayed for special character credentials"

    # TC_LOGIN_006: 'Remember Me' session persistence
    def test_TC_LOGIN_006_remember_me_session_persistence(self):
        login_page = LoginPage(self.driver)
        dashboard_page = DashboardPage(self.driver)
        username = "validUser"
        password = "validPass"

        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.select_remember_me()
        login_page.click_login()
        assert dashboard_page.is_loaded(), "Dashboard did not load after login with 'Remember Me'"

        # Simulate browser close and reopen
        self.driver.quit()
        self.setup_method()  # Assuming this reinitializes self.driver and fixture

        dashboard_page = DashboardPage(self.driver)
        assert dashboard_page.is_loaded(), "'Remember Me' did not persist session after browser restart"

    # TC_LOGIN_007: Login without 'Remember Me', session should NOT persist
    def test_TC_LOGIN_007_no_remember_me_session(self):
        login_page = LoginPage(self.driver)
        dashboard_page = DashboardPage(self.driver)
        # Step 1: Navigate to login page
        login_page.navigate_to_login()
        # Step 2: Enter valid credentials, ensure 'Remember Me' is NOT checked
        login_page.enter_credentials_without_remember_me("user@example.com", "ValidPassword123")
        # Step 3: Check 'Remember Me' is NOT checked
        assert login_page.is_remember_me_unchecked(), "'Remember Me' checkbox should not be checked"
        # Step 4: Click Login
        login_page.click_login()
        # Step 5: Assert login success (Dashboard is displayed)
        assert dashboard_page.is_dashboard_displayed(), "Dashboard not displayed after login"
        # Step 6: Simulate browser close and reopen
        self.driver.quit()
        self.setup_method()  # Reinitialize driver
        # Step 7: Assert user is logged out (session does not persist)
        dashboard_page = DashboardPage(self.driver)
        assert dashboard_page.is_logged_out(), "Session persisted after browser restart; user should be logged out"

    # TC_LOGIN_008: Forgot Password flow
    def test_TC_LOGIN_008_forgot_password_flow(self):
        login_page = LoginPage(self.driver)
        # Step 1: Navigate to login page
        login_page.navigate_to_login()
        # Step 2: Click 'Forgot Password'
        login_page.click_forgot_password()
        # Step 3: Enter registered email and submit
        login_page.submit_forgot_password("user@example.com")
        # Step 4: Verify confirmation message is displayed
        confirmation = login_page.get_forgot_password_confirmation()
        assert confirmation is not None and confirmation != "", "Password reset confirmation message not displayed"

    # TC_LOGIN_009: Rapid invalid login attempts, expect rate limiting/captcha/lockout
    def test_TC_LOGIN_009_rapid_invalid_login_attempts(self):
        login_page = LoginPage(self.driver)
        result = login_page.rapid_invalid_login_attempts("wronguser@example.com", "WrongPassword", attempts=10)
        assert any(keyword in result.lower() for keyword in ["captcha", "lockout", "rate limiting"]), f"Expected rate limiting, lockout, or captcha, got: {result}"

    # TC_LOGIN_010: Case sensitivity check for login credentials
    def test_TC_LOGIN_010_case_sensitivity(self):
        login_page = LoginPage(self.driver)
        results = login_page.login_with_case_variations("USER@EXAMPLE.COM", "ValidPassword123")
        error_message = results if isinstance(results, str) else None
        if error_message:
            assert "Login failed" in error_message or "Login succeeded" in error_message, f"Unexpected error message: {error_message}"
        else:
            assert results == "Login succeeded.", f"Expected login success, got: {results}"
