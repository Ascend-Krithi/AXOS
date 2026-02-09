# TestScripts.py
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
import pytest

@pytest.fixture(scope='function')
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Test Case TC_Login_07: Login without 'Remember Me', session expiration

def test_TC_Login_07(driver):
    login_page = LoginPage(driver)
    driver.get('https://example.com/login')
    # Step 1: Navigate to login page
    assert login_page.enter_username is not None
    # Step 2: Enter valid credentials without selecting 'Remember Me'
    login_page.enter_username('user@example.com')
    login_page.enter_password('ValidPassword123')
    assert not login_page.is_remember_me_selected()
    # Step 3: Click Login
    login_page.click_login()
    dashboard = DashboardPage(driver)
    assert dashboard.is_dashboard_displayed()
    # Step 4: Simulate session expiration and validate redirect
    assert login_page.expire_session_and_validate_redirect()

# Test Case TC_LOGIN_001: Basic login and redirect

def test_TC_LOGIN_001(driver):
    login_page = LoginPage(driver)
    driver.get('https://example.com/login')
    # Step 1: Navigate to login page
    assert login_page.enter_username is not None
    # Step 2: Enter valid email/username and valid password
    login_page.enter_username('user@example.com')
    login_page.enter_password('ValidPassword123')
    # Step 3: Click Login
    login_page.click_login()
    dashboard = DashboardPage(driver)
    assert dashboard.is_dashboard_displayed()

# Test Case TC_LOGIN_002: Invalid credentials

def test_TC_LOGIN_002(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login('https://example.com/login')
    # Step 1: Navigate to the login page
    assert driver.current_url.endswith('/login')
    # Step 2: Enter invalid email/username or password
    login_page.enter_credentials('wronguser@example.com', 'WrongPassword')
    # Step 3: Click the Login button
    login_page.click_login()
    # Step 4: Assert error message for invalid credentials is displayed
    error_msg = login_page.get_error_message()
    assert error_msg != "", "Error message for invalid credentials should be displayed"
    assert driver.current_url.endswith('/login'), "User should remain on login page"

# Test Case TC_LOGIN_003: Empty fields

def test_TC_LOGIN_003(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login('https://example.com/login')
    # Step 1: Navigate to the login page
    assert driver.current_url.endswith('/login')
    # Step 2: Leave email/username and password fields empty
    login_page.enter_credentials('', '')
    # Step 3: Click the Login button
    login_page.click_login()
    # Step 4: Assert validation message for empty fields is displayed
    validation_msg = login_page.get_validation_message()
    assert validation_msg != "", "Validation message for empty fields should be displayed"
    assert driver.current_url.endswith('/login'), "User should remain on login page"
