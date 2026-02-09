# RuleManagementPage.py
"""
Page Object for Rule Management functionality.
This class supports creation of JSON rules with various trigger types and actions as described in test cases.

Test Coverage:
- Define a JSON rule with trigger type 'specific_date' set to a future date.
- Define a JSON rule with trigger type 'recurring' and interval 'weekly'.

Locators should be updated according to Locators.json content for:
- Rule creation form
- Trigger type dropdown
- Date picker
- Action type dropdown
- Amount/Percentage input
- Submit button

Usage:
    rule_page = RuleManagementPage(page)
    await rule_page.create_specific_date_rule(date, amount)
    await rule_page.create_recurring_rule(interval, percentage)
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleManagementPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators (replace with actual values from Locators.json)
        self.rule_create_button = (By.ID, 'rule-create-btn')
        self.trigger_type_dropdown = (By.ID, 'trigger-type')
        self.date_picker = (By.ID, 'trigger-date')
        self.interval_dropdown = (By.ID, 'trigger-interval')
        self.action_type_dropdown = (By.ID, 'action-type')
        self.amount_input = (By.ID, 'action-amount')
        self.percentage_input = (By.ID, 'action-percentage')
        self.submit_button = (By.ID, 'submit-rule')

    def open_rule_creation(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.rule_create_button)
        ).click()

    def select_trigger_type(self, trigger_type):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.trigger_type_dropdown)
        )
        dropdown.send_keys(trigger_type)

    def set_specific_date(self, date):
        date_picker = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.date_picker)
        )
        date_picker.clear()
        date_picker.send_keys(date)

    def set_interval(self, interval):
        interval_dropdown = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.interval_dropdown)
        )
        interval_dropdown.send_keys(interval)

    def select_action_type(self, action_type):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.action_type_dropdown)
        )
        dropdown.send_keys(action_type)

    def set_amount(self, amount):
        amount_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.amount_input)
        )
        amount_input.clear()
        amount_input.send_keys(str(amount))

    def set_percentage(self, percentage):
        percentage_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.percentage_input)
        )
        percentage_input.clear()
        percentage_input.send_keys(str(percentage))

    def submit_rule(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.submit_button)
        ).click()

    def create_specific_date_rule(self, date, amount):
        """
        Create a rule with trigger type 'specific_date' and fixed amount action.
        :param date: str, date in ISO format (e.g., '2024-07-01T10:00:00Z')
        :param amount: int, amount to transfer
        """
        self.open_rule_creation()
        self.select_trigger_type('specific_date')
        self.set_specific_date(date)
        self.select_action_type('fixed_amount')
        self.set_amount(amount)
        self.submit_rule()

    def create_recurring_rule(self, interval, percentage):
        """
        Create a rule with trigger type 'recurring' and percentage action.
        :param interval: str, interval type (e.g., 'weekly')
        :param percentage: int, percentage of deposit to transfer
        """
        self.open_rule_creation()
        self.select_trigger_type('recurring')
        self.set_interval(interval)
        self.select_action_type('percentage_of_deposit')
        self.set_percentage(percentage)
        self.submit_rule()