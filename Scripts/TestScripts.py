import pytest
from selenium import webdriver
from Pages.BillPayPage import BillPayPage
from Pages.NavigationPage import NavigationPage

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

class TestBillPay:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request):
        driver = webdriver.Chrome()
        navigation_page = NavigationPage(driver)
        bill_pay_page = BillPayPage(driver)
        request.cls.driver = driver
        request.cls.navigation_page = navigation_page
        request.cls.bill_pay_page = bill_pay_page
        yield
        driver.quit()

    def test_tc_bp_001_electric_company_payment(self):
        """
        TC-BP-001: Pay 'Electric Company' $150.00 from account 13344.
        """
        self.navigation_page.go_to_bill_pay()
        self.bill_pay_page.fill_bill_pay_form(
            payee_name="Electric Company",
            address="123 Main St",
            city="Springfield",
            state="IL",
            zip_code="62701",
            phone="555-123-4567",
            account="12345",
            verify_account="12345",
            amount="150.00",
            from_account="13344"
        )
        self.bill_pay_page.submit_payment()
        self.bill_pay_page.verify_confirmation(
            expected_payee="Electric Company",
            expected_amount="150.00",
            expected_account="13344"
        )

    def test_tc_bp_002_water_utility_minimum_payment(self):
        """
        TC-BP-002: Pay 'Water Utility' $0.01 from account 13344.
        """
        self.navigation_page.go_to_bill_pay()
        self.bill_pay_page.fill_bill_pay_form(
            payee_name="Water Utility",
            address="456 Oak Ave",
            city="Chicago",
            state="IL",
            zip_code="60601",
            phone="555-987-6543",
            account="67890",
            verify_account="67890",
            amount="0.01",
            from_account="13344"
        )
        self.bill_pay_page.submit_payment()
        self.bill_pay_page.verify_confirmation(
            expected_payee="Water Utility",
            expected_amount="0.01",
            expected_account="13344"
        )
