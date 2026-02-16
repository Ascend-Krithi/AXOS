# Existing imports and TestLoginFunctionality class

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

# Bill Pay Test Cases
from Pages.BillPayPage import BillPayPage

class TestBillPay:
    def __init__(self, driver):
        self.driver = driver
        self.bill_pay_page = BillPayPage(driver)

    def test_tc_bp_001(self):
        '''Test Case TC-BP-001: Full Bill Pay flow with valid data'''
        assert self.bill_pay_page.is_bill_pay_page_loaded(), 'Bill Pay page not loaded.'
        self.bill_pay_page.enter_payee_details(
            name='Electric Company',
            address='123 Main St',
            city='Springfield',
            state='IL',
            zip_code='62701',
            phone='555-123-4567',
            account='12345',
            verify_account='12345'
        )
        self.bill_pay_page.enter_payment_amount(150.00)
        self.bill_pay_page.select_source_account('13344')
        self.bill_pay_page.submit_payment()
        confirmation = self.bill_pay_page.verify_confirmation(
            payee_name='Electric Company',
            amount=150.00,
            from_account='13344'
        )
        assert confirmation['payee_name'] == 'Electric Company'
        assert confirmation['amount'] == '150.00'
        assert '13344' in confirmation['from_account']

    def test_tc_bp_002(self):
        '''Test Case TC-BP-002: Minimum valid payment with valid mandatory fields'''
        assert self.bill_pay_page.is_bill_pay_page_loaded(), 'Bill Pay page not loaded.'
        self.bill_pay_page.enter_payee_details(
            name='Water Utility',
            address='456 Oak Ave',
            city='Chicago',
            state='IL',
            zip_code='60601',
            phone='555-987-6543',
            account='67890',
            verify_account='67890'
        )
        self.bill_pay_page.enter_payment_amount(0.01)
        self.bill_pay_page.select_source_account('13344')
        self.bill_pay_page.submit_payment()
        confirmation = self.bill_pay_page.verify_confirmation(
            payee_name='Water Utility',
            amount=0.01,
            from_account='13344'
        )
        assert confirmation['payee_name'] == 'Water Utility'
        assert confirmation['amount'] == '0.01'
        assert '13344' in confirmation['from_account']
