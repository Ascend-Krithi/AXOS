import asyncio
from RulePage import RulePage
from LoginPage import LoginPage

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
