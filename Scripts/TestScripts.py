# Scripts/TestScripts.py
"""
Test scripts for LoginPage scenarios: TC_LOGIN_007 (Forgot Password flow), TC_LOGIN_008 (SQL injection handling), TC_LOGIN_009 (max input length), TC_LOGIN_010 (unregistered user).
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

# TC_LOGIN_009: Maximum input length validation
def test_max_input_length_login(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    assert driver.current_url.endswith("/login")
    assert login_page.validate_max_input_length(50), "Input fields should accept up to 50 characters and handle errors properly."

# TC_LOGIN_010: Unregistered user login error handling
def test_unregistered_user_login_error(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    assert driver.current_url.endswith("/login")
    assert login_page.validate_unregistered_user_error("unknown@example.com", "RandomPass789"), "Error message for unregistered user should be correct."
