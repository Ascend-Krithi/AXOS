# DashboardPage.py
"""
DashboardPage Class

Executive Summary:
This class represents the dashboard/home page post-login for AXOS application. It provides methods for validating dashboard presence and accessing dashboard-specific elements, supporting verification for TC01.

Implementation Guide:
- Instantiate DashboardPage with a Selenium WebDriver instance.
- Use methods to validate dashboard load and interact with dashboard elements.
- Locators are loaded from Locators.json for maintainability.

QA Report:
- Dashboard presence validation implemented.
- Strict code validation and robust error handling included.

Troubleshooting Guide:
- Ensure dashboard_indicator locator is correctly mapped in Locators.json.
- Verify driver session and page state before invoking actions.

Future Considerations:
- Extend for dashboard widgets and dynamic content validation.
- Integrate analytics for dashboard load performance.
"""

import json
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    """
    Page Object Model for the Dashboard/Home Page.
    """
    def __init__(self, driver: WebDriver, locators_path: str = "Locators.json", timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.locators = self._load_locators(locators_path)

    def _load_locators(self, path):
        with open(path, "r") as f:
            locators = json.load(f)
        return locators.get("DashboardPage", {})

    def is_dashboard_loaded(self):
        """Check if dashboard is loaded (indicator element visible)."""
        try:
            dashboard_element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((By.XPATH, self.locators["dashboard_indicator"]))
            )
            return dashboard_element.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def get_dashboard_title(self):
        """Get dashboard page title."""
        try:
            title_element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((By.XPATH, self.locators["dashboard_title"]))
            )
            return title_element.text
        except (NoSuchElementException, TimeoutException):
            return None
