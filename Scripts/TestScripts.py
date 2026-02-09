import pytest
import asyncio

from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    # Existing test methods...
    # ... [existing methods here] ...

    @pytest.mark.asyncio
    async def test_login_without_remember_me_session_not_persisted(self):
        login_page = LoginPage()
        await login_page.navigate_to_login()
        await login_page.login(username="valid_user", password="valid_pass", remember_me=False)
        await login_page.close_browser()
        await login_page.reopen_browser()
        assert await login_page.verify_session_not_persisted(), "Session should not persist after browser restart when 'Remember Me' is not checked."

    @pytest.mark.asyncio
    async def test_forgot_password_flow_confirmation(self):
        login_page = LoginPage()
        await login_page.navigate_to_login()
        await login_page.forgot_password(email="registered_user@example.com")
        assert await login_page.verify_password_reset_confirmation(), "Password reset confirmation message not found."

    @pytest.mark.asyncio
    async def test_TC_LOGIN_001_valid_login_dashboard_redirection(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_login_page_displayed(), "Login page is not displayed."
        login_page.login("user@example.com", "ValidPass123")
        # Add assertion for dashboard redirection

    @pytest.mark.asyncio
    async def test_TC_LOGIN_002_invalid_login_error_message(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_login_page_displayed(), "Login page is not displayed."
        login_page.login("user@example.com", "WrongPass456")
        assert login_page.verify_invalid_credentials_error(), "Error message 'Invalid credentials' was not displayed."

    @pytest.mark.asyncio
    async def test_TC_LOGIN_003_email_required_error(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_login_page_displayed(), "Login page is not displayed."
        error_message = login_page.login_with_empty_email("ValidPass123")
        assert error_message == "Email/Username required", "Error message 'Email/Username required' was not displayed."

    @pytest.mark.asyncio
    async def test_TC_LOGIN_004_password_required_error(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_login_page_displayed(), "Login page is not displayed."
        error_message = login_page.login_with_empty_password("user@example.com")
        assert error_message == "Password required", "Error message 'Password required' was not displayed."
