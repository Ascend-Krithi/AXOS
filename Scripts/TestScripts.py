import unittest
from RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage
from selenium import webdriver

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

    def test_TC_SCRUM158_03(self):
        """TC_SCRUM158_03: recurring interval rule (weekly), amount >= 1000, transfer to account C with amount 1000"""
        rule_id = 'SCRUM158_03'
        rule_name = 'Recurring Weekly Rule'
        interval_value = 'weekly'
        conditions = [
            {'type': 'amount', 'operator': '>=', 'value': 1000}
        ]
        actions = [
            {'type': 'transfer', 'account': 'C', 'amount': 1000}
        ]
        success, message = self.page.submit_recurring_interval_rule(rule_id, rule_name, interval_value, conditions, actions)
        self.assertTrue(success, f"Rule submission failed: {message}")
        self.assertIn('success', message.lower())

    def test_TC_SCRUM158_04(self):
        """TC_SCRUM158_04: missing trigger field, amount < 50, transfer to account D with amount 50"""
        rule_id = 'SCRUM158_04'
        rule_name = 'Missing Trigger Rule'
        conditions = [
            {'type': 'amount', 'operator': '<', 'value': 50}
        ]
        actions = [
            {'type': 'transfer', 'account': 'D', 'amount': 50}
        ]
        success, message = self.page.submit_rule_missing_trigger(rule_id, rule_name, conditions, actions)
        self.assertFalse(success, f"Rule should not be accepted: {message}")
        self.assertIn('missing', message.lower())

    def test_TC_SCRUM158_05(self):
        """TC_SCRUM158_05: Prepare a schema with unsupported trigger type and verify rejection."""
        driver = self.page.driver
        page = RuleConfigurationPage(driver)
        trigger_type = 'unsupported_type'
        conditions = [["amount", "<", "10"]]
        actions = [["transfer", "E", "10"]]
        page.configure_schema(trigger_type, conditions, actions)
        self.assertTrue(page.is_schema_rejected_due_to_trigger(), "Schema with unsupported trigger type was not rejected as expected.")

    def test_TC_SCRUM158_06(self):
        """TC_SCRUM158_06: Prepare a schema with maximum allowed (10) conditions and actions and verify acceptance."""
        driver = self.page.driver
        page = RuleConfigurationPage(driver)
        trigger_type = 'manual'
        conditions = [["amount", "==", str(i)] for i in range(1, 11)]
        actions = [["transfer", f"F{i}", str(i)] for i in range(1, 11)]
        page.configure_schema(trigger_type, conditions, actions)
        self.assertTrue(page.is_schema_accepted(), "Schema with maximum allowed conditions/actions was not accepted as expected.")

    # --- New test for TC_SCRUM158_07 ---
    def test_TC_SCRUM158_07(self):
        """TC_SCRUM158_07: Prepare a schema with only required fields (manual trigger, one condition, one action)."""
        rule_id = 'SCRUM158_07'
        rule_name = 'Minimal Rule'
        trigger = {'type': 'manual'}
        conditions = [{'type': 'amount', 'operator': '==', 'value': 1}]
        actions = [{'type': 'transfer', 'account': 'G', 'amount': 1}]
        success, message = self.page.submit_rule_schema(rule_id, rule_name, trigger, conditions, actions)
        self.assertTrue(success, f"Rule creation failed: {message}")
        self.assertIn('success', message.lower())

    # --- New test for TC_SCRUM158_08 ---
    def test_TC_SCRUM158_08(self):
        """TC_SCRUM158_08: Prepare a schema with a large metadata field (10,000 characters), manual trigger."""
        rule_id = 'SCRUM158_08'
        rule_name = 'Large Metadata Rule'
        trigger = {'type': 'manual'}
        conditions = []
        actions = []
        large_metadata = 'X' * 10000
        self.page.fill_rule_form(rule_id=rule_id, rule_name=rule_name)
        self.page.select_trigger(trigger)
        self.page.enter_large_metadata(large_metadata)
        self.page.submit_rule()
        self.page.validate_metadata_acceptance(large_metadata)

    # --- New tests for TC03 and TC04 (LoginPage) ---
    def test_TC03_login_empty_credentials(self):
        """TC03: Navigate to login page, submit empty username and password, click login, expect error 'Username and password are required'."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_login('http://example.com/login')
        error_message = login_page.tc03_submit_empty_credentials()
        self.assertEqual(error_message, 'Username and password are required')
        driver.quit()

    def test_TC04_login_empty_username(self):
        """TC04: Navigate to login page, submit empty username and valid password, click login, expect error 'Username is required'."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_login('http://example.com/login')
        error_message = login_page.tc04_submit_empty_username('ValidPass123')
        self.assertEqual(error_message, 'Username is required')
        driver.quit()

if __name__ == "__main__":
    unittest.main()
