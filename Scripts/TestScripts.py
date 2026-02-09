# Existing imports and code
import pytest
from Pages.LoginPage import LoginPage

# ... (existing test methods remain unchanged)

# --- New test methods appended below ---

def test_TC_Login_10_max_length_valid_login(driver):
    """
    TC_Login_10: Valid login with max-length email and password.
    Steps:
      - Enter maximum allowed email and password.
      - Validate max-length input.
      - Attempt login.
      - Expect successful login.
    """
    login_page = LoginPage(driver)
    max_email = 'a' * login_page.EMAIL_MAX_LENGTH + '@test.com'
    max_password = 'P' * login_page.PASSWORD_MAX_LENGTH
    # Validate max-length input
    login_page.validate_max_length_input(max_email, max_password)
    # Attempt login
    login_page.login(max_email, max_password)
    # Assert login success
    assert login_page.is_login_successful(), "Login should succeed with max-length valid credentials."


def test_TC_LOGIN_004_max_length_email_password(driver):
    """
    TC_LOGIN_004: Login with max-length email and password, expect success or error if invalid.
    Steps:
      - Enter maximum allowed email and password.
      - Validate max-length input.
      - Attempt login.
      - Expect success if valid, else error message.
    """
    login_page = LoginPage(driver)
    max_email = 'b' * login_page.EMAIL_MAX_LENGTH + '@test.com'
    max_password = 'Q' * login_page.PASSWORD_MAX_LENGTH
    # Validate max-length input
    login_page.validate_max_length_input(max_email, max_password)
    # Attempt login
    login_page.login(max_email, max_password)
    if login_page.is_login_successful():
        assert True, "Login succeeded with max-length credentials."
    else:
        error_msg = login_page.get_error_message()
        assert error_msg is not None and error_msg != '', "Error message must be shown for invalid max-length credentials."

# End of file
