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
