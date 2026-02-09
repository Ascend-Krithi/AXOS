import unittest
from selenium import webdriver
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.page = RuleConfigurationPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Existing test methods...

    def test_minimum_required_fields(self):
        """
        Test creating a rule schema with only the minimum required fields and assert success.
        """
        self.page.open_rule_configuration()
        min_schema = self.page.prepare_minimum_required_schema()
        self.page.fill_rule_form(min_schema)
        self.page.submit_rule()
        success = self.page.validate_rule_creation(min_schema)
        self.assertTrue(success, "Rule creation with minimum required fields failed.")

    def test_unsupported_trigger_type(self):
        """
        Test creating a rule schema with an unsupported trigger type and assert the proper error/response.
        """
        self.page.open_rule_configuration()
        unsupported_schema = self.page.prepare_schema_with_unsupported_trigger()
        self.page.fill_rule_form(unsupported_schema)
        self.page.submit_rule()
        error = self.page.get_trigger_type_error()
        self.assertIsNotNone(error, "No error displayed for unsupported trigger type.")
        self.assertIn("unsupported trigger", error.lower(), "Error message does not indicate unsupported trigger type.")
