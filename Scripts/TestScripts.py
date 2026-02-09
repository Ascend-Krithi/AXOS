
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

    # TC_SCRUM158_07: Create rule with max conditions and actions
    @pytest.mark.asyncio
    async def test_create_rule_with_max_conditions_and_actions(self):
        rule_page = RuleConfigurationPage()
        rule_id = "R_MAX_001"
        rule_name = "Rule with Max Conditions and Actions"
        conditions = [
            {"condition_type": "balance_above", "balance_threshold": 1000.0, "source": "providerA", "operator": "greater_than"} for _ in range(10)
        ]
        actions = [
            {"action_type": "transfer", "amount": 100.0, "percentage": None, "dest_account": f"ACC{str(i+1).zfill(3)}"} for i in range(10)
        ]
        result = await rule_page.create_rule_with_max_conditions_and_actions(rule_id, rule_name, conditions, actions)
        assert result is True

    # TC_SCRUM158_08: Create rule with empty conditions and actions
    @pytest.mark.asyncio
    async def test_create_rule_with_empty_conditions_and_actions(self):
        rule_page = RuleConfigurationPage()
        rule_id = "R_EMPTY_001"
        rule_name = "Rule with Empty Conditions and Actions"
        result_msg = await rule_page.create_rule_with_empty_conditions_and_actions(rule_id, rule_name)
        assert isinstance(result_msg, str)
        assert "valid" in result_msg.lower() or "error" in result_msg.lower()
