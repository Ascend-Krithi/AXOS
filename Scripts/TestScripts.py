# Import necessary modules
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
import time

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

# --- New Test Methods for Rule Configuration ---
class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_specific_date_rule_transfer(self):
        """
        TC-FT-001: Define a JSON rule with 'specific_date' trigger, validate acceptance, simulate system time, and validate transfer action.
        """
        rule_id = "TCFT001"
        rule_name = "SpecificDateRule"
        date_iso = "2024-07-01T10:00:00Z"
        amount = 100
        self.rule_page.define_json_rule_specific_date(rule_id, rule_name, date_iso, amount)
        assert self.rule_page.validate_rule_accepted(), "Rule was not accepted by the system"
        self.rule_page.simulate_system_time(date_iso)
        assert self.rule_page.validate_transfer_action_executed(), "Transfer action was not executed"

    def test_recurring_weekly_rule_transfer(self):
        """
        TC-FT-002: Define a JSON rule with 'recurring' weekly trigger, validate acceptance, simulate time, and validate transfer action.
        """
        rule_id = "TCFT002"
        rule_name = "RecurringWeeklyRule"
        percentage = 10
        self.rule_page.define_json_rule_recurring_weekly(rule_id, rule_name, percentage)
        assert self.rule_page.validate_rule_accepted(), "Rule was not accepted by the system"
        # Simulate several weeks
        for week in range(3):
            future_date = f"2024-07-0{week+2}T10:00:00Z"
            self.rule_page.simulate_system_time(future_date)
            assert self.rule_page.validate_transfer_action_executed(), f"Transfer action was not executed for week {week+1}"
