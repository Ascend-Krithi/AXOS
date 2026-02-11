# Import necessary modules
from Pages.RuleConfigurationPage import RuleConfigurationPage

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

class TestRuleConfiguration:
    def __init__(self, driver):
        self.page = RuleConfigurationPage(driver)

    def test_negative_amount_rule_creation_and_validation(self):
        rule_id = 'NEG001'
        rule_name = 'Negative Amount Rule'
        self.page.create_rule_negative_amount(rule_id, rule_name)
        self.page.verify_negative_amount_error()

    def test_zero_amount_rule_creation_and_validation(self):
        rule_id = 'ZERO001'
        rule_name = 'Zero Amount Rule'
        self.page.create_rule_zero_amount(rule_id, rule_name)
        self.page.verify_zero_amount_error()

    def test_large_amount_rule_creation_and_validation(self):
        rule_id = 'LARGE001'
        rule_name = 'Large Amount Rule'
        expected_amount = 999999999.99
        self.page.create_rule_large_amount(rule_id, rule_name)
        self.page.verify_large_amount_success()
        self.page.verify_amount_precision(expected_amount)
        expected_balance = 1000000000.00
        self.page.trigger_rule_and_verify_execution(expected_balance)
