from playwright.async_api import Page, expect

class BillPayPage:
    def __init__(self, page: Page):
        self.page = page
        self.bill_pay_link = page.locator('text=Bill Pay')
        self.payee_name = page.locator('name=payee.name')
        self.address = page.locator('name=payee.address.street')
        self.city = page.locator('name=payee.address.city')
        self.state = page.locator('name=payee.address.state')
        self.zip_code = page.locator('name=payee.zipCode')
        self.phone_number = page.locator('name=payee.phoneNumber')
        self.account_number = page.locator('name=payee.accountNumber')
        self.verify_account_number = page.locator('name=verifyAccount')
        self.amount = page.locator('name=amount')
        self.from_account_id = page.locator('name=fromAccountId')
        self.send_payment_button = page.locator("input[value='Send Payment']")

    async def navigate_to_bill_pay(self):
        await self.bill_pay_link.click()
        await expect(self.send_payment_button).to_be_visible()

    async def enter_payee_details(self, name: str, address: str, city: str, state: str, zip_code: str, phone: str, account: str, verify_account: str):
        await self.payee_name.fill(name)
        await self.address.fill(address)
        await self.city.fill(city)
        await self.state.fill(state)
        await self.zip_code.fill(zip_code)
        await self.phone_number.fill(phone)
        await self.account_number.fill(account)
        await self.verify_account_number.fill(verify_account)

    async def enter_amount(self, amount: str):
        await self.amount.fill(amount)

    async def select_account(self, account_id: str):
        await self.from_account_id.select_option(account_id)

    async def send_payment(self):
        await self.send_payment_button.click()
