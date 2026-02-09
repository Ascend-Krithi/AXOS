import unittest
from selenium import webdriver
from LoginPage import LoginPage
from ProfilePage import ProfilePage
from SettingsPage import SettingsPage

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_TC01_valid_login(self):
        # Existing test method for valid login
        self.login_page.go_to_login_page()
        self.login_page.enter_username("validUser")
        self.login_page.enter_password("validPass")
        self.login_page.submit()
        self.assertTrue(self.login_page.is_login_successful())

    def test_TC02_invalid_login(self):
        # Existing test method for invalid login
        self.login_page.go_to_login_page()
        self.login_page.enter_username("invalidUser")
        self.login_page.enter_password("invalidPass")
        self.login_page.submit()
        self.assertTrue(self.login_page.is_login_failed())

    # --- Begin appended methods for TC09 and TC10 ---

    def test_TC09_login_with_special_characters(self):
        """
        TC09: Attempt login with special characters in username and password.
        Steps:
        1. Navigate to login page.
        2. Enter username and password with special characters.
        3. Submit login form.
        4. Verify error message or login failure.
        """
        self.login_page.go_to_login_page()
        special_username = "!@#$%^&*()_+|~=`{}[]:\";'<>?,./"
        special_password = "<>?/\\|}{[]:;'-_=+!@#$%^&*()"
        self.login_page.enter_username(special_username)
        self.login_page.enter_password(special_password)
        self.login_page.submit()
        self.assertTrue(self.login_page.is_login_failed())
        self.assertTrue(self.login_page.is_error_message_displayed("Invalid characters in username or password"))

    def test_TC10_valid_login_with_simulated_network_error(self):
        """
        TC10: Attempt valid login with simulated network/server error.
        Steps:
        1. Navigate to login page.
        2. Enter valid username and password.
        3. Simulate network/server error before submitting.
        4. Submit login form.
        5. Verify appropriate error handling (e.g., error message, retry option).
        """
        self.login_page.go_to_login_page()
        valid_username = "validUser"
        valid_password = "validPass"
        self.login_page.enter_username(valid_username)
        self.login_page.enter_password(valid_password)
        # Simulate network/server error (mock or trigger error)
        self.login_page.simulate_network_error()
        self.login_page.submit()
        self.assertTrue(self.login_page.is_network_error_message_displayed())
        self.assertTrue(self.login_page.is_retry_option_available())

# Other test classes for ProfilePage and SettingsPage...

if __name__ == "__main__":
    unittest.main()
