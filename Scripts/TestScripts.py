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

import pytest
import asyncio

from Pages.RuleConfigurationPage import RuleConfigurationPage

@pytest.mark.asyncio
async def test_TC_FT_005_define_percentage_rule_and_verify_transfer(browser):
    """
    TC-FT-005: Define a rule for 10% of deposit action using trigger type 'after_deposit' and action type 'percentage_of_deposit'
    with percentage=10, then simulate a deposit of 500 units and verify transfer of 50 units is executed.
    """
    rule_page = RuleConfigurationPage(browser)
    await rule_page.define_rule_generic(
        trigger_type="after_deposit",
        action_type="percentage_of_deposit",
        percentage=10
    )

    # Simulate deposit of 500 units and verify transfer of 50 units
    await rule_page.simulate_deposit_and_verify_transfer(
        deposit_amount=500,
        expected_transfer_amount=50
    )

@pytest.mark.asyncio
async def test_TC_FT_006_define_currency_conversion_rule_and_verify_behavior(browser):
    """
    TC-FT-006: Define a rule with trigger type 'currency_conversion' (future type), currency='EUR', action type 'fixed_amount', amount=100.
    Verify the system accepts or gracefully rejects with a clear message, without affecting existing rules.
    Then verify existing rules continue to execute as before.
    """
    rule_page = RuleConfigurationPage(browser)
    result = await rule_page.define_rule_generic(
        trigger_type="currency_conversion",
        action_type="fixed_amount",
        currency="EUR",
        amount=100
    )

    # Check if system accepts or gracefully rejects with a clear message
    assert result["status"] in ["accepted", "rejected"], "Unexpected rule creation status"
    if result["status"] == "rejected":
        assert "currency_conversion is not yet supported" in result["message"], "Expected rejection message for future trigger type"

    # Verify existing rules continue to execute as before
    await rule_page.verify_existing_rules_functionality()
