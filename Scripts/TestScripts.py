# Existing imports
from Pages.RuleConfigurationPage import RuleConfigurationPage
from selenium.webdriver.remote.webdriver import WebDriver

# Existing test class
class TestLoginFunctionality:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('')

# New tests for Rule Configuration Page
class TestRuleConfiguration:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_define_specific_date_rule_and_execute(self):
        """
        TC-FT-001: Define JSON rule with 'specific_date' trigger, validate acceptance, simulate trigger, validate execution.
        """
        rule_id = "TC-FT-001"
        rule_name = "Specific Date Transfer Rule"
        date_str = "2024-07-01T10:00:00Z"
        amount = 100
        # Create rule
        result = self.rule_page.create_specific_date_rule(rule_id, rule_name, date_str, amount)
        assert result, "Rule was not accepted by the system."
        # Simulate system time reaching trigger date
        self.rule_page.simulate_time_reaching_trigger()
        # Validate transfer action
        assert self.rule_page.validate_transfer_action(), "Transfer action was not executed at the specified date."

    def test_define_recurring_rule_and_execute(self):
        """
        TC-FT-002: Define JSON rule with 'recurring' trigger, validate acceptance, simulate trigger, validate execution.
        """
        rule_id = "TC-FT-002"
        rule_name = "Weekly Recurring Transfer Rule"
        interval = "weekly"
        percentage = 10
        # Create rule
        result = self.rule_page.create_recurring_rule(rule_id, rule_name, interval, percentage)
        assert result, "Rule was not accepted by the system."
        # Simulate passing of several weeks
        self.rule_page.simulate_time_reaching_trigger()
        # Validate transfer action
        assert self.rule_page.validate_transfer_action(), "Transfer action was not executed at each interval."
