# Existing imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Pages.RuleConfigurationPage import RuleConfigurationPage

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

# New test methods for Rule Configuration
import datetime
import json

class TestRuleConfiguration:
    def __init__(self, driver):
        self.page = RuleConfigurationPage(driver)

    def test_define_specific_date_rule(self):
        """
        TC-FT-001: Define JSON rule with trigger type 'specific_date', execute fixed amount transfer.
        """
        rule_id = 'TC-FT-001-Rule'
        rule_name = 'Specific Date Transfer Rule'
        trigger_type = 'specific_date'
        date_str = '2024-07-01'
        action_type = 'fixed_amount'
        amount = 100
        destination_account = '123456789'
        json_rule = json.dumps({
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        })

        self.page.enter_rule_id(rule_id)
        self.page.enter_rule_name(rule_name)
        self.page.select_trigger_type(trigger_type)
        self.page.set_specific_date(date_str)
        self.page.select_action_type(action_type)
        self.page.set_transfer_amount(amount)
        self.page.set_destination_account(destination_account)
        self.page.enter_json_schema(json_rule)
        self.page.validate_schema()
        assert self.page.is_success_message_displayed(), "Rule was not accepted by the system."
        self.page.save_rule()
        # Simulate system time reaching the trigger date (pseudo, as actual time manipulation is not possible in Selenium)
        # Verify transfer action executed (would require backend validation or UI confirmation)

    def test_define_recurring_rule(self):
        """
        TC-FT-002: Define JSON rule with trigger type 'recurring', execute percentage transfer.
        """
        rule_id = 'TC-FT-002-Rule'
        rule_name = 'Recurring Transfer Rule'
        trigger_type = 'recurring'
        interval = 'weekly'
        action_type = 'percentage_of_deposit'
        percentage = 10
        destination_account = '987654321'
        json_rule = json.dumps({
            "trigger": {"type": "recurring", "interval": "weekly"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        })

        self.page.enter_rule_id(rule_id)
        self.page.enter_rule_name(rule_name)
        self.page.select_trigger_type(trigger_type)
        self.page.set_recurring_interval(interval)
        self.page.select_action_type(action_type)
        self.page.set_percentage(percentage)
        self.page.set_destination_account(destination_account)
        self.page.enter_json_schema(json_rule)
        self.page.validate_schema()
        assert self.page.is_success_message_displayed(), "Rule was not accepted by the system."
        self.page.save_rule()
        # Simulate passing of several weeks (pseudo, as actual time manipulation is not possible in Selenium)
        # Verify transfer action executed at each interval (would require backend validation or UI confirmation)

    def test_define_multi_condition_rule_and_deposit_simulation(self):
        """
        TC-FT-003: Define a rule with multiple conditions (balance >= 1000, source = 'salary'), simulate deposit from 'salary' with balance 900 (expect no transfer), simulate deposit from 'salary' with balance 1200 (expect transfer).
        """
        rule_id = 'TC-FT-003-Rule'
        rule_name = 'Multi-Condition Salary Rule'
        trigger_type = 'after_deposit'
        action_type = 'fixed_amount'
        amount = 50
        destination_account = '555666777'
        # Step 1: Define rule with multiple conditions
        self.page.set_rule_id(rule_id)
        self.page.set_rule_name(rule_name)
        self.page.select_trigger_type(trigger_type)
        self.page.set_action_type(action_type)
        self.page.set_transfer_amount(amount)
        self.page.set_destination_account(destination_account)
        # Add conditions
        self.page.add_condition('balance_threshold', operator='>=', value=1000)
        self.page.add_condition('transaction_source', value='salary')
        self.page.save_rule()
        assert self.page.validate_rule_success(), "Rule was not accepted."
        # Step 2: Simulate deposit with balance 900 (no transfer)
        self.page.simulate_deposit(balance=900, deposit=100, source='salary')
        assert self.page.validate_transfer_not_executed(), "Transfer should NOT be executed for balance 900."
        # Step 3: Simulate deposit with balance 1200 (transfer executed)
        self.page.simulate_deposit(balance=1200, deposit=100, source='salary')
        assert self.page.validate_transfer_executed(), "Transfer should be executed for balance 1200."

    def test_error_handling_missing_trigger_and_unsupported_action(self):
        """
        TC-FT-004: Submit rule with missing trigger type (expect error), submit rule with unsupported action type (expect error).
        """
        rule_id = 'TC-FT-004-Rule'
        rule_name = 'Error Handling Rule'
        # Step 1: Missing trigger type
        self.page.set_rule_id(rule_id)
        self.page.set_rule_name(rule_name)
        self.page.set_action_type('fixed_amount')
        self.page.set_transfer_amount(100)
        self.page.set_destination_account('111222333')
        self.page.save_rule()
        assert self.page.validate_missing_trigger_error(), "Missing trigger error not detected."
        # Step 2: Unsupported action type
        self.page.set_rule_id(rule_id)
        self.page.set_rule_name(rule_name)
        self.page.select_trigger_type('specific_date')
        self.page.set_action_type('unknown_action')
        self.page.save_rule()
        assert self.page.validate_unsupported_action_error(), "Unsupported action type error not detected."
