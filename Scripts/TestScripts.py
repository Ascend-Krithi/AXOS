import pytest
import asyncio

from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    # Existing test methods...
    # ... [full file content as previously pasted] ...

    @pytest.mark.asyncio
    async def test_login_without_remember_me_session_not_persisted(self):
        """
        TC_LOGIN_007: Login without 'Remember Me', verify session not persisted after browser restart
        Steps:
            1. Navigate to login
            2. Enter valid credentials without 'Remember Me'
            3. Login
            4. Close and reopen browser
            5. Verify session does not persist
        """
        login_page = LoginPage()
        await login_page.navigate_to_login()
        await login_page.login(username="valid_user", password="valid_pass", remember_me=False)
        await login_page.close_browser()
        await login_page.reopen_browser()
        assert await login_page.verify_session_not_persisted(), "Session should not persist after browser restart when 'Remember Me' is not checked."

    @pytest.mark.asyncio
    async def test_forgot_password_flow_confirmation(self):
        """
        TC_LOGIN_008: Forgot password flow, verify confirmation
        Steps:
            1. Navigate to login
            2. Click 'Forgot Password'
            3. Enter registered email
            4. Submit
            5. Verify confirmation message
        """
        login_page = LoginPage()
        await login_page.navigate_to_login()
        await login_page.forgot_password(email="registered_user@example.com")
        assert await login_page.verify_password_reset_confirmation(), "Password reset confirmation message not found."

    @pytest.mark.asyncio
    async def test_rate_limiting_and_lockout_detection(self):
        """
        TC_LOGIN_009: Rapid invalid login attempts, detect rate limiting/lockout/captcha
        Steps:
            1. Navigate to login page
            2. Attempt to login with invalid credentials rapidly multiple times (e.g., 10 times in succession)
            3. System should detect rapid attempts and apply rate limiting, lockout, or captcha
        """
        login_page = LoginPage()
        await login_page.navigate_to_login()
        await login_page.login_multiple_attempts(username="wronguser@example.com", password="WrongPassword", attempts=10, delay=0.5)
        assert await login_page.is_rate_limited_or_locked(), "Rate limiting, lockout, or captcha was not detected after rapid invalid login attempts."

    @pytest.mark.asyncio
    async def test_case_sensitive_login_validation(self):
        """
        TC_LOGIN_010: Case-sensitive login validation
        Steps:
            1. Navigate to login page
            2. Enter email/username and password with different cases (upper/lower/mixed)
            3. Click the Login button
            4. Login should succeed only if credentials match exactly; error otherwise
        """
        login_page = LoginPage()
        await login_page.navigate_to_login()
        await login_page.login(username="USER@EXAMPLE.COM", password="ValidPassword123")
        assert await login_page.is_login_error_displayed(), "Login error message was not displayed for case-mismatched credentials."

class TestRuleConfiguration:
    # Existing test methods...
    # ... [full file content as previously pasted] ...
