import unittest
from RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage
from selenium import webdriver

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.page = RuleConfigurationPage()

    # Existing test methods...
    # ...

    # --- New LoginPage test methods ---
    def test_TC03_empty_username_and_password(self):
        """TC03: Empty username and password should trigger error 'Username and password are required'."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.leave_fields_empty()
        login_page.click_login_button()
        self.assertTrue(login_page.validate_error_message('Username and password are required'), "Expected error message not found.")
        driver.quit()

    def test_TC04_empty_username_valid_password(self):
        """TC04: Empty username and valid password should trigger error 'Username is required'."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.enter_valid_password_empty_username('ValidPass123')
        login_page.click_login_button()
        self.assertTrue(login_page.validate_error_message('Username is required'), "Expected error message not found.")
        driver.quit()

if __name__ == "__main__":
    unittest.main()
