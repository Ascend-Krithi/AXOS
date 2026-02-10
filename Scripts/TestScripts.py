import asyncio
from RuleConfigurationPage import RuleConfigurationPage
from LoginPage import LoginPage
from datetime import datetime, timedelta

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

# --- New Test Methods Appended Below ---

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_create_and_verify_rule_TC_SCRUM_158_001(self):
        """
        TC-SCRUM-158-001: Create a rule with a specific date trigger, balance threshold condition, fixed amount transfer action,
        save and retrieve the rule, verify all components.
        """
        rule_name = "AutoTransfer_158_001"
        trigger_date = datetime.now() + timedelta(days=1)
        trigger_type = "date"
        condition_type = "balance_threshold"
        threshold_amount = 1000.00
        action_type = "transfer"
        transfer_amount = 250.00
        source_account = "AccountA"
        destination_account = "AccountB"

        # Navigate to rule creation interface
        await self.rule_page.navigate_to_rule_creation()

        # Define specific date trigger
        await self.rule_page.set_trigger(trigger_type, date=trigger_date.strftime("%Y-%m-%d %H:%M"))

        # Add balance threshold condition
        await self.rule_page.add_condition(condition_type, threshold=threshold_amount)

        # Add fixed amount transfer action
        await self.rule_page.add_action(action_type, amount=transfer_amount, source=source_account, destination=destination_account)

        # Save the rule
        await self.rule_page.save_rule(rule_name)

        # Retrieve the rule
        rule_data = await self.rule_page.get_rule(rule_name)

        # Verify all components
        assert rule_data['name'] == rule_name
        assert rule_data['trigger']['type'] == trigger_type
        assert rule_data['trigger']['date'] == trigger_date.strftime("%Y-%m-%d %H:%M")
        assert rule_data['conditions'][0]['type'] == condition_type
        assert float(rule_data['conditions'][0]['threshold']) == threshold_amount
        assert rule_data['actions'][0]['type'] == action_type
        assert float(rule_data['actions'][0]['amount']) == transfer_amount
        assert rule_data['actions'][0]['source'] == source_account
        assert rule_data['actions'][0]['destination'] == destination_account

    async def test_rule_execution_and_log_TC_SCRUM_158_002(self):
        """
        TC-SCRUM-158-002: Create a rule with a trigger (current date + 1 min), set account balance, wait for trigger,
        verify rule evaluation, action execution, and check execution log.
        """
        rule_name = "AutoTransfer_158_002"
        trigger_date = datetime.now() + timedelta(minutes=1)
        trigger_type = "date"
        condition_type = "balance_threshold"
        threshold_amount = 1500.00
        action_type = "transfer"
        transfer_amount = 300.00
        source_account = "AccountC"
        destination_account = "AccountD"

        # Navigate to rule creation interface
        await self.rule_page.navigate_to_rule_creation()

        # Define trigger (current date + 1 min)
        await self.rule_page.set_trigger(trigger_type, date=trigger_date.strftime("%Y-%m-%d %H:%M"))

        # Add balance threshold condition
        await self.rule_page.add_condition(condition_type, threshold=threshold_amount)

        # Add fixed amount transfer action
        await self.rule_page.add_action(action_type, amount=transfer_amount, source=source_account, destination=destination_account)

        # Save the rule
        await self.rule_page.save_rule(rule_name)

        # Set account balance to meet threshold
        await self.rule_page.set_account_balance(source_account, threshold_amount + 500)

        # Wait for trigger time
        now = datetime.now()
        wait_seconds = (trigger_date - now).total_seconds()
        if wait_seconds > 0:
            await asyncio.sleep(wait_seconds + 5)  # Add buffer

        # Verify rule evaluation and action execution
        execution_status = await self.rule_page.get_rule_execution_status(rule_name)
        assert execution_status == "Executed"

        # Check rule execution log
        execution_log = await self.rule_page.get_rule_execution_log(rule_name)
        assert execution_log['rule_name'] == rule_name
        assert execution_log['triggered_at'] == trigger_date.strftime("%Y-%m-%d %H:%M")
        assert execution_log['action']['type'] == action_type
        assert float(execution_log['action']['amount']) == transfer_amount
        assert execution_log['action']['source'] == source_account
        assert execution_log['action']['destination'] == destination_account
