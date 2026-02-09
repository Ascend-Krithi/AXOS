from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.url = "https://example-ecommerce.com/login"
        self.email_field = (By.ID, "login-email")
        self.password_field = (By.ID, "login-password")
        self.remember_me_checkbox = (By.ID, "remember-me")
        self.login_submit = (By.ID, "login-submit")
        self.forgot_password_link = (By.CSS_SELECTOR, "a.forgot-password-link")
        self.error_message = (By.CSS_SELECTOR, "div.alert-danger")
        self.validation_error = (By.CSS_SELECTOR, ".invalid-feedback")
        self.empty_field_prompt = (By.XPATH, "//*[text()='Mandatory fields are required']")
        self.dashboard_header = (By.CSS_SELECTOR, "h1.dashboard-title")
        self.user_profile_icon = (By.CSS_SELECTOR, ".user-profile-name")

    def open(self):
        self.driver.get(self.url)

    def login(self, email: str, password: str, remember_me: bool = False):
        self.driver.find_element(*self.email_field).clear()
        self.driver.find_element(*self.email_field).send_keys(email)
        self.driver.find_element(*self.password_field).clear()
        self.driver.find_element(*self.password_field).send_keys(password)
        checkbox = self.driver.find_element(*self.remember_me_checkbox)
        if remember_me != checkbox.is_selected():
            checkbox.click()
        self.driver.find_element(*self.login_submit).click()

    def click_forgot_password(self):
        self.driver.find_element(*self.forgot_password_link).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_message).text

    def get_validation_error(self):
        return self.driver.find_element(*self.validation_error).text

    def is_empty_field_prompt_visible(self):
        elements = self.driver.find_elements(*self.empty_field_prompt)
        return len(elements) > 0 and elements[0].is_displayed()

    def is_dashboard_header_visible(self):
        elements = self.driver.find_elements(*self.dashboard_header)
        return len(elements) > 0 and elements[0].is_displayed()

    def is_user_profile_icon_visible(self):
        elements = self.driver.find_elements(*self.user_profile_icon)
        return len(elements) > 0 and elements[0].is_displayed()
