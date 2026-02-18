# LoginPage.py
"""
PageClass for Parabank Login Page.
Implements all actions and validations required for login functionality.
QA Notes:
- All locators strictly match Locators.json.
- Methods are atomic and non-destructive.
- Imports are minimal and explicit.
- No business logic outside page interaction.
"""
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

    def is_login_page_displayed(self) -> bool:
        return self.username_field.is_displayed() and self.password_field.is_displayed() and self.login_button.is_displayed()
