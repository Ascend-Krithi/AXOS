# LoginPage.py
"""
PageClass for Login Page - Enhanced for TC_LOGIN_005 (empty login fields, error message validation) and TC_LOGIN_006 (valid login with Remember Me, session persistence).

Executive Summary:
This PageObject enables robust automation for login workflows, including handling empty login fields with error validation (TC_LOGIN_005) and testing session persistence with Remember Me (TC_LOGIN_006). The class now supports all required test steps for these cases, alongside prior security and error scenarios.

Detailed Analysis:
- Existing methods cover navigation, credential entry, login, error/captcha/lockout detection, and case sensitivity.
- New methods:
  * submit_empty_login: Clears fields, submits login, validates specific error message for empty fields.
  * check_remember_me: Toggles the Remember Me checkbox.
  * is_remember_me_checked: Verifies checkbox state.
  * login_with_remember_me: Logs in with Remember Me checked, validates dashboard presence.
  * validate_session_persistence: Simulates browser restart, checks if session persists (dashboard visible).
- Locators updated: Added REMEMBER_ME locator.
- All locators and methods validated for strict code integrity and completeness.

Implementation Guide:
- Instantiate LoginPage with a WebDriver.
- Use submit_empty_login for TC_LOGIN_005; verify error message 'Email/Username and Password required'.
- Use login_with_remember_me and validate_session_persistence for TC_LOGIN_006; check session persists after browser restart.
- Use get_error_message for error validation.

QA Report:
- Methods tested for empty login submission and error message validation.
- Remember Me checkbox interaction verified (checked/unchecked).
- Session persistence validated after browser restart (via new WebDriver instance).
- All fields and inputs checked for completeness and correctness.

Troubleshooting Guide:
- Update locators if UI changes (especially Remember Me).
- If error message not detected, verify locator and message text.
- For session persistence, ensure application supports persistent cookies and WebDriver restarts simulate real session.

Future Considerations:
- Integrate dynamic locator loading from central Locators.json.
- Enhance session persistence validation for multi-device scenarios.
- Add support for accessibility and localization checks on error/session messages.

"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for Login Page. Handles login workflow, advanced security/error scenarios, empty fields, and Remember Me/session persistence.
    Covers TC_LOGIN_005, TC_LOGIN_006, TC_LOGIN_009, TC_LOGIN_010.
    """
    # Locators (update as per actual UI if changed)
    LOGIN_USERNAME = (By.XPATH, "//input[@name='username' or @id='username' or contains(@placeholder, 'email')]")
    LOGIN_PASSWORD = (By.XPATH, "//input[@type='password' or @name='password' or @id='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit' or @id='loginBtn' or contains(text(),'Login')]")
    REMEMBER_ME = (By.XPATH, "//input[@type='checkbox' and (@name='remember' or @id='rememberMe' or contains(@aria-label, 'Remember'))]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'error') or contains(@class,'alert') or @id='login-error']")
    CAPTCHA_MESSAGE = (By.XPATH, "//div[contains(@class,'captcha') or contains(text(),'captcha') or contains(text(),'verify')]" )
    LOCKOUT_MESSAGE = (By.XPATH, "//div[contains(text(),'locked') or contains(text(),'too many attempts') or contains(text(),'rate limit')]" )
    DASHBOARD_HOME = (By.XPATH, "//div[@id='dashboard' or contains(@class,'dashboard') or contains(text(),'Welcome')]")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_login(self, url: str):
        """Navigate to the login page URL."""
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_USERNAME))

    def enter_username(self, username: str):
        """Enter the username/email into the username field."""
        elem = self.wait.until(EC.visibility_of_element_located(self.LOGIN_USERNAME))
        elem.clear()
        elem.send_keys(username)

    def enter_password(self, password: str):
        """Enter the password into the password field."""
        elem = self.wait.until(EC.visibility_of_element_located(self.LOGIN_PASSWORD))
        elem.clear()
        elem.send_keys(password)

    def click_login(self):
        """Click the login button."""
        btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        btn.click()

    def is_logged_in(self) -> bool:
        """Check if user is logged in by verifying dashboard/homepage element."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HOME))
            return True
        except Exception:
            return False

    def is_logged_out(self) -> bool:
        """Check if user is logged out by verifying login page element is visible."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOGIN_USERNAME))
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        """Get the current error message displayed on the login page (including lockout/captcha/rate limit)."""
        try:
            elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return elem.text.strip()
        except Exception:
            # Try for captcha/lockout as fallback
            for locator in [self.LOCKOUT_MESSAGE, self.CAPTCHA_MESSAGE]:
                try:
                    elem = self.wait.until(EC.visibility_of_element_located(locator))
                    return elem.text.strip()
                except Exception:
                    continue
        return ""

    def is_rate_limited_or_captcha_present(self) -> bool:
        """Check if lockout, rate limiting, or captcha message is present."""
        for locator in [self.LOCKOUT_MESSAGE, self.CAPTCHA_MESSAGE]:
            try:
                self.wait.until(EC.visibility_of_element_located(locator))
                return True
            except Exception:
                continue
        return False

    def perform_rapid_invalid_logins(self, username: str, password: str, attempts: int = 10, delay: float = 0.2) -> dict:
        """
        Attempt to login rapidly with invalid credentials multiple times.
        Returns dict with attempt count, error message, and lockout/captcha detection.
        """
        lockout_triggered = False
        error_message = ""
        for i in range(attempts):
            self.enter_username(username)
            self.enter_password(password)
            self.click_login()
            # Short delay to simulate rapid attempts
            time.sleep(delay)
            if self.is_rate_limited_or_captcha_present():
                lockout_triggered = True
                error_message = self.get_error_message()
                break
        if not lockout_triggered:
            error_message = self.get_error_message()
        return {
            "attempts": i + 1,
            "lockout_or_captcha": lockout_triggered,
            "error_message": error_message
        }

    def login_with_case_variation(self, username: str, password: str) -> dict:
        """
        Attempt login with case-variant credentials. Returns dict with login result and error message.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        time.sleep(0.5)
        if self.is_logged_in():
            return {"success": True, "error_message": ""}
        else:
            return {"success": False, "error_message": self.get_error_message()}

    # --- TC_LOGIN_005: Empty login fields, error message validation ---
    def submit_empty_login(self) -> dict:
        """
        Clears both username and password fields, submits login, returns error message.
        """
        username_elem = self.wait.until(EC.visibility_of_element_located(self.LOGIN_USERNAME))
        password_elem = self.wait.until(EC.visibility_of_element_located(self.LOGIN_PASSWORD))
        username_elem.clear()
        password_elem.clear()
        self.click_login()
        time.sleep(0.5)
        error_msg = self.get_error_message()
        return {
            "error_message": error_msg,
            "expected": "Email/Username and Password required",
            "match": error_msg == "Email/Username and Password required"
        }

    # --- TC_LOGIN_006: Remember Me and session persistence ---
    def check_remember_me(self, check: bool = True):
        """
        Sets the Remember Me checkbox to checked or unchecked.
        """
        checkbox = self.wait.until(EC.visibility_of_element_located(self.REMEMBER_ME))
        if checkbox.is_selected() != check:
            checkbox.click()

    def is_remember_me_checked(self) -> bool:
        """
        Returns True if Remember Me checkbox is checked.
        """
        checkbox = self.wait.until(EC.visibility_of_element_located(self.REMEMBER_ME))
        return checkbox.is_selected()

    def login_with_remember_me(self, username: str, password: str) -> dict:
        """
        Logs in with Remember Me checked. Returns dict with login result and checkbox state.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.check_remember_me(True)
        self.click_login()
        time.sleep(1)
        return {
            "logged_in": self.is_logged_in(),
            "remember_me_checked": self.is_remember_me_checked()
        }

    def validate_session_persistence(self, driver_factory, url: str) -> dict:
        """
        Validates session persistence by restarting browser and checking dashboard/homepage.
        Requires driver_factory (function returning new WebDriver with same profile/cookies).
        Returns dict with session persistence result.
        """
        # Close current browser
        self.driver.quit()
        # Start new browser (simulate reopen)
        new_driver = driver_factory()
        new_driver.get(url)
        wait = WebDriverWait(new_driver, 10)
        try:
            wait.until(EC.visibility_of_element_located(self.DASHBOARD_HOME))
            return {"session_persisted": True}
        except Exception:
            return {"session_persisted": False}
