import pytest
from Pages.LoginPage import LoginPage

# Existing tests for TC_LOGIN_007 and TC_LOGIN_008 assumed here

def test_TC_LOGIN_007(driver):
    # ... existing logic ...
    pass

def test_TC_LOGIN_008(driver):
    # ... existing logic ...
    pass


def test_TC_LOGIN_009_max_length_fields_and_ui_integrity(driver):
    """
    TC_LOGIN_009: Verify login fields accept max length (50 chars), UI integrity is preserved, and error is shown for invalid credentials.
    """
    driver.get('https://axos.example.com/login')
    login_page = LoginPage(driver)

    # Step 1: Check max length fields and UI integrity
    ui_intact = login_page.test_max_length_fields()
    assert ui_intact, "UI integrity failed or field overflow after entering max length credentials."

    # Step 2: Attempt login with max length invalid credentials
    error_msg = login_page.login_with_max_length_invalid()
    assert error_msg in ["Invalid credentials", "User not found"], f"Unexpected error message: {error_msg}"

    # Step 3: Ensure no UI break or field overflow after error
    ui_intact_after = login_page.test_max_length_fields()
    assert ui_intact_after, "UI integrity failed or field overflow after failed login."


def test_TC_LOGIN_010_login_with_unregistered_user(driver):
    """
    TC_LOGIN_010: Attempt login with unregistered user, verify error message and that user remains on login page.
    """
    driver.get('https://axos.example.com/login')
    login_page = LoginPage(driver)

    # Step 1: Attempt login with unregistered user
    error_msg = login_page.login_with_unregistered_user('unknown@example.com', 'RandomPass789')
    assert error_msg in ["User not found", "Invalid credentials"], f"Unexpected error message: {error_msg}"

    # Step 2: Validate user remains on login page
    assert login_page.validate_remain_on_login_page(), "User did not remain on login page after failed login."
