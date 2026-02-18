from playwright.async_api import Page, expect

class AccountOverviewPage:
    def __init__(self, page: Page):
        self.page = page
        self.account_overview_link = page.locator('text=Accounts Overview')

    async def is_loaded(self):
        await expect(self.account_overview_link).to_be_visible()

    async def navigate_to_account_overview(self):
        await self.account_overview_link.click()
        await self.is_loaded()
