import unittest
from selenium import webdriver
from PageClasses.RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.page = RuleConfigurationPage(self.driver)
        self.driver.get('https://your-app-url.com/rule-config')

    def tearDown(self):
        self.driver.quit()

    # Existing test methods...

    def test_TC_SCRUM158_03_recurring_interval_trigger_weekly(self):
        ...

    def test_TC_SCRUM158_04_missing_trigger_schema_error(self):
        ...

    def test_TC_FT_005_define_rule_percentage_deposit_and_verify_transfer(self):
        """
        TC-FT-005: Define a rule for 10% of deposit action, simulate deposit of 500 units,
        verify transfer of 50 units executed.
        """
        rule_id = "TC_FT_005"
        self.page.set_after_deposit_trigger()
        self.page.set_rule_action_percentage_of_deposit(10)
        self.page.save_rule()
        self.page.validate_rule_schema()
        self.assertTrue(self.page.verify_rule_storage(rule_id), "Rule was not stored correctly.")
        ui_rule = self.page.retrieve_rule_from_ui(rule_id)
        self.assertIsNotNone(ui_rule, "Rule not found in UI.")
        self.page.simulate_deposit(500)
        success_msg = self.page.get_success_message()
        self.assertIn("transfer of 50 units executed", success_msg, "Transfer not executed as expected.")

    def test_TC_FT_006_currency_conversion_trigger_and_existing_rule_integrity(self):
        """
        TC-FT-006: Define a rule with trigger type 'currency_conversion', action fixed amount 100 EUR,
        verify system accepts or rejects gracefully, and verify existing rules continue to execute as before.
        """
        rule_id = "TC_FT_006"
        self.page.set_currency_conversion_trigger("EUR")
        self.page.set_rule_action_fixed_amount(100)
        self.page.save_rule()
        try:
            self.page.validate_rule_schema()
            accepted = True
        except Exception:
            accepted = False
        if accepted:
            self.assertTrue(self.page.verify_rule_storage(rule_id), "Rule was not stored correctly.")
            ui_rule = self.page.retrieve_rule_from_ui(rule_id)
            self.assertIsNotNone(ui_rule, "Rule not found in UI.")
            success_msg = self.page.get_success_message()
            self.assertIn("Rule saved", success_msg, "Rule not saved successfully.")
        else:
            error_msg = self.page.get_error_message()
            self.assertIn("currency_conversion", error_msg, "System did not reject gracefully.")
        # Verify existing rules still work
        existing_rule_id = "TC_FT_005"
        self.page.simulate_deposit(500)
        success_msg = self.page.get_success_message()
        self.assertIn("transfer of 50 units executed", success_msg, "Existing rule execution failed after currency_conversion rule test.")

    def test_TC_SCRUM158_07_required_fields_schema_rule_creation(self):
        """
        TC_SCRUM158_07: Prepare a schema with only required fields (one trigger, one condition, one action).
        Test Data: {"trigger":{"type":"manual"},"conditions":[{"type":"amount","operator":"==","value":1}],"actions":[{"type":"transfer","account":"G","amount":1}]}
        Acceptance Criteria: Rule is accepted and created.
        """
        schema = {"trigger":{"type":"manual"},"conditions":[{"type":"amount","operator":"==","value":1}],"actions":[{"type":"transfer","account":"G","amount":1}]}
        success_msg = self.page.create_rule_from_schema(schema)
        self.assertIn("success", success_msg.lower())

    def test_TC_SCRUM158_08_large_metadata_field_rule_creation(self):
        """
        TC_SCRUM158_08: Prepare a schema with a large metadata field (e.g., 10,000 characters).
        Acceptance Criteria: Rule is accepted if within limits; performance is acceptable.
        """
        large_metadata = "x" * 10000
        result = self.page.test_large_metadata_field(large_metadata)
        self.assertIn("success", result['success'].lower())
        self.assertLess(result['performance_sec'], 10, "Performance degraded for large metadata.")
