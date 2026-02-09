
import pytest
import asyncio
from Pages.LoginPage import LoginPage

@pytest.mark.asyncio
class TestLoginFunctionality:

    async def test_login_valid_credentials(self, driver):
        login_page = LoginPage(driver)
        await login_page.login('validuser@example.com', 'ValidPass123')
        assert await login_page.is_logged_in()

    async def test_login_invalid_credentials(self, driver):
        login_page = LoginPage(driver)
        await login_page.login('invaliduser@example.com', 'WrongPass456')
        error_message = await login_page.get_login_error_message()
        assert error_message == 'Invalid username or password.'

    async def test_login_empty_fields(self, driver):
        login_page = LoginPage(driver)
        await login_page.login('', '')
        error_message = await login_page.get_login_error_message()
        assert error_message == 'Please enter email and password.'

    async def test_login_email_format_validation(self, driver):
        login_page = LoginPage(driver)
        await login_page.login('notanemail', 'SomePass123')
        error_message = await login_page.get_login_error_message()
        assert error_message == 'Please enter a valid email address.'

    async def test_login_password_min_length(self, driver):
        login_page = LoginPage(driver)
        await login_page.login('validuser@example.com', '123')
        error_message = await login_page.get_login_error_message()
        assert error_message == 'Password must be at least 8 characters.'

    async def test_login_email_max_length(self, driver):
        login_page = LoginPage(driver)
        long_email = 'a' * 46 + '@ex.com'  # 50 chars
        await login_page.login(long_email, 'ValidPass123')
        error_message = await login_page.get_login_error_message()
        assert error_message in ['Invalid username or password.', 'Please enter a valid email address.']

    async def test_login_password_max_length(self, driver):
        login_page = LoginPage(driver)
        long_password = 'a' * 50
        await login_page.login('validuser@example.com', long_password)
        error_message = await login_page.get_login_error_message()
        assert error_message in ['Invalid username or password.', 'Password is too long.']

    # TC_LOGIN_009: Test max input length for email and password fields, error handling or successful login
    async def test_login_max_input_length(self, driver):
        login_page = LoginPage(driver)
        max_email = 'a' * 42 + '@example.com'  # 50 chars total
        max_password = 'P' * 50
        # Validate max input length
        await login_page.validate_max_input_length('email', max_email)
        await login_page.validate_max_input_length('password', max_password)
        await login_page.login(max_email, max_password)
        error_message = await login_page.get_login_error_message()
        # Accept either error or successful login depending on app logic
        assert error_message in [
            'Invalid username or password.',
            'Email or password exceeds maximum length.',
            'Please enter a valid email address.',
            ''
        ] or await login_page.is_logged_in()

    # TC_LOGIN_010: Attempt login with unregistered user, verify error and stay on login page
    async def test_login_unregistered_user(self, driver):
        login_page = LoginPage(driver)
        unregistered_email = 'unknown@example.com'
        unregistered_password = 'RandomPass789'
        await login_page.login_and_validate_error(unregistered_email, unregistered_password)
        error_message = await login_page.get_login_error_message()
        assert error_message == 'Invalid username or password.'
        assert await login_page.is_on_login_page()
