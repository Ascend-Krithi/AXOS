import asyncio
from RuleConfigurationPage import RuleConfigurationPage
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
        await self.login_page.fill_email(' ...')
        # Existing test logic continues...

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_TC_SCRUM_158_001_create_and_verify_rule(self):
        # Step 1: Navigate to rule creation
        await self.rule_page.navigate_to_rule_creation()

        # Step 2: Define trigger with specific date
        trigger_datetime = '2024-12-31T10:00:00Z'
        await self.rule_page.set_trigger_date(trigger_datetime)

        # Step 3: Add balance threshold condition (> $500)
        await self.rule_page.add_condition_balance_threshold(500)

        # Step 4: Add fixed transfer action ($100 to SAV-001)
        await self.rule_page.add_action_fixed_transfer(100, 'SAV-001')

        # Step 5: Save rule
        rule_id = await self.rule_page.save_rule()

        # Step 6: Retrieve rule
        rule_data = await self.rule_page.retrieve_rule(rule_id)

        # Step 7: Verify components
        assert rule_data['trigger']['type'] == 'date'
        assert rule_data['trigger']['value'] == trigger_datetime
        assert rule_data['condition']['type'] == 'balance_threshold'
        assert rule_data['condition']['operator'] == '>'
        assert rule_data['condition']['value'] == 500
        assert rule_data['action']['type'] == 'fixed_transfer'
        assert rule_data['action']['amount'] == 100
        assert rule_data['action']['destination_account'] == 'SAV-001'
        # Optional: Validate JSON schema
        assert await self.rule_page.validate_rule_schema(rule_data)

    async def test_TC_SCRUM_158_002_create_evaluate_and_verify_log(self):
        # Step 1: Navigate to rule creation
        await self.rule_page.navigate_to_rule_creation()

        # Step 2: Define trigger with current time + 1min
        from datetime import datetime, timedelta
        import pytz
        now_utc = datetime.now(pytz.UTC)
        trigger_datetime = (now_utc + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        await self.rule_page.set_trigger_date(trigger_datetime)

        # Step 3: Add balance threshold condition (> $300)
        await self.rule_page.add_condition_balance_threshold(300)

        # Step 4: Add fixed transfer action ($50 to SAV-001)
        await self.rule_page.add_action_fixed_transfer(50, 'SAV-001')

        # Step 5: Save rule
        rule_id = await self.rule_page.save_rule()

        # Step 6: Retrieve rule
        rule_data = await self.rule_page.retrieve_rule(rule_id)
        assert rule_data['trigger']['type'] == 'date'
        assert rule_data['trigger']['value'] == trigger_datetime
        assert rule_data['condition']['type'] == 'balance_threshold'
        assert rule_data['condition']['operator'] == '>'
        assert rule_data['condition']['value'] == 300
        assert rule_data['action']['type'] == 'fixed_transfer'
        assert rule_data['action']['amount'] == 50
        assert rule_data['action']['destination_account'] == 'SAV-001'
        assert await self.rule_page.validate_rule_schema(rule_data)

        # Step 7: Update account balance to > $300
        await self.rule_page.update_account_balance(350)

        # Step 8: Wait for rule evaluation (wait until after trigger time)
        from time import sleep
        sleep(70)  # Wait a bit more than 1 minute to ensure trigger

        # Step 9: Verify rule evaluation and action execution
        execution_log = await self.rule_page.get_execution_log(rule_id)
        assert execution_log['status'] == 'executed'
        assert execution_log['triggered_at'] == trigger_datetime
        assert execution_log['action']['amount'] == 50
        assert execution_log['action']['destination_account'] == 'SAV-001'
