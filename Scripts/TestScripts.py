import unittest
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.rule_page = RuleConfigurationPage()

    def test_create_rule_with_daily_interval_and_amount_condition(self):
        # Existing test for rule creation with daily interval and amount > 100 condition
        schema = self.rule_page.prepare_valid_rule_schema(
            trigger_type='daily',
            conditions=[{'type': 'amount', 'operator': '>', 'value': 100}],
            actions=[{'type': 'transfer', 'to': 'account_2'}]
        )
        response = self.rule_page.submit_schema_to_rule_service(schema)
        self.assertTrue(response['success'])
        self.assertEqual(response['data']['trigger'], 'daily')
        self.assertEqual(response['data']['conditions'][0]['type'], 'amount')
        self.assertEqual(response['data']['actions'][0]['type'], 'transfer')

    def test_retrieve_rule_by_id(self):
        # Existing test for rule retrieval by ID
        schema = self.rule_page.prepare_valid_rule_schema(
            trigger_type='daily',
            conditions=[{'type': 'amount', 'operator': '>', 'value': 100}],
            actions=[{'type': 'transfer', 'to': 'account_2'}]
        )
        create_response = self.rule_page.submit_schema_to_rule_service(schema)
        rule_id = create_response['data']['id']
        retrieved_rule = self.rule_page.get_rule_by_id(rule_id)
        self.assertEqual(retrieved_rule['id'], rule_id)
        self.assertEqual(retrieved_rule['trigger'], 'daily')

    # TC_SCRUM158_01: Prepare and submit a valid rule schema with daily interval trigger, amount > 100 condition, and transfer action
    def test_TC_SCRUM158_01_prepare_and_submit_daily_interval_rule(self):
        schema = self.rule_page.prepare_valid_rule_schema(
            trigger_type='daily',
            conditions=[{'type': 'amount', 'operator': '>', 'value': 100}],
            actions=[{'type': 'transfer', 'to': 'account_2'}]
        )
        response = self.rule_page.submit_schema_to_rule_service(schema)
        self.assertTrue(response['success'], "Rule submission should succeed")
        self.assertEqual(response['data']['trigger'], 'daily', "Trigger should be daily")
        self.assertEqual(response['data']['conditions'][0]['type'], 'amount', "Condition type should be amount")
        self.assertEqual(response['data']['conditions'][0]['operator'], '>', "Condition operator should be >")
        self.assertEqual(response['data']['conditions'][0]['value'], 100, "Condition value should be 100")
        self.assertEqual(response['data']['actions'][0]['type'], 'transfer', "Action type should be transfer")
        self.assertEqual(response['data']['actions'][0]['to'], 'account_2', "Action target should be account_2")

    # TC_SCRUM158_02: Prepare and submit schema with manual trigger, two conditions, and two actions
    def test_TC_SCRUM158_02_prepare_and_submit_manual_trigger_rule_multiple_conditions_actions(self):
        schema = self.rule_page.prepare_valid_rule_schema(
            trigger_type='manual',
            conditions=[
                {'type': 'amount', 'operator': '>=', 'value': 500},
                {'type': 'currency', 'operator': '==', 'value': 'USD'}
            ],
            actions=[
                {'type': 'notify', 'message': 'High value transfer'},
                {'type': 'transfer', 'to': 'account_3'}
            ]
        )
        response = self.rule_page.submit_schema_to_rule_service(schema)
        self.assertTrue(response['success'], "Rule submission should succeed")
        self.assertEqual(response['data']['trigger'], 'manual', "Trigger should be manual")
        self.assertEqual(len(response['data']['conditions']), 2, "Should have two conditions")
        self.assertEqual(response['data']['conditions'][0]['type'], 'amount', "First condition type should be amount")
        self.assertEqual(response['data']['conditions'][0]['operator'], '>=', "First condition operator should be >=")
        self.assertEqual(response['data']['conditions'][0]['value'], 500, "First condition value should be 500")
        self.assertEqual(response['data']['conditions'][1]['type'], 'currency', "Second condition type should be currency")
        self.assertEqual(response['data']['conditions'][1]['operator'], '==', "Second condition operator should be ==")
        self.assertEqual(response['data']['conditions'][1]['value'], 'USD', "Second condition value should be USD")
        self.assertEqual(len(response['data']['actions']), 2, "Should have two actions")
        self.assertEqual(response['data']['actions'][0]['type'], 'notify', "First action type should be notify")
        self.assertEqual(response['data']['actions'][0]['message'], 'High value transfer', "First action message should be 'High value transfer'")
        self.assertEqual(response['data']['actions'][1]['type'], 'transfer', "Second action type should be transfer")
        self.assertEqual(response['data']['actions'][1]['to'], 'account_3', "Second action target should be account_3")

if __name__ == '__main__':
    unittest.main()
