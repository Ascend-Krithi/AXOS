# DashboardPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    """
    Page Object for Dashboard functionality.

    Methods:
        is_dashboard_displayed(): Return True if dashboard main element is visible.

    Usage:
        - Used for session validation post-login.
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.dashboard_locator = (By.ID, "dashboard_main")

    def is_dashboard_displayed(self):
        try:
            dashboard_element = self.wait.until(EC.visibility_of_element_located(self.dashboard_locator))
            return dashboard_element.is_displayed()
        except:
            return False
