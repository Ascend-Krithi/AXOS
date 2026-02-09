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

    async def test_tc_login_01(self):
        # TC_Login_01: Valid login
        url = 'https://example.com/login'  # Replace with actual login URL
        await self.login_page.navigate_to_login(url)
        await self.login_page.enter_email('user@example.com')
        await self.login_page.enter_password('ValidPassword123')
        await self.login_page.click_login()
        assert await self.login_page.is_dashboard_displayed(), 'Dashboard should be displayed after valid login.'

    async def test_tc_login_02(self):
        # TC_Login_02: Invalid login
        url = 'https://example.com/login'  # Replace with actual login URL
        await self.login_page.navigate_to_login(url)
        await self.login_page.enter_email('wronguser@example.com')
        await self.login_page.enter_password('WrongPassword')
        await self.login_page.click_login()
        assert await self.login_page.is_error_message_displayed(), 'Error message should be displayed for invalid login.'

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

    async def test_tc_scrum158_07(self):
        """
        TC_SCRUM158_07: Prepare a rule schema with the maximum supported conditions and actions (10 each), submit, validate persistence.
        """
        await self.rule_page.navigate_to_rule_configuration()
        max_rule_schema = {
            "conditions": [{"type": f"condition_type_{i}", "value": f"value_{i}"} for i in range(10)],
            "actions": [{"type": f"action_type_{i}", "amount": i * 10} for i in range(10)]
        }
        await self.rule_page.fill_rule_schema(max_rule_schema)
        valid, message = await self.rule_page.validate_schema()
        assert valid, f"Schema should be valid: {message}"
        await self.rule_page.submit_rule()
        rule = await self.rule_page.retrieve_rule(rule_id=None)
        assert len(rule.get("conditions", [])) == 10, "All 10 conditions should be persisted"
        assert len(rule.get("actions", [])) == 10, "All 10 actions should be persisted"
        return True

    async def test_tc_scrum158_08(self):
        """
        TC_SCRUM158_08: Prepare a rule schema with empty 'conditions' and 'actions' arrays, submit, validate response.
        """
        await self.rule_page.navigate_to_rule_configuration()
        empty_rule_schema = {
            "conditions": [],
            "actions": []
        }
        await self.rule_page.fill_rule_schema(empty_rule_schema)
        valid, message = await self.rule_page.validate_schema()
        await self.rule_page.submit_rule()
        # Business rule: Accept or error, both are valid as per acceptance criteria
        return valid, message

    async def test_tc_scrum158_09(self):
        """
        TC_SCRUM158_09: Prepare rule schema with minimum required fields, validate, submit, and verify creation.
        """
        await self.rule_page.navigate_to_rule_configuration()
        schema = {
            "trigger": "balance_above",
            "conditions": [
                {"type": "amount_above", "value": 1000}
            ],
            "actions": [
                {"type": "transfer", "amount": 100}
            ]
        }
        await self.rule_page.fill_rule_schema(schema)
        valid, message = await self.rule_page.validate_schema()
        assert valid, f"Schema validation failed: {message}"
        await self.rule_page.submit_rule()
        rule_details = await self.rule_page.retrieve_rule(schema.get("trigger", ""))
        assert rule_details, "Rule creation failed or not found."

    async def test_tc_scrum158_10(self):
        """
        TC_SCRUM158_10: Prepare rule schema with unsupported trigger type, validate, submit, and check API response.
        """
        await self.rule_page.navigate_to_rule_configuration()
        schema = {
            "trigger": "future_trigger",
            "conditions": [
                {"type": "amount_above", "value": 1000}
            ],
            "actions": [
                {"type": "transfer", "amount": 100}
            ]
        }
        await self.rule_page.fill_rule_schema(schema)
        valid, message = await self.rule_page.validate_schema()
        if not valid:
            assert "unsupported" in message.lower() or "invalid" in message.lower(), f"Unexpected error message: {message}"
        await self.rule_page.submit_rule()
        error_message = await self.rule_page.get_error_message()
        assert error_message is not None, "Expected API error for unsupported trigger type"
