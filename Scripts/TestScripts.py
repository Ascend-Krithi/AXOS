import pytest
from Pages.LoginPage import LoginPage
from Pages.BillPayPage import BillPayPage

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
        # Additional code for remember me functionality...

class TestBillPayFunctionality:
    def __init__(self, page):
        self.page = page
        self.bill_pay_page = BillPayPage(page)

    async def test_pay_electric_company(self):
        # TC-BP-001: Pay Electric Company ($150) from account 13344
        await self.bill_pay_page.navigate()
        await self.bill_pay_page.fill_payee_details(
            payee_name="Electric Company",
            address="123 Electric Ave",
            city="ElectriCity",
            state="EC",
            zip="12345",
            phone="555-1234"
        )
        await self.bill_pay_page.fill_account_details(
            account_number="13344",
            verify_account_number="13344"
        )
        await self.bill_pay_page.fill_payment_amount("150.00")
        await self.bill_pay_page.select_account("13344")
        await self.bill_pay_page.send_payment()
        confirmation = await self.bill_pay_page.get_confirmation()
        assert "Payment to Electric Company of $150.00 was successful" in confirmation

    async def test_pay_water_utility(self):
        # TC-BP-002: Pay Water Utility ($0.01) from account 13344
        await self.bill_pay_page.navigate()
        await self.bill_pay_page.fill_payee_details(
            payee_name="Water Utility",
            address="456 Water St",
            city="Watertown",
            state="WU",
            zip="67890",
            phone="555-5678"
        )
        await self.bill_pay_page.fill_account_details(
            account_number="13344",
            verify_account_number="13344"
        )
        await self.bill_pay_page.fill_payment_amount("0.01")
        await self.bill_pay_page.select_account("13344")
        await self.bill_pay_page.send_payment()
        confirmation = await self.bill_pay_page.get_confirmation()
        assert "Payment to Water Utility of $0.01 was successful" in confirmation
