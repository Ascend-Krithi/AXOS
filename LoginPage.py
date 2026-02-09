from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    URL = "https://example-ecommerce.com/login"

    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def login(self, email: str, password: str, remember_me: bool = False):
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
        if remember_me:
            self.driver.find_element(*self.REMEMBER_ME_CHECKBOX).click()
        self.driver.find_element(*self.LOGIN_SUBMIT).click()

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def get_validation_error(self):
        return self.driver.find_element(*self.VALIDATION_ERROR).text

    def is_empty_field_prompt_displayed(self):
        return len(self.driver.find_elements(*self.EMPTY_FIELD_PROMPT)) > 0

    def is_logged_in(self):
        return len(self.driver.find_elements(*self.DASHBOARD_HEADER)) > 0 and len(self.driver.find_elements(*self.USER_PROFILE_ICON)) > 0
