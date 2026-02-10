import time
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
        await self.login_page.fill_email('...')

# ---- Appended Test Methods for Rule Configuration Page ----

class TestRuleConfiguration:
    def setup_method(self, method):
        # Assume driver is setup elsewhere and passed here
        self.page = None  # Replace with actual driver/page fixture
        self.rule_page = RuleConfigurationPage(self.page)

    def test_sql_injection_in_rule_name(self):
        rule_data = {
            "rule_id": "R008",
            "rule_name": "Test'; DROP TABLE transfer_rules;--",
            "triggers": [{"type": "event"}],
            "conditions": [],
            "actions": []
        }
        error = self.rule_page.test_sql_injection_in_rule_name(rule_data)
        assert error is not None

    def test_xss_in_description(self):
        rule_data = {
            "rule_id": "R009",
            "description": "<script>alert('XSS')</script>",
            "triggers": [{"type": "event"}],
            "conditions": [],
            "actions": []
        }
        error = self.rule_page.test_xss_in_description(rule_data)
        assert error is not None

    def test_command_injection_in_condition(self):
        rule_data = {
            "rule_id": "R010",
            "triggers": [{"type": "event"}],
            "conditions": [{"field": "command", "operator": "=", "value": "; rm -rf /"}],
            "actions": []
        }
        error = self.rule_page.test_command_injection_in_condition(rule_data)
        assert error is not None

    def test_security_log_verification(self):
        assert self.rule_page.verify_security_log_entry(threat_type='injection_attempt')

    def test_create_rule_with_max_triggers(self):
        rule_data = {
            "rule_id": "R011",
            "triggers": [{"type": f"t{i+1}"} for i in range(10)],
            "conditions": [{"field": "f", "operator": "=", "value": 1}],
            "actions": [{"type": "a1"}]
        }
        result = self.rule_page.create_rule_with_max_triggers(rule_data)
        assert result

    def test_create_rule_with_excess_triggers(self):
        rule_data = {
            "rule_id": "R012",
            "triggers": [{"type": f"t{i+1}"} for i in range(11)],
            "conditions": [{"field": "f", "operator": "=", "value": 1}],
            "actions": [{"type": "a1"}]
        }
        error = self.rule_page.create_rule_with_excess_triggers(rule_data)
        assert error is not None

    def test_create_rule_with_max_conditions_actions(self):
        rule_data = {
            "rule_id": "R013",
            "triggers": [{"type": "t1"}],
            "conditions": [{"field": f"c{i+1}", "operator": "=", "value": i+1} for i in range(20)],
            "actions": [{"type": f"a{i+1}"} for i in range(20)]
        }
        result = self.rule_page.create_rule_with_max_conditions_actions(rule_data)
        assert result

    def test_performance_measurement(self):
        rule_data = {
            "rule_id": "R013",
            "triggers": [{"type": "t1"}],
            "conditions": [{"field": f"c{i+1}", "operator": "=", "value": i+1} for i in range(20)],
            "actions": [{"type": f"a{i+1}"} for i in range(20)]
        }
        create_time, eval_time = self.rule_page.measure_performance(rule_data)
        assert create_time < 2.0, f"Rule creation took too long: {create_time}s"
        assert eval_time < 0.5, f"Rule evaluation took too long: {eval_time}s"
