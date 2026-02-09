# Existing imports
import unittest
from selenium import webdriver
from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.ProfilePage import ProfilePage
from Pages.SettingsPage import SettingsPage

# Existing test classes and methods
class TestRuleConfiguration(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.rule_page = RuleConfigurationPage(self.driver)
    def tearDown(self):
        self.driver.quit()
    # ... existing methods ...

class TestProfile(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.profile_page = ProfilePage(self.driver)
    def tearDown(self):
        self.driver.quit()
    # ... existing methods ...

class TestSettings(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.settings_page = SettingsPage(self.driver)
    def tearDown(self):
        self.driver.quit()
    # ... existing methods ...

# --- NEW TEST METHODS ---

class TestMetadataSchema(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.rule_page = RuleConfigurationPage(self.driver)
    def tearDown(self):
        self.driver.quit()

    def test_TC_SCRUM158_03_create_and_validate_metadata_schema(self):
        """
        TC_SCRUM158_03: Metadata schema creation and validation
        Steps:
        1. Navigate to Rule Configuration page
        2. Click 'Create New Metadata Schema'
        3. Fill out schema name, description, and fields
        4. Save schema
        5. Validate schema appears in list and fields are correct
        """
        self.rule_page.navigate_to()
        self.rule_page.click_create_metadata_schema()
        schema_name = "TestSchema"
        schema_description = "Schema for automated test"
        fields = [
            {"name": "Field1", "type": "String", "required": True},
            {"name": "Field2", "type": "Number", "required": False}
        ]
        self.rule_page.fill_metadata_schema_form(schema_name, schema_description, fields)
        self.rule_page.save_metadata_schema()
        self.assertTrue(self.rule_page.is_metadata_schema_listed(schema_name))
        self.assertTrue(self.rule_page.verify_metadata_schema_fields(schema_name, fields))

    def test_TC_SCRUM158_04_missing_trigger_field_validation(self):
        """
        TC_SCRUM158_04: Missing trigger field validation
        Steps:
        1. Navigate to Rule Configuration page
        2. Click 'Create New Rule'
        3. Fill rule details WITHOUT trigger field
        4. Attempt to save
        5. Validate error message for missing trigger field
        """
        self.rule_page.navigate_to()
        self.rule_page.click_create_rule()
        rule_name = "TestRuleWithoutTrigger"
        rule_details = {
            "name": rule_name,
            "description": "Rule missing trigger field",
            # intentionally omitting 'trigger' field
        }
        self.rule_page.fill_rule_form(rule_details)
        self.rule_page.save_rule()
        self.assertTrue(self.rule_page.is_trigger_field_error_displayed())

if __name__ == "__main__":
    unittest.main()
