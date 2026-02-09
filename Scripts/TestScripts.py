
import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage

class TestScripts(unittest.TestCase):

    def test_login_valid_credentials(self):
        """TC01: Validate successful login redirects to dashboard."""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.go_to_login_page()
            login_page.enter_username('valid_user')
            login_page.enter_password('valid_password')
            login_page.click_login()
            dashboard_page = DashboardPage(driver)
            self.assertTrue(dashboard_page.is_dashboard_displayed(), "Dashboard should be displayed after valid login.")
        finally:
            driver.quit()

    def test_login_invalid_credentials(self):
        """TC02: Validate error handling for invalid credentials."""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.go_to_login_page()
            login_page.enter_username('invalid_user')
            login_page.enter_password('invalid_password')
            login_page.click_login()
            self.assertTrue(login_page.is_error_message_displayed(), "Error message should be displayed for invalid login.")
        finally:
            driver.quit()

    def test_login_empty_fields(self):
        """TC03: Validate error message 'Username and password are required' is displayed when both fields are empty."""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.navigate('https://your-login-page-url.com')
            login_page.enter_username('')
            login_page.enter_password('')
            login_page.click_login()
            self.assertTrue(login_page.is_empty_fields_error_displayed(), "Error message 'Username and password are required' should be displayed.")
        finally:
            driver.quit()

    def test_login_empty_username(self):
        """TC04: Validate error message 'Username is required' is displayed when username is empty and password is provided."""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.navigate('https://your-login-page-url.com')
            login_page.enter_username('')
            login_page.enter_password('ValidPass123')
            login_page.click_login()
            self.assertTrue(login_page.is_username_required_error_displayed(), "Error message 'Username is required' should be displayed.")
        finally:
            driver.quit()

    def test_forgot_password_flow(self):
        """TC07: Forgot Password flow - Navigate, click 'Forgot Password', enter registered email, submit, assert success message."""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.navigate('https://your-login-page-url.com')
            login_page.click_forgot_password()
            login_page.enter_password_recovery_email('valid_user@example.com')
            login_page.submit_password_recovery()
            self.assertTrue(login_page.is_password_recovery_success_message_displayed(), "Password reset instructions should be sent and success message displayed.")
        finally:
            driver.quit()

    def test_max_length_credentials_validation(self):
        """TC08: Max-Length Credentials Validation - Navigate, enter max-length username/password, click login, assert fields accept max input and login is processed."""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.navigate('https://your-login-page-url.com')
            max_username = 'u' * 50
            max_password = 'p' * 50
            username_valid = login_page.enter_max_length_username(max_username)
            password_valid = login_page.enter_max_length_password(max_password)
            login_page.click_login()
            login_successful, username_field_valid, password_field_valid = login_page.validate_max_length_login(max_username, max_password)
            self.assertTrue(username_valid and password_valid, "Fields should accept maximum length input.")
            self.assertTrue(username_field_valid, "Username field should accept max-length input.")
            self.assertTrue(password_field_valid, "Password field should accept max-length input.")
            self.assertTrue(login_successful or login_page.is_error_displayed(), "Login should be processed and either succeed or show proper error message.")
        finally:
            driver.quit()
