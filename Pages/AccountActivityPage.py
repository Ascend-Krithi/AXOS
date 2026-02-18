from playwright.async_api import Page, expect

class AccountActivityPage:
    def __init__(self, page: Page):
        self.page = page
        self.transaction_table = page.locator('#transactionTable')
        self.latest_transaction = page.locator('#transactionTable tbody tr:first-child')

    async def is_loaded(self):
        await expect(self.transaction_table).to_be_visible()

    async def get_latest_transaction(self):
        await self.is_loaded()
        return await self.latest_transaction.inner_text()
