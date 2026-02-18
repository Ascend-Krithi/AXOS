from playwright.async_api import Page, expect

class PaymentConfirmationPage:
    def __init__(self, page: Page):
        self.page = page
        self.success_message = page.locator('#billpayResult')
        self.conf_payee_name = page.locator('#payeeName')
        self.conf_amount = page.locator('#amount')
        self.conf_from_account = page.locator('#fromAccountId')

    async def is_confirmation_displayed(self):
        await expect(self.success_message).to_be_visible()
        await expect(self.conf_payee_name).to_be_visible()
        await expect(self.conf_amount).to_be_visible()
        await expect(self.conf_from_account).to_be_visible()

    async def get_confirmation_details(self):
        return {
            'payee_name': await self.conf_payee_name.inner_text(),
            'amount': await self.conf_amount.inner_text(),
            'from_account': await self.conf_from_account.inner_text()
        }
