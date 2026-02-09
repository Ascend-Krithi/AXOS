# LoginPage.py
"""
PageClass for LoginPage generated based on Locators.json.
Implements login interactions, error handling, and post-login validation.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.url = 'https://example-ecommerce.com/login'
        self.emailField = (By.ID, 'login-email')
        self.passwordField = (By.ID, 'login-password')
        self.rememberMeCheckbox = (By.ID, 'remember-me')
        self.loginSubmit = (By.ID, 'login-submit')
        self.forgotPasswordLink = (By.CSS_SELECTOR, 'a.forgot-password-link')
        self.errorMessage = (By.CSS_SELECTOR, 'div.alert-danger')
        self.validationError = (By.CSS_SELECTOR, '.invalid-feedback')
        self.emptyFieldPrompt = (By.XPATH, "//*[text()='Mandatory fields are required']")
        self.dashboardHeader = (By.CSS_SELECTOR, 'h1.dashboard-title')
        self.userProfileIcon = (By.CSS_SELECTOR, '.user-profile-name')

    def load(self):
        self.driver.get(self.url)

    def login(self, email: str, password: str, remember_me: bool = False):
        self.driver.find_element(*self.emailField).clear()
        self.driver.find_element(*self.emailField).send_keys(email)
        self.driver.find_element(*self.passwordField).clear()
        self.driver.find_element(*self.passwordField).send_keys(password)
        if remember_me:
            checkbox = self.driver.find_element(*self.rememberMeCheckbox)
            if not checkbox.is_selected():
                checkbox.click()
        self.driver.find_element(*self.loginSubmit).click()

    def click_forgot_password(self):
        self.driver.find_element(*self.forgotPasswordLink).click()

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.errorMessage).text
        except Exception:
            return None

    def get_validation_error(self):
        try:
            return self.driver.find_element(*self.validationError).text
        except Exception:
            return None

    def is_empty_field_prompt_present(self):
        elements = self.driver.find_elements(*self.emptyFieldPrompt)
        return len(elements) > 0

    def is_dashboard_header_present(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.dashboardHeader)
            )
            return True
        except Exception:
            return False

    def is_user_profile_icon_present(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.userProfileIcon)
            )
            return True
        except Exception:
            return False