import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from LoginPage import LoginPage
from RuleConfigurationPage import RuleConfigurationPage
from SecurityAuditLogPage import SecurityAuditLogPage

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

class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)
        self.audit_log_page = SecurityAuditLogPage(driver)

    def wait_for_element(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            pytest.fail(f"Element {locator} not found after {timeout} seconds.")

    def test_TC_SCRUM_158_001_create_and_validate_rule(self):
        """
        TC-SCRUM-158-001: Create a rule, add trigger, condition, action, save, retrieve, and validate.
        """
        try:
            self.rule_page.navigate_to_rule_configuration()
            self.wait_for_element((By.ID, "create-rule-btn"))
            self.rule_page.click_create_rule()

            self.wait_for_element((By.ID, "rule-name-input"))
            self.rule_page.enter_rule_name("AutoTestRule001")
            self.rule_page.enter_rule_description("Automated test rule creation.")

            self.rule_page.add_trigger(trigger_type="OnEvent", trigger_value="UserLogin")
            self.rule_page.add_condition(condition_type="UserType", condition_value="Admin")
            self.rule_page.add_action(action_type="SendNotification", action_value="Email")

            self.rule_page.save_rule()
            self.wait_for_element((By.XPATH, "//div[contains(text(), 'Rule saved successfully')]")

            self.rule_page.search_rule("AutoTestRule001")
            self.wait_for_element((By.XPATH, "//td[contains(text(), 'AutoTestRule001')]")
            rule_details = self.rule_page.get_rule_details("AutoTestRule001")

            assert rule_details['name'] == "AutoTestRule001"
            assert rule_details['trigger'] == "OnEvent:UserLogin"
            assert rule_details['condition'] == "UserType:Admin"
            assert rule_details['action'] == "SendNotification:Email"
        except Exception as e:
            pytest.fail(f"TC-SCRUM-158-001 failed: {str(e)}")

    def test_TC_SCRUM_158_002_rule_duplicate_validation(self):
        """
        TC-SCRUM-158-002: Attempt to create a rule with a duplicate name and validate error handling.
        """
        try:
            self.rule_page.navigate_to_rule_configuration()
            self.wait_for_element((By.ID, "create-rule-btn"))
            self.rule_page.click_create_rule()

            self.wait_for_element((By.ID, "rule-name-input"))
            self.rule_page.enter_rule_name("AutoTestRule001")  # Duplicate name
            self.rule_page.enter_rule_description("Duplicate rule test.")

            self.rule_page.add_trigger(trigger_type="OnEvent", trigger_value="UserLogin")
            self.rule_page.add_condition(condition_type="UserType", condition_value="Admin")
            self.rule_page.add_action(action_type="SendNotification", action_value="Email")

            self.rule_page.save_rule()
            error_message = self.rule_page.get_error_message()
            assert error_message == "A rule with this name already exists"
        except Exception as e:
            pytest.fail(f"TC-SCRUM-158-002 failed: {str(e)}")

    # --- New test methods for TC-SCRUM-387-007 ---
    def test_TC_SCRUM_387_007_security_validations(self):
        """
        TC-SCRUM-387-007:
        1. Attempt SQL injection in rule_name
        2. Attempt XSS in description
        3. Attempt command injection in condition value
        4. Validate log captures malicious attempts
        """
        # Step 1: SQL Injection
        sql_payload = "Test'; DROP TABLE transfer_rules;--"
        error_msg_sql = self.rule_page.attempt_sql_injection(sql_payload)
        assert "error" in error_msg_sql.lower() or "invalid" in error_msg_sql.lower()

        # Step 2: XSS
        xss_payload = "<script>alert('XSS')</script>"
        error_msg_xss = self.rule_page.attempt_xss(xss_payload)
        assert "error" in error_msg_xss.lower() or "invalid" in error_msg_xss.lower()

        # Step 3: Command Injection
        cmd_payload = "; rm -rf /"
        error_msg_cmd = self.rule_page.attempt_command_injection(cmd_payload)
        assert "error" in error_msg_cmd.lower() or "invalid" in error_msg_cmd.lower()

        # Step 4: Validate security logs
        injection_logs = self.audit_log_page.validate_injection_attempt(threat_type='injection_attempt')
        assert len(injection_logs) > 0
        for entry in injection_logs:
            assert 'timestamp' in entry
            assert 'payload' in entry
            assert 'rejection_reason' in entry
            assert entry['threat_type'] == 'injection_attempt'

    # --- New test methods for TC-SCRUM-387-008 ---
    def test_TC_SCRUM_387_008_max_triggers_conditions_actions(self):
        """
        TC-SCRUM-387-008:
        1. Create rule with max triggers (10)
        2. Attempt to create rule exceeding max triggers (11)
        3. Create rule with max conditions and actions (20 each)
        4. Measure performance
        """
        # Step 1: Max triggers
        triggers_10 = [{'type': f't{i+1}'} for i in range(10)]
        conditions_1 = [{'field': 'f', 'operator': '=', 'value': 1}]
        actions_1 = [{'type': 'a1'}]
        self.rule_page.create_rule_with_triggers('R011', triggers_10)
        success_msg = self.rule_page.get_success_message()
        assert 'success' in success_msg.lower()

        # Step 2: Exceed max triggers
        triggers_11 = [{'type': f't{i+1}'} for i in range(11)]
        self.rule_page.create_rule_with_triggers('R012', triggers_11)
        error_msg = self.rule_page.get_schema_error_message()
        assert 'limit' in error_msg.lower() or 'exceed' in error_msg.lower() or 'error' in error_msg.lower()

        # Step 3: Max conditions and actions
        conditions_20 = [{'field': f'f{i+1}', 'operator': '=', 'value': i+1} for i in range(20)]
        actions_20 = [{'type': f'a{i+1}', 'amount': 100+i} for i in range(20)]
        self.rule_page.create_rule_with_conditions_actions('R013', conditions_20, actions_20)
        success_msg_2 = self.rule_page.get_success_message()
        assert 'success' in success_msg_2.lower()

        # Step 4: Performance measurement
        def create_rule():
            self.rule_page.create_rule_with_conditions_actions('R013', conditions_20, actions_20)
        response_time = self.rule_page.measure_response_time(create_rule)
        assert response_time <= 2.0  # Rule creation within 2 seconds

        # For rule evaluation, assume a function exists (not shown in PageClass) or mock
        # evaluation_time = self.rule_page.measure_response_time(self.rule_page.evaluate_rule, 'R013')
        # assert evaluation_time <= 0.5  # Evaluation within 500ms
