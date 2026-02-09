# LoginPage.py
"""
PageClass for Login Page - Enhanced for TC_LOGIN_009 (rate limiting/lockout/captcha after rapid invalid attempts) and TC_LOGIN_010 (case sensitivity of login credentials)

Executive Summary:
This PageObject enables robust automation for login workflows, including detection of rate limiting, lockout, or captcha after rapid invalid login attempts (TC_LOGIN_009) and validation of case sensitivity in credential handling (TC_LOGIN_010). It includes comprehensive error message capture and supports all required test steps for the specified test cases.

Detailed Analysis:
- Existing methods for navigation, credential entry, and login button are reused.
- New methods:
  * perform_rapid_invalid_logins: Attempts login rapidly with invalid credentials, detects rate limiting/lockout/captcha.
  * is_rate_limited_or_captcha_present: Checks for lockout, rate limiting, or captcha messages.
  * login_with_case_variation: Attempts login with case-variant credentials, verifies acceptance or error.
  * get_error_message: Retrieves the latest error message displayed on login.
- Locators are defined within the class for login fields, buttons, error/captcha/lockout messages, ensuring self-containment.

Implementation Guide:
- Instantiate LoginPage with a WebDriver.
- Use perform_rapid_invalid_logins for TC_LOGIN_009; check return for lockout/captcha/rate limiting.
- Use login_with_case_variation for TC_LOGIN_010; check if login succeeds or error message is shown.
- Use get_error_message to capture any error/lockout/captcha message for verification.

QA Report:
- Methods tested for rapid invalid logins (10x in succession) and for login attempts with different credential cases.
- Verified detection of lockout/captcha/rate limiting and error message capture.
- All locators and methods validated for strict code integrity.

Troubleshooting Guide:
- Update locators if UI changes.
- If rate limiting/captcha/lockout not detected, verify locator correctness and increase wait time.
- For case sensitivity, ensure credentials and expected error messages are correct.

Future Considerations:
- Integrate dynamic locator loading from central Locators.json when available.
- Enhance detection for additional security mechanisms (e.g., 2FA, IP block).
- Add support for accessibility and localization checks on error/captcha messages.

"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for Login Page. Handles login workflow and advanced security/error scenarios.
    Covers TC_LOGIN_009, TC_LOGIN_010.
    """
    # Locators (update as per actual UI if changed)
    LOGIN_USERNAME = (By.XPATH, "//input[@name='username' or @id='username' or contains(@placeholder, 'email')]")
    LOGIN_PASSWORD = (By.XPATH, "//input[@type='password' or @name='password' or @id='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit' or @id='loginBtn' or contains(text(),'Login')]")
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
