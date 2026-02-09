# DashboardPage.py
"""
PageClass for Dashboard Page
Covers: TC_LOGIN_001, TC_LOGIN_07 (post-login validation, session expiration), TC_LOGIN_006 (session persistence after browser reopen)
Ensures dashboard access and session management.
Strict adherence to Selenium Python best practices, atomic methods, robust locator handling, and comprehensive docstrings.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    """
    Page Object Model for the Dashboard/Home Page.
    Covers:
    - Post-login redirection
    - Session expiration handling
    - Session persistence after browser reopen
    """

    DASHBOARD_HEADER = (By.ID, "dashboardHeader")  # Assumed locator

    def __init__(self, driver: WebDriver):
        """
        Initializes the DashboardPage with a WebDriver instance.
        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_dashboard_displayed(self) -> bool:
        """
        Validates that the dashboard/home page is displayed.
        :return: True if dashboard header is visible, else False
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except Exception:
            return False

    def is_session_active(self) -> bool:
        """
        Checks if session is still active (dashboard visible).
        :return: True if dashboard is displayed, False otherwise
        """
        return self.is_dashboard_displayed()

    # --- TC_LOGIN_006: Session persistence validation after browser reopen ---
    def validate_session_after_browser_reopen(self, url: str) -> bool:
        """
        Validates that session persists and dashboard is displayed after browser is reopened and site revisited.
        :param url: URL to revisit after browser reopen
        :return: True if dashboard is displayed, False otherwise
        """
        self.driver.get(url)
        return self.is_dashboard_displayed()
