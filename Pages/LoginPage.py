# LoginPage.py
"""
Page Object Model for Login Page of example-ecommerce.com
Includes all locators and actions as per Locators.json.
QA Report:
- All locators mapped from Locators.json.
- Methods for each input, button, and message.
- Strict Selenium best practices (explicit waits, error handling).
- Comprehensive docstrings and code comments.
- Ready for downstream automation.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    """
    Page Object for the Login Page.
    URL: https://example-ecommerce.com/login
    """

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

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

    # Actions
    def open(self):
        """Navigate to the login page."""
        self.driver.get("https://example-ecommerce.com/login")

    def enter_email(self, email):
        """Enter email address."""
        elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD)
        )
        elem.clear()
        elem.send_keys(email)

    def enter_password(self, password):
        """Enter password."""
        elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD)
        )
        elem.clear()
        elem.send_keys(password)

    def click_remember_me(self):
        """Click the 'Remember Me' checkbox."""
        elem = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX)
        )
        elem.click()

    def click_login(self):
        """Click the login submit button."""
        elem = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT)
        )
        elem.click()

    def click_forgot_password(self):
        """Click the 'Forgot Password' link."""
        elem = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK)
        )
        elem.click()

    # Verification Methods
    def get_error_message(self):
        """Retrieve the error message after login attempt."""
        try:
            elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return elem.text
        except TimeoutException:
            return None

    def get_validation_error(self):
        """Retrieve validation error message."""
        try:
            elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.VALIDATION_ERROR)
            )
            return elem.text
        except TimeoutException:
            return None

    def is_empty_field_prompt_present(self):
        """Check if the empty field prompt is present."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT)
            )
            return True
        except TimeoutException:
            return False

    def is_dashboard_header_present(self):
        """Verify dashboard header presence after login."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.DASHBOARD_HEADER)
            )
            return True
        except TimeoutException:
            return False

    def is_user_profile_icon_present(self):
        """Verify user profile icon presence after login."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.USER_PROFILE_ICON)
            )
            return True
        except TimeoutException:
            return False
