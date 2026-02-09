# Existing imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from Pages.RulePage import RulePage
from Pages.DepositPage import DepositPage

class TestScripts:
    def test_rule_creation_valid(self, driver):
        rule_page = RulePage(driver)
        rule_page.navigate()
        rule_page.define_rule('Minimum Deposit', 'amount > 100')
        assert rule_page.is_rule_defined('Minimum Deposit')

    def test_deposit_simulation(self, driver):
        deposit_page = DepositPage(driver)
        deposit_page.navigate()
        deposit_page.simulate_deposit(account_id='ACC123', amount=150)
        assert deposit_page.is_transfer_executed(account_id='ACC123')

    # TC-FT-003: Define rule with multiple conditions, simulate deposit, validate transfer execution
    def test_rule_with_multiple_conditions_deposit(self, driver):
        rule_page = RulePage(driver)
        rule_page.navigate()
        # Define a rule with multiple conditions
        rule_conditions = [
            {'field': 'amount', 'operator': '>', 'value': 100},
            {'field': 'currency', 'operator': '==', 'value': 'USD'}
        ]
        rule_page.define_rule('USD High Deposit', rule_conditions)
        assert rule_page.is_rule_defined('USD High Deposit')

        deposit_page = DepositPage(driver)
        deposit_page.navigate()
        # Simulate deposit that meets all conditions
        deposit_page.simulate_deposit(account_id='ACC456', amount=200, currency='USD')
        assert deposit_page.is_transfer_executed(account_id='ACC456')

    # TC-FT-004: Error handling for missing/unsupported fields during rule definition
    def test_rule_definition_error_handling(self, driver):
        rule_page = RulePage(driver)
        rule_page.navigate()
        # Attempt to define a rule with a missing field
        invalid_conditions = [
            {'field': '', 'operator': '>', 'value': 50},
            {'field': 'unsupported_field', 'operator': '==', 'value': 'XYZ'}
        ]
        rule_page.define_rule('Invalid Rule', invalid_conditions)
        error_messages = rule_page.get_error_messages()
        assert 'Field is required' in error_messages
        assert 'unsupported_field is not supported' in error_messages

    # TC-FT-007: Performance test for bulk rule loading and evaluation
    def test_bulk_rule_loading_and_evaluation_performance(self, driver):
        '''
        Loads 10,000 valid rules and triggers evaluation for all rules simultaneously.
        Verifies system meets defined performance thresholds.
        '''
        import random
        rule_page = RulePage(driver)
        # Generate 10,000 valid rules
        rules_batch = []
        for i in range(10000):
            rule = {
                'trigger_type': f'automated_trigger_{i}',
                'action_type': 'fixed_amount',
                'amount': random.randint(1, 10000),
                'conditions': [
                    {'type': 'balance_threshold', 'value': random.randint(100, 10000)},
                    {'type': 'transaction_source', 'value': f'source_{i}'}
                ]
            }
            rules_batch.append(rule)
        perf_result = rule_page.load_bulk_rules_and_evaluate(rules_batch)
        assert perf_result['load_time'] <= 60, f"Load time too high: {perf_result['load_time']}s"
        assert perf_result['evaluation_time'] <= 180, f"Evaluation time too high: {perf_result['evaluation_time']}s"
        assert perf_result['performance_ok'] is True, "Performance criteria not met"

    # TC-FT-008: SQL injection rejection test
    def test_rule_sql_injection_rejection(self, driver):
        '''
        Submits a rule with SQL injection in a condition value and verifies system rejection.
        '''
        rule_page = RulePage(driver)
        sql_injection_rule = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": [{"type": "balance_threshold", "value": "1000; DROP TABLE users;--"}]
        }
        result = rule_page.submit_rule_with_sql_injection(sql_injection_rule)
        assert result['rejected'] is True, "System did not reject SQL injection rule"
        assert any(word in result['error_message'].lower() for word in ['sql', 'invalid', 'rejected']), f"Unexpected error message: {result['error_message']}"

    # TC-FT-009: Rule creation and storage in PostgreSQL, retrieval from backend
    def test_rule_creation_and_retrieval_postgresql(self, driver):
        '''
        Test Case 1061 / TC-FT-009
        1. Store a valid rule in PostgreSQL via the UI.
        2. Retrieve the rule from the backend via the UI and verify it matches the input.
        '''
        rule_page = RulePage(driver)
        rule_data = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        submission_result = rule_page.store_rule_in_postgresql(rule_data)
        assert "success" in submission_result.lower() or "stored" in submission_result.lower(), f"Unexpected submission result: {submission_result}"
        # Assuming the rule_id can be returned or is fixed for test
        rule_id = "1061"  # Or obtain from the UI if available
        retrieved_rule = rule_page.retrieve_rule_from_backend(rule_id)
        # If backend returns a dict, compare fields
        for key in rule_data:
            assert key in retrieved_rule, f"Missing key {key} in retrieved rule"
            assert rule_data[key] == retrieved_rule[key], f"Mismatch for key {key}: {rule_data[key]} != {retrieved_rule[key]}"

    # TC-FT-010: Rule definition with empty conditions and unconditional execution
    def test_rule_unconditional_execution(self, driver):
        '''
        Test Case 1062 / TC-FT-010
        1. Define a rule with empty conditions (unconditional).
        2. Simulate a triggering event and assert that the transfer is executed without checking conditions.
        '''
        rule_page = RulePage(driver)
        rule_data = {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        submission_result = rule_page.store_rule_in_postgresql(rule_data)
        assert "success" in submission_result.lower() or "stored" in submission_result.lower(), f"Unexpected submission result: {submission_result}"
        # Simulate deposit to trigger rule
        deposit_page = DepositPage(driver)
        deposit_page.simulate_deposit(balance=1000, deposit=1000, source="test_source")
        # Check transfer status
        transfer_status = deposit_page.get_transfer_status()
        assert "executed" in transfer_status.lower() or "success" in transfer_status.lower(), f"Transfer not executed unconditionally: {transfer_status}"
