from playwright.async_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_field = page.locator('name=username')
        self.password_field = page.locator('name=password')
        self.login_button = page.locator("input[value='Log In']")

    async def navigate(self, url: str):
        await self.page.goto(url)
        await expect(self.login_button).to_be_visible()

    async def enter_username(self, username: str):
        await self.username_field.fill(username)

    async def enter_password(self, password: str):
        await self.password_field.fill(password)

    async def click_login(self):
        await self.login_button.click()

    async def login(self, url: str, username: str, password: str):
        await self.navigate(url)
        await self.enter_username(username)
        await self.enter_password(password)
        await self.click_login()
