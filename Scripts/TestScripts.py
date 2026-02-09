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
        await self.login_page.fill_email('testuser@example.com')
        await self.login_page.fill_password('password123')
        await self.login_page.toggle_remember_me(True)
        await self.login_page.submit_login('testuser@example.com', 'password123')
        assert await self.login_page.is_logged_in()

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_config_page = RuleConfigurationPage(page)

    async def test_TC_SCRUM158_03_create_rule_with_metadata(self):
        # Prepare rule schema with metadata
        rule_schema = {
            "name": "Test Rule Metadata",
            "trigger": "on_event",
            "metadata": {
                "author": "qa_automation",
                "priority": "high",
                "description": "Rule for testing metadata"
            },
            "actions": [
                {"type": "notify", "target": "admin"}
            ]
        }
        await self.rule_config_page.navigate()
        await self.rule_config_page.open_create_rule()
        await self.rule_config_page.fill_rule_schema(rule_schema)
        await self.rule_config_page.submit_rule()
        # Retrieve rule and verify metadata
        rule_id = await self.rule_config_page.get_last_created_rule_id()
        retrieved_rule = await self.rule_config_page.get_rule_by_id(rule_id)
        assert retrieved_rule["metadata"] == rule_schema["metadata"], "Rule metadata does not match input"

    async def test_TC_SCRUM158_04_missing_trigger_field_validation(self):
        # Prepare rule schema missing 'trigger' field
        rule_schema = {
            "name": "Test Rule Missing Trigger",
            "metadata": {
                "author": "qa_automation",
                "priority": "medium"
            },
            "actions": [
                {"type": "log", "target": "system"}
            ]
        }
        await self.rule_config_page.navigate()
        await self.rule_config_page.open_create_rule()
        await self.rule_config_page.fill_rule_schema(rule_schema)
        await self.rule_config_page.submit_rule()
        error_message = await self.rule_config_page.get_error_message()
        assert error_message == "Trigger field is required", "Validation error message for missing trigger is incorrect"
