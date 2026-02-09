import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for Login Page. Handles login workflow, including 'Remember Me' and session handling.
    """
    def __init__(self, driver: WebDriver, locators: dict):
        self.driver = driver
        self.locators = locators
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_login(self, url: str):
        """Navigate to the login page URL."""
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["login_username"])))

    def enter_username(self, username: str):
        """Enter the username/email into the username field."""
        elem = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["login_username"])))
        elem.clear()
        elem.send_keys(username)

    def enter_password(self, password: str):
        """Enter the password into the password field."""
        elem = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["login_password"])))
        elem.clear()
        elem.send_keys(password)

    def set_remember_me(self, selected: bool):
        """Set the 'Remember Me' checkbox to the desired state."""
        checkbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators["login_remember_me"])))
        is_selected = checkbox.is_selected()
        if selected != is_selected:
            checkbox.click()

    def click_login(self):
        """Click the login button."""
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.locators["login_button"])))
        btn.click()

    def is_logged_in(self) -> bool:
        """Check if user is logged in by verifying dashboard/homepage element."""
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["dashboard_home"])))
            return True
        except Exception:
            return False

    def simulate_browser_restart(self, url: str):
        """
        Simulate closing and reopening the browser by deleting all cookies and navigating back to the site.
        """
        self.driver.delete_all_cookies()
        self.driver.get(url)
        time.sleep(2)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["login_username"])))

    def is_logged_out(self) -> bool:
        """Check if user is logged out by verifying login page element is visible."""
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["login_username"])))
            return True
        except Exception:
            return False
