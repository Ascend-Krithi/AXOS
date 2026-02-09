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
        await self.login_page.fill_email('...')

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

    async def test_rule_multiple_conditions(self):
        """
        TC-FT-003: Define a rule with multiple conditions (balance >= 1000, source = 'salary').
        Simulate deposit from 'salary' when balance is 900 (transfer NOT executed).
        Simulate deposit from 'salary' when balance is 1200 (transfer executed).
        Acceptance:
        - Rule is accepted.
        - Transfer is NOT executed for balance 900.
        - Transfer IS executed for balance 1200.
        """
        await self.rule_page.navigate()
        rule_data = {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "fixed_amount", "amount": 50},
            "conditions": [
                {"type": "balance_threshold", "operator": ">=", "value": 1000},
                {"type": "transaction_source", "value": "salary"}
            ]
        }
        rule_created = self.rule_page.define_rule_with_multiple_conditions(rule_data)
        assert rule_created, "Rule was not accepted."
        # Simulate deposit from 'salary' with balance 900
        simulation_data_900 = {"balance": 900, "deposit": 100, "source": "salary"}
        transfer_executed_900 = self.rule_page.simulate_deposit(simulation_data_900)
        assert transfer_executed_900 is False, "Transfer should NOT be executed for balance 900."
        # Simulate deposit from 'salary' with balance 1200
        simulation_data_1200 = {"balance": 1200, "deposit": 100, "source": "salary"}
        transfer_executed_1200 = self.rule_page.simulate_deposit(simulation_data_1200)
        assert transfer_executed_1200 is True, "Transfer should be executed for balance 1200."

    async def test_rule_missing_trigger(self):
        """
        TC-FT-004: Submit a rule with missing trigger type (expect error).
        Acceptance:
        - System returns error indicating missing required field.
        """
        await self.rule_page.navigate()
        rule_data = {
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        error_returned = self.rule_page.submit_rule_with_missing_fields(rule_data)
        assert error_returned, "Error was not returned for missing trigger type."

    async def test_rule_unsupported_action(self):
        """
        TC-FT-004: Submit a rule with unsupported action type (expect error).
        Acceptance:
        - System returns error indicating unsupported action type.
        """
        await self.rule_page.navigate()
        rule_data = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "unknown_action"},
            "conditions": []
        }
        error_returned = self.rule_page.submit_rule_with_unsupported_action(rule_data)
        assert error_returned, "Error was not returned for unsupported action type."
