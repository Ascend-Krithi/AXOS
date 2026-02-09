
import pytest
import asyncio

from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    @pytest.mark.asyncio
    async def test_valid_login(self):
        login_page = LoginPage()
        result = await login_page.login('valid_user', 'valid_password')
        assert result['success'] is True
        assert 'token' in result

    @pytest.mark.asyncio
    async def test_invalid_login(self):
        login_page = LoginPage()
        result = await login_page.login('invalid_user', 'invalid_password')
        assert result['success'] is False
        assert 'error' in result

class TestRuleConfiguration:
    @pytest.mark.asyncio
    async def test_valid_rule_schema(self):
        rule_page = RuleConfigurationPage()
        schema = {
            'trigger': 'amount_above',
            'conditions': [{'type': 'amount_above', 'value': 100}],
            'action': 'notify'
        }
        result = await rule_page.submit_rule_schema(schema)
        assert result['valid'] is True

    @pytest.mark.asyncio
    async def test_invalid_rule_schema(self):
        rule_page = RuleConfigurationPage()
        schema = {
            'trigger': 'amount_above',
            'conditions': [{'type': 'amount_above'}],  # missing value
            'action': 'notify'
        }
        result = await rule_page.submit_rule_schema(schema)
        assert result['valid'] is False
        assert 'error' in result

    @pytest.mark.asyncio
    async def test_invalid_trigger_schema(self):
        rule_page = RuleConfigurationPage()
        # TC_SCRUM158_05: Prepare a rule schema with an invalid trigger value
        schema = {
            'trigger': 'unknown_trigger',
            'conditions': [{'type': 'amount_above', 'value': 100}],
            'action': 'notify'
        }
        result = await rule_page.test_invalid_trigger_schema(schema)
        assert result['valid'] is False
        assert 'error' in result
        assert 'invalid trigger' in result['error'].lower() or 'unknown_trigger' in result['error']

    @pytest.mark.asyncio
    async def test_condition_missing_parameters_schema(self):
        rule_page = RuleConfigurationPage()
        # TC_SCRUM158_06: Prepare a rule schema with a condition missing required parameters
        schema = {
            'trigger': 'amount_above',
            'conditions': [{'type': 'amount_above'}],  # missing 'value'
            'action': 'notify'
        }
        result = await rule_page.test_condition_missing_parameters_schema(schema)
        assert result['valid'] is False
        assert 'error' in result
        assert 'missing' in result['error'].lower() or 'incomplete' in result['error'].lower()
