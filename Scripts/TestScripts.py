import asyncio
from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.RuleManagementPage import RuleManagementPage

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

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_config_page = RuleConfigurationPage(page)
        self.rule_mgmt_page = RuleManagementPage(page)

    # ...[existing async test methods]...

    async def test_TC_SCRUM158_09(self):
        '''
        TC_SCRUM158_09: Prepare a schema with malicious metadata and verify error response.
        '''
        malicious_schema = '{"trigger":{"type":"manual"},"conditions":[{"type":"amount","operator":"==","value":1}],"actions":[{"type":"transfer","account":"I","amount":1}],"metadata":"<script>alert(\'hack\')</script>"}'
        self.rule_config_page.prepare_schema_with_malicious_metadata(malicious_schema)
        self.rule_config_page.submit_schema()
        error_msg = self.rule_config_page.get_error_message()
        assert any(keyword in error_msg.lower() for keyword in ['invalid', 'error', 'malicious']), f"Expected error indication for malicious metadata, got: {error_msg}"
