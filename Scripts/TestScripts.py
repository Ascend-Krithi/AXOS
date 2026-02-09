
import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage

class TestScripts(unittest.TestCase):

    # Existing test methods...

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
