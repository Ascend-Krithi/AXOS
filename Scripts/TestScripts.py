import pytest
from Pages.LoginPage import LoginPage
from Pages.AccountOverviewPage import AccountOverviewPage
from Pages.BillPayPage import BillPayPage
from Pages.PaymentConfirmationPage import PaymentConfirmationPage
from Pages.AccountActivityPage import AccountActivityPage

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
        await self.login_page.fill_email('...')
        # ...

class TestBillPay:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.account_overview_page = AccountOverviewPage(page)
        self.bill_pay_page = BillPayPage(page)
        self.payment_confirmation_page = PaymentConfirmationPage(page)
        self.account_activity_page = AccountActivityPage(page)

    async def test_end_to_end_bill_payment_valid(self):
        """
        TC-SCRUM-15483-001: Full end-to-end bill payment with valid data, including login, bill pay, confirmation, and transaction history.
        """
        # Step 1: Login
        await self.login_page.navigate()
        await self.login_page.submit_login('valid_user@example.com', 'valid_password')
        assert await self.account_overview_page.is_loaded()

        # Step 2: Go to Bill Pay
        await self.account_overview_page.navigate_to_bill_pay()
        assert await self.bill_pay_page.is_loaded()

        # Step 3: Fill Bill Pay Form
        await self.bill_pay_page.fill_payee_details({
            'payee_name': 'John Doe',
            'address': '123 Main St',
            'city': 'Metropolis',
            'state': 'NY',
            'zip_code': '10001',
            'phone': '5551234567',
            'account': '987654321',
            'verify_account': '987654321',
            'amount': '150.00',
            'from_account': '123456789'
        })
        await self.bill_pay_page.submit_payment()

        # Step 4: Payment Confirmation
        assert await self.payment_confirmation_page.is_loaded()
        confirmation_details = await self.payment_confirmation_page.get_confirmation_details()
        assert confirmation_details['amount'] == '150.00'
        assert confirmation_details['payee'] == 'John Doe'

        # Step 5: Verify Transaction in Account Activity
        await self.account_overview_page.navigate_to_account_activity()
        assert await self.account_activity_page.is_loaded()
        transactions = await self.account_activity_page.get_recent_transactions()
        assert any(t['amount'] == '150.00' and t['payee'] == 'John Doe' for t in transactions)

    async def test_bill_payment_insufficient_funds(self):
        """
        TC-SCRUM-15483-002: Bill payment with insufficient funds (should show error, no transaction).
        """
        # Step 1: Login
        await self.login_page.navigate()
        await self.login_page.submit_login('valid_user@example.com', 'valid_password')
        assert await self.account_overview_page.is_loaded()

        # Step 2: Go to Bill Pay
        await self.account_overview_page.navigate_to_bill_pay()
        assert await self.bill_pay_page.is_loaded()

        # Step 3: Fill Bill Pay Form with high amount
        await self.bill_pay_page.fill_payee_details({
            'payee_name': 'Jane Smith',
            'address': '456 Elm St',
            'city': 'Gotham',
            'state': 'NJ',
            'zip_code': '07001',
            'phone': '5559876543',
            'account': '123123123',
            'verify_account': '123123123',
            'amount': '1000000.00',  # Exceeds balance
            'from_account': '123456789'
        })
        await self.bill_pay_page.submit_payment()

        # Step 4: Validate error message
        error_message = await self.bill_pay_page.get_error_message()
        assert error_message == 'Insufficient funds'

        # Step 5: Ensure no transaction is recorded
        await self.account_overview_page.navigate_to_account_activity()
        assert await self.account_activity_page.is_loaded()
        transactions = await self.account_activity_page.get_recent_transactions()
        assert not any(t['amount'] == '1000000.00' and t['payee'] == 'Jane Smith' for t in transactions)
