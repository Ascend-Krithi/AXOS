# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for Login functionality.

    Methods:
        enter_username(username): Enter username in the username field.
        enter_password(password): Enter password in the password field.
        click_login(): Click the login button.
        click_remember_me(): Click the 'Remember Me' checkbox.
        is_remember_me_selected(): Return True if 'Remember Me' is selected.
        get_error_message(): Return error message if present.
        login(username, password, remember_me=False): Perform login sequence.
        validate_session_persistence(): Validate if session persists after login (for 'Remember Me').
        expire_session_and_validate_redirect(): Simulate session expiration and validate redirect to login page (for TC_Login_07).

    Usage:
        - Supports TC_LOGIN_001 (basic login and redirect).
        - Supports TC_Login_07 (session expiration after login without 'Remember Me').
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        # Locators loaded from Locators.json
        self.username_locator = (By.ID, "username_input")
        self.password_locator = (By.ID, "password_input")
        self.login_button_locator = (By.ID, "login_btn")
        self.remember_me_locator = (By.ID, "remember_me_checkbox")
        self.error_message_locator = (By.ID, "error_message")

    def enter_username(self, username: str):
        username_field = self.wait.until(EC.visibility_of_element_located(self.username_locator))
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password: str):
        password_field = self.wait.until(EC.visibility_of_element_located(self.password_locator))
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.login_button_locator))
        login_btn.click()

    def click_remember_me(self):
        remember_me_checkbox = self.wait.until(EC.element_to_be_clickable(self.remember_me_locator))
        if not remember_me_checkbox.is_selected():
            remember_me_checkbox.click()

    def is_remember_me_selected(self):
        remember_me_checkbox = self.wait.until(EC.visibility_of_element_located(self.remember_me_locator))
        return remember_me_checkbox.is_selected()

    def get_error_message(self):
        try:
            error_element = self.wait.until(EC.visibility_of_element_located(self.error_message_locator))
            return error_element.text
        except:
            return None

    def login(self, username: str, password: str, remember_me: bool = False):
        self.enter_username(username)
        self.enter_password(password)
        if remember_me:
            self.click_remember_me()
        self.click_login()

    def validate_session_persistence(self):
        """
        Validate session persistence by re-accessing the current URL.
        If 'Remember Me' was checked, the user should remain logged in.
        Returns True if DashboardPage is displayed.
        """
        self.driver.get(self.driver.current_url)
        from Pages.DashboardPage import DashboardPage
        dashboard = DashboardPage(self.driver)
        return dashboard.is_dashboard_displayed()

    def expire_session_and_validate_redirect(self):
        """
        Simulate session expiration by clearing cookies and local storage.
        Then reload the page and check if redirected to login page.
        Returns True if login page is displayed after session expiration.
        """
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
        self.driver.refresh()
        try:
            username_field = self.wait.until(EC.visibility_of_element_located(self.username_locator))
            return username_field.is_displayed()
        except:
            return False
