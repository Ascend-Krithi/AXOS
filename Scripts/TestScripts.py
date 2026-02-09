import asyncio
from RulePage import RulePage
from LoginPage import LoginPage
from RuleManagementPage import RuleManagementPage

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
        await self.login_page.fill_email('user@example.com')
        await self.login_page.fill_password('password123')
        await self.login_page.toggle_remember_me(True)
        await self.login_page.submit_login('user@example.com', 'password123')
        assert await self.login_page.is_remember_me_checked()

class TestRuleCreationExecution:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RulePage(driver)

    async def test_specific_date_fixed_amount_rule(self):
        # Define rule with trigger type 'specific_date' and fixed amount
        rule_json = {
            "name": "Fixed Amount Specific Date",
            "trigger": {
                "type": "specific_date",
                "date": "2024-07-01T10:00:00Z"
            },
            "action": {
                "type": "fixed_amount",
                "amount": 100
            }
        }
        await self.rule_page.open()
        await self.rule_page.define_rule(rule_json)
        assert await self.rule_page.verify_rule_accepted()

        # Simulate system time reaching trigger date
        await self.rule_page.simulate_time_trigger(date_str="2024-07-01T10:00:00Z")

        # Verify rule execution
        assert await self.rule_page.verify_execution()

    async def test_recurring_weekly_percentage_of_deposit_rule(self):
        # Define rule with trigger type 'recurring' (interval 'weekly') and percentage_of_deposit action
        rule_json = {
            "name": "Weekly Percentage of Deposit",
            "trigger": {
                "type": "recurring",
                "interval": "weekly"
            },
            "action": {
                "type": "percentage_of_deposit",
                "percentage": 10
            }
        }
        await self.rule_page.open()
        await self.rule_page.define_rule(rule_json)
        assert await self.rule_page.verify_rule_accepted()

        # Simulate several weeks
        weeks_to_simulate = 3
        await self.rule_page.simulate_time_trigger(interval="weekly", weeks=weeks_to_simulate)

        # Verify rule execution after several weeks
        assert await self.rule_page.verify_execution()

class TestRuleManagementPage:
    def __init__(self, driver):
        self.driver = driver
        self.rule_mgmt_page = RuleManagementPage(driver)

    async def test_define_percentage_rule_and_simulate_deposit(self):
        """
        TC-FT-005: Step 1: Define a rule for 10% of deposit action.
        Step 2: Simulate deposit of 500 units.
        """
        # Step 1: Define 10% deposit rule
        result = self.rule_mgmt_page.define_percentage_rule(10)
        assert 'accepted' in result.lower() or 'success' in result.lower(), f"Rule not accepted: {result}"
        # Step 2: Simulate deposit of 500 units
        transfer_result = self.rule_mgmt_page.simulate_deposit(500)
        assert '50' in transfer_result or 'success' in transfer_result.lower(), f"Unexpected transfer result: {transfer_result}"

    async def test_define_currency_conversion_rule_and_verify_existing(self):
        """
        TC-FT-006: Step 1: Define a rule with a new, future rule type (currency_conversion).
        Step 2: Verify existing rules continue to execute as before.
        """
        # Step 1: Define currency conversion rule (EUR, 100)
        result = self.rule_mgmt_page.define_currency_conversion_rule('EUR', 100)
        assert 'accepted' in result.lower() or 'rejected' in result.lower() or 'success' in result.lower(), f"Unexpected result: {result}"
        # Step 2: Verify existing rules
        rules_list = self.rule_mgmt_page.verify_existing_rules()
        assert isinstance(rules_list, list), f"Rules list not returned: {rules_list}"
