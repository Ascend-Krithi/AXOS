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

    def test_define_rule_with_multiple_conditions(self):
        """
        TC-FT-003: Define a rule with multiple conditions (balance >= 1000, source = 'salary'), simulate deposits, and validate transfer execution.
        """
        trigger = {"type": "after_deposit"}
        action = {"type": "fixed_amount", "amount": 50}
        conditions = [
            {"type": "balance_threshold", "operator": ">=", "value": 1000},
            {"type": "transaction_source", "value": "salary"}
        ]
        # Step 1: Define rule
        self.rule_page.create_rule_with_conditions(trigger, action, conditions)
        # Step 2: Simulate deposit with balance 900, source 'salary'
        self.rule_page.simulate_deposit(balance=900, deposit=100, source="salary")
        self.rule_page.validate_transfer_execution(expected=False)
        # Step 3: Simulate deposit with balance 1200, source 'salary'
        self.rule_page.simulate_deposit(balance=1200, deposit=100, source="salary")
        self.rule_page.validate_transfer_execution(expected=True)

    def test_submit_rule_with_missing_trigger_and_unsupported_action(self):
        """
        TC-FT-004: Submit a rule with missing trigger type and unsupported action type, validate error messages.
        """
        # Step 1: Missing trigger type
        action_missing_trigger = {"type": "fixed_amount", "amount": 100}
        conditions_missing_trigger = []
        self.rule_page.submit_rule_missing_trigger(action_missing_trigger, conditions_missing_trigger)
        self.rule_page.validate_error_message("Missing required field: trigger type")
        # Step 2: Unsupported action type
        trigger_unsupported_action = {"type": "specific_date", "date": "2024-07-01T10:00:00Z"}
        action_unsupported = {"type": "unknown_action"}
        conditions_unsupported = []
        self.rule_page.submit_rule_unsupported_action(trigger_unsupported_action, action_unsupported, conditions_unsupported)
        self.rule_page.validate_error_message("Unsupported action type")
