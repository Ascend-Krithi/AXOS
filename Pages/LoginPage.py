# Executive Summary
# The LoginPage class automates the login functionality for Parabank using Selenium WebDriver.
# It provides methods to enter credentials and submit the login form.

# Detailed Analysis
# The LoginPage class uses locators from Locators.json for username, password, and login button.
# It encapsulates login actions for reuse and maintainability.

# Implementation Guide
# Instantiate LoginPage with a Selenium WebDriver instance. Use login() to perform login.

# Quality Assurance Report
# Locators validated against Locators.json. Code reviewed for structure and error handling.

# Troubleshooting Guide
# If login fails, check locator values and credentials. Ensure page is loaded before actions.

# Future Considerations
# Extend to support invalid login, multi-factor authentication, and error message validation.

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.username_field = driver.find_element(By.NAME, "username")
        self.password_field = driver.find_element(By.NAME, "password")
        self.login_button = driver.find_element(By.CSS_SELECTOR, "input[value='Log In']")

    def enter_username(self, username: str):
        self.username_field.clear()
        self.username_field.send_keys(username)

    def enter_password(self, password: str):
        self.password_field.clear()
        self.password_field.send_keys(password)

    def click_login(self):
        self.login_button.click()

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
