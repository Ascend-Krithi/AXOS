import pytest
from LoginPage import LoginPage

class TestLoginFunctionality:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('')

    # TC-FT-001: Valid Login
    async def test_valid_login(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('user@example.com')
        await self.login_page.fill_password('securePassword123')
        await self.login_page.click_login_button()
        assert await self.login_page.is_logged_in() is True

    # TC-FT-002: Invalid Login
    async def test_invalid_login(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('user@example.com')
        await self.login_page.fill_password('wrongPassword')
        await self.login_page.click_login_button()
        assert await self.login_page.get_error_message() == 'Invalid credentials'
