# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.username_field = (By.NAME, "username")
        self.password_field = (By.NAME, "password")
        self.login_button = (By.CSS_SELECTOR, "input[value='Log In']")

    def enter_username(self, username: str):
        elem = self.driver.find_element(*self.username_field)
        elem.clear()
        elem.send_keys(username)

    def enter_password(self, password: str):
        elem = self.driver.find_element(*self.password_field)
        elem.clear()
        elem.send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
