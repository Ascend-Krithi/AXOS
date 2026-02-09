# LoginPage.py
"""
Selenium Page Object for LoginPage
URL: https://example-ecommerce.com/login
Generated based on Locators.json and coding standards.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object representing the Login Page.
    """
    URL = "https://example-ecommerce.com/login"

    # Locators
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
        self.wait = WebDriverWait(driver, 10)

    def go_to(self):
        """Navigates to the Login Page URL."""
        self.driver.get(self.URL)

    def enter_email(self, email: str):
        """Enters the email address."""
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_field.clear()
        email_field.send_keys(email)

    def enter_password(self, password: str):
        """Enters the password."""
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(password)

    def set_remember_me(self, remember: bool):
        """Sets the 'Remember Me' checkbox."""
        checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
        if checkbox.is_selected() != remember:
            checkbox.click()

    def submit_login(self):
        """Clicks the login submit button."""
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        submit_btn.click()

    def click_forgot_password(self):
        """Clicks the 'Forgot Password' link."""
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        link.click()

    def get_error_message(self) -> str:
        """Returns the error message text if present."""
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.text
        except Exception:
            return ""

    def get_validation_error(self) -> str:
        """Returns validation error text if present."""
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return error.text
        except Exception:
            return ""

    def is_empty_field_prompt_displayed(self) -> bool:
        """Checks if the empty field prompt is displayed."""
        try:
            prompt = self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return prompt.is_displayed()
        except Exception:
            return False

    def is_logged_in(self) -> bool:
        """Checks if the user is logged in by verifying dashboard header and user profile icon."""
        try:
            dashboard = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            user_icon = self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return dashboard.is_displayed() and user_icon.is_displayed()
        except Exception:
            return False

"""
Documentation:
- This PageClass is strictly generated from Locators.json for the LoginPage.
- All locator strategies are mapped to Selenium best practices (By.ID, By.CSS_SELECTOR, By.XPATH).
- Methods provide clear actions and validations for login workflow, error handling, and post-login status.
- Designed for integration with downstream automation pipelines and version control.
- No existing PageClasses were updated; this is a new addition.
- All imports are explicit and strictly required for Selenium operations.
- Class is structured for maintainability and extensibility.
"""
