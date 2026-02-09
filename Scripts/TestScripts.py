# Existing imports
from selenium import webdriver
import unittest
from PageClasses.RulePage import RulePage
from PageClasses.DepositPage import DepositPage

class TestScripts(unittest.TestCase):
    # Existing test methods ...

    # TC-FT-009: Create/store a rule, retrieve it, and verify it matches input
    def test_TC_FT_009_create_store_retrieve_verify_rule(self):
        driver = webdriver.Chrome()
        rule_page = RulePage(driver)
        # Input data for the rule
        rule_data = {
            'name': 'TestRule009',
            'condition': 'amount > 1000',
            'action': 'transfer',
            'value': '2000'
        }
        # Step 1: Create and store the rule
        rule_page.create_rule(rule_data)
        rule_page.store_rule(rule_data)
        # Step 2: Retrieve the rule
        retrieved_rule = rule_page.retrieve_rule(rule_data['name'])
        # Step 3: Verify it matches input
        self.assertEqual(retrieved_rule['name'], rule_data['name'], "Rule name mismatch")
        self.assertEqual(retrieved_rule['condition'], rule_data['condition'], "Rule condition mismatch")
        self.assertEqual(retrieved_rule['action'], rule_data['action'], "Rule action mismatch")
        self.assertEqual(retrieved_rule['value'], rule_data['value'], "Rule value mismatch")
        driver.quit()

    # TC-FT-010: Define rule with empty conditions, trigger it, and verify unconditional execution
    def test_TC_FT_010_unconditional_rule_execution(self):
        driver = webdriver.Chrome()
        rule_page = RulePage(driver)
        deposit_page = DepositPage(driver)
        # Step 1: Define rule with empty conditions
        rule_data = {
            'name': 'UnconditionalRule010',
            'condition': '',  # Empty condition
            'action': 'transfer',
            'value': '1000'
        }
        rule_page.create_rule(rule_data)
        rule_page.store_rule(rule_data)
        # Step 2: Trigger the rule (simulate deposit)
        deposit_page.simulate_deposit(amount=1000)
        # Step 3: Verify unconditional execution
        executed = rule_page.verify_unconditional_execution(rule_data['name'])
        self.assertTrue(executed, "Unconditional rule did not execute as expected.")
        driver.quit()
