import unittest
from selenium import webdriver
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.rule_page = RuleConfigurationPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Existing test methods...

    def test_TC_FT_007_load_bulk_rules_and_measure_performance(self):
        """TC-FT-007: Test loading 10,000 valid rules and measure performance."""
        result = self.rule_page.load_bulk_rules_and_evaluate_performance(num_rules=10000)
        self.assertTrue(result['success'], f"Bulk rule load failed: {result.get('error')}")
        self.assertLessEqual(result['duration'], 300, f"Bulk load took too long: {result['duration']}s")
        self.assertEqual(result['loaded_count'], 10000, "Not all rules were loaded.")

    def test_TC_FT_008_submit_rule_with_sql_injection_and_validate_rejection(self):
        """TC-FT-008: Submit a rule with SQL injection in a field and validate rejection."""
        injection_payload = "'; DROP TABLE rules;--"
        result = self.rule_page.submit_rule_with_sql_injection_and_validate_rejection(injection_payload)
        self.assertFalse(result['accepted'], "Rule with SQL injection should not be accepted.")
        self.assertIn("SQL injection", result['rejection_reason'], "Rejection reason should reference SQL injection.")

if __name__ == "__main__":
    unittest.main()
