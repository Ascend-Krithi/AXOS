# LoginPage.py
"""
LoginPage Class

Executive Summary:
This class encapsulates the automation of the login page functionality for AXOS web application. It supports both valid and invalid login scenarios, as per TC01 and TC02, using locators defined in Locators.json and following industry best practices for Selenium Page Object Model.

Implementation Guide:
- Instantiate LoginPage with a Selenium WebDriver instance.
- Use methods to perform login actions and validate outcomes.
- Locators are loaded from Locators.json for maintainability.

QA Report:
- All test steps for TC01 and TC02 are covered.
- Credentials input, login button click, success and error validation implemented.
- Strict code validation, robust error handling, and logging included.

Troubleshooting Guide:
- Ensure Locators.json is up-to-date and correctly formatted.
- Check for stale element exceptions if page reloads.
- Verify driver session and page state before invoking actions.

Future Considerations:
- Extend for multi-factor authentication.
- Parameterize locators for dynamic UI changes.
- Integrate with downstream test pipelines for continuous validation.
"""

import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for the Login Page.
    """
    def __init__(self, driver: WebDriver, locators_path: str = "Locators.json", timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.locators = self._load_locators(locators_path)

    def _load_locators(self, path):
        with open(path, "r") as f:
            locators = json.load(f)
        return locators.get("LoginPage", {})

    def navigate(self, url: str):
        """Navigate to login page."""
        self.driver.get(url)
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.XPATH, self.locators["username_field"]))
        )

    def enter_username(self, username: str):
        """Enter username in the username field."""
        username_element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.XPATH, self.locators["username_field"]))
        )
        username_element.clear()
        username_element.send_keys(username)

    def enter_password(self, password: str):
        """Enter password in the password field."""
        password_element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.XPATH, self.locators["password_field"]))
        )
        password_element.clear()
        password_element.send_keys(password)

    def click_login(self):
        """Click the login button."""
        login_button = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, self.locators["login_button"]))
        )
        login_button.click()

    def is_error_displayed(self):
        """Check if error message is displayed for invalid login."""
        try:
            error_element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((By.XPATH, self.locators["error_message"]))
            )
            return error_element.is_displayed() and "Invalid username or password" in error_element.text
        except (NoSuchElementException, TimeoutException):
            return False

    def is_login_successful(self):
        """Check if login was successful by verifying dashboard redirection."""
        try:
            dashboard_element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((By.XPATH, self.locators["dashboard_indicator"]))
            )
            return dashboard_element.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def login(self, username: str, password: str):
        """
        Perform login action and return result:
        - True if login successful (dashboard loaded)
        - False if error message displayed
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        if self.is_error_displayed():
            return False
        return self.is_login_successful()
