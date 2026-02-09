# Scripts/TestScripts.py
"""
Test scripts for LoginPage scenarios: TC_LOGIN_007 (Forgot Password flow), TC_LOGIN_008 (SQL injection handling), TC_LOGIN_009 (max input length and invalid credentials error), and TC_LOGIN_010 (user not found error).
"""
import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# TC_LOGIN_007: Forgot Password flow
def test_forgot_password_flow(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    # Step 1: Login page is displayed
    assert driver.current_url.endswith("/login")
    # Step 2: Click 'Forgot Password' link
    login_page.click_forgot_password()
    # Step 3: Verify presence of password recovery form
    assert login_page.is_password_recovery_form_displayed(), "Password recovery form should be displayed."

# TC_LOGIN_008: SQL Injection attempt handling
def test_sql_injection_login(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    # Step 1: Login page is displayed
    assert driver.current_url.endswith("/login")
    # Step 2: Enter SQL injection strings
    sql_email = "' OR 1=1;--"
    sql_password = "' OR 1=1;--"
    login_page.login_with_sql_injection(sql_email, sql_password)
    # Step 3: Click 'Login' button (done in login_with_sql_injection)
    # Step 4: Verify error message and no security breach
    assert login_page.validate_invalid_credentials_error(), "Invalid credentials error should be shown."

# TC_LOGIN_009: Max input length and invalid credentials error
def test_login_max_length_invalid_credentials(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    # Step 1: Login page is displayed
    assert driver.current_url.endswith("/login")
    # Step 2: Enter maximum allowed characters in email and password fields
    assert login_page.validate_email_max_length(), "Email field should accept up to 50 characters, not more."
    assert login_page.validate_password_max_length(), "Password field should accept up to 50 characters, not more."
    login_page.enter_max_length_email()
    login_page.enter_max_length_password()
    # Step 3: Click Login
    login_page.click_login()
    # Step 4: Verify error message 'Invalid credentials' is shown
    assert login_page.handle_invalid_credentials_error(), "Invalid credentials error should be shown."

# TC_LOGIN_010: User not found error
def test_login_user_not_found(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    # Step 1: Login page is displayed
    assert driver.current_url.endswith("/login")
    # Step 2: Enter email/username and password for a user not registered
    login_page.enter_email("unknown@example.com")
    login_page.enter_password("RandomPass789")
    # Step 3: Click Login
    login_page.click_login()
    # Step 4: Verify error message 'User not found' or 'Invalid credentials' is shown
    assert login_page.handle_user_not_found_error() or login_page.handle_invalid_credentials_error(), "User not found or invalid credentials error should be shown."
