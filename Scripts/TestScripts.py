# Import necessary modules
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        await self.login_page.fill_email('')

class TestRuleConfiguration:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)
        self.wait = WebDriverWait(driver, 10)

    def test_TC_SCRUM158_001(self):
        # Step 1: Navigate to rule creation interface
        self.driver.get('/rules/create')
        assert 'Rule Creation' in self.driver.title or self.rule_page.rule_id_input.is_displayed()

        # Step 2: Create JSON schema with specific_date
        self.rule_page.set_specific_date_trigger('2024-12-31')
        assert self.rule_page.date_picker.get_attribute('value') == '2024-12-31'

        # Step 3: Add balance_threshold condition
        self.rule_page.add_balance_threshold_condition(500)
        assert self.rule_page.balance_threshold_input.get_attribute('value') == '500'

        # Step 4: Add fixed_amount action
        self.rule_page.add_fixed_amount_action(100)
        assert self.rule_page.transfer_amount_input.get_attribute('value') == '100'

        # Step 5: Submit rule for validation and storage
        schema_valid = self.rule_page.validate_json_schema()
        assert schema_valid, 'Schema validation failed'
        success_text = self.rule_page.save_rule()
        assert 'successfully' in success_text.lower()

    def test_TC_SCRUM158_002(self):
        # Step 1: Access automated transfer rule configuration
        self.driver.get('/rules/configure')
        assert 'Configuration' in self.driver.title or self.rule_page.rule_id_input.is_displayed()

        # Step 2: Create rule with after_deposit trigger
        self.rule_page.toggle_after_deposit(True)
        assert self.rule_page.after_deposit_toggle.is_selected()

        # Step 3: Set transaction_source condition
        self.rule_page.add_transaction_source_condition('Employer Y')
        # No direct assertion, but can check dropdown value

        # Step 4: Configure percentage action
        self.rule_page.add_percentage_action(10)
        assert self.rule_page.percentage_input.get_attribute('value') == '10'

        # Step 5: Save rule and simulate deposit
        schema_valid = self.rule_page.validate_json_schema()
        assert schema_valid, 'Schema validation failed'
        success_text = self.rule_page.save_rule()
        assert 'successfully' in success_text.lower()

    def test_TC_SCRUM158_003(self):
        # Test Case TC_SCRUM158_003: Monthly recurring rule, balance threshold, fixed amount transfer
        rule_id = 'TC003'
        rule_name = 'Monthly Recurring Rule'
        trigger_type = 'Monthly'
        interval_value = '1'
        after_deposit = False
        conditions = [
            {'type': 'balance_threshold', 'operator': '>', 'value': 1000}
        ]
        actions = [
            {'type': 'fixed_amount', 'amount': 200, 'destination_account': 'ACC123'}
        ]
        self.rule_page.configure_advanced_rule(rule_id, rule_name, trigger_type, interval_value, after_deposit, conditions, actions)
        assert self.rule_page.verify_rule_saved(), 'Rule was not saved successfully.'
        assert 'successfully' in self.rule_page.get_success_message_text().lower()

    def test_TC_SCRUM158_004(self):
        # Test Case TC_SCRUM158_004: Advanced rule, multiple conditions, after deposit trigger, multiple actions
        rule_id = 'TC004'
        rule_name = 'Advanced Multi-Condition Rule'
        trigger_type = 'After Deposit'
        interval_value = '0'
        after_deposit = True
        conditions = [
            {'type': 'balance_threshold', 'operator': '>=', 'value': 5000},
            {'type': 'transaction_source', 'source_provider': 'Employer Y'}
        ]
        actions = [
            {'type': 'fixed_amount', 'amount': 300, 'destination_account': 'ACC789'},
            {'type': 'percentage', 'percentage': 15, 'destination_account': 'ACC456'}
        ]
        self.rule_page.configure_advanced_rule(rule_id, rule_name, trigger_type, interval_value, after_deposit, conditions, actions)
        assert self.rule_page.verify_rule_saved(), 'Rule was not saved successfully.'
        assert 'successfully' in self.rule_page.get_success_message_text().lower()

    # TC_SCRUM158_005: Invalid trigger type rule creation and validation
    def test_TC_SCRUM158_005(self):
        # Step 1: Access rule creation interface
        self.driver.get('/rules/create')
        assert 'Rule Creation' in self.driver.title or self.rule_page.rule_id_input.is_displayed()
        # Step 2: Attempt to create rule with trigger_type='invalid_trigger'
        invalid_rule = {
            'trigger_type': 'invalid_trigger',
            'condition_type': 'balance_threshold',
            'threshold': 500
        }
        # Step 3: Submit invalid rule for validation
        error_message = self.rule_page.submit_invalid_rule(invalid_rule)
        assert error_message is not None
        assert 'invalid_trigger' in error_message.lower()
        # Step 4: Verify rule not created in database
        assert self.rule_page.verify_rule_not_created('invalid_trigger')

    # TC_SCRUM158_006: Missing required fields in rule creation and validation
    def test_TC_SCRUM158_006(self):
        # Step 1: Prepare rule JSON without action_type field
        incomplete_rule_1 = {
            'trigger_type': 'after_deposit',
            'condition_type': 'balance_threshold',
            'threshold': 500
        }
        # Step 2: Submit incomplete rule to validation service
        error_message_1 = self.rule_page.submit_incomplete_rule(incomplete_rule_1)
        assert error_message_1 is not None
        assert 'action_type' in error_message_1.lower()
        assert 'required' in error_message_1.lower()
        # Step 4: Attempt to create another rule without trigger_type field
        incomplete_rule_2 = {
            'condition_type': 'balance_threshold',
            'action_type': 'fixed_amount',
            'amount': 100
        }
        error_message_2 = self.rule_page.submit_incomplete_rule(incomplete_rule_2)
        assert error_message_2 is not None
        assert 'trigger_type' in error_message_2.lower()
        assert 'required' in error_message_2.lower()
