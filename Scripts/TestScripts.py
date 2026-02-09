import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('')

class TestRuleCreationAndScheduling:
    def __init__(self, driver):
        self.driver = driver
        self.rule_creation_page = RuleCreationPage(driver)
        self.rule_scheduling_page = RuleSchedulingPage(driver)

    def test_specific_date_rule(self):
        # TC-FT-001: Specific Date Rule
        rule_data = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        self.rule_creation_page.open_rule_creation()
        self.rule_creation_page.enter_rule_json(rule_data)
        self.rule_creation_page.submit_rule()
        assert self.rule_creation_page.verify_rule_accepted() is True, "Rule was not accepted by the system."
        self.rule_scheduling_page.simulate_time()
        assert self.rule_scheduling_page.verify_transfer_executed() is True, "Transfer action was not executed at the specified date."

    def test_recurring_weekly_rule(self):
        # TC-FT-002: Recurring Weekly Rule
        rule_data = {
            "trigger": {"type": "recurring", "interval": "weekly"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        self.rule_creation_page.open_rule_creation()
        self.rule_creation_page.enter_rule_json(rule_data)
        self.rule_creation_page.submit_rule()
        assert self.rule_creation_page.verify_rule_accepted() is True, "Rule was not accepted by the system."
        for _ in range(3):  # Simulate three weeks
            self.rule_scheduling_page.simulate_time()
            assert self.rule_scheduling_page.verify_transfer_executed() is True, "Transfer action was not executed at the interval."
        history = self.rule_scheduling_page.get_transfer_history()
        assert history.count('Transfer executed') >= 3, "Transfer action was not executed at the start of each interval."

# TC-FT-003: Define rule with multiple conditions (balance >= 1000, source = 'salary'), simulate deposits, verify transfer
class TestMultipleConditionsRule:
    def __init__(self, page):
        self.profile_page = ProfilePage(page)

    async def test_define_rule_and_simulate_deposit(self):
        # Define rule with multiple conditions
        await self.profile_page.define_rule(
            trigger_type='after_deposit',
            action_type='fixed_amount',
            amount=50,
            conditions=[
                {"type": "balance_threshold", "operator": ">=", "value": 1000},
                {"type": "transaction_source", "value": "salary"}
            ]
        )
        # Simulate deposit with balance 900, deposit 100, source 'salary'
        await self.profile_page.simulate_deposit(balance=900, deposit=100, source='salary')
        await self.profile_page.verify_transfer_execution(expected_result=False)
        # Simulate deposit with balance 1200, deposit 100, source 'salary'
        await self.profile_page.simulate_deposit(balance=1200, deposit=100, source='salary')
        await self.profile_page.verify_transfer_execution(expected_result=True)

# TC-FT-004: Submit rule with missing trigger and unsupported action, verify error
class TestRuleSubmissionErrors:
    def __init__(self, page):
        self.settings_page = SettingsPage(page)

    async def test_missing_trigger_type(self):
        # Submit a rule with missing trigger type
        rule_data = {
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        await self.settings_page.submit_rule(rule_data)
        await self.settings_page.verify_error_message("missing required field")

    async def test_unsupported_action_type(self):
        # Submit a rule with unsupported action type
        rule_data = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "unknown_action"},
            "conditions": []
        }
        await self.settings_page.submit_rule(rule_data)
        await self.settings_page.verify_error_message("unsupported action type")

# TC-FT-009: Backend API rule creation and retrieval
import requests
import logging

class TestRuleApiManagement:
    def __init__(self, base_url, auth_token=None):
        from RuleApiPage import RuleApiPage
        self.api = RuleApiPage(base_url, auth_token)

    def test_create_and_retrieve_rule(self):
        """
        TC-FT-009: Create and store a valid rule, then retrieve and verify it matches the original input.
        """
        rule_data = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        logging.info("Creating rule via API...")
        create_resp = self.api.create_rule(rule_data)
        assert create_resp.status_code == 201, f"Rule creation failed: {create_resp.text}"
        rule_id = create_resp.json().get("id")
        assert rule_id, "Rule ID not returned in creation response."
        logging.info(f"Retrieving rule with ID: {rule_id}")
        retrieve_resp = self.api.retrieve_rule(rule_id)
        assert retrieve_resp.status_code == 200, f"Failed to retrieve rule: {retrieve_resp.text}"
        retrieved_rule = retrieve_resp.json()
        # Remove fields like id, created_at, updated_at if present for comparison
        for k in ["id", "created_at", "updated_at"]:
            retrieved_rule.pop(k, None)
        assert retrieved_rule == rule_data, f"Retrieved rule does not match input. Got: {retrieved_rule}"
        logging.info("TC-FT-009 passed.")

    def test_rule_with_empty_conditions_and_trigger(self):
        """
        TC-FT-010: Define a rule with empty conditions, trigger it, and verify unconditional execution.
        """
        rule_data = {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        logging.info("Creating unconditional rule via API...")
        create_resp = self.api.create_rule(rule_data)
        assert create_resp.status_code == 201, f"Rule creation failed: {create_resp.text}"
        rule_id = create_resp.json().get("id")
        assert rule_id, "Rule ID not returned in creation response."
        trigger_data = {"deposit": 1000, "rule_id": rule_id}
        logging.info(f"Triggering rule with ID: {rule_id}")
        trigger_resp = self.api.trigger_rule(trigger_data)
        assert trigger_resp.status_code == 200, f"Failed to trigger rule: {trigger_resp.text}"
        # Optionally, check response for unconditional execution
        result = trigger_resp.json().get("executed")
        assert result is True, f"Rule did not execute unconditionally. Response: {trigger_resp.text}"
        logging.info("TC-FT-010 passed.")
