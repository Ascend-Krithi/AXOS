# LoginPage.py
"""
PageClass: LoginPage
This class automates the Login page actions for https://example-ecommerce.com/login using Selenium.
Generated based on Locators.json and validated against test cases TC-FT-001 and TC-FT-002.
Quality Assurance:
- All locators mapped from Locators.json.
- Methods are atomic, non-destructive, and appended only (no alteration to existing logic).
- Comprehensive docstrings for downstream automation agents.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver: WebDriver):
        """
        Initializes LoginPage with Selenium WebDriver.
        """
        self.driver = driver
        self.url = 'https://example-ecommerce.com/login'

    def go_to_login_page(self):
        """
        Navigates to the login page.
        """
        self.driver.get(self.url)

    def enter_email(self, email: str):
        """
        Enters email into the email field.
        """
        email_field = self.driver.find_element(By.ID, 'login-email')
        email_field.clear()
        email_field.send_keys(email)

    def enter_password(self, password: str):
        """
        Enters password into the password field.
        """
        password_field = self.driver.find_element(By.ID, 'login-password')
        password_field.clear()
        password_field.send_keys(password)

    def toggle_remember_me(self, check: bool):
        """
        Toggles the 'Remember Me' checkbox.
        """
        checkbox = self.driver.find_element(By.ID, 'remember-me')
        if checkbox.is_selected() != check:
            checkbox.click()

    def click_login_submit(self):
        """
        Clicks the login submit button.
        """
        login_btn = self.driver.find_element(By.ID, 'login-submit')
        login_btn.click()

    def click_forgot_password_link(self):
        """
        Clicks the forgot password link.
        """
        link = self.driver.find_element(By.CSS_SELECTOR, 'a.forgot-password-link')
        link.click()

    def get_error_message(self):
        """
        Returns the error message text.
        """
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.alert-danger'))
            )
            return error.text
        except Exception:
            return None

    def get_validation_error(self):
        """
        Returns the validation error text.
        """
        try:
            validation = self.driver.find_element(By.CSS_SELECTOR, '.invalid-feedback')
            return validation.text
        except Exception:
            return None

    def get_empty_field_prompt(self):
        """
        Returns the empty field prompt text.
        """
        try:
            prompt = self.driver.find_element(By.XPATH, "//*[contains(text(),'Mandatory fields are required')]")
            return prompt.text
        except Exception:
            return None

    def is_dashboard_header_present(self):
        """
        Checks if dashboard header is present after login.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.dashboard-title'))
            )
            return True
        except Exception:
            return False

    def is_user_profile_icon_present(self):
        """
        Checks if user profile icon is present after login.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.user-profile-name'))
            )
            return True
        except Exception:
            return False

# END OF FILE
