import pytest
from Pages.LoginPage import LoginPage
from Pages.ProfilePage import ProfilePage
from Pages.SettingsPage import SettingsPage

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
        await self.login_page.fill_email('testuser@example.com')
        await self.login_page.fill_password('password123')
        await self.login_page.toggle_remember_me(True)
        await self.login_page.submit_login('testuser@example.com', 'password123')
        assert await self.login_page.is_logged_in()

class TestProfileAndSettings:
    def __init__(self, page):
        self.page = page
        self.profile_page = ProfilePage(page)
        self.settings_page = SettingsPage(page)

    async def test_TC_SCRUM_15483_001_navigate_to_profile(self):
        # TC-SCRUM-15483-001: Verify user can navigate to Profile page via profile icon
        await self.profile_page.click_profile()
        # Assuming there is a method to assert profile page loaded
        assert await self.page.locator('#profile-header').is_visible()

    async def test_TC_SCRUM_15483_002_open_settings_menu(self):
        # TC-SCRUM-15483-002: Verify user can open Settings menu from the navigation
        await self.settings_page.open_settings()
        # Assuming there is a method to assert settings menu loaded
        assert await self.page.locator('#settings-header').is_visible()
