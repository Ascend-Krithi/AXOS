import pytest
import asyncio
import time
from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.RuleManagementPage import RuleManagementPage

class TestRuleConfiguration:
    # ... [existing test methods here] ...
    async def test_batch_rule_loading_and_evaluation_performance(self): ...
    async def test_sql_injection_in_rule_submission(self): ...

    async def test_create_and_retrieve_valid_rule_TC_FT_009(self):
        """
        TC-FT-009:
        1. Create and store a valid rule (trigger type 'specific_date', date '2024-07-01T10:00:00Z', action type 'fixed_amount', amount 100, conditions []).
           Expected: Rule is stored in PostgreSQL.
        2. Retrieve the rule from backend.
           Expected: Retrieved rule matches the original input.
        """
        rule_management = RuleManagementPage()
        rule_data = {
            "trigger_type": "specific_date",
            "trigger_date": "2024-07-01T10:00:00Z",
            "action_type": "fixed_amount",
            "amount": 100,
            "conditions": []
        }
        # Step 1: Create and store the rule
        create_result = await rule_management.create_rule(rule_data)
        assert create_result["status"] == "success", f"Rule creation failed: {create_result}"
        rule_id = create_result["rule_id"]
        # Step 2: Retrieve the rule
        retrieve_result = await rule_management.retrieve_rule(rule_id)
        assert retrieve_result["status"] == "success", f"Rule retrieval failed: {retrieve_result}"
        stored_rule = retrieve_result["rule"]
        # Validate stored rule matches input
        assert stored_rule["trigger_type"] == rule_data["trigger_type"]
        assert stored_rule.get("trigger_date") == rule_data["trigger_date"]
        assert stored_rule["action_type"] == rule_data["action_type"]
        assert stored_rule["amount"] == rule_data["amount"]
        assert stored_rule["conditions"] == rule_data["conditions"]

    async def test_define_and_trigger_rule_with_empty_conditions_TC_FT_010(self):
        """
        TC-FT-010:
        1. Define a rule with empty conditions array (trigger type 'after_deposit', action type 'fixed_amount', amount 100, conditions []).
           Expected: Rule is accepted and executes unconditionally when triggered.
        2. Trigger the rule (deposit 1000).
           Expected: Transfer is executed without checking any conditions.
        """
        rule_management = RuleManagementPage()
        rule_data = {
            "trigger_type": "after_deposit",
            "action_type": "fixed_amount",
            "amount": 100,
            "conditions": []
        }
        # Step 1: Define rule with empty conditions
        define_result = await rule_management.define_rule_with_empty_conditions(rule_data)
        assert define_result["status"] == "success", f"Rule definition failed: {define_result}"
        rule_id = define_result["rule_id"]
        # Step 2: Trigger the rule
        trigger_payload = {
            "rule_id": rule_id,
            "deposit_amount": 1000
        }
        trigger_result = await rule_management.trigger_rule(trigger_payload)
        assert trigger_result["status"] == "executed", f"Rule trigger failed or did not execute: {trigger_result}"
        assert trigger_result["transfer_amount"] == 100, f"Transfer amount mismatch: {trigger_result}"
