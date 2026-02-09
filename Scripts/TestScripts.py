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
        # Step 1: Set up rule configuration
        self.rule_page.set_rule_id(rule_id)
        self.rule_page.set_rule_name(rule_name)
        self.rule_page.select_trigger_type('specific_date')
        self.rule_page.set_trigger_date(date_iso)
        self.rule_page.select_action_type('fixed_amount')
        self.rule_page.set_transfer_amount(amount)
        self.rule_page.save_rule()
        # Step 2: Validate rule acceptance
        success_message = self.rule_page.get_success_message()
        assert success_message is not None and 'accepted' in success_message.lower(), "Rule was not accepted by the system"
        # Step 3: Simulate system time
        self.rule_page.simulate_system_time(date_iso)
        # Step 4: Validate transfer action
        transfer_result = self.rule_page.validate_transfer_action()
        assert transfer_result is not None, "Transfer action was not executed"

    def test_recurring_weekly_rule_transfer(self):
        """
        TC-FT-002: Define a JSON rule with 'recurring' weekly trigger, validate acceptance, simulate time, and validate transfer action.
        """
        rule_id = "TCFT002"
        rule_name = "RecurringWeeklyRule"
        interval = "weekly"
        percentage = 10
        # Step 1: Set up rule configuration
        self.rule_page.set_rule_id(rule_id)
        self.rule_page.set_rule_name(rule_name)
        self.rule_page.select_trigger_type('recurring')
        self.rule_page.set_recurring_interval(interval)
        self.rule_page.select_action_type('percentage_of_deposit')
        self.rule_page.set_percentage(percentage)
        self.rule_page.save_rule()
        # Step 2: Validate rule acceptance
        success_message = self.rule_page.get_success_message()
        assert success_message is not None and 'accepted' in success_message.lower(), "Rule was not accepted by the system"
        # Step 3: Simulate several weeks
        for week in range(3):
            future_date = f"2024-07-0{week+2}T10:00:00Z"
            self.rule_page.simulate_system_time(future_date)
            transfer_result = self.rule_page.validate_transfer_action()
            assert transfer_result is not None, f"Transfer action was not executed for week {week+1}"
