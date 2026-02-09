# Import necessary modules
from Pages.LoginPage import LoginPage
from Pages.RulePage import RulePage
from selenium.webdriver.remote.webdriver import WebDriver

class TestLoginFunctionality:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.login_page.open()
        self.login_page.login('', '')
        assert self.login_page.is_empty_field_prompt_visible(), "Mandatory fields are required prompt not visible"

    def test_remember_me_functionality(self):
        self.login_page.open()
        self.login_page.login('user@example.com', 'password', remember_me=True)
        assert self.login_page.is_dashboard_header_visible(), "Dashboard header not visible after login"
        assert self.login_page.is_user_profile_icon_visible(), "User profile icon not visible after login"

class TestRuleDefinition:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.rule_page = RulePage(driver)

    def test_tc_ft_001_specific_date_rule(self):
        """
        TC-FT-001: Login, define JSON rule with 'specific_date' trigger, simulate system time, verify transfer action.
        """
        self.login_page.open()
        self.login_page.login('user@example.com', 'password')
        assert self.login_page.is_dashboard_header_visible(), "Login failed"
        rule_json = {
            "trigger": {
                "type": "specific_date",
                "date": "2024-07-01T10:00:00Z"
            },
            "action": {
                "type": "fixed_amount",
                "amount": 100
            },
            "conditions": []
        }
        self.rule_page.define_rule(rule_json)
        assert self.rule_page.is_rule_accepted(), "Rule was not accepted by the system"
        self.rule_page.simulate_time_trigger("specific_date", "2024-07-01T10:00:00Z")
        assert self.rule_page.is_transfer_action_executed(), "Transfer action was not executed at the specified date"

    def test_tc_ft_002_recurring_rule(self):
        """
        TC-FT-002: Login, define JSON rule with 'recurring' trigger, simulate weekly intervals, verify transfer action.
        """
        self.login_page.open()
        self.login_page.login('user@example.com', 'password')
        assert self.login_page.is_dashboard_header_visible(), "Login failed"
        rule_json = {
            "trigger": {
                "type": "recurring",
                "interval": "weekly"
            },
            "action": {
                "type": "percentage_of_deposit",
                "percentage": 10
            },
            "conditions": []
        }
        self.rule_page.define_rule(rule_json)
        assert self.rule_page.is_rule_accepted(), "Rule was not accepted by the system"
        self.rule_page.simulate_time_trigger("recurring", "weekly")
        assert self.rule_page.is_transfer_action_executed(), "Transfer action was not executed at the start of each interval"
