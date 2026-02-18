from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.username_field = (By.NAME, "username")
        self.password_field = (By.NAME, "password")
        self.login_button = (By.CSS_SELECTOR, "input[value='Log In']")

    def enter_username(self, username: str):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_field)
        ).clear()
        self.driver.find_element(*self.username_field).send_keys(username)

    def enter_password(self, password: str):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_field)
        ).clear()
        self.driver.find_element(*self.password_field).send_keys(password)

    def click_login(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        ).click()
