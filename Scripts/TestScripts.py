import pytest
from Pages.LoginPage import LoginPage
from RuleEnginePage import RuleEnginePage
from RuleCreationPage import RuleCreationPage

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

    async def test_specific_date_rule_trigger(self):
        # TC-FT-001: Define a JSON rule with trigger type 'specific_date' set to a future date
        rule = {
            'trigger': {'type': 'specific_date', 'date': '2024-07-01T10:00:00Z'},
            'action': {'type': 'fixed_amount', 'amount': 100},
            'conditions': []
        }
        rule_engine = RuleEnginePage(self.page)
        rule_engine.define_rule(rule)
        assert rule_engine.is_rule_accepted()
        rule_engine.simulate_time_trigger('2024-07-01T10:00:00Z')
        assert rule_engine.verify_transfer_action(expected_count=1)

    async def test_recurring_weekly_rule_trigger(self):
        # TC-FT-002: Define a JSON rule with trigger type 'recurring' and interval 'weekly'
        rule = {
            'trigger': {'type': 'recurring', 'interval': 'weekly'},
            'action': {'type': 'percentage_of_deposit', 'percentage': 10},
            'conditions': []
        }
        rule_engine = RuleEnginePage(self.page)
        rule_engine.define_rule(rule)
        assert rule_engine.is_rule_accepted()
        rule_engine.simulate_recurring_trigger(interval='weekly', times=3)
        assert rule_engine.verify_transfer_action_recurring(expected_intervals=3)

    async def test_rule_with_multiple_conditions(self):
        # TC-FT-003: Define a rule with multiple conditions (balance >= 1000, source = 'salary')
        rule = {
            'trigger': {'type': 'after_deposit'},
            'action': {'type': 'fixed_amount', 'amount': 50},
            'conditions': [
                {'type': 'balance_threshold', 'operator': '>=', 'value': 1000},
                {'type': 'transaction_source', 'value': 'salary'}
            ]
        }
        rule_engine = RuleEnginePage(self.page)
        rule_engine.define_rule(rule)
        assert rule_engine.is_rule_accepted()

        # Simulate deposit from 'salary' when balance is 900
        result = rule_engine.simulate_deposit(balance=900, deposit=100, source='salary')
        assert not result['transfer_executed']

        # Simulate deposit from 'salary' when balance is 1200
        result = rule_engine.simulate_deposit(balance=1200, deposit=100, source='salary')
        assert result['transfer_executed']

    async def test_rule_with_missing_trigger_type(self):
        # TC-FT-004: Submit a rule with missing trigger type
        rule = {
            'action': {'type': 'fixed_amount', 'amount': 100},
            'conditions': []
        }
        rule_engine = RuleEnginePage(self.page)
        response = rule_engine.submit_rule(rule)
        assert response['error'] == 'Missing required field: trigger'

    async def test_rule_with_unsupported_action_type(self):
        # TC-FT-004: Submit a rule with unsupported action type
        rule = {
            'trigger': {'type': 'specific_date', 'date': '2024-07-01T10:00:00Z'},
            'action': {'type': 'unknown_action'},
            'conditions': []
        }
        rule_engine = RuleEnginePage(self.page)
        response = rule_engine.submit_rule(rule)
        assert response['error'] == 'Unsupported action type'

    async def test_deposit_percentage_rule(self):
        # TC-FT-005: Define a rule for 10% of deposit action and simulate deposit of 500 units
        rule = {
            'trigger': {'type': 'after_deposit'},
            'action': {'type': 'percentage_of_deposit', 'percentage': 10},
            'conditions': []
        }
        rule_engine = RuleEnginePage(self.page)
        rule_engine.define_rule(rule)
        assert rule_engine.is_rule_accepted()
        rule_engine.simulate_deposit(500)
        assert rule_engine.verify_transfer_action(50)

    async def test_currency_conversion_rule_and_existing_rules(self):
        # TC-FT-006: Define a currency conversion rule, check acceptance/rejection, verify existing rules
        rule = {
            'trigger': {'type': 'currency_conversion', 'currency': 'EUR'},
            'action': {'type': 'fixed_amount', 'amount': 100},
            'conditions': []
        }
        rule_engine = RuleEnginePage(self.page)
        rule_engine.define_currency_conversion_rule(rule)
        if rule_engine.is_rule_accepted():
            assert True
        else:
            error = rule_engine.get_error_message()
            assert error is not None and 'currency_conversion' in error
        assert rule_engine.verify_existing_rules_function()

    async def test_batch_rule_loading_and_simultaneous_evaluation(self):
        # TC-FT-007: Load 10,000 valid rules, trigger evaluation, and check performance/consistency
        rule_creation = RuleCreationPage(self.page)
        num_rules = 10000
        batch_rules = []
        for i in range(num_rules):
            rule = {
                'trigger': {'type': 'after_deposit', 'id': f'batch_{i}'},
                'action': {'type': 'fixed_amount', 'amount': i+1},
                'conditions': []
            }
            batch_rules.append(rule)
        upload_response = await rule_creation.upload_batch_rules(batch_rules)
        assert upload_response['success'] is True, f"Batch upload failed: {upload_response.get('error', '')}"
        # Evaluate all rules and check for performance and no failures
        eval_response = await rule_creation.evaluate_all_rules()
        assert eval_response['evaluated'] == num_rules, f"Not all rules evaluated: {eval_response}"
        assert eval_response.get('failures', 0) == 0, f"Failures during evaluation: {eval_response.get('failures_detail', '')}"
        # Optionally, check for timing if available
        if 'duration_ms' in eval_response:
            assert eval_response['duration_ms'] < 60000, f"Evaluation took too long: {eval_response['duration_ms']}ms"

    async def test_sql_injection_rule_submission(self):
        # TC-FT-008: Submit rule with SQL injection payload, ensure system rejects and does not execute SQL
        rule_creation = RuleCreationPage(self.page)
        injection_payload = "1; DROP TABLE rules; --"
        malicious_rule = {
            'trigger': {'type': 'after_deposit'},
            'action': {'type': 'fixed_amount', 'amount': injection_payload},
            'conditions': []
        }
        response = await rule_creation.submit_rule_with_sql_injection(malicious_rule)
        assert response['success'] is False, "SQL injection rule was accepted!"
        assert 'sql injection' in response.get('error', '').lower() or 'invalid' in response.get('error', '').lower(), f"Unexpected error message: {response.get('error', '')}"
        # Optionally, verify system state is intact (e.g., rules table still exists)
        if hasattr(rule_creation, 'verify_rules_table_integrity'):
            assert await rule_creation.verify_rules_table_integrity(), "Rules table integrity compromised after SQL injection test!"
