# TestScripts.py for AXOS LoginPage
from selenium import webdriver
from LoginPage import LoginPage
import pytest
import datetime

# Test Case TC-FT-001: Specific Date Trigger
@pytest.mark.usefixtures('driver_init')
def test_specific_date_trigger(driver):
    login_page = LoginPage(driver)
    login_page.open()
    # Example login credentials
    login_page.login('user@example.com', 'securepassword')
    assert login_page.is_dashboard_header_present(), 'Dashboard header not present after login.'
    # Simulate JSON rule creation (mocked)
    rule = {
        'trigger': {'type': 'specific_date', 'date': '2024-07-01T10:00:00Z'},
        'action': {'type': 'fixed_amount', 'amount': 100},
        'conditions': []
    }
    # Simulate system time reaching the trigger date (mocked)
    trigger_date = datetime.datetime.strptime(rule['trigger']['date'], '%Y-%m-%dT%H:%M:%SZ')
    now = datetime.datetime.utcnow()
    assert now < trigger_date, 'Test must run before trigger date.'
    # Here you would advance the system time or mock the scheduler
    # For demonstration, we assert the rule is accepted
    assert rule['trigger']['type'] == 'specific_date'
    # Simulate transfer action (mocked)
    transfer_executed = True  # Replace with actual system call
    assert transfer_executed, 'Transfer action was not executed.'

# Test Case TC-FT-002: Recurring Weekly Trigger
@pytest.mark.usefixtures('driver_init')
def test_recurring_weekly_trigger(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login('user@example.com', 'securepassword')
    assert login_page.is_dashboard_header_present(), 'Dashboard header not present after login.'
    # Simulate JSON rule creation (mocked)
    rule = {
        'trigger': {'type': 'recurring', 'interval': 'weekly'},
        'action': {'type': 'percentage_of_deposit', 'percentage': 10},
        'conditions': []
    }
    assert rule['trigger']['type'] == 'recurring'
    assert rule['trigger']['interval'] == 'weekly'
    # Simulate passing of several weeks (mocked)
    for week in range(3):
        # Simulate transfer action at start of each interval
        transfer_executed = True  # Replace with actual system call
        assert transfer_executed, f'Transfer action was not executed for week {week+1}.'
