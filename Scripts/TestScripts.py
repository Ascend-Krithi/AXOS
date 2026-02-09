import pytest
from Pages.LoginPage import LoginPage
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
        await self.login_page.fill_email('...'

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_rule_specific_date(self):
        """
        TC-FT-001: Test rule creation with specific_date trigger and fixed_amount action.
        Steps:
        - Define JSON rule {"trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"}, "action": {"type": "fixed_amount", "amount": 100}, "conditions": []}
        - Simulate system time
        - Validate transfer
        Acceptance:
        - Rule is accepted, transfer executed once at specified date.
        """
        await self.rule_page.navigate()
        rule_json = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        await self.rule_page.test_specific_date_rule(rule_json)
        # Assumes test_specific_date_rule handles form filling, saving, time simulation, and validation

    async def test_rule_recurring(self):
        """
        TC-FT-002: Test rule creation with recurring trigger (weekly) and percentage_of_deposit action.
        Steps:
        - Define JSON rule {"trigger": {"type": "recurring", "interval": "weekly"}, "action": {"type": "percentage_of_deposit", "percentage": 10}, "conditions": []}
        - Simulate weeks passing
        - Validate transfer
        Acceptance:
        - Rule is accepted, transfer executed at each interval.
        """
        await self.rule_page.navigate()
        rule_json = {
            "trigger": {"type": "recurring", "interval": "weekly"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        await self.rule_page.test_recurring_rule(rule_json)
        # Assumes test_recurring_rule handles form filling, saving, time simulation, and validation
