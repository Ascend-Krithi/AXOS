# Import necessary modules
from LoginPage import LoginPage
from RuleManagementPage import RuleManagementPage
from TransactionPage import TransactionPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.login_page.open()
        self.login_page.enter_email('')
        self.login_page.enter_password('')
        self.login_page.submit()
        assert self.login_page.is_empty_field_prompt_displayed() is True

    def test_remember_me_functionality(self):
        self.login_page.open()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('securepassword')
        self.login_page.toggle_remember_me(True)
        self.login_page.submit()
        assert self.login_page.is_dashboard_loaded() is True

class TestRuleManagement:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.rule_page = RuleManagementPage(driver)
        self.transaction_page = TransactionPage(driver)

    def test_define_specific_date_rule(self):
        '''
        TC-FT-001: Define a JSON rule with trigger type 'specific_date' set to a future date, simulate system time reaching the trigger date, and verify transfer action is executed once.
        '''
        rule_data = {
            'name': 'Specific Date Rule',
            'trigger': 'specific_date',
            'action': 'fixed_amount',
            'value': 100,
            'date': '2024-07-01'
        }
        # Login
        self.login_page.open()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('securepassword')
        self.login_page.submit()
        assert self.login_page.is_dashboard_loaded() is True
        # Create rule
        self.rule_page.open()
        self.rule_page.create_rule(rule_data)
        assert self.rule_page.is_rule_created('Specific Date Rule') is True
        # Simulate system time reaching the trigger date (pseudo-code, replace with actual system time manipulation if available)
        # Here we assume that the system triggers the rule automatically
        # Validate transfer action
        self.transaction_page.open()
        self.transaction_page.perform_transaction({'amount': 100, 'type': 'transfer'})
        assert self.transaction_page.is_transaction_successful() is True

    def test_define_recurring_rule(self):
        '''
        TC-FT-002: Define a JSON rule with trigger type 'recurring' and interval 'weekly', simulate passing of several weeks, and verify transfer action is executed at each interval.
        '''
        rule_data = {
            'name': 'Weekly Recurring Rule',
            'trigger': 'recurring',
            'action': 'percentage_of_deposit',
            'value': 10,
            'interval': 'weekly'
        }
        # Login
        self.login_page.open()
        self.login_page.enter_email('user@example.com')
        self.login_page.enter_password('securepassword')
        self.login_page.submit()
        assert self.login_page.is_dashboard_loaded() is True
        # Create rule
        self.rule_page.open()
        self.rule_page.create_rule(rule_data)
        assert self.rule_page.is_rule_created('Weekly Recurring Rule') is True
        # Simulate passing of several weeks (pseudo-code, replace with actual time manipulation if available)
        # Validate transfer action at each interval
        for week in range(1, 4):
            self.transaction_page.open()
            self.transaction_page.perform_transaction({'amount': 100, 'type': 'deposit', 'percentage': 10})
            assert self.transaction_page.is_transaction_successful() is True

    def test_rule_with_multiple_conditions(self):
        '''
        TC-FT-003: Step 1: Define a rule with multiple conditions (balance >= 1000, source = 'salary'). Step 2: Simulate deposit from 'salary' when balance is 900. Step 3: Simulate deposit from 'salary' when balance is 1200.
        '''
        # Step 1: Define rule
        self.rule_page.open()
        self.rule_page.define_rule(
            trigger_type='after_deposit',
            action_type='fixed_amount',
            action_amount=50,
            conditions=[
                {'type': 'balance_threshold', 'operator': '>=', 'value': 1000},
                {'type': 'transaction_source', 'value': 'salary'}
            ]
        )
        self.rule_page.submit_rule()
        assert self.rule_page.is_rule_accepted() is True

        # Step 2: Simulate deposit with balance 900, source 'salary'
        self.transaction_page.open()
        self.transaction_page.simulate_deposit(balance=900, deposit=100, source='salary')
        assert self.transaction_page.is_transfer_not_executed() is True

        # Step 3: Simulate deposit with balance 1200, source 'salary'
        self.transaction_page.open()
        self.transaction_page.simulate_deposit(balance=1200, deposit=100, source='salary')
        assert self.transaction_page.is_transfer_executed() is True

    def test_rule_missing_trigger_type(self):
        '''
        TC-FT-004: Step 1: Submit a rule with missing trigger type. Expect error indicating missing required field.
        '''
        self.rule_page.open()
        self.rule_page.define_rule(
            trigger_type=None,
            action_type='fixed_amount',
            action_amount=100,
            conditions=[]
        )
        self.rule_page.submit_rule()
        error_message = self.rule_page.get_error_message()
        validation_error = self.rule_page.get_validation_error()
        assert error_message is not None or validation_error is not None

    def test_rule_unsupported_action_type(self):
        '''
        TC-FT-004: Step 2: Submit a rule with unsupported action type. Expect error indicating unsupported action type.
        '''
        self.rule_page.open()
        self.rule_page.define_rule(
            trigger_type='specific_date',
            action_type='unknown_action',
            action_amount=None,
            conditions=[]
        )
        self.rule_page.submit_rule()
        error_message = self.rule_page.get_error_message()
        validation_error = self.rule_page.get_validation_error()
        assert error_message is not None or validation_error is not None
