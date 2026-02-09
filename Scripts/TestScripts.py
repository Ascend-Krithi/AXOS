# TestScripts.py
"""
Automated test scripts for LoginPage and DashboardPage scenarios.
Covers: TC_LOGIN_005 (empty fields, error message validation), TC_LOGIN_006 (valid login, 'Remember Me', session persistence after browser reopen)
Strict adherence to Selenium Python best practices, atomic test methods, robust locator handling, and comprehensive docstrings.
"""
import pytest
from selenium import webdriver
from LoginPage import LoginPage
from DashboardPage import DashboardPage

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

class TestLogin:
    """
    Test suite for LoginPage scenarios.
    """
    def test_login_empty_fields(self, driver):
        """
        TC_LOGIN_005: Validate error message for empty email/username and password fields.
        Steps:
        1. Navigate to login page.
        2. Leave both fields empty, click login.
        3. Validate error message.
        """
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page("https://your-app-url.com/login")
        results = login_page.login_with_empty_fields()
        assert results['both_empty'], "Error message for both empty fields is incorrect."
        assert results['email_empty'], "Error message for email empty is incorrect."
        assert results['password_empty'], "Error message for password empty is incorrect."

    def test_valid_login_remember_me_session_persistence(self, driver):
        """
        TC_LOGIN_006: Valid login with 'Remember Me' checked, session persists after browser reopen.
        Steps:
        1. Navigate to login page.
        2. Enter valid credentials, check 'Remember Me'.
        3. Click login.
        4. Close and reopen browser, revisit site.
        5. Validate session persistence and dashboard display.
        """
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        login_page.navigate_to_login_page("https://your-app-url.com/login")
        login_page.login_and_persist_session("user@example.com", "ValidPass123", remember_me=True)
        assert dashboard_page.is_on_dashboard(), "User was not redirected to dashboard after login."
        # Simulate browser close and reopen for session persistence
        driver.quit()
        driver2 = webdriver.Chrome()
        dashboard_page2 = DashboardPage(driver2)
        driver2.get("https://your-app-url.com/dashboard")
        assert dashboard_page2.is_session_persistent(), "Session did not persist after browser reopen."
        driver2.quit()
