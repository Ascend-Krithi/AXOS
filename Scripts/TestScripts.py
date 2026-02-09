Import necessary modules

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
        await self.login_page.fill_email(''

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_config_page = RuleConfigurationPage(page)

    async def test_specific_date_trigger(self):
        # TC-FT-001: Define a JSON rule with trigger type 'specific_date' set to a future date. Simulate system time reaching the trigger date. Verify transfer action executed once.
        future_date = self.rule_config_page.get_future_date(days=7)
        rule_json = {
            "trigger": {
                "type": "specific_date",
                "date": future_date
            },
            "action": {
                "type": "transfer",
                "amount": 100,
                "destination": "AccountB"
            }
        }
        await self.rule_config_page.navigate()
        await self.rule_config_page.define_rule(rule_json)
        await self.rule_config_page.save_rule()
        await self.rule_config_page.simulate_system_time(future_date)
        executed_count = await self.rule_config_page.get_transfer_action_count(rule_json)
        assert executed_count == 1, f"Expected transfer action executed once, got {executed_count}"

    async def test_recurring_weekly_trigger(self):
        # TC-FT-002: Define a JSON rule with trigger type 'recurring' and interval 'weekly'. Simulate passing of several weeks. Verify transfer action executed at each interval.
        rule_json = {
            "trigger": {
                "type": "recurring",
                "interval": "weekly"
            },
            "action": {
                "type": "transfer",
                "amount": 50,
                "destination": "AccountC"
            }
        }
        await self.rule_config_page.navigate()
        await self.rule_config_page.define_rule(rule_json)
        await self.rule_config_page.save_rule()
        weeks_to_simulate = 4
        for i in range(weeks_to_simulate):
            await self.rule_config_page.simulate_system_time(self.rule_config_page.get_future_date(days=7*(i+1)))
        executed_count = await self.rule_config_page.get_transfer_action_count(rule_json)
        assert executed_count == weeks_to_simulate, f"Expected transfer action executed {weeks_to_simulate} times, got {executed_count}"

    async def test_after_deposit_percentage_transfer(self):
        # TC-FT-005: Define a rule for 10% of deposit action. Simulate deposit of 500 units. Verify transfer of 50 units is executed.
        rule_id = "TC-FT-005"
        rule_name = "After Deposit 10 Percent Rule"
        percentage = 10
        deposit_amount = 500
        expected_transfer = 50
        schema_str = '{"type": "object", "properties": {}}'  # Replace with actual schema if needed
        await self.rule_config_page.navigate()
        self.rule_config_page.define_rule_after_deposit_percentage(rule_id, rule_name, percentage, schema_str)
        self.rule_config_page.simulate_deposit_and_verify_transfer(deposit_amount, expected_transfer)

    async def test_currency_conversion_trigger(self):
        # TC-FT-006: Define a rule with trigger type 'currency_conversion', fixed amount 100 EUR. System accepts or gracefully rejects. Verify existing rules continue to execute as before.
        rule_id = "TC-FT-006"
        rule_name = "Currency Conversion Rule"
        currency = "EUR"
        amount = 100
        schema_str = '{"type": "object", "properties": {}}'  # Replace with actual schema if needed
        await self.rule_config_page.navigate()
        self.rule_config_page.define_rule_currency_conversion(rule_id, rule_name, currency, amount, schema_str)
        self.rule_config_page.verify_existing_rules_function()

    # --- TC-FT-003: Rule with Multiple Conditions ---
    async def test_rule_with_multiple_conditions(self):
        rule_id = "TC-FT-003"
        rule_name = "Multiple Conditions Rule"
        trigger_type = "after_deposit"
        action_type = "fixed_amount"
        amount = 50
        conditions = [
            {"type": "balance_threshold", "operator": ">=", "value": 1000},
            {"type": "transaction_source", "operator": "=", "transaction_source": "salary"}
        ]
        schema_str = '{"type": "object", "properties": {}}'
        await self.rule_config_page.navigate()
        self.rule_config_page.define_rule_with_multiple_conditions(rule_id, rule_name, trigger_type, action_type, amount, conditions, schema_str)

        # Simulate deposit from 'salary' when balance is 900 (should NOT execute transfer)
        self.rule_config_page.simulate_deposit(balance=900, deposit=100, source="salary")
        self.rule_config_page.verify_transfer_not_executed()

        # Simulate deposit from 'salary' when balance is 1200 (should execute transfer)
        self.rule_config_page.simulate_deposit(balance=1200, deposit=100, source="salary")
        self.rule_config_page.verify_transfer_executed()

    # --- TC-FT-004: Error Handling ---
    async def test_rule_missing_trigger(self):
        rule_id = "TC-FT-004-MissingTrigger"
        rule_name = "Missing Trigger Rule"
        action_type = "fixed_amount"
        amount = 100
        schema_str = '{"type": "object", "properties": {}}'
        await self.rule_config_page.navigate()
        self.rule_config_page.submit_rule_missing_trigger(rule_id, rule_name, action_type, amount, schema_str)

    async def test_rule_unsupported_action(self):
        rule_id = "TC-FT-004-UnsupportedAction"
        rule_name = "Unsupported Action Rule"
        trigger_type = "specific_date"
        schema_str = '{"type": "object", "properties": {}}'
        await self.rule_config_page.navigate()
        self.rule_config_page.submit_rule_unsupported_action(rule_id, rule_name, trigger_type, schema_str)

    # --- TC-FT-009: Store and Verify Valid Rule with Specific Date ---
    async def test_store_and_verify_valid_rule_specific_date(self):
        rule_id = "TC-FT-009"
        rule_name = "Valid Rule Specific Date"
        date_str = "2024-07-01T10:00:00Z"
        amount = 100
        schema_str = '{"type": "object", "properties": {}}'
        expected_rule = {
            "trigger": {"type": "specific_date", "date": date_str},
            "action": {"type": "fixed_amount", "amount": amount},
            "conditions": []
        }
        await self.rule_config_page.navigate()
        self.rule_config_page.define_and_store_valid_rule_specific_date(rule_id, rule_name, date_str, amount, schema_str)
        self.rule_config_page.verify_rule_stored(rule_id, expected_rule)

    # --- TC-FT-010: Unconditional Execution After Deposit ---
    async def test_define_rule_after_deposit_empty_conditions_and_trigger(self):
        rule_id = "TC-FT-010"
        rule_name = "After Deposit Empty Conditions"
        amount = 100
        schema_str = '{"type": "object", "properties": {}}'
        deposit_amount = 1000
        await self.rule_config_page.navigate()
        self.rule_config_page.define_rule_after_deposit_empty_conditions(rule_id, rule_name, amount, schema_str)
        self.rule_config_page.trigger_rule_and_verify_unconditional_execution(deposit_amount)

    # --- TC_SCRUM158_03: Recurring Interval Trigger Rule Creation and Scheduling Verification ---
    async def test_create_and_verify_recurring_interval_rule(self):
        """
        TC_SCRUM158_03: Create a schema with a recurring interval trigger (e.g., weekly), submit, verify scheduling logic
        """
        rule_id = "TC_SCRUM158_03"
        rule_name = "Recurring Interval Rule"
        interval_value = "weekly"
        condition_operator = ">="
        condition_value = 1000
        action_account = "C"
        action_amount = 1000
        await self.rule_config_page.create_recurring_interval_rule(rule_id, rule_name, interval_value, condition_operator, condition_value, action_account, action_amount)
        assert self.rule_config_page.verify_rule_scheduling(), "Rule scheduling logic verification failed."

    # --- TC_SCRUM158_04: Rule Creation with Missing Trigger and Error Validation ---
    async def test_submit_rule_without_trigger_and_verify_error(self):
        """
        TC_SCRUM158_04: Prepare a schema missing the 'trigger' field, attempt to create rule, verify error handling
        """
        rule_id = "TC_SCRUM158_04"
        rule_name = "Missing Trigger Rule"
        condition_operator = "<"
        condition_value = 50
        action_account = "D"
        action_amount = 50
        await self.rule_config_page.submit_rule_without_trigger(rule_id, rule_name, condition_operator, condition_value, action_account, action_amount)
        assert self.rule_config_page.verify_missing_trigger_error(), "Missing trigger error was not displayed as expected."
