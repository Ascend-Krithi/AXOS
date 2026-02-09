import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('')

class TestRuleCreationAndScheduling:
    def __init__(self, driver):
        self.driver = driver
        self.rule_creation_page = RuleCreationPage(driver)
        self.rule_scheduling_page = RuleSchedulingPage(driver)

    def test_specific_date_rule(self):
        # TC-FT-001: Specific Date Rule
        rule_data = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        self.rule_creation_page.open_rule_creation()
        self.rule_creation_page.enter_rule_json(rule_data)
        self.rule_creation_page.submit_rule()
        assert self.rule_creation_page.verify_rule_accepted() is True, "Rule was not accepted by the system."
        self.rule_scheduling_page.simulate_time()
        assert self.rule_scheduling_page.verify_transfer_executed() is True, "Transfer action was not executed at the specified date."

    def test_recurring_weekly_rule(self):
        # TC-FT-002: Recurring Weekly Rule
        rule_data = {
            "trigger": {"type": "recurring", "interval": "weekly"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        }
        self.rule_creation_page.open_rule_creation()
        self.rule_creation_page.enter_rule_json(rule_data)
        self.rule_creation_page.submit_rule()
        assert self.rule_creation_page.verify_rule_accepted() is True, "Rule was not accepted by the system."
        for _ in range(3):  # Simulate three weeks
            self.rule_scheduling_page.simulate_time()
            assert self.rule_scheduling_page.verify_transfer_executed() is True, "Transfer action was not executed at the interval."
        history = self.rule_scheduling_page.get_transfer_history()
        assert history.count('Transfer executed') >= 3, "Transfer action was not executed at the start of each interval."
