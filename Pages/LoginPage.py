from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = driver.find_element(By.NAME, 'username')
        self.password_field = driver.find_element(By.NAME, 'password')
        self.login_button = driver.find_element(By.CSS_SELECTOR, "input[value='Log In']")

    def enter_username(self, username):
        self.username_field.clear()
        self.username_field.send_keys(username)

    def enter_password(self, password):
        self.password_field.clear()
        self.password_field.send_keys(password)

    def click_login(self):
        self.login_button.click()

    def is_login_page_displayed(self):
        return self.username_field.is_displayed() and self.password_field.is_displayed() and self.login_button.is_displayed()
