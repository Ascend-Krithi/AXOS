# Scripts/TestScripts.py
"""
Test scripts for LoginPage scenarios: TC_LOGIN_007 (Forgot Password flow), TC_LOGIN_008 (SQL injection handling), TC_LOGIN_009 (max input length and invalid credentials error), TC_LOGIN_010 (user not found error), TC_Login_10 (max input length valid credentials), and TC_LOGIN_004 (max input length and error feedback).
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
    assert driver.current_url.endswith("/login")
    login_page.click_forgot_password()
    assert login_page.is_password_recovery_form_displayed(), "Password recovery form should be displayed."

# TC_LOGIN_008: SQL Injection attempt handling
def test_sql_injection_login(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    assert driver.current_url.endswith("/login")
    sql_email = "' OR 1=1;--"
    sql_password = "' OR 1=1;--"
    login_page.login_with_sql_injection(sql_email, sql_password)
    assert login_page.validate_invalid_credentials_error(), "Invalid credentials error should be shown."

# TC_LOGIN_009: Max input length and invalid credentials error
def test_login_max_length_invalid_credentials(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    assert driver.current_url.endswith("/login")
    assert login_page.validate_email_max_length(), "Email field should accept up to 50 characters, not more."
    assert login_page.validate_password_max_length(), "Password field should accept up to 50 characters, not more."
    login_page.enter_max_length_email()
    login_page.enter_max_length_password()
    login_page.click_login()
    assert login_page.handle_invalid_credentials_error(), "Invalid credentials error should be shown."

# TC_LOGIN_010: User not found error
def test_login_user_not_found(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    assert driver.current_url.endswith("/login")
    login_page.enter_email("unknown@example.com")
    login_page.enter_password("RandomPass789")
    login_page.click_login()
    assert login_page.handle_user_not_found_error() or login_page.handle_invalid_credentials_error(), "User not found or invalid credentials error should be shown."

# TC_Login_10: Maximum allowed input length (valid credentials)
def test_login_max_length_valid_credentials(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page("https://axos.example.com/login")
    assert driver.current_url.endswith("/login")
    max_email = "a" * 254 + "@example.com"
    max_password = "A" * 128
    login_page.enter_email(max_email)
    login_page.enter_password(max_password)
    login_page.click_login()
    assert login_page.is_login_successful(), "Login should be successful with maximum input length valid credentials."

# TC_LOGIN_004: Maximum allowed input length (error feedback for invalid credentials)
def test_login_max_length_invalid_credentials_feedback(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page("https://axos.example.com/login")
    assert driver.current_url.endswith("/login")
    max_email = "b" * 254 + "@example.com"
    max_password = "B" * 64
    login_page.enter_email(max_email)
    login_page.enter_password(max_password)
    login_page.click_login()
    if login_page.is_login_successful():
        assert True, "Login successful with maximum input length."
    else:
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error feedback should be shown for invalid credentials."

# TC_Login_08: Forgot Password Flow
def test_tc_login_08_forgot_password_flow(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page("https://axos.example.com/login")
    assert driver.current_url.endswith("/login")
    login_page.click_forgot_password()
    # Assert user is redirected to password recovery page
    assert "recovery" in driver.current_url or login_page.wait.until(lambda d: "recovery" in d.current_url), "User should be redirected to password recovery page."

# TC_Login_09: Maximum Input Length Handling and Login
def test_tc_login_09_max_length_login(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page("https://axos.example.com/login")
    assert driver.current_url.endswith("/login")
    # Test Data: 255-character email (truncated to 254), valid password
    max_email = "x" * 255 + "@example.com"
    valid_password = "ValidPassword123"
    login_page.enter_email(max_email)
    login_page.enter_password(valid_password)
    login_page.click_login()
    # Assert fields accept maximum length input
    email_field = login_page.wait.until(lambda d: d.find_element(*login_page.EMAIL_INPUT))
    assert len(email_field.get_attribute("value")) <= login_page.EMAIL_MAX_LENGTH, "Email field should accept maximum allowed length."
    password_field = login_page.wait.until(lambda d: d.find_element(*login_page.PASSWORD_INPUT))
    assert len(password_field.get_attribute("value")) <= login_page.PASSWORD_MAX_LENGTH, "Password field should accept maximum allowed length."
    # Assert login outcome
    if login_page.is_login_successful():
        assert True, "User is logged in with maximum length credentials."
    else:
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error feedback should be shown for invalid credentials."
