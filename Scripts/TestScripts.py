# Import necessary modules
from BillPayPage import BillPayPage

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

class TestBillPayFunctionality:
    def __init__(self, driver, locators):
        self.bill_pay_page = BillPayPage(driver, locators)

    def test_tc_bp_001(self):
        # Step 1: Navigate to Bill Pay section
        self.bill_pay_page.go_to_bill_pay()
        # Step 2: Enter valid payee details
        self.bill_pay_page.fill_payee_details(
            payee_name="Electric Company",
            address="123 Main St",
            city="Springfield",
            state="IL",
            zip_code="62701",
            phone="555-123-4567"
        )
        # Step 3: Enter account number and verify
        self.bill_pay_page.fill_account_details("12345", "12345")
        # Step 4: Enter payment amount
        self.bill_pay_page.fill_payment_amount(150.00)
        # Step 5: Select source account
        self.bill_pay_page.select_source_account("13344")
        # Step 6: Submit payment
        self.bill_pay_page.submit_payment()
        # Step 7: Verify confirmation
        assert self.bill_pay_page.is_confirmation_displayed(), "Confirmation page not displayed"
        confirmation = self.bill_pay_page.get_confirmation_details()
        assert confirmation['payeeName'] == "Electric Company"
        assert confirmation['amount'] == "$150.00"
        assert confirmation['fromAccount'] == "13344"

    def test_tc_bp_002(self):
        # Step 1: Navigate to Bill Pay section
        self.bill_pay_page.go_to_bill_pay()
        # Step 2: Enter valid payee details
        self.bill_pay_page.fill_payee_details(
            payee_name="Water Utility",
            address="456 Oak Ave",
            city="Chicago",
            state="IL",
            zip_code="60601",
            phone="555-987-6543"
        )
        # Step 3: Enter account number and verify
        self.bill_pay_page.fill_account_details("67890", "67890")
        # Step 4: Enter minimum valid amount
        self.bill_pay_page.fill_payment_amount(0.01)
        # Step 5: Select account with sufficient balance
        self.bill_pay_page.select_source_account("13344")
        # Step 6: Submit payment
        self.bill_pay_page.submit_payment()
        # Step 7: Verify confirmation
        assert self.bill_pay_page.is_confirmation_displayed(), "Confirmation page not displayed"
        confirmation = self.bill_pay_page.get_confirmation_details()
        assert confirmation['payeeName'] == "Water Utility"
        assert confirmation['amount'] == "$0.01"
        assert confirmation['fromAccount'] == "13344"
