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