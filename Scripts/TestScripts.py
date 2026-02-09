import unittest
from RuleDefinitionPage import RuleDefinitionPage
from RulePage import RulePage

class TestRuleFeature(unittest.TestCase):

    def setUp(self):
        self.rule_definition_page = RuleDefinitionPage()
        self.rule_page = RulePage()

    # Existing test methods ...

    def test_TC_FT_009_create_and_store_valid_rule_and_verify_backend(self):
        # Step 1: Create and store a valid rule
        trigger = {'type': 'specific_date', 'date': '2024-07-01T10:00:00Z'}
        action = {'type': 'fixed_amount', 'amount': 100}
        conditions = []
        rule_id = self.rule_definition_page.create_and_store_rule(trigger=trigger, action=action, conditions=conditions)
        # Step 2: Retrieve the rule from backend and assert it matches input
        retrieved_rule = self.rule_page.retrieve_rule_from_backend(rule_id)
        self.assertEqual(retrieved_rule['trigger'], trigger, "Trigger does not match")
        self.assertEqual(retrieved_rule['action'], action, "Action does not match")
        self.assertEqual(retrieved_rule['conditions'], conditions, "Conditions do not match")

    def test_TC_FT_010_define_rule_with_empty_conditions_and_verify_unconditional_execution(self):
        # Step 1: Define a rule with empty conditions
        trigger = {'type': 'after_deposit'}
        action = {'type': 'fixed_amount', 'amount': 100}
        rule_id = self.rule_definition_page.define_rule_with_empty_conditions(trigger=trigger, action=action)
        # Step 2: Trigger the rule and verify unconditional execution
        deposit_amount = 1000
        transfer_result = self.rule_page.trigger_rule_and_verify_unconditional_execution(rule_id=rule_id, deposit_amount=deposit_amount)
        self.assertTrue(transfer_result['executed'], "Transfer was not executed unconditionally")
        self.assertEqual(transfer_result['amount_transferred'], 100, "Transferred amount is incorrect")
