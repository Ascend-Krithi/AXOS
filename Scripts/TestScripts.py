# Existing imports
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from Pages.RuleConfigurationPage import RuleConfigurationPage
from selenium import webdriver

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

class TestRuleConfigurationNegativeCases:
    def setup_method(self):
        # Setup WebDriver for each test
        self.driver = webdriver.Chrome()
        self.rule_page = RuleConfigurationPage(self.driver)

    def teardown_method(self):
        # Quit WebDriver after each test
        self.driver.quit()

    def test_tc_scrum158_05_invalid_trigger(self):
        """
        TC_SCRUM158_05: Prepare invalid trigger schema, validate, assert error message includes 'invalid value', submit, assert API returns 400 Bad Request.
        """
        self.rule_page.run_tc_scrum158_05()
        error_message = self.rule_page.get_schema_error_message()
        assert error_message is not None and 'invalid value' in error_message.lower(), 'Expected schema error for invalid trigger'

    def test_tc_scrum158_06_incomplete_condition(self):
        """
        TC_SCRUM158_06: Prepare incomplete condition schema, validate, assert error message includes 'incomplete condition', submit, assert API returns 400 Bad Request.
        """
        self.rule_page.run_tc_scrum158_06()
        error_message = self.rule_page.get_schema_error_message()
        assert error_message is not None and 'incomplete condition' in error_message.lower(), 'Expected schema error for incomplete condition'
