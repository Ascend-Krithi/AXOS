import datetime
from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage

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

# --- Appended Test Methods for TC-SCRUM-158-001 and TC-SCRUM-158-002 ---

class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    async def test_create_rule_specific_date_trigger_balance_500_transfer_100(self):
        """
        TC-SCRUM-158-001:
        - Create rule with specific date trigger (2024-12-31T10:00:00Z)
        - Condition: balance > $500
        - Action: $100 transfer to SAV-001
        - Verify save and retrieval
        """
        await self.rule_page.navigate_to_rule_creation_interface()
        await self.rule_page.define_specific_date_trigger("2024-12-31T10:00:00Z")
        await self.rule_page.add_balance_threshold_condition(500)
        await self.rule_page.add_fixed_transfer_action(100, "SAV-001")
        await self.rule_page.save_rule_and_verify()
        saved_rule = await self.rule_page.retrieve_saved_rule()
        assert saved_rule is not None, "Saved rule could not be retrieved"
        assert saved_rule["trigger"]["type"] == "specific_date"
        assert saved_rule["trigger"]["value"] == "2024-12-31T10:00:00Z"
        assert saved_rule["condition"]["balance_gt"] == 500
        assert saved_rule["action"]["transfer_amount"] == 100
        assert saved_rule["action"]["destination_account"] == "SAV-001"
        await self.rule_page.validate_json_schema(saved_rule)

    async def test_create_rule_current_time_plus_1min_balance_300_transfer_50_verify_execution_log(self):
        """
        TC-SCRUM-158-002:
        - Create rule with specific date trigger (current time + 1min)
        - Condition: balance > $300
        - Action: $50 transfer
        - Verify execution and log
        """
        now = datetime.datetime.utcnow()
        trigger_time = (now + datetime.timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        await self.rule_page.navigate_to_rule_creation_interface()
        await self.rule_page.define_specific_date_trigger(trigger_time)
        await self.rule_page.add_balance_threshold_condition(300)
        await self.rule_page.add_fixed_transfer_action(50, None)
        await self.rule_page.save_rule_and_verify()
        saved_rule = await self.rule_page.retrieve_saved_rule()
        assert saved_rule is not None, "Saved rule could not be retrieved"
        assert saved_rule["trigger"]["type"] == "specific_date"
        assert saved_rule["trigger"]["value"] == trigger_time
        assert saved_rule["condition"]["balance_gt"] == 300
        assert saved_rule["action"]["transfer_amount"] == 50
        await self.rule_page.validate_json_schema(saved_rule)
        # Verify execution and log
        execution_log = await self.rule_page.get_execution_log(saved_rule["id"])
        assert execution_log is not None, "Execution log not found"
        assert execution_log["status"] == "executed"
        assert execution_log["transfer_amount"] == 50
