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
        await self.login_page.fill_email('')

class TestRuleConfigurationNegativeCases:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_invalid_trigger_value(self):
        """
        TC_SCRUM158_05: Prepare schema with invalid trigger value, submit, assert error.
        """
        await self.rule_page.navigate_to_rule_configuration()
        invalid_rule_schema = {
            "name": "Invalid Trigger Rule",
            "trigger": "INVALID_TRIGGER",  # Invalid trigger value
            "conditions": [{"type": "status", "value": "active"}],
            "actions": [{"type": "notify", "params": {"email": "test@example.com"}}]
        }
        await self.rule_page.fill_rule_schema(invalid_rule_schema)
        await self.rule_page.submit_rule()
        error_msg = await self.rule_page.get_error_message()
        assert error_msg == "Invalid trigger value", f"Expected 'Invalid trigger value', got '{error_msg}'"

    async def test_missing_condition_parameters(self):
        """
        TC_SCRUM158_06: Prepare schema with missing condition parameters, submit, assert error.
        """
        await self.rule_page.navigate_to_rule_configuration()
        invalid_rule_schema = {
            "name": "Missing Condition Params Rule",
            "trigger": "ON_CREATE",
            "conditions": [{"type": "status"}],  # Missing 'value' parameter
            "actions": [{"type": "notify", "params": {"email": "test@example.com"}}]
        }
        await self.rule_page.fill_rule_schema(invalid_rule_schema)
        await self.rule_page.submit_rule()
        error_msg = await self.rule_page.get_error_message()
        assert error_msg == "Condition parameters missing", f"Expected 'Condition parameters missing', got '{error_msg}'"
