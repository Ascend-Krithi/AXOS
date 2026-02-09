# Import necessary modules
from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.login_page.enter_email("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        assert self.login_page.get_error_message().strip() == "Email/Username required"

    def test_remember_me_functionality(self):
        # Placeholder for remember me test
        pass

class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_invalid_trigger(self):
        error_message = self.rule_page.validate_invalid_trigger()
        assert "invalid" in error_message.lower()

    def test_missing_condition_parameter(self):
        error_message = self.rule_page.validate_missing_condition_parameter()
        assert "missing" in error_message.lower() or "incomplete" in error_message.lower()

    def test_create_rule_with_max_conditions_actions(self):
        """
        TC_SCRUM158_07 - Prepare a rule schema with 10 conditions/actions, submit, retrieve, and validate persistence.
        """
        # Create rule with maximum conditions and actions
        rule_id = self.rule_page.create_rule_with_max_conditions_actions(num_conditions=10, num_actions=10)
        # Retrieve rule and validate persistence
        persisted_rule = self.rule_page.get_rule_by_id(rule_id)
        assert persisted_rule is not None, "Rule was not persisted"
        assert len(persisted_rule['conditions']) == 10, "Not all conditions persisted"
        assert len(persisted_rule['actions']) == 10, "Not all actions persisted"
        assert persisted_rule['id'] == rule_id, "Rule ID mismatch"

    def test_create_rule_with_empty_conditions_actions(self):
        """
        TC_SCRUM158_08 - Prepare a rule schema with empty conditions/actions arrays, submit, and validate schema as per business rule.
        """
        # Create rule with empty conditions and actions
        rule_id, validation_result = self.rule_page.create_rule_with_empty_conditions_actions()
        # Validate schema according to business rule (e.g., must be allowed, or must fail with specific error)
        assert validation_result['is_valid'], f"Rule schema not valid: {validation_result['error']}"
        # Optionally check rule is persisted if business rule allows
        if validation_result['is_valid']:
            persisted_rule = self.rule_page.get_rule_by_id(rule_id)
            assert persisted_rule is not None, "Rule with empty conditions/actions was not persisted"
            assert persisted_rule['conditions'] == [], "Conditions array is not empty"
            assert persisted_rule['actions'] == [], "Actions array is not empty"
