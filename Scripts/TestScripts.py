import unittest
from RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage
from Pages.ForgotPasswordPage import ForgotPasswordPage
from selenium import webdriver

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.page = RuleConfigurationPage()

    # Existing test methods...

    def test_TC_SCRUM158_01(self):
        ...
    # (all other methods as above)

    def test_TC03_login_empty_credentials(self):
        ...
    def test_TC04_login_empty_username(self):
        ...

    def test_TC05_login_empty_password(self):
        """TC05: Navigate to login page, enter valid username and leave password empty, click login, expect error 'Password is required'."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        try:
            login_page.navigate_to_login_page()
            login_page.enter_username("valid_user")
            login_page.leave_password_empty()
            login_page.click_login_button()
            result = login_page.validate_error_message("Password is required")
            self.assertTrue(result, "Expected error message 'Password is required' not displayed.")
        finally:
            driver.quit()

    def test_TC06_login_remember_me(self):
        """TC06: Navigate to login page, enter valid username and password, check 'Remember Me', click login, expect session persists after browser restart."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        try:
            login_page.navigate_to_login_page()
            login_page.enter_username("valid_user")
            login_page.enter_password("ValidPass123")
            login_page.select_remember_me()
            login_page.click_login_button()
            result = login_page.validate_session_persistence()
            self.assertTrue(result, "Session did not persist after browser restart.")
        finally:
            driver.quit()

    def test_TC07_forgot_password_flow(self):
        """TC07: Navigate to login page, click 'Forgot Password', enter registered email, submit, validate reset instructions sent."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        forgot_password_page = ForgotPasswordPage(driver)
        try:
            login_page.navigate_to_login_page()
            login_page.click_forgot_password_link()
            forgot_password_page.enter_registered_email("registered_user@example.com")
            forgot_password_page.submit_reset_request()
            result = forgot_password_page.validate_reset_instructions_sent()
            self.assertTrue(result, "Reset instructions were not sent to the registered email.")
        finally:
            driver.quit()

    def test_TC08_login_max_length_credentials(self):
        """TC08: Navigate to login page, enter username and password at max allowed length (50 chars), click login, validate system response."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        try:
            login_page.navigate_to_login_page()
            max_length_username = "u" * 50
            max_length_password = "p" * 50
            login_page.enter_username(max_length_username)
            login_page.enter_password(max_length_password)
            login_page.click_login_button()
            # Validate system response: either successful login or specific error message
            success = login_page.validate_login_success()
            if not success:
                error_displayed = login_page.validate_error_message("Invalid credentials")
                self.assertTrue(error_displayed, "Neither login success nor expected error message was displayed.")
            else:
                self.assertTrue(success, "Login with max-length credentials should succeed or fail with proper error.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
