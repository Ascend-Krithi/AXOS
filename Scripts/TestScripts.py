# Scripts/TestScripts.py
"""
Test scripts for LoginPage scenarios: TC_LOGIN_007 (Forgot Password flow) and TC_LOGIN_008 (SQL injection handling).
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
    driver.get("https://axos.example.com/login")
    assert driver.current_url.endswith("/login"), "Login page is not displayed."
    login_page.click_forgot_password()
    assert login_page.is_password_recovery_form_displayed(), "Password recovery form should be displayed."

# TC_LOGIN_008: SQL Injection attempt handling
def test_sql_injection_login(driver):
    login_page = LoginPage(driver)
    driver.get("https://axos.example.com/login")
    assert driver.current_url.endswith("/login"), "Login page is not displayed."
    sql_email = "' OR 1=1;--"
    sql_password = "' OR 1=1;--"
    error_msg = login_page.attempt_sql_injection(sql_email, sql_password)
    assert error_msg == "Invalid credentials", "Invalid credentials error should be shown and no security breach should occur."
