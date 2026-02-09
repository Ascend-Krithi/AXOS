
import unittest
from RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.page = RuleConfigurationPage()

    # Existing test methods...

    def test_TC_SCRUM158_01(self):
        """TC_SCRUM158_01: interval trigger (daily), amount > 100, transfer to account A with amount 100"""
        rule_schema = {
            'trigger': {
                'type': 'interval',
                'value': 'daily'
            },
            'conditions': [
                {
                    'type': 'amount',
                    'operator': '>',
                    'value': 100
                }
            ],
            'actions': [
                {
                    'type': 'transfer',
                    'account': 'A',
                    'amount': 100
                }
            ]
        }
        submit_result = self.page.submit_rule_schema(rule_schema)
        self.assertTrue(submit_result['success'], f"Submission failed: {submit_result.get('error')}")
        rule_id = submit_result.get('rule_id')
        self.assertIsNotNone(rule_id, "Rule ID not returned after submission.")
        retrieved_rule = self.page.retrieve_rule(rule_id)
        self.assertEqual(retrieved_rule['trigger']['type'], 'interval')
        self.assertEqual(retrieved_rule['trigger']['value'], 'daily')
        self.assertEqual(len(retrieved_rule['conditions']), 1)
        self.assertEqual(retrieved_rule['conditions'][0]['type'], 'amount')
        self.assertEqual(retrieved_rule['conditions'][0]['operator'], '>')
        self.assertEqual(retrieved_rule['conditions'][0]['value'], 100)
        self.assertEqual(len(retrieved_rule['actions']), 1)
        self.assertEqual(retrieved_rule['actions'][0]['type'], 'transfer')
        self.assertEqual(retrieved_rule['actions'][0]['account'], 'A')
        self.assertEqual(retrieved_rule['actions'][0]['amount'], 100)

    def test_TC_SCRUM158_02(self):
        """TC_SCRUM158_02: manual trigger, amount > 500, country == US, transfer to account B with amount 500, notify with message"""
        rule_schema = {
            'trigger': {
                'type': 'manual'
            },
            'conditions': [
                {
                    'type': 'amount',
                    'operator': '>',
                    'value': 500
                },
                {
                    'type': 'country',
                    'operator': '==',
                    'value': 'US'
                }
            ],
            'actions': [
                {
                    'type': 'transfer',
                    'account': 'B',
                    'amount': 500
                },
                {
                    'type': 'notify',
                    'message': 'Transfer complete'
                }
            ]
        }
        submit_result = self.page.submit_rule_schema(rule_schema)
        self.assertTrue(submit_result['success'], f"Submission failed: {submit_result.get('error')}")
        rule_id = submit_result.get('rule_id')
        self.assertIsNotNone(rule_id, "Rule ID not returned after submission.")
        retrieved_rule = self.page.retrieve_rule(rule_id)
        self.assertEqual(retrieved_rule['trigger']['type'], 'manual')
        self.assertEqual(len(retrieved_rule['conditions']), 2)
        self.assertEqual(retrieved_rule['conditions'][0]['type'], 'amount')
        self.assertEqual(retrieved_rule['conditions'][0]['operator'], '>')
        self.assertEqual(retrieved_rule['conditions'][0]['value'], 500)
        self.assertEqual(retrieved_rule['conditions'][1]['type'], 'country')
        self.assertEqual(retrieved_rule['conditions'][1]['operator'], '==')
        self.assertEqual(retrieved_rule['conditions'][1]['value'], 'US')
        self.assertEqual(len(retrieved_rule['actions']), 2)
        self.assertEqual(retrieved_rule['actions'][0]['type'], 'transfer')
        self.assertEqual(retrieved_rule['actions'][0]['account'], 'B')
        self.assertEqual(retrieved_rule['actions'][0]['amount'], 500)
        self.assertEqual(retrieved_rule['actions'][1]['type'], 'notify')
        self.assertEqual(retrieved_rule['actions'][1]['message'], 'Transfer complete')

if __name__ == "__main__":
    unittest.main()