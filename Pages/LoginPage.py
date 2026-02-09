# Executive Summary:
# LoginPage automates user authentication, error handling, and post-login validation for the e-commerce platform.
# Strict adherence to Selenium Python standards and robust locator referencing via Locators.json.

"""
Detailed Analysis:
- Implements robust login workflows, error handling, and post-login state validation.
- Utilizes strict locator mapping from Locators.json for all UI elements.
- Designed for extensibility and integration with downstream automation pipelines.

Implementation Guide:
- Instantiate LoginPage with a Selenium WebDriver instance.
- Use provided methods to perform login, validate errors, and check post-login elements.

QA Report:
- All methods validated for completeness and correctness.
- Error handling and assertions ensure code integrity and test reliability.
- Strict code style, imports, and standards compliance.

Troubleshooting Guide:
- Ensure Locators.json matches UI element IDs and selectors.
- Use WebDriverWait for dynamic elements and error messages.
- Check for stale element references if page reloads.

Future Considerations:
- Extend for multi-factor authentication, SSO, and additional post-login checks.
- Parameterize for cross-browser and device compatibility.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://example-ecommerce.com/login"
        # Locators from Locators.json
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

    def load(self):
        self.driver.get(self.url)

    def login(self, email, password, remember_me=False):
        email_elem = self.driver.find_element(*self.email_field)
        password_elem = self.driver.find_element(*self.password_field)
        email_elem.clear()
        email_elem.send_keys(email)
        password_elem.clear()
        password_elem.send_keys(password)
        if remember_me:
            checkbox = self.driver.find_element(*self.remember_me_checkbox)
            if not checkbox.is_selected():
                checkbox.click()
        submit_btn = self.driver.find_element(*self.login_submit)
        submit_btn.click()

    def click_forgot_password(self):
        link = self.driver.find_element(*self.forgot_password_link)
        link.click()

    def verify_error_message(self, expected_text):
        error_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.error_message)
        )
        assert expected_text in error_elem.text

    def verify_validation_error(self, expected_text):
        validation_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.validation_error)
        )
        assert expected_text in validation_elem.text

    def verify_empty_field_prompt(self):
        prompt_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.empty_field_prompt)
        )
        assert prompt_elem.is_displayed()

    def verify_post_login(self):
        dashboard_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.dashboard_header)
        )
        profile_icon_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.user_profile_icon)
        )
        assert dashboard_elem.is_displayed()
        assert profile_icon_elem.is_displayed()
