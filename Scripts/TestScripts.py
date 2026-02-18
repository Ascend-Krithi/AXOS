{Import necessary modules}

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
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.navigation_page = NavigationPage(driver)
        self.bill_pay_page = BillPayPage(driver)
        self.account_activity_page = AccountActivityPage(driver)

    async def test_TC_SCRUM_15483_001(self):
        # Step 2: Navigate to login page
        # Step 3: Enter valid username and password
        self.login_page.enter_username('testuser')
        self.login_page.enter_password('testpass')
        # Step 4: Click Login button
        self.login_page.click_login()
        # Step 5: Verify Account Overview page is displayed
        self.navigation_page.go_to_account_overview()
        # Step 6: Click Bill Pay option
        self.navigation_page.go_to_bill_pay()
        # Step 7: Enter valid payee details
        payee_info = {
            'name': 'Electric Company',
            'address': '123 Main Street',
            'city': 'New York',
            'state': 'NY',
            'zipCode': '10001',
            'phoneNumber': '555-1234',
            'accountNumber': '987654321',
            'verifyAccount': '987654321',
            'amount': '150.00',
            'fromAccountId': '12345678'
        }
        self.bill_pay_page.fill_payment_form(payee_info)
        # Step 10: Click Send Payment button
        self.bill_pay_page.click_send_payment()
        # Step 11: Verify payment confirmation message
        confirmation = self.bill_pay_page.get_confirmation_details()
        assert confirmation['payeeName'] == 'Electric Company'
        assert confirmation['amount'] == '150.00'
        assert confirmation['fromAccountId'] == '12345678'
        # Step 12: Navigate to Account Activity
        # Step 13: Verify transaction appears in history
        transactions = self.account_activity_page.get_all_transactions()
        assert any('Electric Company' in tx for tx in transactions)

    async def test_TC_SCRUM_15483_002(self):
        # Step 1: Login and navigate to Bill Pay
        self.login_page.enter_username('testuser')
        self.login_page.enter_password('testpass')
        self.login_page.click_login()
        self.navigation_page.go_to_bill_pay()
        # Step 2: Enter valid payee information
        payee_info = {
            'name': 'Electric Company',
            'address': '123 Main Street',
            'city': 'New York',
            'state': 'NY',
            'zipCode': '10001',
            'phoneNumber': '555-1234',
            'accountNumber': '987654321',
            'verifyAccount': '987654321',
            'amount': '10000.00',
            'fromAccountId': '87654321'  # Insufficient funds
        }
        self.bill_pay_page.fill_payment_form(payee_info)
        # Step 5: Click Send Payment button
        self.bill_pay_page.click_send_payment()
        # Step 6: Verify error message: Insufficient funds
        error_message = self.bill_pay_page.get_success_message()
        assert 'Insufficient funds' in error_message
        # Step 7: Verify payment not processed
        transactions = self.account_activity_page.get_all_transactions()
        assert all('10000.00' not in tx for tx in transactions)
