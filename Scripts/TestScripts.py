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
        await self.login_page.fill_email('...')

class TestRuleConfiguration:
    def __init__(self, driver):
        self.rule_page = RuleConfigurationPage(driver)

    def test_define_percentage_of_deposit_rule(self):
        """
        TC-FT-005 Step 1: Define a rule for 10% of deposit action.
        """
        result = self.rule_page.define_percentage_of_deposit_rule(10)
        assert result is True, 'Rule for 10% deposit was not accepted.'

    def test_simulate_deposit_and_verify_transfer(self):
        """
        TC-FT-005 Step 2: Simulate deposit of 500 units, verify transfer of 50 units.
        """
        deposit_amount = 500
        expected_transfer = 50
        result = self.rule_page.simulate_deposit_and_verify_transfer(deposit_amount, expected_transfer)
        assert result is True, f'Transfer of {expected_transfer} units was not executed after deposit.'

    def test_define_rule_with_future_trigger(self):
        """
        TC-FT-006 Step 1: Define a rule with a new, future rule type (currency_conversion, EUR, fixed_amount 100).
        """
        feedback = self.rule_page.define_rule_with_future_trigger('currency_conversion', 'EUR', 'fixed_amount', 100)
        assert feedback in ['System accepts or gracefully rejects with a clear message', 'No feedback received.'], f'Unexpected feedback: {feedback}'

    def test_verify_existing_rules_execution(self):
        """
        TC-FT-006 Step 2: Verify existing rules continue to execute as before.
        """
        result = self.rule_page.verify_existing_rules_execution()
        assert result is True, 'Existing rules did not function as expected.'
